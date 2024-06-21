#!/usr/bin/env python3

import collections
import sys


def calculate_probabilities(words, n):

    model = collections.defaultdict(lambda: collections.defaultdict(int))

    for word in words:
        word = word.lower()
        for i in range(len(word) - n):
            prefix = word[i : i + n]
            suffix = word[i + n]
            model[prefix][suffix] += 1

    probabilities = {}
    for prefix, suffix_counts in model.items():
        total = sum(suffix_counts.values())
        probabilities[prefix] = {
            suffix: count / total for suffix, count in suffix_counts.items()
        }

    return probabilities
def load_words(filename):
    with open(filename, "r") as file:
        words = file.read().splitlines()
    return words
def print_probabilities(probabilities, n):
    print(f"Probabilities for {n}-grams:")
    for prefix, suffix_probs in probabilities.items():
        print(f"{prefix}: {suffix_probs}")
def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    words = load_words(filename)

    bigram_probabilities = calculate_probabilities(words, 2)
    trigram_probabilities = calculate_probabilities(words, 3)

    print_probabilities(bigram_probabilities, 2)
    print_probabilities(trigram_probabilities, 3)
if __name__ == "__main__":
    main()
