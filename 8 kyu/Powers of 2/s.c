#include <inttypes.h>
#include <stddef.h>

void powers_of_two (size_t n, uint64_t powers[n + 1])
{
  for (size_t i = 0; i <= n; i++) {
    powers[i] = (uint64_t)1 << i;
  }
}
___________________________________
#include <inttypes.h>
#include <stddef.h>
#include <math.h>

void powers_of_two (size_t n, uint64_t powers[n + 1])
{
  for (size_t i=0;i<=n;i++) powers[i]=pow(2,i);
}
___________________________________
#include <inttypes.h>
#include <stddef.h>

void powers_of_two (size_t n, uint64_t powers[n + 1])
{
  do powers[n] = 1L << n; while (n--);
}
___________________________________
#include <inttypes.h>
#include <stddef.h>

void powers_of_two (size_t n, uint64_t powers[n + 1])
{
  powers[0] = 1;
  for (size_t i = 1; i <= n; i++) 
    powers[i] = powers[i - 1] * 2;   
}
___________________________________
#include <inttypes.h>
#include <stddef.h>
#include <math.h>

void powers_of_two (size_t n, uint64_t powers[n + 1])
{
  for(int i = 0; i <= n; i++){
    powers[i] = pow(2,i);
  }
}
