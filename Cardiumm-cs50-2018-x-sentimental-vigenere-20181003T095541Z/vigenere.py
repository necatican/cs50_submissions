import sys
from cs50 import get_string

key = sys.argv[1]
current_key = 0

# Checking if arg matches our needs
if key.isalpha() == False:
    print("Key can only include alphabetic characters.")
    sys.exit(1)
if len(sys.argv) != 2:
    print("You can only use one argument")
    sys.exit(1)

user_string = get_string("String: ")


# Header
print("ciphertext: ", end="")

# Loops through function
for i in user_string:
    if i.isalpha():
        # Saving the charCase to restore it later
        charCase = i.isupper()
        cValue = ord(i.upper())
        # Loops through our key
        if current_key >= len(key):
            current_key = 0
        cKey = ord(key[current_key].upper())
        current_key += 1
        cValue = ((cKey + cValue) % 26) + 65
        if cValue > 90:
            cValue -= 26
        # Restoring the charCase
        if charCase:
            print(chr(cValue), end="")
        else:
            print(chr(cValue).lower(), end="")
    else:
        print(i, end="")
print()