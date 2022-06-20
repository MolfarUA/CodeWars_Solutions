559b8e46fa060b2c6a0000bf


typedef unsigned long long ull;
ull diagonal(int n, int p)
{
      ull sum = 0;
      ull T[n+1][p+1];
      for(int i = 0; i <= n; i++) T[i][0] = 1;
      
      for(int j = 1; j <= p; j++)
      {
        for(int i = j; i <= n; i++)
        {
          if(i == j)
            T[i][j] = 1;
          else
            T[i][j] = T[i-1][j-1] + T[i-1][j];
        }
      }
      for(int i = p; i <= n; i++) sum += T[i][p];
      return sum;
}
_____________________________
typedef unsigned long long ull;

ull diagonal(int n, int p) 
{
    ull numbers[256] = {1};
    ull result = 0;

    for (int i = 0; i <= p; ++i)
        for (int j = 1; j <= n - p; ++j)
            numbers[j] += numbers[j - 1];

    for (int i = 0; i <= n - p; ++i)
        result += numbers[i];

    return result;
}
_____________________________
typedef unsigned long long ull;
ull diagonal(int n, int p)
{
  ull sum = 1, binom = 1;
  for (int i = 1; i <= n - p; ++i)
    sum += binom = binom * (i + p) / i;
  
  return sum;
}
