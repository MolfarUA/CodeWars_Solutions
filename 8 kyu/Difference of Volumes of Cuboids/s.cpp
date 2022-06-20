58cb43f4256836ed95000f97
  
  
#include <array>
int findDifference(std::array<int, 3> a, std::array<int, 3> b) {
  return abs(a[0] * a[1] * a[2] - b[0] * b[1] * b[2]);
}
________________________
#include <functional>
#include <numeric>
#include <array>
#include <cmath>

int findDifference(std::array<int, 3> a, std::array<int, 3> b) {
  long v1 = std::accumulate(a.cbegin(), a.cend(), 1, std::multiplies<long>());
  long v2 = std::accumulate(b.cbegin(), b.cend(), 1, std::multiplies<long>());
  return std::abs(v1 - v2);
}
________________________
#include <array>
#include <numeric>
#include <functional>

int findDifference(std::array<int, 3> a, std::array<int, 3> b) {
  return std::abs(
    std::accumulate(a.begin(), a.end(), 1, std::multiplies<int>()) - 
    std::accumulate(b.begin(), b.end(), 1, std::multiplies<int>())
  );
}
