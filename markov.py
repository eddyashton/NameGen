#!/usr/bin/env python3

import sys
from collections import Counter
import random
import argparse


def load_from_file(filename):
    with open(filename, "r") as folder:
        lines = folder.readlines()
    lines = [line.strip() for line in lines]
    return lines


def ngrams(s, n):
    if n == 1:
        return s

    for i in range(0, len(s) - n + 1):
        yield s[i : i + n]


MAX_NGRAM_LEN = 5


def find_tokens(text):
    token_counts = Counter()
    for ngram_size in range(1, MAX_NGRAM_LEN + 1):
        token_counts.update(ngrams(text, ngram_size))
    best_tokens = sorted(token_counts.items(), key=lambda p: p[1], reverse=True)[:1000]
    # TODO: Configure number of tokens kept, for differently sized data sets?
    return [bt[0] for bt in best_tokens]


def tokenisations(s, tokens):
    # TODO: More efficient tokenisation process?
    l = []
    for t in tokens:
        if s.startswith(t):
            remainder = s[len(t) :]
            rest = tokenisations(remainder, tokens)
            if len(rest) == 0:
                l += [[t]]
            else:
                l += [[t, *r] for r in rest]
    return l


def count_tokens(strings_list, tokens):
    token_probabilities = {}

    for string in strings_list:
        seqs = tokenisations(string.lower(), tokens)
        for seq in seqs:
            for first, second in zip([""] + seq, seq + [""]):
                if first not in token_probabilities:
                    token_probabilities[first] = {}
                first_counts = token_probabilities[first]
                if second not in first_counts:
                    first_counts[second] = 0
                first_counts[second] += 1

    return token_probabilities


def weighted_random_choice(probability):
    keys = list(probability.keys())
    values = list(probability.values())
    return random.choices(keys, weights=values, k=1)[0]


def gen_string(all_probabilities, seed):
    random.seed(seed)
    l = []
    while True:
        c = len(l) > 0 and l[-1] or ""
        probabilities = all_probabilities[c]
        c = weighted_random_choice(probabilities)
        l += [c]
        if c == "":
            return "".join(l)


class Markov:
    def __init__(self, file):
        with open(file) as f:
            text = f.read()
        tokens = find_tokens(text)
        # TODO: Remove empty string, to avoid infinite loops in tokeniser?
        self.token_probabilities = count_tokens(text.splitlines(), tokens)

    def generate(self, seed):
        s = gen_string(self.token_probabilities, seed)
        s = s[0].upper() + s[1:]
        return s


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="create a readable name using a marok chain"
    )
    parser.add_argument(
        "file",
        help="name of the file you want to use as data",
    )
    parser.add_argument("seed", nargs="+")

    args = parser.parse_args()

    markov = Markov(args.file)

    for seed in args.seed:
        s = markov.generate(seed)
        print(s)
