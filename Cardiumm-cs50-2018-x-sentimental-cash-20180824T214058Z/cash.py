from cs50 import get_float

# Get users cash
while True:
    cash = get_float("Your current cash: ")
    if cash > 0:
        break

# Turn it into cents.
cents = round(cash * 100)
counter = 0

# Calculate the coins
while cents >= 25:
    cents -= 25
    counter += 1
    if cents < 25:
        cents = cents % 25

while cents >= 10:
    cents -= 10
    counter += 1
    if cents < 10:
        cents = cents % 10

while cents >= 5:
    cents -= 5
    counter += 1
    if cents < 5:
        cents = cents % 5

while cents >= 1:
    cents -= 1
    counter += 1
    if cents < 1:
        cents = cents % 1

print(counter)