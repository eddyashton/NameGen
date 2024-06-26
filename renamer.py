#!/usr/bin/env python3

from markov import Markov
from combinator import Combinator
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("seed", nargs="+")
    parser.add_argument("--kind", choices=["markov", "combinator"], default="combinator")

    args = parser.parse_args()

    name_generator = Combinator(data_dir="data", template="{adjective} {animal}") if args.kind == "combinator" else Markov(file="data/name")

    for seed in args.seed:
        print(name_generator.generate(seed))