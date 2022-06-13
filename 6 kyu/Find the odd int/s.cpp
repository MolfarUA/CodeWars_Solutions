#include <vector>

int findOdd(const std::vector<int>& numbers){
  for (auto elem: numbers){
    if (std::count(numbers.begin(), numbers.end(), elem) % 2 != 0) {
      return elem;
    }
  }
  return 0;
}
_______________________________
#include <functional>
#include <numeric>
#include <vector>

int findOdd(const std::vector<int>& numbers) {
  return std::accumulate(numbers.cbegin(), numbers.cend(), 0, std::bit_xor<>());
}
_______________________________
#include <vector>
#include <algorithm>    // std::count

int findOdd(const std::vector<int>& numbers){
  //your code here
  std::vector<int> alreadyTested; // already tested ints
  int result = 0;
  int count = 0;
  for (int e : numbers)
  {
    if (std::count(alreadyTested.begin(),alreadyTested.end(),e) == 0)
    {
      count = std::count(numbers.begin(),numbers.end(),e);
      if (count % 2 != 0)
      {
        result = e;
        break;
      }
      alreadyTested.push_back(e);
    }
  }
  return result;
}
_______________________________
#include <algorithm>
#include <vector>

int findOdd(const std::vector<int>& numbers){
    for (auto i : numbers)
        if (std::count(numbers.begin(), numbers.end(), i) & 1)
            return i;
    return 0;
}
_______________________________
#include <vector>

int findOdd(const std::vector<int>& numbers){
    for (const auto &i : numbers) {
        int temp = count(cbegin(numbers), cend(numbers), i);
        if (temp % 2 != 0) {
           return i;
        }
    }
    throw "condition not met";
}
