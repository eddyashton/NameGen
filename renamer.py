#!/usr/bin/env python3

from markov import Markov
from combinator import Combinator
import argparse
import re

def load_from_file(filename):
    with open(filename, "r") as folder:
        lines = folder.readlines()
    lines = [line.strip() for line in lines]
    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="File to be renamed")
    parser.add_argument("--kind", choices=["markov", "combinator"], default="combinator")

    args = parser.parse_args()

    name_generator = Combinator(data_dir="data", template="{firstname} {surname}") if args.kind == "combinator" else Markov(file="data/name")

    pattern = re.compile(r"[0-9a-fA-F]{8,}")
    input_lines = load_from_file(args.file)
    for line in input_lines:
        matches = pattern.findall(line)
        for match in matches:
            replacement = name_generator.generate(match)
            line = line.replace(match, replacement)
        print(line)