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


def lookup(l, n):
    return l[n % len(l)]


def populate_template(identifier, template_s, data):
    n = 0
    s = template_s
    for k, v in data.items():
        while k in s:
            n = do_hash(identifier + str(n))
            choice = lookup(v, n)
            s = s.replace(k, choice, 1)
            n += 1

    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create a readable name with a key of any characters"
    )
    parser.add_argument(
        "--animalnames",
        default="namelist/animal",
        help="path to the first required file, animalnames",
    )
    parser.add_argument(
        "--adjectives",
        default="namelist/adjective",
        help="path to the second required file, adjectiveslist",
    )
    parser.add_argument(
        "identifier",
        help="Key to transform into a name + adjective",
    )
    parser.add_argument(
        "--template",
        default="{adjective} {animal}",
        help="Template for name to create",
    )

    args = parser.parse_args()

    animal_names = load_from_file(args.animalnames)
    adjectives = load_from_file(args.adjectives)

    data = {
        "{animal}": animal_names,
        "{adjective}": adjectives,
    }

    print(
        populate_template(
            args.identifier,
            args.template,
            data,
        )
    )
