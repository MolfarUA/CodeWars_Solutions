int *parse(char *program)
{
  int *ret = malloc(sizeof(int) * strlen(program)), *r = ret;
  int v = 0;
  for (char *p = program; *p; p++)
  {
    switch (*p) 
    {
      case 'i' : v++;      break;
      case 'd' : v--;      break;
      case 's' : v*=v;     break;
      case 'o' : *r++ = v; break;
    }  
  }
  return ret;
}
__________________________________________
int* count_outputs(char *program)
{
  int outputs = 0;
  
  char c;
  while (c = *program++)
  {
    if (c == 'o') 
    {
      ++outputs;
    }
  }
  
  return outputs;
}

int* parse(char* program)
{
  int val = 0;
  int result_len = count_outputs(program);
  int *result = malloc(result_len * sizeof(int));
  int outputPos = 0;
  
  char c;
  while (c = *program++) 
  {
    if (c == 'i') { ++val; }
    else if (c == 'd') { --val; }
    else if (c == 's') { val *= val; }
    else if (c == 'o') { result[outputPos++] = val; }
  }
  
  return result;
}
__________________________________________
#include <stdio.h>
#include <stdlib.h>

int* parse(const char* program) {
    int outputSize = 0;
    int value = 0;
    int index = 0;
    int* output;
    char * current = program;
    while (*current) {
        if (*current == 'o') outputSize++;
        current++;
    }
    output = malloc(outputSize*sizeof (int));
    if (output == NULL) exit(1);
    
    current = program;
    while (*current) {
        switch (*(current++)) {
            case 'o': {
                output[index++] = value;
                break;
            }
            case 'i': {
                value++;
                break;
            }
            case 'd': {
                value--;
                break;
            }
            case 's': {
                value *= value;
                break;
            }
        }
    }
    
    return output;
}
__________________________________________
#include<stdio.h>

int* parse(char* program)
{
  int value = 0; // initiating integer to append to array
  int* returnarr; // initiating array

  unsigned long int size = 0; // initial size of the array
  returnarr = malloc(size * sizeof(int)); // allocating size 0 initially
  
  while( *program != '\0')
  {
    switch (*program)
    {
        case 'i': value++; break;
        case 'd': value--; break;
        case 's': value *= value; break;
        case 'o':  
            size++; 
            returnarr = realloc(returnarr, size*sizeof(int));  // increase size of array
            returnarr [size-1] = value; // assigning value to returnarr
            break;
        default: break;
    }
    program++;
  }
  return returnarr;
}
