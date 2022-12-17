598d91785d4ce3ec4f000018


#include <stddef.h>

int wv(const char *str) 
{
  int v = 0;
  for (char *p = str; *p; p++)
  {
    if (*p != ' ') v += *p - 'a' + 1;
  }
  return v;
}

const int* name_value(size_t n, const char *const words[n]) 
{
  int * arr = malloc(n * sizeof(int));
  for (int i = 0; i < n; i++)
  {
    arr[i] = (i+1) * wv(words[i]);
  }
  return arr;
}
_____________________________
#include <stddef.h>
#include <stdlib.h>
const int* name_value(size_t n, const char *const words[n]) {
    int *result = (int*)calloc(n, sizeof(int));
    for(int i=0; i<n; i++){
        for(int k=0; words[i][k] !='\0'; k++) if(words[i][k] != ' ') result[i] += words[i][k] - 'a' + 1;
        result[i] *= (i+1);
    }
    return result;
}
_____________________________
#include <stddef.h>

const int* name_value(size_t n, const char *const words[n]) 
{
  int *arr = calloc(n, sizeof(int));
  while (n--) for (char *s = words[n]; *s; s++) arr[n] += (*s != ' ') * (n + 1) * (*s - 'a' + 1);
  return arr;
}
