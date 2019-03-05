// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>
#include <stdio.h>

typedef struct node
{
    struct node *children[27];
    bool is_word;
}
node;

node *createNode(void);
// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Prototypes
bool check(const char *word);
bool load(const char *dictionary);
unsigned int size(void);
bool unload(void);
void unloader(struct node *mainNode);



#endif // DICTIONARY_H
