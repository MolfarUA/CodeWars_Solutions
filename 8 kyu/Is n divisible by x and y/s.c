5545f109004975ea66000086


#include <stdbool.h>

bool isDivisible(int n, int x, int y) {
  return n % x == 0 && n % y == 0;
}
_____________________
#include <stdbool.h>

bool isDivisible(int n, int x, int y) {
  return n%x == 0 && n%y == 0 ? 1 : 0;
}
_____________________
#include <stdbool.h>

bool isDivisible(int n, int x, int y) 
{
  if(!(n % x || n % y))
    return true;
  else
    return false;
}
