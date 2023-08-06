import os
import sys
from multiprocessing import pool

import tqdm
from reynir import TOK, Greynir

from greynirseq.nicenlp.models.icebert import IcebertModel
from greynirseq.nicenlp.models.multi_span_model import IcebertConstModel
from greynirseq.settings import IceBERT_NER_CONFIG, IceBERT_NER_PATH

kkpfn = ["hann", "honum", "hans"]
kvkpfns = ["hún", "hana", "henni", "hennar"]
gen_map = {"k": "kk", "v": "kvk"}
pfns = set(kkpfn + kvkpfns)


class KnowRef:
    def __init__(self, infile=None, outfile=None, has_ner=False, has_pos=False):
        self.infile = infile
        if outfile:
            self.outfile = open(outfile, "w")
        self.has_ner = has_ner
        self.has_pos = has_pos

        if not has_pos:
            self.ib = IcebertModel.pos_from_settings()
            self.ib.eval()
            self.ib.to("cpu")
            self.g = Greynir()
        if not has_ner:
            self.ner = IcebertConstModel.from_pretrained(IceBERT_NER_PATH, **IceBERT_NER_CONFIG)
            self.ner.eval()
            self.ner.to("cpu")  # fix when refactor is done

    def get_pos_ib(self, sent, pos=None):
        if pos is None:
            pos = self.ib.predict_to_idf(sent, device="cpu")
        simple_tags = []
        for i in range(len(pos)):
            tag = pos[i]
            if tag[0] == "c":
                # samtenging
                simple_tags.append(("st", None))
            elif tag[0] == "n" and (tag[-1] == "m" or tag[-1] == "s"):
                # sérnafn / para við ner ?
                gen = gen_map.get(tag[1], None)
                simple_tags.append(["person", gen, 1])
            elif tag[:2] == "fp":
                # persónufornafn
                gen = gen_map.get(tag[2], None)
                singular = tag[3] == "e"
                if not singular:
                    simple_tags.append((None, None))
                    continue
                simple_tags.append(("pfn", gen))
            else:
                simple_tags.append((None, None))

        # Join adjacent persons for length
        simple_tags_clean = []
        i = 0
        tok_c = len(simple_tags)
        while i < tok_c:
            tok = simple_tags[i]
            if tok[0] == "person":
                p_len = 1
                i += 1
                while i < tok_c and simple_tags[i][0] == "person":
                    i += 1
                    p_len += 1
                tok[-1] = p_len
                simple_tags_clean.append(tok)
            else:
                simple_tags_clean.append(tok)
                i += 1
        return simple_tags_clean

    def get_pos_greynir(self, sent):
        p = self.g.parse_single(sent)
        tree = p.tree
        if tree is None:
            return
        terminals = [l.terminal for l in tree.leaves]
        simple_terminals = []
        for i in range(len(terminals)):
            t = terminals[i]
            if t is None:
                simple_terminals.append((None, None))
                continue
            t = t.split("_")
            if t[0] == "st":
                simple_terminals.append((t[0], None))
                continue
            elif t[0] == "person":
                if len(t) > 2:
                    gen = t[2]
                else:
                    gen = t[1]
                tok_count = len(p.tokens[i].txt.split())
                simple_terminals.append((t[0], gen, tok_count))
                continue
            elif t[0] == "pfn":
                if len(t) > 2:
                    if t[2] != "et":
                        simple_terminals.append((None, None))
                        continue
                simple_terminals.append((t[0], t[1]))
                continue
            elif t[0] == "no":
                gen = t[-1]
                simple_terminals.append((t[0], gen))
                continue
            for j in range(len(p.tokens[i].txt.split())):
                simple_terminals.append((None, None))
        return simple_terminals

    def get_pos(self, sent, pos=None):
        greynir_pos = self.get_pos_greynir(sent)
        if greynir_pos:
            return greynir_pos
        ib_pos = self.get_pos_ib(sent, pos)
        tokens = sent.split()
        if len(ib_pos) == len(tokens):
            return ib_pos
        return

    def check_constr(self, sent, pos, ner):
        # only run if rudimentary checks pass
        st_c = 0
        pers = []
        pfn_loc = None
        pfn_gen = None
        komma_count = 0
        no_genders = []

        toks = sent.split()
        tok_len = len(toks)

        for i in range(len(pos)):

            if not pos[i]:
                continue

            pt, gen = pos[i][:2]
            if pt == "st":
                if len(pers) != 2:
                    return
                if st_c:
                    return
                st_c += 1
            elif pt == "person":
                if not gen:
                    continue
                if len(pers) > 1:
                    return
                if pers and pers[0][1] == gen:
                    return
                tok_count = pos[i][2]
                pers.append([pt, gen, i, tok_count])
            elif pt == "pfn":
                if st_c != 1:
                    continue
                if gen not in ["kvk", "kk"]:
                    continue
                if pfn_loc is not None:
                    return

                pfn_loc = i
                pfn_gen = gen
            elif i < tok_len and toks[i] == ",":
                komma_count += 1
            elif pt == "no":
                if pfn_loc is None:
                    no_genders.append(gen)

        if len(pers) != 2:
            return

        if pfn_loc is None:
            return

        # Modify offset if needed
        pers[1][2] += pers[0][3] - 1
        pfn_loc += pers[0][3] + pers[1][3] - 2

        if pers[0][0] == pfn_gen:
            ploc_start = pers[0][2]
            ploc_end = pers[0][2] + pers[0][3]
            oploc_start = pers[1][2]
            oploc_end = pers[1][2] + pers[1][3]
        else:
            ploc_start = pers[1][2]
            ploc_end = pers[1][2] + pers[1][3]
            oploc_start = pers[0][2]
            oploc_end = pers[0][2] + pers[0][3]

        # Adjacent
        # start_sec - start_first - len_first
        if pers[1][2] - pers[0][2] - pers[0][3] == 0:
            return

        if pers[1][2] - pers[0][2] - pers[0][3] == 1 and toks[pers[0][2] + pers[0][3]] == "(":
            return

        if toks[oploc_start:oploc_end] == toks[ploc_start:ploc_end]:
            return

        toks[pfn_loc] = "[{}]".format(toks[pfn_loc])
        toks[ploc_start] = "_{}".format(toks[ploc_start])
        toks[ploc_end - 1] = "{}_".format(toks[ploc_end - 1])
        toks[oploc_start] = "-{}".format(toks[oploc_start])
        toks[oploc_end - 1] = "{}-".format(toks[oploc_end - 1])

        return {
            "sent": sent,
            "formated": " ".join(toks),
            "pers": pers,
            "pfn_loc": pfn_loc,
            "pfn_gen": pfn_gen,
            "pos": pos,
            "ner": ner,
            "komma_count": komma_count,
            "noun_ambig": pfn_gen in no_genders,
        }

    def sent_has_noise(self, line):
        if "|" in line:
            return True
        if "@" in line:
            return True
        return False

    def get_ner(self, sentence):
        cat_idx, labels, sentence = self.ner.predict_pos([sentence], device="cpu")
        # todo consider using tokenisation of sent from here
        return labels

    def sent_has_two_persons(self, sentence, ner=None):
        if ner is None:
            ner = self.get_ner(sentence)
        p_c = 0
        for t in ner:
            if t == "B-Person":
                p_c += 1
        return p_c == 2

    def crude_person_filter(self, sentence):
        # use to speed up retrieval
        # check for two uppercase words at least
        # use tokenizer?
        upc = 0
        toks = sentence.split()
        for w in toks:
            if len(w) > 2 and w[0].isupper() and w[1].islower():
                upc += 1
        if pfns.isdisjoint(set(toks)):
            return False
        if upc > 1 and upc < 6:
            return True
        return False

    def write_data(self, json):
        # decide tabular output

        self.outfile.writelines(
            "\t".join(
                [
                    json["sent"],
                    json["formated"],
                    str(json["pers"]),
                    str(json["pos"]),
                    str(json["ner"]),
                    str(json["pfn_loc"]),
                    str(json["pfn_gen"]),
                    str(json["komma_count"]),
                    str(json["noun_ambig"]),
                ]
            )
            + "\n"
        )

    def parse_line(self, line):
        pos, ner = None, None
        if self.has_pos and self.has_ner:
            sent, pos, ner = line[:-1].split("\t")
            pos = pos.split()
            ner = ner.split()
        elif self.has_ner:
            sent, ner = line[:-1].split("\t")
            ner = ner.split()
        elif self.has_pos:
            sent, pos = line[:-1].split("\t")
            pos = pos.split()
        else:
            sent = line[:-1]

        if self.sent_has_noise(sent):
            return

        if not self.crude_person_filter(sent):
            return

        if ner is None:
            ner = self.get_ner(sent)

        if not self.sent_has_two_persons(sent, ner):
            return

        pos = self.get_pos(sent, pos)
        if pos is None:
            return

        hit = self.check_constr(sent, pos, ner)
        return hit

    def parse_file(self):
        for line in tqdm.tqdm(open(self.infile).readlines()):
            if not line.strip():
                continue

            hit = self.parse_line(line)

            if hit:
                print(hit)
                self.write_data(hit)
        self.outfile.close()


