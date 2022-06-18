#include <stdio.h>

char *find_needle(const char **haystack, size_t count)
{
  for(int i=0; i<count;++i)
  {
    if(!strcmp(haystack[i], "needle")) // strcmp will return 0 if true, so we need '!' to it to work
    {
      char* buff;
      asprintf(&buff, "found the needle at position %d", i);
      return buff;
    }
  }
}
________________________
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

char *find_needle(const char **haystack, size_t count)
{
  while (strcmp(haystack[--count], "needle"));
  char *buf = malloc(128);
  sprintf(buf, "found the needle at position %d", count);
  return buf;
}
________________________
#include <stddef.h>
#include <string.h>
#include <stdio.h>

char *find_needle(const char **haystack, size_t count){
  char * return_string = malloc(100);
  int i;
  
  for(i = 0; i < (int)count && strcmp(haystack[i],"needle"); i++);
  
  sprintf(return_string,"found the needle at position %d",i);
  
  return !strcmp(haystack[i],"needle") ? return_string: 0;
}
________________________
#include <stddef.h>
#include <string.h>
#include <stdio.h>

char *find_needle(const char **haystack, size_t count){
  int index;
  for(index = 0; index<count; index++)
    if(strcmp(haystack[index],"needle")==0)
      break;
  static char ret[40];
  sprintf(ret,"found the needle at position %d", index);
  return ret;
}
________________________
#include <stddef.h>
#include <stdio.h>
#include <string.h>

char result[32];
char *find_needle(const char **haystack, size_t count){
  for(unsigned long i = 0;i < count;i++)
    if(!strcmp(haystack[i], "needle"))
      sprintf(result, "found the needle at position %lu", i);
  return result;
}
