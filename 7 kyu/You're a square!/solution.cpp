#include<cmath>

bool is_square(int n) {
  if (n < 0) return false;
  int square = sqrt(n);
  return square * square == n;
}
__________________________________
#include <cmath>

bool is_square(int n)
{
  return fmod(sqrt(n), 1) == 0;
}
__________________________________
bool is_square(int n)
{
  for (int i = 0; i <= n/2 + 1; i++){
  if ( i * i == n)
  return true;
  }
  return false;
}
__________________________________
#include <math.h>
bool is_square(int n)
{
  double x;
  if(n<0) return false;
  x=sqrt(n);
  if(int(x)!=x) return false;
  return true;
}
