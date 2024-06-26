#!/usr/bin/env python3

import argparse
import hashlib
import os
import math
import random


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
            choice = v(identifier, i)
            s = s.replace(k, choice, 1)
            i += 1

    return s


# possible bug
def load_data(dir):
    data = {}
    files = os.listdir(dir)
    for file in files:
        path = os.path.join(dir, file)
        data[f"{{{file}}}"] = make_hasher_lookup(load_from_file(path))

    data["{original}"] = lambda seed, _: seed
    return data


def print_measure_info(data_dir, template):
    lengths = {}
    files = os.listdir(data_dir)
    for file in files:
        path = os.path.join(data_dir, file)
        lengths[f"{{{file}}}"] = len(load_from_file(path))

    print(f"Measuring template '{template}'")

    output_size = 1
    for k, v in lengths.items():
        if k in template:
            print(
                f" - {k} file provides {v:,} unique values (and appears {template.count(k)} time(s))"
            )
            output_size *= v * template.count(k)

    print(f"=> {output_size:,} unique values")

    entropy = math.floor(math.log(output_size, 2))

    if entropy > 0:
        print(f"This could uniquely identify:")

        bin_0 = random.getrandbits(entropy)
        bin_1 = random.getrandbits(entropy)
        print(
            f" - {entropy} bits of entropy (eg: {bin_0:0{entropy}b}, {bin_1:0{entropy}b})"
        )

        octal = math.floor(math.log(output_size, 8))
        if octal == 0:
            return
        b_0 = " ".join(f"{n:02x}" for n in os.urandom(octal))
        b_1 = " ".join(f"{n:02x}" for n in os.urandom(octal))
        print(f" - {octal} bytes of data (eg: {b_0}, {b_1})")

        dec_chars = [str(n) for n in range(10)]
        assert len(dec_chars) == 10

        hex_chars = dec_chars + [chr(n) for n in range(ord("a"), ord("f") + 1)]
        assert len(hex_chars) == 16

        alphanum = (
            dec_chars
            + [chr(n) for n in range(ord("a"), ord("z") + 1)]
            + [chr(n) for n in range(ord("A"), ord("Z") + 1)]
        )

        for characters, prefix in (
            (dec_chars, "{n}-decimal-place numbers"),
            (hex_chars, "{n}-character hexadecimal IDs"),
            (alphanum, "{n}-character alpha-numeric (mixed-case) IDs"),
        ):
            n = math.floor(math.log(output_size, len(characters)))
            if n == 0:
                return
            ex_0 = "".join(random.choices(characters, k=n))
            ex_1 = "".join(random.choices(characters, k=n))
            prefix = prefix.format(n=n)
            print(f" - {prefix} (eg: {ex_0}, {ex_1})")


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
    parser.add_argument(
        "--measure",
        help="Measure how many unique identifiers could be created with the current template",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    if args.measure:
        print_measure_info(args.data_dir, args.template)
    else:
        combinator = Combinator(args.data_dir, args.template)

        for identifier in args.identifier:
            print(combinator.generate(identifier))
