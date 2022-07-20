53ee5429ba190077850011d4
  
  
#include <cstdint>

int32_t double_integer(int32_t n) {
  return n << 1;
}
__________________________
#include <cstdint>

int32_t double_integer( int32_t n )
{
  return n * 2;
}
__________________________
#include <iostream>
#include <cstdint>

int32_t double_integer(int32_t n)
{
    return n + n;
}
