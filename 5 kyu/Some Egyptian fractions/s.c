54f8693ea58bce689100065f

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* array2StringLongLong(long long* array, int sz);

char* decompose(char* nrStr, char* drStr) {
    long long num = strtoll(nrStr, NULL, 10), den = strtoll(drStr, NULL, 10);
    long long* arr = (long long*)malloc(0 * sizeof(long long));
    int cnt = 0;
    if (num > den) {
        arr = (long long*)realloc(arr, (cnt + 1) * sizeof(long long));
        arr[cnt++] = num / den;
        num %= den;
    }
    for (int i = 2; ; i++) {
        if (den <= i * num) {
            arr = (long long*)realloc(arr, (cnt + 2) * sizeof(long long));
            arr[cnt++] = 1;
            arr[cnt++] = i;
            num = num * i - den;
            den *= i;
        }
        if (num == 0)
            break;
    }
    char* res =array2StringLongLong(arr, cnt);
    free(arr);
    return res;
}
_________________________________
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
char* decompose(const char* nrStr, const char* drStr) {
    char *out = malloc(sizeof(char) * 1000);
    char *ptr = out;
    *out = 0;
    unsigned long long d;
    unsigned long long nr = strtol(nrStr, (char **)NULL, 10), dr = strtol(drStr, (char **)NULL, 10), nr2 = 0, dr2 = 1;
    if (nr > dr) {
        unsigned long long divisor = nr / dr;
        nr -= divisor * dr;
        sprintf(ptr, "%llu,", divisor);
        ptr += 2 + (int)(log10(divisor));
    }
    while (nr2 * dr != nr * dr2) {
        d = ceil(1/((double)(nr * dr2 - dr * nr2) / (double)(dr * dr2)));
        nr2 = dr2 + d * nr2;
        dr2 *= d;
        sprintf(ptr, "1/%llu,", d);
        ptr += 4 + (int)(log10(d));
    }
    *--ptr = 0;
    return out;
}
_________________________________
#include <stdlib.h>
#include <math.h>
#include <stdio.h>


typedef long long ll;

// extending array of denominators
typedef struct s_DomList DomList;
struct s_DomList {
  ll *data;
  ll wholepart;
  size_t size;
  size_t allocated;
};


#define CLEAR(domlist) (domlist_clear(&(domlist)))

void domlist_clear(DomList *domlist) {
  free(domlist->data);

  domlist->data = NULL;
  domlist->wholepart = 0;
  domlist->size = 0;
  domlist->allocated = 0;
}


// append a number to the domlist, reallocating the array or handling the
// whole part special case if necessary
#define APPEND(domlist, dom)                                  \
  do {                                                        \
    domlist_append(&(domlist), (dom));                        \
    if ((domlist).data == NULL && (domlist).wholepart == 0)   \
      return NULL;                                            \
  } while(0)

void domlist_append(DomList *domlist, ll dom) {
  // check for whole part special case: increment wholepart everytime we see a
  // 1 denominator. the algorithm yields a 1 for the denominator n times for
  // a whole part of n.
  if (dom == 1) {
    ++domlist->wholepart;
    return;
  }

  if (domlist->size == domlist->allocated) {
    // need to allocate more space
    size_t newallocated;
    ll *newdata;

    newallocated = domlist->allocated == 0
                     ? 8
                     : ((domlist->allocated * 3) >> 2);
    newdata = realloc(domlist->data, newallocated * sizeof(ll));

    if (newdata == NULL) {
      domlist_clear(domlist);
      return;
    }

    domlist->allocated = newallocated;
    domlist->data = newdata;
  }

  // append the denominator to the array
  domlist->data[domlist->size++] = dom;
}


// Return the correct formatted string for the domlist
#define TOSTR(domlist) (domlist_tostr(&(domlist)))

char *domlist_tostr(DomList *domlist) {
  char *result;
  char *p;
  size_t numbytes = 0, i;
  int n;
  size_t size = domlist->size;
  ll *data = domlist->data;
  ll wholepart = domlist->wholepart;

#define BYTEC(n)  ((size_t)floor(log10(n)) + 1)

  // compute the number of bytes to allocate:
  // denominators
  for (i = 0; i < size; i++)
    numbytes += BYTEC(data[i]);
  // separating commas
  numbytes += size - 1;
  // "1/" for each denominator
  numbytes += 2 * size;
  // null byte and extra byte for snprintf
  numbytes += 2;
  // wholepart plus an extra comma
  if (wholepart > 0)
    numbytes += BYTEC(wholepart) + 1;

  // allocate string
  result = (char *)calloc(numbytes, sizeof(char));
  if (result == NULL)
    return NULL;
  p = result;

#define WRITE(format, number)                      \
  do {                                             \
    n = snprintf(p, numbytes, (format), (number)); \
    p += n;                                        \
    numbytes -= n;                                 \
  } while(0)

  // write wholepart
  if (wholepart > 0)
    WRITE("%lld,", wholepart);

  // write each denominator
  for (i = 0; i < size; i++)
    WRITE("1/%lld,", data[i]);

  // overwrite last comma with null byte
  *--p = '\0';

  return result;
  
#undef BYTEC
#undef WRITE
}


void simplify_fraction(ll *nump, ll *domp) {
  ll a = *nump, b = *domp, gcd, tmp;

  // compute greatest common denominator of num and dom using
  // the Euclidean algorithm
  while (b > 0) {
    tmp = a % b;
    a = b;
    b = tmp;
  }

  gcd = a;

  *nump /= gcd;
  *domp /= gcd;
}

char *decompose(char *numstr, char *domstr) {
  char *result;
  ll num = strtoll(numstr, NULL, 10);
  ll dom = strtoll(domstr, NULL, 10);
  ll ldom;
  DomList domlist = {0};

  if (num == 0 || dom == 0)
    // we want to return the empty string in this case, but we can't
    // return the static empty string because the caller frees it,
    // causing a segfault.
    return (char *)calloc(1, sizeof(char));

  // loop until the egyptian algorithm yields a 1 for the numerator
  for (simplify_fraction(&num, &dom);
       num > 1;
       simplify_fraction(&num, &dom))
  {
    ldom = (ll)ceil((double)dom / num);
    num  = (-dom % num) + num;
    dom *= ldom;

    APPEND(domlist, ldom);
  }

  // Add the final denominator to the list
  APPEND(domlist, dom);

  result = TOSTR(domlist);
  CLEAR(domlist);
  return result;
}
