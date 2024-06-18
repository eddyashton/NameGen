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
# make it so the hash goes 2 times giving different results simply adding a letter or a number
#at the end, and then connect these two different numbers with animalnames and adjectives to get the 
#two parts of the word

bob = "Bob"
print(bob)