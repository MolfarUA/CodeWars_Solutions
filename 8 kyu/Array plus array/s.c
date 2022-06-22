5a2be17aee1aaefe2a000151


#include <stddef.h>

long arr_plus_arr(const int *a,  const int *b, size_t na, size_t nb)
{
    long total = 0;
    for(int i=0; i<na;i++) total += a[i];
    for(int i=0; i<nb;i++) total += b[i];
    return total;
}
_________________________
#include <stddef.h>

long arr_plus_arr(const int *a,  const int *b, size_t na, size_t nb)
{
    long t = 0;
    while (na--) t += *a++;
    while (nb--) t += *b++;
    return t;
}
_________________________
#include <stddef.h>

long arr_plus_arr(const int *a,  const int *b, size_t na, size_t nb)
{ long sum_a = 0;
  long sum_b = 0;
    for (int i=0; i<(int) na; i++) {
      sum_a += a[i];
    }
    for (int j=0; j<(int) nb; j++) {
      sum_b += b[j];
    }
    return sum_a + sum_b;
}
