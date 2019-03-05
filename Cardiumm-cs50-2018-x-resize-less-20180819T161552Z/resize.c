// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    int resizeFactor = atoi(argv[1]);
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }
    else if (resizeFactor > 100 || resizeFactor < 1)
    {
        fprintf(stderr, "Resizing factor should be a positive integer with a value less than 100");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }


    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Save Height, width and padding of the original file.
    int infileHeight = abs(bi.biHeight);
    int infileWidth = bi.biWidth;
    int infile_padding = (4 - (infileWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Get the output file values after resizing.
    bi.biWidth = bi.biWidth * resizeFactor;
    bi.biHeight = bi.biHeight * resizeFactor;
    // Get the output file padding
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // Calculate the sizes of output file.
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + abs(padding)) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // Create an array to store the colors
    RGBTRIPLE colorArray[bi.biWidth];

    // iterate over infile's scanlines
    for (int i = 0; i < infileHeight; i++)
    {
        // Reset the array width
        int iterationCounter = 0;
        // iterate over pixels in scanline
        for (int j = 0; j < infileWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // Place the pixels in the array.
            for (int n = 0; n < resizeFactor; n++)
            {
                colorArray[iterationCounter] = triple;
                iterationCounter++;
            }
        }
        // Vertical resizing
        for (int factor = 0; factor < resizeFactor; factor++)
        {
            // Horizontal resizing
            for (int resize = 0; resize < bi.biWidth; resize++)
            {
                RGBTRIPLE color = colorArray[resize];
                fwrite(&color, sizeof(RGBTRIPLE), 1, outptr);

            }
            // Padding
            for (int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }
        }
        // skip over padding, if any
        fseek(inptr, infile_padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

