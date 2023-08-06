#!/usr/bin/env python
import argparse
import json
import random
from typing import Dict

import tqdm
from reynir import Greynir
from reynir import NounPhrase as NP

from greynirseq.nicenlp.models.icebert import IcebertModel

g = Greynir()
ib = IcebertModel.pos_from_settings()
ib.eval()
ib.to("cpu")

CASES = {"nf": "nominative", "þf": "accusative", "þgf": "dative", "ef": "genitive"}
CASES_IFD = {"n": "nominative", "o": "accusative", "þ": "dative", "e": "genitive"}


class WinograndeExporter:
    data = []
    names = {"kk": [], "kvk": []}

    def __init__(self, input_file: str, name_file: str) -> None:
        self._load_data(input_file)
        self._load_names(name_file)

    def _load_data(self, input_file: str) -> None:
        with open(input_file) as input_data:
            for line in input_data:
                (
                    sent,
                    tagged,
                    per_gen,
                    simp_pos,
                    ner,
                    pfn_loc,
                    pfn_gen,
                    num_com,
                    ambig,
                ) = line.strip().split("\t")
                self.data.append(
                    {
                        "sent": sent,
                        "tagged": tagged,
                        "per_gen": eval(per_gen),
                        "simp_pos": eval(simp_pos),
                        "ner": ner,
                        "pfn_loc": int(pfn_loc),
                        "pfn_gen": pfn_gen,
                        "num_com": num_com,
                        "ambig": ambig,
                    }
                )

    def _load_names(self, name_file) -> None:
        # Expects name_file lines to have format "{gender}\t{name}\n"

        # TODO: does it matter if we use only first names vs full names?

        with open(name_file) as fh:
            for line in fh.readlines():
                gender, name = line.strip().split("\t")
                self.names[gender].append(name)

    @classmethod
    def inflect_word(cls, parsed_sentence, location, replacement) -> str:
        # TODO: possibly rethink since also parsing in preprocessing
        np = NP(replacement)
        case = set(parsed_sentence.terminals[int(location)].variants).intersection(set(CASES.keys())).pop()
        inflected = getattr(np, CASES[case])
        return inflected

    def inflect_word_ib(self, sentence, location, replacement) -> str:
        pos = ib.predict_to_idf(sentence, device="cpu")
        np = NP(replacement)
        case = pos[location][3]
        inflected = getattr(np, CASES_IFD[case])
        return inflected

    def replace_gender_related_words(self):
        # eiginmaður, eiginkona etc
        pass

    def substitute_sentence(self, sent: Dict[str, str]) -> Dict[str, str]:
        print("Parsing: {}".format(sent["tagged"]))
        tokens = sent["sent"].split()

        new_name = random.sample(self.names[sent["pfn_gen"]], 1)

        answer_location = None
        wrong_answer_location = None

        new_tokens = []
        i = 0
        pfn_offset = 0
        wrong_ans_orig_loc = None

        while i < len(tokens):
            for per in sent["per_gen"]:
                _, gen, start, length = per
                if i == start:
                    if gen == sent["pfn_gen"]:
                        answer_location = i - pfn_offset
                    else:
                        wrong_ans_orig_loc = i
                        wrong_answer_location = i - pfn_offset
                    end = start + length
                    new_tokens.append(" ".join(tokens[start:end]))
                    i += length
                    pfn_offset += length - 1
                    continue
            new_tokens.append(tokens[i])
            i += 1

        pfn_loc = sent["pfn_loc"] - pfn_offset
        parsed_sentence = g.parse_single(sent["sent"])
        override = False

        # if parsed
        if parsed_sentence.terminals is not None:
            option_1 = self.inflect_word(parsed_sentence, pfn_loc, new_tokens[answer_location])
            option_2 = self.inflect_word(parsed_sentence, pfn_loc, new_name)
            replacement_name = self.inflect_word(parsed_sentence, wrong_answer_location, new_name)
        else:
            option_1 = self.inflect_word_ib(sent["sent"], sent["pfn_loc"], new_tokens[answer_location])
            option_2 = self.inflect_word_ib(sent["sent"], sent["pfn_loc"], new_name)
            replacement_name = self.inflect_word_ib(sent["sent"], wrong_ans_orig_loc, new_name)
        # if not parsed ... we should have this information already, but need to bring in icebert

        new_tokens[wrong_answer_location] = replacement_name

        pfn_loc = sent["pfn_loc"] - pfn_offset
        new_tokens[pfn_loc] = "_"
        gapped_sentence = " ".join(new_tokens)

        print("Gapped: {}".format(gapped_sentence))
        print("Option1: {}\tOption2:\t{}\n".format(option_1, option_2))
        answer = "1"  # 1 as in Option_1

        return {
            "answer": answer,
            "sentence": gapped_sentence,
            "option1": option_1,
            "option2": option_2,
            "qID": "",
        }

    def to_winogrande(self, outfile):
        errors = 0
        with open(outfile, "w") as of_handler:
            for sentence_data in tqdm.tqdm(self.data):
                try:
                    subst = self.substitute_sentence(sentence_data)
                    of_handler.writelines(json.dumps(subst) + "\n")
                except:
                    errors += 1
        print("Total errors {} .".format(errors))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coref", type=str)
    parser.add_argument("--names", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    wgg = WinograndeExporter(args.coref, args.names)
    wgg.to_winogrande(args.output)


if __name__ == "__main__":
    main()
