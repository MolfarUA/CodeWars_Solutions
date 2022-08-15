52f677797c461daaf7000740


#include <stddef.h>

int GCD(int a, int b) {
    while (a) {
        b %= a;
        if (!b) return a;
        a %= b;
    }
    return b;
}

int smallest_possible_sum(size_t n, const int array[n]) {
    size_t i; int ret;
    ret = array[0];
    for (i =1; i<n && ret>1; i++) ret = GCD(ret, array[i]);
    return ret*n;
}
_______________________________
#include <stddef.h>

int change ( int start, int tmp )
{
  while ( tmp != start )
  {
    if ( tmp > start )
    {
      if ( tmp % start == 0 )
        return start;
      tmp %= start;
    } else
    {
      if ( start % tmp == 0 )
        return tmp;
      start %= tmp;
    }
  }
  return tmp;
}


int smallest_possible_sum(size_t n, const int array[n]) 
{
  if ( n == 1 )
    return array[0];
  int tmp, start = array[0];
  for (size_t i = 1; i < n; i++)
  {
    tmp = array[i];
    tmp = change (start, tmp);
    if ( tmp == 1 )
      return n;
    start = tmp;
  }
  return tmp * n;
}
_______________________________
#include <stddef.h>

int gcd(int x, int y)
{
    while(y)
    {
        int z = x;
            x = y;
            y = z % y;
    }
    return x;
}

int smallest_possible_sum(size_t n, const int array[n])
{
    int x = 0; size_t i = n;
    while(i) x = gcd(array[--i], x);
    return x * (int)n;
}
