# NameGen

A repo for exploration of the generation of _pronounceable names_.

Given some unpronounceable input string (a hash digest, a 256-bit number, a monotonic user ID), can we generate pronounceable (memorable, human-distinct) identifiers algorithmically? How do we trade-off uniqueness (collision-resistance) against this concept of pronounceability? How do we measure it?

# Git flow

```
git status
```

See the state of your local copy, which files are being added/modified.

```
git add <path>
```

_Stage_ files, containing changes you want to share

```
git commit
```

Store a set of (staged) changes, as a single atomic change.

```
git push
```

Share your local commits with the central upstream copy.

```
git pull
```

Fetch changes from the upstream copy

# To read
https://en.wikipedia.org/wiki/Markov_chain
https://en.wikipedia.org/wiki/Hash_function
