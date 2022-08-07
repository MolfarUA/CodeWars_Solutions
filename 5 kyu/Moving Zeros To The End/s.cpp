52597aa56021e91c93000cb0
  
  
auto move_zeroes(std::vector<int> v) {
  stable_partition(begin(v), end(v), std::negate());
  return v;
}
_____________________________
#include <vector>

std::vector<int> move_zeroes(const std::vector<int>& input) {
  
  std::vector<int> v(input.size(),0);
  int a = 0;
  for (auto c : input){
    if(c != 0){
      v[a] = c;
      ++a;
    }
  }

  return v;
}
_____________________________
auto move_zeroes(std::vector<int> v) {
  std::stable_partition(begin(v), end(v), [](auto x) {return x;});
  return v;
}
_____________________________
#include <algorithm>
#include <vector>

std::vector<int> move_zeroes(std::vector<int> input) {
  std::fill(std::remove(input.begin(), input.end(), 0), input.end(), 0);
  return input;
}
