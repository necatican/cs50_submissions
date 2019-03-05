// Helper functions for music

#include <cs50.h>
#include <stdlib.h>
#include "helpers.h"
#include <math.h>
#include <string.h>
#include <ctype.h>

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    // Gets an x/y and gives us x/8
    int first_int = (int) fraction[0] - 48;
    int second_int = (int) fraction[2] - 48;
    return round(first_int * (8 / second_int));
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // Declares note and octave value
    int note_value;
    int octave;
    // Set note values using A4 as a start point
    switch (note[0])
    {
        case 'A':
            note_value = 0;
            break;

        case 'B':
            note_value = 2;
            break;

        case 'C':
            note_value = -9;
            break;

        case 'D':
            note_value = -7;
            break;

        case 'E':
            note_value = -5;
            break;

        case 'F':
            note_value = -4;
            break;

        case 'G':
            note_value = -2;
            break;
    }

    // Check if the note is a flat or a sharp
    if (note[1] == '#')
    {
        note_value++;
        octave = (int) note[2] - 48;
    }
    else if (note[1] == 'b')
    {
        note_value--;
        octave = (int) note[2] - 48;
    }
    else
    {
        octave = (int) note[1] - 48;
    }
    // Calculate the frequency
    return round(440 * pow(2, (((octave - 4) * 12.0) + note_value) / 12));


}
// Determines whether a string represents a rest
bool is_rest(string s)
{
    // Check if it's an emptpy line or a note
    if (strcmp(s, "\n") && !isalpha(s[0]))
    {
        return true;
    }
    return false;

}
