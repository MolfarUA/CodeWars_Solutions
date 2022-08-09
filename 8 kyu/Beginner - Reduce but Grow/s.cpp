57f780909f7e8e3183000078
  
  
#include <vector>
#include <numeric>
#include <functional>

int grow(const std::vector<int>& nums) {
  return std::accumulate(nums.cbegin(), nums.cend(), 1, std::multiplies<int>());
}
_______________________
#include <vector>
int grow(std::vector<int> nums) {
  int result = 1;
  for(auto x: nums)  result = result * x;
  return result;
}
_______________________
#include <vector>
int grow(std::vector<int> nums) {
  int total = nums[0];
  for (int i = 1; i < nums.size(); i++) {
    total = total * nums[i];
  }
  
  return total;
}
