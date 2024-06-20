import sys
from collections import Counter


def animalnameslist(animalnames):

    with open(animalnames, "r") as folder:
        linesanimal = folder.readlines()
    linesanimal = [lines.strip() for lines in linesanimal]
    return linesanimal


def count_letters(strings_list):

    letter_counts = Counter()

    for string in strings_list:
        s = string.lower()
        for (first, second) in zip(s[:-1], s[1:]):
            print(first, second)
            # letter_counts.update({c: 1})

    return dict(letter_counts)


strings_list = animalnameslist(sys.argv[1])
letter_counts = count_letters(strings_list)
print(letter_counts)

from collections import Counter

def transform_string_to_pair_counter(pair_string):
    pairs = [tuple(pair) for pair in pair_string.split()]
    pair_counter = Counter(pairs)
    return pair_counter

pair_string = (letter_counts)
pair_counter = transform_string_to_pair_counter(pair_string)
print(pair_counter)