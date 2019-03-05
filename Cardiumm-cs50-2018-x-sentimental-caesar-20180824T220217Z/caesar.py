from cs50 import get_string
import sys

# Get the key from arguments
key = int(sys.argv[1])
user_string = get_string("String: ")

# Crypt the user string
print("ciphertext: ", end="")
for c in user_string:
    charCase = False

    if c.isalpha() == False:
        print(c, end="")
        continue
    if c.isupper():
        charCase = True
    cryptedChar = (ord(c.lower()) - 97 + key) % 26
    if charCase:
        # Preserve the char case.
        cryptedChar = chr(cryptedChar + 97).upper()
    else:
        cryptedChar = chr(cryptedChar + 97)
    print(cryptedChar, end="")
print()