53ee5429ba190077850011d4


#include <stdint.h>

int32_t double_integer(int32_t number){
  return number*2;
};
__________________________
#include <stdint.h>

int32_t double_integer(int32_t n) {
  return n << 1;
}
__________________________
#include <stdint.h>

int32_t double_integer(int32_t x) {
  return 2*x;
}
__________________________
#include <stdint.h>

int32_t double_integer(int32_t var)
{
  return var + var;
}
