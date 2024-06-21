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


def tokenise(line, token_splitter):
    if token_splitter is None:
        return list(line.lower())
    return [word.lower() for word in line.split(token_splitter)]


def find_tokens(strings_list, token_splitter):
    tokens = []
    for line in strings_list:
        tokens += tokenise(line, token_splitter)
    return list(set(tokens))


def tokenisations(s, tokens):
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


def gen_string(all_probabilities, seed, token_splitter):
    random.seed(seed)
    l = []
    while True:
        c = len(l) > 0 and l[-1] or ""
        probabilities = all_probabilities[c]
        c = weighted_random_choice(probabilities)
        l += [c]
        if c == "":
            return (token_splitter or "").join(l)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="create a readable name using a marok chain"
    )
    parser.add_argument(
        "file",
        help="name of the file you want to use as data",
    )
    parser.add_argument("seed", nargs="+")
    parser.add_argument("--token-splitter", default=None)

    args = parser.parse_args()

    strings_list = load_from_file(args.file)
    tokens = find_tokens(strings_list, args.token_splitter)
    token_probabilities = count_tokens(strings_list, tokens)

    for seed in args.seed:
        s = gen_string(token_probabilities, seed, args.token_splitter)
        s = s[0].upper() + s[1:]
        print(s)
