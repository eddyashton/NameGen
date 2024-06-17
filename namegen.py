# Code goes here

"bcd"
"arhwrh"
"agsg"

# python namegen.py namelist/animalnames "bcd45235af"

# Steps:
# - Open the file named in the first argument
# - Read all of the names into a list
# 
# - Hash the second argument (h = hashlib.md5(...))
# - Convert the hash to a number (n = int.from_bytes(h.digest(), "little"))
# - Select an animal from the list, based on n (l[n % len(l)])

# Adder

# python namegen.py "abcd"
# dbac

bob = "Bob"
print(bob)