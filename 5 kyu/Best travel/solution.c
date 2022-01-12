#include <stdio.h>
#include <stdlib.h>

int bit_count(long n) {
  int bits = 0;
  for(int bit = 0; n > 0; n &= ~(1 << bit), bit++) {
    if(n & (1 << bit)) {
      bits++;
    }
  }
  return bits;
}

int chooseBestSum(int t, int k, int ls[], int szls) {
  if(szls < k) return -1;
  int sum = t + 1;
  int max = 0;
  int min = -1;
  for(long i = 0; i < (1 << szls); i++) {
    if(bit_count(i) == k) {
      sum = 0;
      for(int bit = 0; bit <= szls; bit++) {
        if(i & (1 << bit)) {
          sum += ls[szls - bit - 1];
        }
      }
      max = sum > max ? sum : max;
      min = sum <= t && sum > min ? sum : min; 
    }
  }
  return min <= t && max > t ? min : max;
}
_______________________________________
int maxi(int a, int b) {
    return a >= b ? a : b;
}
int chooseBestSumAux(int t, int k, int ls[], int szls, int from) {
    if(k == 0)
        return t >= 0 ? 0 : t;
    else if (t < k)
        return -1;
    int best = -1;
    for(int i = from; i < szls; ++i) {
        int tmpBest = chooseBestSumAux(t - ls[i], k - 1, ls, szls, i + 1);
        if(tmpBest >= 0) {
            best = maxi(best, ls[i] + tmpBest);
        }
    }
    return best;
}
// szls: size of ls
int chooseBestSum(int t, int k, int ls[], int szls) {
    return chooseBestSumAux(t, k, ls, szls, 0);
}
_______________________________________
int chooseBestSum(int t, int k, int ls[], int szls)
{
    int res = -1;
    
    int indexes[k];
    for (int i = 0; i < k; ++i)
        indexes[i] = i;
    
    while (indexes[k - 1] < szls)
    {
        int tmp = 0;
        for (int i = 0; i < k; ++i)
            tmp += ls[indexes[i]];
        if (tmp <= t && res < tmp)
            res = tmp;
        
        int i = k - 1;
        while (i >= 0 && indexes[i] == szls + i - k)
            --i;
        for (++indexes[i++]; i < k; ++i)
            indexes[i] = indexes[i - 1] + 1;
    }
    
    return res;
}
_______________________________________
void combinationUtil(int ls[], int data[], int start, int end, int index, int k, int t, int *currentMax) { 
    unsigned sum = 0;
    if (index == k) { 
        for (int j = 0; j < k; j++) sum += data[j];
        if(sum <= t && *currentMax < sum) *currentMax = sum; 
        return; 
    }
    for (int i = start; i <= end && end-i + 1 >= k - index; i++) { 
        data[index] = ls[i]; 
        combinationUtil(ls, data, i+1, end, index+1, k, t, currentMax); 
    }
} 
    
int chooseBestSum(int t, int k, int ls[], int szls) {
    int currentMax = 0, data[k]; 
    combinationUtil(ls, data, 0, szls-1, 0, k, t, &currentMax);
    return (currentMax != 0 && currentMax <= t) ? currentMax : -1;
}
_______________________________________
#include <limits.h>

int maxNumber(int num1, int num2)
{
    return (num1 > num2) ? num1 : num2;
}

int combinations(int t, int k, int ls[], int szls, int i)
{
    if (k == 0 && t >= 0)
    {
        return 0;
    }
    else if (k < 0 || i >= szls)
    {
        return INT_MIN;
    }
    else
    {
        return maxNumber(combinations(t, k, ls, szls, i + 1), ls[i] + combinations(t - ls[i], k - 1, ls, szls, i + 1));
    }
}

// szls: size of ls
int chooseBestSum(int t, int k, int ls[], int szls)
{
    int result = combinations(t, k, ls, szls, 0);
    return result > 0 ? result : -1;
}
