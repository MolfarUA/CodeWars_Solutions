561e9c843a2ef5a40c0000a4


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool isPrime(long long n) {
  if (n % 2 == 0) return false;
  for (int i = 3; i * i <= n ; i += 2)
    if (n % i == 0) return false;
  return true;
}
long long* gap(int g, long long m, long long n) {
    long long* candidates = (long long*)calloc(2, sizeof(long long));
    candidates[0] = 0; candidates[1] = 0;
    long long i = m;
    for (; i <= n; i++) {
        if (candidates[1] - candidates[0] == (long long)g) {
            return candidates;
        }
        if (isPrime(i)) {
            candidates[0] = candidates[1];
            candidates[1] = i;
        }
    }
    candidates[0] = 0; candidates[1] = 0;
    return candidates;
}
__________________________________
#include <math.h>
int is_prime(long long num);

long long* gap(int g, long long m, long long n) {
  long long *res = malloc(sizeof(long long)*2);
  long long j=0;
  for (long long i=m;i<=n;i++) {
    if(is_prime(i)){
      if(i-j==g){
        res[0] = j;
        res[1] = i;
        return res;
      }
      j=i;
    }
  }
  res[0] = 0;
  res[1] = 0;
  return res;
}

int is_prime(long long num) {
     if (num <= 1) return 0;
     if (num % 2 == 0 && num > 2) return 0;
     for(long long i = 3; i <= sqrt(num) ; i+= 2){
         if (num % i == 0)
             return 0;
     }
     return 1;
}
__________________________________
#include <stdio.h>
#include <stdlib.h>

typedef int bool;
#define true 1
#define false 0

bool isPrime(long long n)
{
  if(n <= 3 && n > 1)
    return true;
  else if(n%2 == 0 || n%3 == 0)
    return false;
  else
  {
    for(unsigned int i = 5; i * i <= n; i += 6)
      if(n % i == 0 || n % (i + 2) == 0)
        return false;
  }
  return true;
}

long long *gap(int g, long long m, long long n)
{
  long long *ans = (long long *) calloc(2, sizeof(long long));

  while(m < n)
  {
    //Find the next prime and if  number + g is also prime
    if(isPrime(m) && isPrime(m + g))
    {
      long long i = m + 1;
      //Search if there is a prime number in between
      for(i; i < m + g; ++i)
        if(isPrime(i))
          break;

      if(i == m + g)
      {
        ans[0] = m;
        ans[1] = i;
        break;
      }
    }
    ++m;
  }
  return ans;
}
