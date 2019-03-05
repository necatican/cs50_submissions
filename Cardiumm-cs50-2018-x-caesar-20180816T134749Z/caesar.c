#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Rejects the user if we don't get the key or get other values with it.
    if (argc == 1 || argc > 2)
    {
        printf("INVALID");
        return 1;
    }
    // Making sure the key is in range of our alphabet.
    int key = atoi(argv[1]) % 26;
    string user_string = get_string("plaintext: "); // Getting user input.
    for (int i = 0, str_len = strlen(user_string); i < str_len; i++) // Iterating over each character in user text.
    {
        if (isalpha(user_string[i]))  // Only iterating over letters
        {
            bool charCase = isupper(user_string[i]); // Saving uppercase as a bool to make sure we preserve it afterwards.
            int cValue = (int) toupper(user_string[i]); // Getting uppercase letter value before shifting.
            cValue += key;
            if (cValue > 90)
            {
                cValue = cValue - 26;
            }
            if (charCase) // Replacing char with uppercase latter if previous bool is true and lower case if it's false.
            {
                user_string[i] = (char) cValue;
            }
            else
            {
                user_string[i] = tolower((char) cValue);
            }

        }
    }
    printf(" ciphertext: %s\n", user_string);
}