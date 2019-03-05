#include <stdio.h>
#include <cs50.h>

int main(void)
{

    int n;
    // Gets a positive number which is less than 23 from the user.
    do
    {
        n = get_int("Positive number between 1 and 23: ");
    }
    while (n < 0 || n > 23);

    // Loops until desired pyramid length
    for (int i = 0; i < n; i++)
    {
        // Drawing spaces to alin right.
        for (int j = 0; j < (n - i) - 1; j++)
        {
            printf(" ");
        }

        //Drawing pound signs. Using (i+1) to get 2 blocks on the first row.
        for (int r = 0; r <= (i + 1); r++)
        {
            printf("#");
        }
        // New line to give a proper shape.
        printf("\n");
    }

}
