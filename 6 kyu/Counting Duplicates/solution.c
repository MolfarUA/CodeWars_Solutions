#include <stddef.h>
#include <ctype.h>

size_t duplicate_count(const char* text) 
{
  char cache[36] = {0};
  size_t result = 0;
  
  while (*text)
    {
      if (isdigit(*text))
        cache[*text - '0']++;
      else
        cache[tolower(*text) - 'a' + 10]++;
      text++;
    }
  
  for (size_t i = 0; i < 36; i++)
   if (cache[i] > 1)
     result++;
     
  return result;
}

________________________
#include <stddef.h>

size_t duplicate_count(const char* text) {
  int freq[128] = {0}, dups = 0;
  while (*text) dups += ++freq[tolower(*text++)] == 2;
  return dups;
}

______________________
#include <stddef.h>
#include <string.h>

size_t duplicate_count(const char *text) {
    int chars[256] = {0};
    int len = strlen(text);    
    for(int i = 0; i<len; i++){
      if(text[i] >= 65 && text[i]<=90) chars[text[i]+32]++;
      else chars[text[i]]++;
    }
    int dups = 0;
    for(int i = 0; i<256; i++) if(chars[i]>1) dups++;
    return dups;

}

_______________________
#include <stddef.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <ctype.h>

#define NO_OF_CHARS 256 

void fillCharCounts(const char *str, int *count) 
{ 
   for (int i = 0; *(str+i);  i++) 
      count[(int)tolower(*(str+i))]++; 
} 

size_t duplicate_count(const char *text) {
  int *count = (int *)calloc(NO_OF_CHARS, sizeof(int)); 
  fillCharCounts(text, count); 
  
  int res = 0;
  for (int i = 0; i < NO_OF_CHARS; i++) 
    if(count[i] > 1) 
        res++; 
  
  free(count); 
  return res;
}

____________________
#include <stddef.h>
#include <string.h> 
#include <ctype.h>

const char *strichr(const char *hay, const char needle) {
  const char needlei = tolower(needle);
  do 
    if (tolower(*hay) == needlei)
      return hay;
  while (*hay++);
  return 0;
}

int has_duplicates(const char *text, const char t) {
  const char *find = strichr(text, t);
  if (find)
    return strichr(find+1, t)? 1 : 0; 
  return 0;
}

size_t duplicate_count(const char* text) {
  const char *tp = "0123456789abcdefghijklmnopqrstuvwxyz";
  int count_duplicates = 0;
  for (; *tp; tp++) {
      count_duplicates += has_duplicates(text, *tp);  
  }
  return count_duplicates;
}
