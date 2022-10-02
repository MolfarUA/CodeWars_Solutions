5547cc7dcad755e480000004


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Pair Pair;
struct Pair {
    long long first;
    long long snd;
};
// length is the number of pairs
Pair** removNb(long long n, int* length) {
    long long s = (long long)(n * (n + 1) / 2.0);
    Pair** res = calloc(0, sizeof(Pair*));
    long long i = (long long)(n / 2);
    int cnt = 0;
    while (i <= n) {
        long long b = (long long)(s - i);
        if (b % (i + 1) == 0) {
            Pair* pr = calloc(1, sizeof(Pair));
            pr->first = i;
            pr->snd = (long long)(b / (i + 1));
            res = (Pair**)realloc(res, (cnt + 1) * sizeof(Pair*));
            res[cnt++] = pr;
        }
        i += 1;
    }
    *length = cnt;
    return res;
}
______________________________
typedef struct Pair Pair;

struct Pair
{
    long long first;
    long long snd;
};

// fill length with the number of pairs in your array of pairs
Pair** removNb(long long n, int* length)
{
  Pair** result = (Pair**)malloc(0);
  
  *length = 0;
  
  long long sum = n * (n + 1) / 2;
  
  for(long long a = 1; a <= n; a++)
  {
    long long b = (sum - a) / (a + 1);
    if (b > n)
    {
      continue;
    }
    
    if (sum == a * b + a + b)
    {
      Pair* pair = (Pair*)malloc(sizeof(Pair));
      pair->first = a;
      pair->snd = b;
      
      result = (Pair**)realloc(result, ++(*length) * sizeof(Pair*));
      result[*length - 1] = pair;
    }
  }
  
  return result;
}
______________________________
typedef struct Pair Pair;
struct Pair {
    long long first;
    long long snd;
};

// fill length with the number of pairs in your array of pairs
Pair** removNb(long long n, int* length) {
    long long sum = (n*(n+1))/2;
    
    Pair** pairs = (Pair**)malloc(sizeof(Pair*)*n);
    *length=0;
    for (long long a=n;a>0;a--) {
        long long b = (sum-a)/(a+1);
        if (b>n)break;

        long long verificationSum = (b*a)+b+a;
        if (verificationSum==sum) {
            pairs[*length]=(Pair*)malloc(sizeof(Pair));
            pairs[*length]->snd=a;
            pairs[*length]->first=b;
            *length = *length+1;
        }
    }
    return pairs;
}
