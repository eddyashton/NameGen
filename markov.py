#!/usr/bin/env python3

import sys
from collections import Counter
import random
import argparse


def animalnameslist(animalnames):

    with open(animalnames, "r") as folder:
        linesanimal = folder.readlines()
    linesanimal = [lines.strip() for lines in linesanimal]
    return linesanimal


def tokenise(line):
    return list(line.lower())


def count_letters(strings_list):
    letter_counts = {}

    for string in strings_list:
        s = tokenise(string)
        for first, second in zip([""] + s, s + [""]):
            if first not in letter_counts:
                letter_counts[first] = {}
            first_counts = letter_counts[first]
            if second not in first_counts:
                first_counts[second] = 0
            first_counts[second] += 1

    return dict(letter_counts)


def weighted_random_choice(probability):
    keys = list(probability.keys())
    values = list(probability.values())
    return random.choices(keys, weights=values, k=1)[0]


def gen_string(letter_counts, seed):
    random.seed(seed)
    s = ""
    while True:
        c = len(s) > 0 and s[-1] or ""
        probabilities = letter_counts[c]
        c = weighted_random_choice(probabilities)
        s += c
        if c == "":
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

    strings_list = animalnameslist(args.file)
    letter_counts = count_letters(strings_list)

    for seed in args.seed:
        s = gen_string(letter_counts, seed)
        s = s[0].upper() + s[1:]
        print(s)
