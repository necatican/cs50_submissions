from cs50 import get_int

# Gets the user input.
while True:
    size = get_int("Size of the tower: ")
    if 0 <= size < 24:
        break

# Prints the tower
for i in range(size):
    i += 1
    print(" " * (size - i), end="")
    print("#" * (i + 1))