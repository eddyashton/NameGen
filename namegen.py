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

#possible bug
def load_data(dir):
    data = {}
    files = os.listdir(dir)
    for file in files:
        path = os.path.join(dir, file)
        data[f"{{{file}}}"] = load_from_file(path)

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="create a readable name with a key of any characters",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--data-dir",
        default="namelist",
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

    data = load_data(args.data_dir)

    for identifier in args.identifier:
        print(
            populate_template(
                identifier,
                args.template,
                data,
            )
        )
