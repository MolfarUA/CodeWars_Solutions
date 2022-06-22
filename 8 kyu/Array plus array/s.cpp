5a2be17aee1aaefe2a000151
  
  
#include <numeric>
#include <vector>

int arrayPlusArray(std::vector<int> a, std::vector<int> b)
{
  return std::accumulate(a.begin(), a.end(), 0) + std::accumulate(b.begin(), b.end(), 0);
}
_________________________
#include <vector>

int arrayPlusArray(std::vector<int> a, std::vector<int> b) {
    int total = 0;
    for( int i : a ) total += i;
    for( int i : b ) total += i;
    return total;
}
_________________________
#include <vector>
#include <numeric>

int arrayPlusArray(std::vector<int> a, std::vector<int> b) {
  return std::accumulate(a.begin(), a.end(), std::accumulate(b.begin(), b.end(), 0));
}
