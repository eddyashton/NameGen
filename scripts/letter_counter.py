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

        letter_counts.update(string.lower())

    return dict(letter_counts)


strings_list = animalnameslist(sys.argv[1])
letter_counts = count_letters(strings_list)
print(letter_counts)
