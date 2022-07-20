54d496788776e49e6b00052f


// In C return a char *
char* sumOfDivided(int* lst, int l) {
  long int sum;
  int atleast;
  char *result = calloc(1000, sizeof(char));
  char *buffer = calloc(25, sizeof(char));
  for(int i = 2; i <= absmax(lst, l); i++) {
    if(isSimple(i)) {
      sum = 0; atleast = 0;
      for (int j = 0; j < l; j++)
        if (lst[j] % i == 0) {
          sum += lst[j];
          atleast = 1;
        }
      if (atleast) {
        sprintf(buffer, "(%ld %ld)", i, sum);
        strcat(result, buffer);
      }
    }
  }
  return result;
}

int isSimple(int n) {
  for (int i = 2; i <= sqrt(n); i++)
    if (n % i == 0)
      return 0;
  return 1;
}

int absmax(int *lst, int l) {
  int max = 0;
  for (int i = 0; i < l; i++)
    if (abs(lst[i]) > max)
      max = abs(lst[i]);
  return max;
}
________________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

typedef struct Data Data;

struct Data {
  int* array;
  int size;
};

char* array2StringDataInt(Data *d) {
  if (d->size == 0) return "";
  int l = d->size;
  int* list = d->array;
  char *dest = (char*)calloc(l + 1, sizeof(int) + 2);
  char *p = dest;

  for(int i = 0; i < l; i += 2) {
    sprintf(p += strlen(p), "(%d %d)", list[i], list[i + 1]);
  }

  free(d->array);
  free(d);
  return dest;
}

int* arrdup(int const *src, int len) {
  int* p = malloc(len * sizeof(int));
  memcpy(p, src, len * sizeof(int));
  return p;
}

Data* sumOfDividedAux(int* lst, int l) {
  Data* d = (Data*)malloc(sizeof(Data));
  int* list = (int*)malloc(0 * sizeof(int));
  int sizearr =  0;

  int* rem = arrdup(lst, l);
  int max = 0;

  for (int i = 0; i < l; ++i) {
    int v = abs(lst[i]);
    rem[i] = v;
    max = max > v ? max : v;
  }

  for (int fac = 2; fac <= max; ++fac) {
    bool isFactor = false;
    int tot = 0;

    for (int i = 0; i < l; ++i) {
      if (rem[i] % fac == 0) {
        isFactor = true;
        tot += lst[i];
        while (rem[i] % fac == 0)
          rem[i] /= fac;
      }
    }

    if (isFactor) {
      list = (int*)realloc(list, (sizearr + 2) * sizeof(int));
      list[sizearr] = fac;
      list[sizearr + 1] = tot;
      sizearr += 2;
    }
  }

  free(rem);
  d->size = sizearr;
  d->array = list;
  return d;
}

char* sumOfDivided(int* lst, int l) {
  Data* d = sumOfDividedAux(lst, l);
  char* s = array2StringDataInt(d);
  return s;
}
________________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

typedef struct Data Data;
struct Data {
     int* array;
     int sz;
};
char* array2StringDataInt(Data *d) {
    if (d->sz == 0) return "";
    int l = d->sz;
    int* arr = d->array;
    char *dest = (char*)calloc(l + 1, sizeof(int) + 2);
    char *p = dest;
    for(int i = 0; i < l; i += 2) {
        sprintf(p += strlen(p), "(%d %d)", arr[i], arr[i + 1]);
    }
    free(d->array);
    free(d);
    return dest;
}
int* arrdup(int const *src, int len) {
   int* p = malloc(len * sizeof(int));
   memcpy(p, src, len * sizeof(int));
   return p;
}
Data* sumOfDividedAux(int* lst, int l) {
    Data* d = (Data*)malloc(sizeof(Data));
    int* arr = (int*)malloc(0 * sizeof(int));
    int szarr =  0;

    int* rem = arrdup(lst, l);
    int max = 0;
    for (int i = 0; i < l; ++i) {
        int v = abs(lst[i]);
        rem[i] = v;
        max = max > v ? max : v;
    }

    for (int fac = 2; fac <= max; ++fac) {
        bool isFactor = false;
        int tot = 0;
        for (int i = 0; i < l; ++i) {
            if (rem[i] % fac == 0) {
                isFactor = true;
                tot += lst[i];
                while (rem[i] % fac == 0)
                    rem[i] /= fac;
            }
        }
        if (isFactor) {
            arr = (int*)realloc(arr, (szarr + 2) * sizeof(int));
            arr[szarr] = fac;
            arr[szarr + 1] = tot;
            szarr += 2;
        }
    }
    free(rem);
    d->sz = szarr;
    d->array = arr;
    return d;
}
char* sumOfDivided(int* lst, int l) {
    Data* d = sumOfDividedAux(lst, l);
    char* s = array2StringDataInt(d);
    return s;
}
________________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int is_prime(int x) {
  if (x < 4) return 1;
  if (x % 2 == 0) return 0;
  if (x % 3 == 0) return 0;

  int k = 5;
  int m = 2;
          
  while (k * k <= x) {
    if (x % k == 0) return 0;
    k += m;
    m = 6 - m;
  }
            
  return 1;
}

int maximum_prime_factor(int x) {
  if (x < 0) return maximum_prime_factor(-x);
  if (is_prime(x)) return x;
  if (x == 4) return 2;
  
  if (x % 2 == 0) x /= 2;
  
  int max_factor = 2;
  for (int i = 3; x > 1 && i <= x; i += 2) {
    if (is_prime(i) && x % i == 0) {
      max_factor = i;
      x /= i;
    }
  }
  return max_factor;
}

int maximum_prime_factor_array(int *array, int n) {
  if (n == 0) return 0;
  
  int max = maximum_prime_factor(array[0]);
  for (int i = 1; i < n; i++) {
    int curr_max = maximum_prime_factor(array[i]);
    if (curr_max > max) max = curr_max;
  }

  return max;
}

int sum_factors(int *array, int n, int factor, int *count) {
  *count = 0;
  int sum = 0;
  for (int i = 0; i < n; i++) {
    if (array[i] % factor == 0) {
      *count = *count + 1;
      sum += array[i];
    }
  }
    
  return sum;
}

char* concat_sum_factor(int *array, int n, int factor, char *ptr) {
  int count = 0;
  int sum = sum_factors(array, n, factor, &count);
  if (count > 0) {
    sprintf(ptr, "(%d %d)", factor, sum);
    while (*ptr) ptr++;
  }
  return ptr;
}

char* sumOfDivided(int* array, int n) {
  int max_factor = maximum_prime_factor_array(array, n);
  char buffer[2048] = {0};
  
  char *ptr = buffer;
  ptr = concat_sum_factor(array, n, 2, ptr);
  
  for (int i = 3; i <= max_factor; i += 2) {
    if (is_prime(i)) {
      ptr = concat_sum_factor(array, n, i, ptr);
    }
  }

  return strdup(buffer);
}
