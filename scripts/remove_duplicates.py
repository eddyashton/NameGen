import sys

path = sys.argv[1]

# example:
# "Aaaa\nBababa\nB\nB"
# ["Aaaa", "Bababa", "B", "B"]
# {"Aaaa", "Bababa", "B"}
contents = set(open(path).read().splitlines())


with open(path, 'w') as f:
    for entry in sorted(contents):
        f.write(f"{entry}\n")
