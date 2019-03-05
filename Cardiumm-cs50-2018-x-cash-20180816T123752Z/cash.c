#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float cash;
    // Counter to count the coin amount
    int counter = 0;

    // Getting users cash in a positive amount.
    do
    {
        cash = get_float("Your current cash: ");
    }
    while (cash < 0);

    //Turning cash to cents.
    int cents = round(cash * 100);

    //Calculating coins below.
    while (cents >= 25)
    {
        cents -= 25;
        counter++;
        if (cents < 25)
        {
            cents = cents % 25;
        }
    }

    while (cents >= 10)
    {
        cents -= 10;
        counter++;
        if (cents < 10)
        {
            cents = cents % 10;
        }
    }

    while (cents >= 5)
    {
        cents -= 5;
        counter++;
        if (cents < 5)
        {
            cents = cents % 5;
        }
    }


    // Just adding cents / 1 because cents wont be less than 1
    while (cents >= 1)
    {
        counter += cents / 1;
        cents = cents % 1 ;
    }

    printf("%i", counter);
}