56d0a591c6c8b466ca00118b


#include <stdbool.h>

bool is_triangular(long t) {
    double d = sqrt(8 * t + 1);
    return d == (long long) d;
}
__________________________
#include <stdbool.h>
#include <math.h>

bool is_triangular(long t) {
  long n = floor(sqrt(2*t));
  return n*(n+1) == 2*t;
}
__________________________
#include <stdbool.h>

bool is_triangular(int t) {
  int ok = 0;
  for (int i = 1; i <= t; i++) {
    ok += i;
    if (ok == t) {
      return true;
    } 
  }
  
  return false;
}
__________________________
#include <math.h>
#include <stdbool.h>

bool is_triangular(int t) {
  return (fmod(-1 + sqrt(1 + 8 * (double) t), 2) == 0 || fmod(-1 - sqrt(1 + 8 * (double) t), 2) == 0);
}
__________________________
#include <stdbool.h>

bool is_triangular(int t) {
  int sum = 0;
  
  for(int i = 0;; i++){
    sum += i;
    if(sum >= t)
      break;
  }
  if(sum == t)
    return true;
  return false;
}
__________________________
#include <stdbool.h>
#include <math.h>
bool is_triangular(int t) {
  double x = (double)t;
  x = (sqrt(x * 8 + 1) - 1) / 2;
  double y = (int)x;
  y = fabs(y - x);
  return y < 1e-6;
}
__________________________
#include <stdbool.h>
#include <math.h>

bool is_triangular(long t) {
    long n = sqrt(2 * t);
    return n * (n + 1) == 2 * t;
}
__________________________
#include <stdbool.h>
#include <inttypes.h>
#include <limits.h>

bool is_perfect_square(int64_t n);

bool is_triangular(int t) {
    return is_perfect_square((int64_t)t * 8 + 1);
}

bool is_perfect_square(int64_t n){
    int64_t sum = 0;
    for (int i = 1; sum <= (int64_t)INT32_MAX * 8 + 1; i += 2){
        sum += i;
        if (sum == n)
            return true;
    }
    return false;
}
