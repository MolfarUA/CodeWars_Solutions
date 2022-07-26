595970246c9b8fa0a8000086


#define _GNU_SOURCE
#include <ctype.h>
#include <string.h>

char *capitalize_word (const char *word)
{
  char *capitalized = strdup(word);
  capitalized[0] = toupper(word[0]);
  return capitalized;
}
______________________
#include <ctype.h>
#include <stdio.h>
#include <string.h>
char word_temp[64];
char *capitalize_word (char *word)
{

  strcpy(word_temp,word);
  word_temp[0] = toupper(word_temp[0]); //  something goes wrong here !
  printf("%s\n%s\n",word,word_temp);
  return word_temp;
}
______________________
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

char *capitalize_word (char *word)
{
  char* s = calloc(strlen(word) + 1, sizeof(char));
  s[0] = toupper(word[0]);
  for(size_t i = 1; i < strlen(word); i++) s[i] = word[i];
  s[strlen(word)] = '\0';
  return s;
}
