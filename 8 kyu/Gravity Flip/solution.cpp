#include <vector>

std::vector<int> flip(const char dir, std::vector<int> arr) {
    if(dir == 'R')
      sort(arr.begin(),arr.end());
    else
      sort(arr.rbegin(),arr.rend());
    return arr;
}

____________________________
#include <vector>
#include <algorithm>
bool compareL(int a, int b) {return (a > b);}

std::vector<int> flip(const char dir, const std::vector<int>& arr) {
  std::vector<int> a (arr);
  if(dir == 'R'){
    std::sort(a.begin(), a.end());
  } else {
    std::sort(a.begin(), a.end(),compareL);
  } 
  return a;
}

____________________________
#include <vector>

std::vector<int> flip(const char dir, const std::vector<int>& arr) {
  auto res = arr;
  if (dir == 'R') {
    std::sort(res.begin(), res.end(), std::less{});
  } else {
    std::sort(res.begin(), res.end(), std::greater{});
  }
  return res;
}

____________________________
#include <vector>

std::vector<int> flip(const char dir, std::vector<int> arr) {
    if (dir == 'R') {
        std::sort(arr.begin(), arr.end());
    } else if (dir == 'L') {
        std::sort(arr.begin(), arr.end(), [](int lhs, int rhs) { return rhs < lhs; });
    }
    return arr;
}

____________________________
#include <vector>
#include <algorithm>

std::vector<int> flip(const char dir, const std::vector<int>& arr) {
  
  std::vector<int> output = arr;
  if (dir == 'R') {
    std::sort(output.begin(), output.end());
  }
  else {
    std::sort(output.rbegin(), output.rend());
  }
    return output;
}
