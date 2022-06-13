#include <vector>
#include <cstdint>
#include <cmath>

std::vector<uint64_t> powers_of_two(int n) {
  std::vector<uint64_t> vec;
  for(int i = 0; i<=n; i++){
    vec.push_back(pow(2,i));
  }
  return vec;
}
___________________________________
#include <vector>
#include <cstdint>

std::vector<uint64_t> powers_of_two(int n) {
  std::vector<uint64_t> v;
  uint64_t t = 1;
  for (int i = 0; i <= n; ++i) {
    v.push_back(t);
    t = t << 1;
  }
  return v;
}
___________________________________
#include <vector>
#include <cstdint>

std::vector<uint64_t> powers_of_two(int n)
{
   std::vector<uint64_t>result(n + 1);
   for (int i = 0; i < n + 1; i++) result[i] = (uint64_t)1 << i;
   return result;
}
___________________________________
#include <vector>
#include <cstdint>
#include<cmath>
std::vector<uint64_t> powers_of_two(int n) {
  std::vector<uint64_t>a;
  for(int i=0;i<=n;i++)
    a.push_back(pow(2,i));
  return a;
}
___________________________________
#include <vector>
#include <cstdint>
#include <cmath>
#include <algorithm>

std::vector<uint64_t> powers_of_two(int n) {
  std::vector<uint64_t> arr(n+1);
  std::generate(arr.begin(), arr.end(), [i=0]() mutable{ return pow(2, i++); });
  return arr;
}
