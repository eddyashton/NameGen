#!/usr/bin/env python3

import argparse
import hashlib
import os


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

def make_hasher_lookup(vals):
    def hasher_lookup(seed, i):
        n = do_hash(seed + str(i))
        choice = lookup(vals, n)
        return choice
    return hasher_lookup

def populate_template(identifier, template_s, data):
    i = 0
    s = template_s
    for k, v in data.items():
        while k in s:
            choice = v(identifier,i)
            s = s.replace(k, choice, 1)
            i += 1

    return s

#possible bug
def load_data(dir):
    data = {}
    files = os.listdir(dir)
    for file in files:
        path = os.path.join(dir, file)
        data[f"{{{file}}}"] = make_hasher_lookup(load_from_file(path))

    data["{original}"] = lambda seed, _: seed
    return data

class Combinator:
    def __init__(self, data_dir, template):
        self.data = load_data(data_dir)
        
        self.template = template

    def generate(self, seed):
        return populate_template(seed, self.template, self.data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create a readable name with a key of any characters",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Path to directory where namelists are stored",
    )
    parser.add_argument(
        "identifier",
        help="Key to transform into a name + adjective",
        nargs="+",
    )
    parser.add_argument(
        "--template",
        default="{adjective} {animal}",
        help="Template for name to create",
    )

    args = parser.parse_args()

    combinator = Combinator(args.data_dir, args.template)

    for identifier in args.identifier:
        print(
            combinator.generate(identifier)
        )
