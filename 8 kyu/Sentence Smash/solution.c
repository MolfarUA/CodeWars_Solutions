#include <stdio.h>
#include <string.h>

char *smash(const char **words, size_t count)
{
  int total_len = count - 1;
  for (int x = 0; x < count; ++x)
    total_len += strlen(words[x]);
    
  char *r = malloc(total_len + 1);
  if (!r) return 0;
  
  for (int x = 0, fwd = 0; x < count; ++x)
    fwd += sprintf(r + fwd, "%s ", words[x]);
    
  r[total_len] = 0;
  return r;
}

_____________________________________
#include <string.h>

char *smash(const char **words, size_t count)
{
  char *sentance = malloc(1000);
  int index = 0;
  
  for (int x = 0; x < count; x++) {
    for (int y = 0; words[x][y] != 0; y++) {
    sentance[index] = words[x][y];
    index++;
    }
    if (x + 1 != count) {
      sentance[index] = ' ';
      index++;
    }
  }
  sentance[index] = 0;
  return (sentance);
}

_____________________________________
#include <string.h>

char *smash(const char **words, size_t count){
    
    int len = 0;
    for(int i=0; i< count; i++) len += strlen(words[i]);
    
    char *res = (char*)calloc(len + count, sizeof(char));
    
    for(int i=0; i < count-1; i++){
        strcat(res, words[i]);
        strcat(res, " ");
    }
    
    strcat(res, words[count-1]);
    return res;
}