def test():
    test_data = [
        (
            "Guðrún segir Einar hafa þekkt ágætlega til í Bretlandi og verk hans hafi mögulega borist þangað .",
            [
                "nveo-s",
                "sfg3en",
                "nkeo-s",
                "sng",
                "ssg",
                "aa",
                "aa",
                "aþ",
                "nheþ-s",
                "c",
                "nhfn",
                "fpkee",
                "svg3en",
                "aa",
                "ssm",
                "aa",
                "p",
            ],
            [
                "B-Person",
                "O",
                "B-Person",
                "O",
                "O",
                "O",
                "O",
                "O",
                "B-Location",
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
                "O",
            ],
            "-Guðrún- segir _Einar_ hafa þekkt ágætlega til í Bretlandi og verk [hans] hafi mögulega borist þangað .",
        ),
    ]
    kr = KnowRef(has_ner=True, has_pos=True)
    line = "\t".join([test_data[0][0], " ".join(test_data[0][1]), " ".join(test_data[0][2])]) + "\n"
    hit = kr.parse_line(line)
    assert hit["formated"] == test_data[0][3]

    kr = KnowRef()
    hit = kr.parse_line(test_data[0][0] + "\n")
    assert hit["formated"] == test_data[0][3]


if __name__ == "__main__":
    # test()

    # mon_is_tr = "/tmp/cc_is_prefilter_knowref.txt"
    # mon_is_tr = "rmh_test.clean.txt"
    kr = KnowRef(infile=sys.argv[1], outfile="data/{}.tsv".format(sys.argv[1].split("/")[-1]))
    kr.parse_file()
