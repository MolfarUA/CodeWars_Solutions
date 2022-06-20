58e230e5e24dde0996000070


#include <math.h>
#include <stdbool.h>

bool isPrime(unsigned long long n){
  for(int i = 2; i <= sqrt(n); i++){
    if(n % i == 0)
      return false;
  }
  return n > 1;
}

unsigned long long next_prime(unsigned long long n) {
  while(!isPrime(n + 1))
    n++;
  return n + 1;
}
__________________________
#include <math.h>
#include <stdbool.h>

bool isPrime(unsigned long long n){
  for(int i = 2; i <= sqrt(n); i++){
    if(n % i == 0)
      return false;
  }
  return n > 1;
}

unsigned long long next_prime(unsigned long long n) {
  while(!isPrime(n + 1))
    n++;
  return n + 1;
}
__________________________
#include <math.h>
#include <stdbool.h>
typedef unsigned long long uint64;
bool isPrime(uint64 n);

uint64 next_prime(uint64 n) {
  while (!isPrime(++n));
    return n;
}

bool isPrime(uint64 n) {
  for (uint64 i = 2; i <= sqrt(n); i++)
    if ((n % i) == 0)
      return false;
  return n > 1;
}
