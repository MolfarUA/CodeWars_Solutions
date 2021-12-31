#include <stdio.h>
#include <stdlib.h>
#include<stdint.h>

uint64_t minimum(uint64_t a,uint64_t b,uint64_t c){
   uint64_t min;
   if( (a<b) && (a<c) )
   {
      min = a;
   }
   else if(b<c)
   {
      min = b;
   }
   else
   {
      min = c;
   }
   return min;
}

uint64_t hamber(int n)
{   
    uint64_t i2=0,i3=0,i5=0;
    int i=0;
    uint64_t *ugly=calloc(n+1,sizeof(uint64_t));
    ugly[0]=1;
    uint64_t nxt2=ugly[i2]*2;
    uint64_t nxt3=ugly[i3]*3;
    uint64_t nxt5=ugly[i5]*5;
    for(i=1;i<n;i++){
      uint64_t next_ugly=minimum(nxt2,nxt3,nxt5);
      ugly[i]=next_ugly;
      if(next_ugly==nxt2){
        i2++;
        nxt2=ugly[i2]*2;
      }
      if(next_ugly==nxt3){
        i3++;
        nxt3=ugly[i3]*3;
      }
      if(next_ugly==nxt5){
        i5++;
        nxt5=ugly[i5]*5;
      }
    }
    return ugly[n-1];
}

___________________________________________________
#include <stdint.h>
#define MIN(a,b) (((a)<(b))?(a):(b))
uint64_t hamber(int n)
{
    uint64_t ham[n];
    ham[0] = 1;
    uint64_t ham2 = 2, ham3 = 3, ham5 = 5;
    int i = 0, j = 0, k = 0;
 
    for (int m = 1; m < n; m++) 
    {
      ham[m] = MIN(ham2, MIN(ham3, ham5));
      if (ham[m] == ham2) ham2 = 2 * ham[++i];
      if (ham[m] == ham3) ham3 = 3 * ham[++j];
      if (ham[m] == ham5) ham5 = 5 * ham[++k];
    }
    
    return ham[n - 1];
}

___________________________________________________
#include <stdint.h>
#include <stdlib.h>

#define PRIME_COUNT 3

uint64_t min_element(uint64_t *arr, uint64_t n)
{
    uint64_t min = arr[0];
    for (int i = 1; i < n; i++)
    {
        if (min > arr[i])
            min = arr[i];
    }
    return min;
}

uint64_t hamber(int n)
{
    uint64_t hamming_numbers[n];
    hamming_numbers[0] = 1;

    const uint64_t BASE_PRIMES[] = {2, 3, 5}; // base primes
    uint64_t indices[] = {0, 0, 0};           // indices back into hamming numbers
    uint64_t next_multiple[] = {2, 3, 5};     // next multiples: xs[k]==ps[k]*h[is[k]]

    for (size_t i = 1; i < n; i++)
    {
        hamming_numbers[i] = min_element(next_multiple, PRIME_COUNT);

        for (size_t j = 0; j < PRIME_COUNT; j++)
        {
            if (hamming_numbers[i] == next_multiple[j])
                next_multiple[j] = BASE_PRIMES[j] * hamming_numbers[++indices[j]];
        }
    }

    return hamming_numbers[n - 1];
}

___________________________________________________
#include <stdint.h>
#include <stdlib.h>

#define PRIME_COUNT 3
uint64_t min_element(uint64_t arr[PRIME_COUNT])
{
    uint64_t min = arr[0];
    for (int i = 1; i < PRIME_COUNT; i++)
    {
        if (min > arr[i])
            min = arr[i];
    }
    return min;
}

uint64_t hamber(int n)
{
    size_t sz = 0;
    uint64_t *hamming_numbers = NULL;
    hamming_numbers = (uint64_t *)realloc(hamming_numbers, (sz += 16) * sizeof(uint64_t));
    int pos = -1;
    hamming_numbers[++pos] = 1;

    uint64_t base_primes[PRIME_COUNT] = {2, 3, 5};   // base primes
    uint64_t indices[PRIME_COUNT] = {0, 0, 0};       // indices back into hamming numbers
    uint64_t next_multiple[PRIME_COUNT] = {2, 3, 5}; // next multiples: xs[k]==ps[k]*h[is[k]]

    for (size_t i = 0; i < n; i++)
    {
        uint64_t most_recent = min_element(next_multiple);
        hamming_numbers[++pos] = most_recent;
        if (pos == sz - 1)
            hamming_numbers = (uint64_t *)realloc(hamming_numbers, (sz += 16) * sizeof(uint64_t));

        for (size_t j = 0; j < PRIME_COUNT; j++)
        {
            if (next_multiple[j] == most_recent)
                next_multiple[j] = base_primes[j] * hamming_numbers[++indices[j]];
        }
    }
    uint64_t ret = hamming_numbers[n - 1];
    free(hamming_numbers);

    return ret;
}
