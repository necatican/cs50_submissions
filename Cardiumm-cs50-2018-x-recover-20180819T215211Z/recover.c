#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Controlling argument count to see if we only got one.
    if (argc != 2)
    {
        fprintf(stderr, "Only supply 1 filename as an argument.\n");
        return 1;
    }
    // Trying to open the file and returning error code 2 if it fails.
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Cannot open the requested file.\n");
        return 2;
    }
    // Initializing upcoming variables.
    uint8_t buffer[512];
    int blockcounter = 0;
    char filename[8];
    FILE *outptr;


    while (!feof(inptr))
    {
        // We might not get a full block so saving returnsize to know how many bytes we will write.
        int returnsize = fread(&buffer, 1, 512, inptr);
        // Looking for signs of a new JPEG block.
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            sprintf(filename, "%03i.jpg", blockcounter);
            blockcounter++;
            if (blockcounter == 1)
            {
                outptr = fopen(filename, "w");
                fwrite(&buffer, 1, 512, outptr);
            }
            else
            {
                fclose(outptr); // Closing the previous file.
                outptr = fopen(filename, "w");
                fwrite(&buffer, 1, 512, outptr);
            }
        }
        else if (blockcounter >= 1) // Adding the block to previous file if it's not a new block.
        {
            fwrite(&buffer, 1, returnsize, outptr);
        }
    }

}