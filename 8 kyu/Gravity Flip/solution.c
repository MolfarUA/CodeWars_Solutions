#include <stddef.h>
#include <stdlib.h>
#include <string.h>

int int_asc_cmp (const void *a, const void *b) { return (*(int*)a - *(int*)b); }
int int_desc_cmp (const void *a, const void *b) { return (*(int*)b - *(int*)a); }

void flip(char d, const int *array, size_t n, int *result) {
    memcpy(result, array, n * sizeof(int));
    qsort(result, n, sizeof(int), d == 'R' ? int_asc_cmp : int_desc_cmp);
}

____________________________
#include <stddef.h>

void flip(char d, int *array, int n, int *result) {

    if(d == 'R')
    {
      for(int i=0;i<n;i++)
      {
        for(int j=i;j<n;j++)
        {
          if(array[i]>array[j])
          {
            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
          }
        }
        result[i]=array[i];
      }
    }
    else
    {
      for(int i=0;i<n;i++)
      {
        for(int j=i;j<n;j++)
        {
          if(array[i]<array[j])
          {
            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
          }
        }
        result[i]=array[i];
      }
    }    
    
 
}
____________________________
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

cmpL (*a, *b) { return *b - *a; }
cmpR (*a, *b) { return *a - *b; }

void flip(char d, const int *array, size_t n, int *result) 
{
  memcpy(result, array, n * sizeof(int));
  qsort(result, n, sizeof(int), d == 'L' ? cmpL : cmpR);
}

____________________________
#include <stddef.h>
#include <stdlib.h>

typedef int (*srt_func)(const void*, const void*);

int asc(const void* a, const void* b) { return ( *(int*)a - *(int*)b ); }
int dsc(const void* a, const void* b) { return ( *(int*)b - *(int*)a ); }
srt_func srt(char d) { return d == 'R' ? asc : dsc; }

void flip(char d, const int* array, size_t n, int* result) {
  for (int i = 0; i < (int)n; i++) result[i] = array[i];
  qsort(result, n, sizeof(int), srt(d));
}
