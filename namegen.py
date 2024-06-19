import argparse
import hashlib


def load_from_file(filename):
    with open(filename, "r") as folder:
        lines = folder.readlines()
    lines = [line.strip() for line in lines]
    return lines


def do_hash(I):
    h = hashlib.md5(bytes(I, "utf-8"))
    n = int.from_bytes(h.digest(), "little")
    return n


def finalnames(Nanimalname, Nadjectives, l1, l2):
    Finalanimal = l1[Nanimalname % len(l1)]
    Finaladjective = l2[Nanimalname % len(l2)]
    Result = Finaladjective + " " + Finalanimal
    print(Result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create a readable name with a key of any characters"
    )
    parser.add_argument(
        "--animalnames",
        default="namelist/animalnames",
        metavar="",
        help="path to the first required file, animalnames",
    )
    parser.add_argument(
        "--adjectives",
        default="namelist/adjectives",
        metavar="",
        help="path to the second required file, adjectiveslist",
    )
    parser.add_argument(
        "key_to_transform", metavar="", help="Key to transform into a name + adjective"
    )

    args = parser.parse_args()
    # index = n
    animal_names = load_from_file(args.animalnames)
    adjectives = load_from_file(args.adjectives)
    Nadjectives = do_hash(args.key_to_transform)
    Nanimalnames = do_hash(args.key_to_transform + "1")

    finalnames(Nanimalnames, Nadjectives, animal_names, adjectives)
