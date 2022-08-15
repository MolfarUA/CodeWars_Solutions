5659c6d896bc135c4c00021e


#include <string.h>
#include <stdlib.h>

void swap(char *a, char *b){
    char temp = *a; 
    *a = *b; 
    *b = temp; 
}

unsigned long long next_smaller_number(unsigned long long n){
    unsigned long long final;
    char *num, *current, *prev, *big, sm = '0';
    asprintf(&num, "%lld", n);
    const size_t size = strlen(num);

    //check special cases:
    if(size == 1) return -1;    //if num consists merely of 1 digit
    int flag = 0;   //is it possible to make smaller num
    for(size_t i = 0; i < size - 1; i++){
        if(num[i] - '0' > num[i+1] - '0'){
            flag = 1;
            break;
        }
    }
    if(flag == 0) return -1;

    //finding number which digit is bigger than the previous one
    short i;
    for(i = size - 2; i >= 0; i--){
        current = &num[i];
        prev = &num[i+1];
        if(*current - '0' > *prev - '0') break;
    }
    //finding the biggest number from the right of number from above which is smaller than current
    big = &sm;
    for(short j = size-1; j > i; j--)
        if(num[j] - '0' < *current - '0' && *big - '0' <= num[j] - '0') big = &num[j];
    //swap them
    swap(current, big);
    //sort the right side in the descent order
    for(size_t q = i+1; q < size; q++){
        for(size_t k = q+1; k < size; k++){
            if(num[k] - '0' > num[q] - '0'){
                swap(&num[k], &num[q]);
            }
        }
    }
    if(num[0] == '0') return -1;    //check whether the first digit is '0'
    final =  (unsigned long long)atoll(num);    //convert the new number which is now represented by string
    free(num);    //asprintf() function allocates memory dynamically
    return (n != final && final < n) ? final : -1;
}
_______________________________
#include <limits.h>

#define FMT_LLONG       (CHAR_BIT * sizeof(long long) / 3)
#define SWAP(r, a, b)   (r = a, a = b, b = r)

long long next_smaller_number(long long num)
{
    unsigned char dig[FMT_LLONG];
    int x, n, i, j, nd = 0;
    do
        dig[nd++] = num % 10;
    while (num /= 10);
    x = -1;
    for (i = 1; i < nd; ++i) {
        if (dig[i] > dig[i-1]) {
            n = j = i - 1;
            while (j--)
                if (dig[i] > dig[j] && dig[n] < dig[j])
                    n = j;
            SWAP(x, dig[n], dig[i]);
            break;
        }
    }
    if (x == -1 || !x && i+1 == nd)
        return -1;
    while (i--) {
        j = n = i;
        while (j--)
            if (dig[n] < dig[j])
                n = j;
        if (n != i)
            SWAP(x, dig[n], dig[i]);
    }
    while (nd--)
        num = num * 10 + dig[nd];
    return num;
}
_______________________________
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

int comp(const void *a, const void *b) {return (*(char*)b - *(char*)a);}

long long next_smaller_number(unsigned long long n){
    //insert code here
    uint32_t nLen = snprintf(0, 0, "%lld", n);
    char *nStr = (char *) calloc(nLen + 1, sizeof(char));
    snprintf(nStr, nLen + 1, "%lld", n);
  
    int lastChar = nLen - 1;
    int max = 0;
  
    for (int i = lastChar - 1; i >= 0; i--) {
      if (nStr[i] <= nStr[i + 1]) continue;
      max = i + 1;
      for (int j = i + 1; j <= lastChar; j++) 
          if (nStr[j] < nStr[i] && nStr[j] > nStr[max]) max = j;
      char tmp = nStr[i];
      nStr[i] = nStr[max];
      nStr[max] = tmp;
      qsort(nStr + i + 1, lastChar - i, sizeof(char), comp);
      break;
    }
    
    if (max && nStr[0] != '0') return strtoll(nStr, 0, 10);
    return -1;
}
_______________________________
#define swap(a, b) { char t = a; a = b; b = t; }

void reverse(char * buf, int sz) {
  for (int i = 0, hsz = sz/2; i < hsz; ++i)
    swap(buf[i], buf[sz - i - 1]);
}

unsigned long long next_smaller_number(unsigned long long n){
  char buf[64];
  int sz = sprintf(buf, "%llu", n);
  reverse(buf, sz);
  
  int slope = 1;
  for (; slope < sz && buf[slope] <= buf[slope - 1]; ++slope);
  if (slope == sz) return -1;
  
  int pivot = 0;
  for (; buf[pivot] >= buf[slope]; ++pivot);

  swap(buf[pivot], buf[slope]);
  reverse(buf, slope);
  reverse(buf, sz);
  
  if (buf[0] == '0') return -1;
  
  return strtoull(buf, 0, 10);
}
