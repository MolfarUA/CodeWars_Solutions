55aa075506463dac6600010d


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct Pair Pair;
struct Pair {
    long long first;
    long long snd;
};
// fill length with the number of pairs in your array of pairs
Pair** listSquared(long long m, long long n, int* length) {
    Pair** result = calloc(0, sizeof(Pair*));
    int cnt = 0;
    for (long long i = m; i <= n; i++) {
        long long sum = 0;
        for (long long j = 1; j <= i; j++)
            if (i % j == 0) sum += j * j;
            double sqrt_sum = sqrt(sum);
            if ((long long)floor(sqrt_sum) == sqrt_sum) {
                Pair* pr = calloc(1, sizeof(Pair));
                pr->first = i;
                pr->snd = sum;
                result = (Pair**)realloc(result, (cnt + 1) * sizeof(Pair*));
                result[cnt++] = pr;
            }
    }
    *length = cnt;
    return result;
}
________________________________
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef long long int64;
typedef struct Pair Pair;
struct Pair 
{
    int64 first;
    int64 snd;
};

Pair** listSquared(int64 m, int64 n, int* length)
{
    Pair** arr = (Pair**) malloc(0 * sizeof(Pair*));
    int cnt = 0;
    
    for (int64 i=m; i<=n; i++) 
    {
        int64 sum = 0;
        int64 t = (int64)sqrt(i);
      
        for (int64 j=1; j<=t; j++) 
        {
            if (i%j == 0) sum += j*j;
            if (i%j == 0 && j!=i/j) sum += (i/j)*(i/j);
        }
        
        if (sqrt(sum) == ceil(sqrt(sum))) 
        {
            Pair* pair = (Pair*) calloc(1, sizeof(Pair));
            pair->first = i;
            pair->snd = sum;
            arr = (Pair**) realloc(arr, (cnt + 1) * sizeof(Pair*));
            *(arr + cnt++) = pair;
        }
    }
  
    *length = cnt;
    return arr;
}
________________________________
typedef struct Pair Pair;
struct Pair {
    long long first;
    long long snd;
};
// fill length with the number of pairs in your array of pairs
Pair** listSquared(long long m, long long n, int* length) {
    int i,j;
    Pair** res = (Pair**) malloc(sizeof(Pair*)*(n-m+1));
    int pos = 0;
    int s;
    for (i=m; i<= n; i++)
    {
      s = 0;
      for(j=1;j<=i/2;j++)
      {
        if(i%j==0) s += j*j;
      }
      s += i*i;
      int root = (int)sqrt(s); 
      if(root*root == s)
      {
        res[pos] = (Pair*)malloc(sizeof(Pair));
        res[pos]->first = i;
        res[pos]->snd = s;
        pos++;
      }
    }
    *length = pos;
    return res;
}
