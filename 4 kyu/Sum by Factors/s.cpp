54d496788776e49e6b00052f
  
  
#include <sstream>
#include <iostream>
#include <string>
#include <vector>

class SumOfDivided
{
   static std::vector<long> primes(long n) {
      std::vector<long> result;
      std::vector<bool> sieve(n, true);
      for (long p = 2; p < n; p++ ) 
         if (sieve[p]) {
            result.push_back(p);
            for (long i = p*p; i < n; i+=p) sieve[i] = false;
         }
      return result;
   }
   
public:
   static std::string sumOfDivided(std::vector<int> &lst) {
      std::ostringstream result;
      
      if (lst.empty())
         return result.str();
      else {
         long max = lst[0];
         for(long x : lst) { if (x>max) max=x; if (-x>max) max=-x; }
         std::vector<long> prime_numbers = primes(max+1);
      
         for(auto p : prime_numbers) {
            long sum = 0;
            int count = 0;
            for(auto l : lst) if (l%p==0) { sum+=l; count++; }
            if (count>0) result << "(" << p << " " << sum << ")";
         }
      
         return result.str();
      }
   }
};
________________________________________________
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>

#define SSTRING(x)(std::ostringstream() << std::dec << x ).str()

class SumOfDivided
{
public:
    static std::string sumOfDivided(std::vector<int> &lst);
};

std::string SumOfDivided::sumOfDivided(std::vector<int> &lst)
{
    std::vector<int> rem(lst.size());
    int max = 0;
    std::string result = "";
    for (unsigned int i = 0; i < lst.size(); ++i)
    {
        rem[i] = std::abs(lst[i]);
        max = std::max(max, std::abs(lst[i]));
    }
    for (int fac = 2; fac <= max; ++fac)
    {
        bool isFactor = false;
        int tot = 0;
        for (unsigned int i = 0; i < lst.size(); ++i)
        {
            if (rem[i] % fac == 0)
            {
                isFactor = true;
                tot += lst[i];
                while (rem[i] % fac == 0)
                    rem[i] /= fac;
            }
        }
        if (isFactor)
            result += "(" + SSTRING(fac) + " " + SSTRING(tot) + ")";
    }
    return result;
}
________________________________________________
#include <set>
#include <numeric>
struct SumOfDivided {
  static std::string sumOfDivided(std::vector<int> &lst) {
    std::set<int> s;
    for (int n : lst)
      for (int d = (n = abs(n), 2); n > 1; ++d)
        while (n % d == 0 && n != 1)
          n /= d, s.insert(d);
    return std::accumulate(s.begin(), s.end(), std::string(), [&](auto sum, int j) {
      return sum + '(' + std::to_string(j) + ' ' + std::to_string(std::accumulate(lst.begin(), lst.end(), 0, [j](int sum, int n) {
        return n % j ? sum : sum + n;
      })) + ')';
    });
  }
};
