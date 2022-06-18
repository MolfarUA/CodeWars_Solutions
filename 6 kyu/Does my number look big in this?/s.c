#include <stdbool.h>
#include <math.h>

bool narcissistic(int num)
{
    int p = log10(num) + 1;
    int n = num;
    do
        num -= pow(n % 10, p);
    while (n /= 10);
    return !num;
}
________________________
#include <stdbool.h>
#include <math.h>

bool narcissistic(int num)
{
  long sum = 0;
  for (int v = num, ndigits = log10(num) + 1; v; v /= 10)
  {
    sum += pow(v % 10, ndigits);
    if (sum > num) return false;
  }
  return sum == num;
}
________________________
#include <stdbool.h>
#include <math.h>


bool narcissistic(int num)
{
  int number_digits = log10(num)+1;
  int cpy = num;
  do 
    num -= pow(cpy % 10, number_digits);
  while(cpy /= 10);
  return !num;
}
________________________
#include <stdbool.h>
#include <stdio.h>
#include <math.h>

bool narcissistic(int num)
{
    int divisor = 1;
    int length = 0;
    int aux = num;
    int sum = 0;
  
    while (aux) {
        aux /= 10;
        divisor *= 10;
        length++;
    }
  
    aux = num;
  
    printf("\n\nEach number:");
  
    while (divisor>1) {
        divisor /= 10;
        sum += (pow((aux/divisor), length));
        
        printf("%i",(aux/divisor));
        
        aux = aux % divisor; 
    }
  
    printf("\nLength: %i", length);
    printf("\nSum: %i", sum);
  
    if (sum == num) {
      return true;
    }
  
    return false;
}
