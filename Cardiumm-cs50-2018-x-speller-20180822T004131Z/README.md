# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

A medical illness related to lungs. Also the word with our maximum length limit.

## According to its man page, what does `getrusage` do?

It records resource usages and program running times.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

So we don't lose or accidentally edit values while calculating.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

First our main opens a file in read mode. Having a file open in read mode we can use fgetc to get contents of the file character by character. The for loop ensures that our loop will go until we hit the end of file. With the first check program gets
a character or an apostrophe if our index is higher than 0 since English words can't start with an apostrophe. Next if check checks if we get a number and if we do it loops through the word and sets index to 0 basically starting a new array for a new
word. If our index is higher than 0 which means we got some characters in our array and if we didn't find any integers, It must mean that we got a full word stored in our array. This statement adds a NUL operator to turn our array into a string,
adds to word counter, sends the word on our checkers way and saves the response time and the response.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

We can use fscanf but then we wouldn't be able to limit our input. We have a 45 char limit and we don't allow integers in our program so fgetc makes more sense.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So we don't accidentally change main program values and cause problems.
