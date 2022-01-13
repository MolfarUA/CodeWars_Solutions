#include <stdbool.h>
#include <math.h>

bool is_constructable(long a)
{
  long n = floor(sqrt(a));
  // Try to find a y, such that x² + y² = a
  // (This is an application of Pythagoras)
  for (int x = n; x >= 0; x--) {
    double y = sqrt(a - pow(x, 2));
    if (y == floor(y))
      return true;
  }
  return false;
}
__________________________________
#include <stdbool.h>
#include <math.h>

long sqrt_long(long x)
{
    return (long)(sqrt(x) + 1e-6);
}

bool is_perfect_square(long x)
{
    long t = sqrt_long(x);
    return t * t == x;
}

bool is_constructable(long a)
{
    long m = sqrt_long(a);
    for (long x = 0; x <= m; ++x) {
        if (is_perfect_square(a - x * x)) return true;
    }
    return false;
}
__________________________________
#include <math.h>
#include <stdbool.h>

bool is_constructable(long area) {
    long max_side = sqrt(area);
    for (long i = 0; i <= max_side; i++) {
        double side = sqrt(area - i * i);
        if (side == (long) side) {
            return true;
        }
    }
    return false;
}
__________________________________
#include <math.h>
#include <stdbool.h>

bool is_constructable(long area) {
    // Is "area" the sum of two perfect squares?
    long side = sqrt(area);
    for (long num = 0; num <= side; num++) {
        double temp = sqrt(area - num * num);
        if (temp == (long) temp) {
            return true;
        }
    }
    return false;
}
__________________________________
#include <stdbool.h>
#include <math.h>

bool is_constructable(long a)
{
  long sq = sqrt(a);
  if(sq*sq == a) return true;
  for(long i=1;i<=sq;i++) 
    for(long j=sq;j>0;j--) 
      if(a == i*i + j*j) return true;
  return false;
}
