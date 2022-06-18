#include <stddef.h>
#include <inttypes.h>

void digitize (uint64_t n, uint8_t digits[], size_t *length_out)
{
  *length_out = 0;
  do {
    digits[(*length_out)++] = n % 10;
    n /= 10;
  } while(n);
}
________________________
#include <stddef.h>
#include <inttypes.h>

void digitize (uint64_t n, uint8_t digits[], size_t *length_out) {
    uint64_t x1=1;
    uint64_t x2=9;
    *length_out=0;
    uint64_t temp = n;
    while(temp) {
        *length_out+=1;
        temp /=10;
    }
    if(n==0) {
        *length_out=1;
    }
    for(uint64_t i=0; i<*length_out; i++) {
        digits[i] = n%10;
        n=n/10;
    }
}
________________________
#include <stddef.h>
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
void digitize (uint64_t n, uint8_t digits[], size_t *length_out)
{
  int i = 0, j;
  int  size =0;
  char number[30]; 
  sprintf(number,"%lu", n);
  *length_out = strlen(number);
  size = strlen(number);
  j = size-1;
  
  for(i;i<size;i++)
  {
    digits[i] = (number[j--] - '0');
  }
  
}
________________________
#include <stddef.h>
#include <inttypes.h>

void digitize (uint64_t n, uint8_t digits[], size_t *length_out)
{
  digits[0] = 6;
  int x=0;
  if(n == 0){ x = 1; digits[0] = 0;}
  for (int i = 0; n != 0; n /=10, i++){
    digits[i]= n%10;
    printf("%d ", x);
    x++;
  }

  *length_out = x;
}
________________________
#include <stddef.h>
#include <inttypes.h>

#include <stdio.h>

void digitize (uint64_t n, uint8_t digits[], size_t *length_out)
{
  if(n == 0) {
    *length_out = 1;
    digits[0] = 0;
  } else {
    int i;
    for(i=0; n > 0; i++) {
      digits[i] = n % 10;
      n /= 10;
    }
    *length_out = i;
  }
}
________________________
#include <stdio.h>
#include <stddef.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>

void digitize (uint64_t n, uint8_t digits[], size_t *length_out)
{
  char s[100];
  sprintf(s, "%lu", n);
  int len = strlen(s)-1;
  *length_out = (size_t)strlen(s);
  digits[len] = '\0';
  
  int i = 0;
  while(s[i] != '\0'){
    digits[len--] = s[i++]-48;
  };

}
