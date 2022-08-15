52f677797c461daaf7000740
  
  
#include <vector>

unsigned long long solution(const std::vector<unsigned long long>& arr) {    
    unsigned long long cur_gcd = arr.front();
    
    for(auto num : arr){
        cur_gcd = std::__gcd(num, cur_gcd);
    
    }    
    return cur_gcd * arr.size();
}
_______________________________
#include <vector>
#include <numeric>

unsigned long long gcd(unsigned long long a, unsigned long long b)
{
    for (;;)
    {
        if (a == 0) return b;
        b %= a;
        if (b == 0) return a;
        a %= b;
    }
}

unsigned long long solution(const std::vector<unsigned long long>& arr){
  return std::accumulate(arr.begin(), arr.end(), arr[0], gcd) * arr.size();
}
_______________________________
#include <numeric>
#include <vector>

unsigned long long solution(const std::vector<unsigned long long>& xs) {
  return xs.size() * std::reduce(xs.cbegin(), xs.cend(), xs[0], std::gcd<unsigned long long, unsigned long long>);
}
