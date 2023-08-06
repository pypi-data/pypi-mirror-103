#!/usr/bin/env python
import json
import operator
import os
from collections import defaultdict, namedtuple

import tqdm
from gensim.summarization.bm25 import BM25
from lemmatizer import Lemmatizer

#
# Everything straight into memory while we can afford it
#


def load_wiki(wiki_file, target_length=100):
    # Loads TSV of format
    # title_id, idx, text, lemmas

    articles = defaultdict(list)

    with open(wiki_file) as file_handler:

        cur_text = ""
        cur_lemmas = []
        cur_title = None

        for line in file_handler.readlines():
            title, idx, text, lemmas = line.strip().split("\t")
            if cur_title != title:
                if cur_title is not None:
                    articles[cur_title].append([cur_text, cur_lemmas])
                cur_title = title
                cur_lemmas = []
                cur_text = ""

            lemmas = lemmas.split()
            len_so_far = len(cur_lemmas)
            total_length = len(lemmas) + len_so_far
            if total_length > 100:
                if total_length - 100 > 100 - len_so_far:
                    # Don't add sentence
                    articles[title].append([cur_text, cur_lemmas])
                    cur_text = text
                    cur_lemmas = lemmas
                else:
                    cur_text += " " + text
                    cur_lemmas += lemmas
                    articles[title].append([cur_text, cur_lemmas])
            else:
                if cur_text != "":
                    cur_text += " " + text
                else:
                    cur_text = text
                cur_lemmas += lemmas

        articles[title].append([text, lemmas])

    return articles


Question = namedtuple(
    "Question", ["question", "answer", "yes_no", "has_answer", "article", "span", "source"], defaults=(None,) * 7
)


def load_tidy_questions(tidy_folder):
    questions = []
    qa_files = [fname for fname in os.listdir(tidy_folder) if "json" in fname]
    for file_name in qa_files:
        path = os.path.join(tidy_folder, file_name)
        passage_sets = json.load(open(path))
        for passages in passage_sets:
            for passages in passages["passages"]:
                for q in passages["question_answer_pairs"]:
                    question = q["question"]
                    answer = " ".join(q["answer"]["spans"])
                    q = q["answer"]
                    yes_no = q["yes_no_answer"]
                    has_answer = not q["no_gold"]
                    article = q["gold_paragraph"]
                    span = q.get("indices", None)
                    if span:
                        # '(a,b)'
                        start, end = span[0][1:-1].split(",")
                        span = [int(start), int(end)]

                    if article:
                        # title:XXXX_....:i
                        name = article.split("_")[0].split(":")[-1]
                        id = article.split(":")[-1]
                        article = "{}_{}".format(name, id)
                    questions.append(Question(question, answer, yes_no, has_answer, article, span, "tidy"))
    return questions


def load_gettu_betur_questions(file_name):
    # Format:
    # human	individual		Á ævisögu hvers byggir Paradísarheimt?	Eiríks frá Brúnum	Á ævisögu hvers byggir Paradísarheimt	á ævisaga hver byggja paradísarheimt	a n f s n	Á ævisögu hvers byggir
    questions = []
    with open(file_name) as qfile:
        for line in qfile.readlines():
            sp = line.strip().split("\t")
            question = sp[3]
            answer = sp[4]
            questions.append(Question(question=question, answer=answer))
    return questions


def load_trivia_questions(file_name):
    # Format:
    # 6,Tónlist,2,,"Hver gerði lagið ""Jump they say""",David Bowie
    questions = []
    with open(file_name) as qfile:
        for line in qfile.readlines():
            sp = line.strip().split(",")
            question = sp[4]
            answer = sp[5]
            questions.append(Question(question=question, answer=answer))
    return questions


class QAMatcher:
    bm25 = None
    l = None
    lookup_lemmas = None

    def __init__(self, articles, questions):
        self.articles = articles
        self.questions = questions
        self.question_segments = dict()
        self.bm25_segments = dict()

    def lookup_question_segment(self, question):
        article = self.articles.get(question.article)
        if not article:
            return None
        start, end = question.span
        pos = 0
        for i, segment in enumerate(article):
            seg_len = len(segment[0])
            if pos + seg_len > start:
                return segment
            pos += seg_len
        return segment

    def match_article_segments(self):
        for i, q in enumerate(self.questions):
            if q.span:
                segment = self.lookup_question_segment(q)
                if segment is None:
                    continue
                self.question_segments[i] = {
                    "question": q.question,
                    "title": q.article.split("_")[0],
                    "text": segment,
                    "score": 1000,
                    "title_score": 1,
                    "passage_id": "",
                    "answer": q.answer,
                }

    def setup_bm25(self):
        self.lookup_lemmas = []
        for article in self.articles:
            for i, segment in enumerate(self.articles[article]):
                self.lookup_lemmas.append((segment[1], article, i))
        self.bm25 = BM25([l[0] for l in self.lookup_lemmas])

    def lookup_b25(self, question, candidates=1):
        if self.bm25 is None:
            self.setup_bm25()
        if self.l is None:
            self.l = Lemmatizer()
        lemmas = self.l.lemmatize(question)[0][0]
        indexes, values = max(enumerate(self.bm25.get_scores(lemmas)), key=operator.itemgetter(1))
        return indexes, values

    def lookup_answer(self, question):
        idx, value = self.lookup_b25(question.lower())
        _, article, idx = self.lookup_lemmas[idx]
        return self.articles[article][idx][0]

    def check_overlap_tidy(self):
        hits = 0
        for idx in tqdm.tqdm(self.question_segments):
            q = self.question_segments[idx]
            segment = self.lookup_answer(q["question"])
            if self.questions[idx].answer in segment:
                hits += 1
        return hits / len(self.question_segments)

    def check_overlap(self):
        hits = 0
        qcount = len(self.questions)
        for q in tqdm.tqdm(self.questions):
            segment = self.lookup_answer(q.question)
            if q.answer.lower() in segment.lower():
                hits += 1
                print(hits / qcount)
        return hits / qcount


#
# TODO Add arguments to write matches to json file and print statistics
#


# if __name__ == "__main__":
question_folder = "/home/vesteinn/work/projects/GreynirQA/data/raw/2020_09_07"
article_file = "is_wiki_sentences_all.tsv"
tidy_questions = load_tidy_questions(question_folder)
articles = load_wiki(article_file)
gettu_betur_questions = load_gettu_betur_questions("/data/datasets/QA/gettu-betur.txt")
trivia_questions = load_trivia_questions("/data/datasets/QA/questions.csv")

qam1 = QAMatcher(articles, gettu_betur_questions)
qam2 = QAMatcher(articles, trivia_questions)


# qam.match_article_segments()
