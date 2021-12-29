#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *alphabet_position(char *text) {
  const size_t text_len = strlen(text);
  char *s = calloc(text_len * 3 + 1, sizeof(char));

  for (char *ptr = text; *ptr; ptr++) {
    if (*ptr < 'A' || *ptr > 'z')
      continue;
    int c = 0;
    if (*ptr < 'a')
      c = *ptr - 'A' + 1;
    else
      c = *ptr - 'a' + 1;
    if (ptr == text)
      sprintf(s, "%d", c);
    else
      sprintf(s, "%s %d", s, c);
  }

  return s;
}

_______________________________________________
#include <stdio.h>
char *alphabet_position(char *text) 
{
  
  char *str = calloc(sizeof(char), strlen(text));
  int i = 0, index = 0, a;
  
  while (text[i] != '\0')
  {
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
              if (text[i] >= 'A' && text[i] <= 'Z')
                    a = text[i] - 'A' + 1;
              else if (text[i] >= 'a' && text[i] <= 'z')
                    a = text[i] - 'a' + 1;
                    
              if (a < 10)
              {
                    str[index] = a + '0';
                    index += 1;
              }
              else if (a >= 10)
              {
                    str[index] = (a / 10) + '0';
                    str[index + 1] = (a % 10) + '0';
                    index += 2;
              }
              if (text[i + 1] != '\0')
                    str[index] = ' ';
              index++;
        }
        i++;
  }
  return str;
}

_______________________________________________
#include <stdio.h>
char *alphabet_position(char *text)
{
  char  *ret = calloc(sizeof(char), strlen(text) * 2 + 1);
  int   i = -1;
  int   j = 0;

  while (text[++i])
    if (isalpha(text[i]))
      j += sprintf(&ret[j], "%d ", tolower(text[i]) - 96);
  ret[j - 1] = '\0';
  return (ret);
}

_______________________________________________
#include <stdio.h>
char* alphabet_position(char* text) {
  char* str = malloc(strlen(text) * 3); str[0] = 0;
  int   k   = 0;
  while (*text) {
    if(*text > 64) k += sprintf(str + k, "%d ", *text&31);
    text++;
  }
  str[k - 1] = 0;
  return str;
}

_______________________________________________
#include <stdio.h>
#include <memory.h>

#define STR_MAX_SIZE 32

char* alphabet_position(char* text) {
  char* ret = (char*)malloc(sizeof(char) * STR_MAX_SIZE);
  size_t pos = 0;
  size_t i = 0;
  while(text[i]){
    if(isalpha(text[i])){
      int curr = tolower(text[i]) - ('a'- 1);
      if(curr >= 10){
        ret[pos+1] = curr % 10 + '0';
        ret[pos++] = curr / 10 + '0';
      }else{
        ret[pos] = curr + '0';
      }
      ret[pos+1] = ' ';
      pos += 2;
    }
    i++;
  }
  pos = pos < 1 ? 1 : pos;
  ret[pos-1] = 0;
  return ret;
}
