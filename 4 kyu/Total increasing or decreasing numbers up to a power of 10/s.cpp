55b195a69a6cc409ba000053
  
  
unsigned long long total_inc_dec(unsigned int n) {
  std::vector<std::vector<unsigned long long>> dp(n+1, std::vector<unsigned long long>(10, 0));
  for (unsigned i = 0; i <= n; ++i) {
    for (unsigned j = 0; j < 10; ++j) 
      dp[i][j] = (i == 0 || j == 0) ? 1 : dp[i][j-1] + dp[i-1][j];
  }
  unsigned long long sum = 0; for (unsigned i = 1; i <= n; ++i) sum += dp[i][9];
  return dp[n][9] + sum - n * 10;
}
__________________________
#include <cmath>

unsigned long long total_inc_dec(unsigned int n)
{
    auto nCk = [](unsigned long long n, unsigned long long k) -> unsigned long long {
        if (k > n)
            return 0;
        if (2 * k > n)
            k = n - k;
        if (k == 0)
            return 1;

        auto res = n;
        for (auto i = 2; i <= k; ++i)
        {
            res *= (n - i + 1);
            res /= i;
        }

        return res;
    };

    return nCk(n + 9, 9) + nCk(n + 10, 10) - (n + 1) - 9 * n;
}
__________________________
unsigned long long total_inc_dec(unsigned int x) {
    unsigned long long n = 1;
    for (unsigned long long i = 1; i < 10; ++i)
        n = n*(x + i)/i;
    return n * (20 + x) / 10 - 10 * x - 1;
}
