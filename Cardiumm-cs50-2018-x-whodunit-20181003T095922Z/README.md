# Questions

## What's `stdint.h`?

stdint.h is used to declare ints with specific bit values.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

They allow us to create signed or unsigned integers with specific width in our program.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

Byte is unsigned 1 byte, a dword is usigned 4 byte , a long is signed 32 byte and a word is unsigned 2 byte.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

B and M characters in ASCII which are respectively 66 and 77 in ASCII.

## What's the difference between `bfSize` and `biSize`?

bfSize is the size total and biSize is a constant with a value of 40 which represents BITMAPINFOHEADER.

## What does it mean if `biHeight` is negative?

Bitmap starts from top left corner instead of bottom.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biClrUsed

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

Our memory might not be enough to load the requested file.

## Why is the third argument to `fread` always `1` in our code?

It indicated how many times the read command will activate.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Lets us to change the pointer location. We can give negative or positive value to go back or forward.

## What is `SEEK_CUR`?

Gives us the current pointer location.

## Whodunit?

Professor Plum
