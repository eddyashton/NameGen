import sys
from collections import Counter
import random

def animalnameslist(animalnames):

    with open(animalnames, "r") as folder:
        linesanimal = folder.readlines()
    linesanimal = [lines.strip() for lines in linesanimal]
    return linesanimal


def count_letters(strings_list):
    letter_counts = {}

    for string in strings_list:
        s = list(string.lower())
        for (first, second) in zip([''] + s, s + ['']):
            if first not in letter_counts:
                letter_counts[first] = {}
            first_counts = letter_counts[first]
            if second not in first_counts:
                first_counts[second] = 0
            first_counts[second] += 1

    return dict(letter_counts)


strings_list = animalnameslist(sys.argv[1])
letter_counts = count_letters(strings_list)


def weighted_random_choice(probability):
    keys=list(probability.keys())
    values=list(probability.values())
    print(random.choices(keys, weights=values, k=1)[0])



def gen_string(letter_counts):
    l = ['']
    current = l[-1]
    probabilities = letter_counts[current]
    choice = weighted_random_choice()
    l += choice
weighted_random_choice(letter_counts[''])
weighted_random_choice(letter_counts[''])
weighted_random_choice(letter_counts[''])
weighted_random_choice(letter_counts[''])
weighted_random_choice(letter_counts[''])

weighted_random_choice(letter_counts['a'])
weighted_random_choice(letter_counts['a'])
weighted_random_choice(letter_counts['a'])
weighted_random_choice(letter_counts['a'])
weighted_random_choice(letter_counts['a'])

from collections import Counter

def transform_string_to_pair_counter(pair_string):
    pairs = [tuple(pair.split()) for pair in pair_string.items()]
    pair_counter = Counter(pairs)
    return pair_counter

pair_string = (letter_counts)
#pair_counter = transform_string_to_pair_counter(pair_string)
#print(pair_counter)