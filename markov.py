#!/usr/bin/env python3

from collections import Counter
import random
import argparse
import pickle
import datetime


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
    # Delete any tokens with internal newlines
    token_counts = {
        k: v for k, v in dict(token_counts).items() if k.find("\n") in (-1, len(k) - 1)
    }
    best_tokens = sorted(token_counts.items(), key=lambda p: p[1], reverse=True)[:1000]
    # TODO: Configure number of tokens kept, for differently sized data sets?
    return set(bt[0] for bt in best_tokens)


def tokenisations(s, tokens):
    # TODO: More efficient tokenisation process?
    l = []
    for ngram_size in range(MAX_NGRAM_LEN, 0, -1):
        prefix = s[:ngram_size]
        if prefix in tokens:
            remainder = s[ngram_size:]
            rest = tokenisations(remainder, tokens)
            if len(rest) == 0:
                l += [[prefix]]
            else:
                l += [[prefix, *r] for r in rest]
            # Don't look for shorter tokens that are a prefix of this!
            break
    return l


def count_tokens(strings_list, tokens):
    token_probabilities = {}

    for string in strings_list:
        seqs = tokenisations(string, tokens)
        for seq in seqs:
            for first, second in zip(["\n"] + seq, seq + ["\n"]):
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
        c = len(l) > 0 and l[-1] or "\n"
        probabilities = all_probabilities[c]
        c = weighted_random_choice(probabilities)
        l += [c]
        if c.endswith("\n"):
            return "".join(l[:-1])


class Markov:
    def __init__(self, file):
        with open(file) as f:
            text = f.read()
        tokens = find_tokens(text)
        # TODO: Remove empty string, to avoid infinite loops in tokeniser?
        self.token_probabilities = count_tokens(text.splitlines(keepends=True), tokens)

    def generate(self, seed):
        s = gen_string(self.token_probabilities, seed)
        return s


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Create a readable name using a markov chain"
    )
    parser.add_argument(
        "file",
        help="Path to the file you want to use as source data",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--store-probabilities",
        help="Path to file where calculated probabilities should be stored",
        type=str,
    )
    group.add_argument(
        "--load-probabilities",
        help="Input path is pre-calculated probabilities, rather than raw source data",
        action="store_true",
    )
    parser.add_argument("seed", nargs="*")

    args = parser.parse_args()

    if args.load_probabilities:
        with open(args.file, "rb") as f:
            markov = pickle.load(f)
    else:
        markov = Markov(args.file)
        if args.store_probabilities:
            with open(args.store_probabilities, "wb") as f:
                pickle.dump(markov, f)

    for seed in args.seed:
        s = markov.generate(seed)
        print(s)
