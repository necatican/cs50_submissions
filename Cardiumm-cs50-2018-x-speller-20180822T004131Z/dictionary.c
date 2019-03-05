// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>



#include "dictionary.h"

node *createNode(void);
node *root;
char buffer[46];
int totalSize = 0;
// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Setting depth and length to know how far we will dwell. Using wordValue because i cannot modify const.
    int wordValue;
    int depth = 0;
    int length = strlen(word);
    node *tempNode = root;
    for (depth = 0; depth < length; depth++)
    {
        if (word[depth] == '\'')
        {
            wordValue = '{' - 'a';
        }
        else
        {
            wordValue = tolower(word[depth]) - 'a';
        }
        // If the node is empty we hit the rock.
        if (tempNode -> children[wordValue] == 0)
        {
            return false;
        }
        // Next node in the list.
        tempNode = tempNode -> children[wordValue];
    }
    // If the node is marked as a word.
    if (tempNode -> is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    root = createNode();
    // Open the file
    FILE *dict = fopen(dictionary, "r");
    // I use fscan because I know how I will get my input.
    for (int c = fscanf(dict, "%s", buffer); c != EOF; c = fscanf(dict, "%s", buffer))
    {
        int depth;
        char *wordValue = buffer;
        int length = strlen(wordValue);
        node *tempNode = root;
        int charValue;
        for (depth = 0; depth < length; depth++)
        {
            if (isalpha(wordValue[depth]))
            {
                charValue = wordValue[depth] - 'a';
            }
            // If we get an apostrophe we assign
            else if (wordValue[depth] == '\'')
            {
                charValue = 26;
            }
            if (tempNode -> children[charValue] == 0)
            {
                tempNode -> children[charValue] = createNode();
            }
            // Next node
            tempNode = tempNode -> children[charValue];
        }
        // Declares then node as a leaf and adds +1 to our counter.
        tempNode -> is_word = true;
        totalSize++;
    }

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return totalSize;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // I use another function to unload recursively.
    unloader(root);
    return true;
}

node *createNode(void)
{
    // Creating a new node filled with zeroes.
    node *newNode;
    newNode = calloc(sizeof(node), 1);
    newNode -> is_word = false;
    return newNode;
}
void unloader(struct node *mainNode)
{
    // Goes through all branches frees nodes as it hits
    node *tempNode = mainNode;
    for (int i = 0; i < 27; i++)
    {
        if (tempNode -> children[i] != 0)
        {
            unloader(tempNode ->children[i]);
        }
    }
    free(tempNode);
}
