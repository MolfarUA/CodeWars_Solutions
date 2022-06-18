#include <vector>
#include <numeric>
using namespace std;

int find_even_index (const vector <int> numbers) {
  for (int index = 0; index < numbers.size(); index++)
  {
    int left_sum = std::accumulate(numbers.begin(), numbers.begin() + index, 0);
    int right_sum = std::accumulate(numbers.begin() + index + 1, numbers.end(), 0);
    if (left_sum == right_sum)
      return index;
  }
  return -1;
}
________________________
#include <vector>
#include <numeric>
using namespace std;

int find_even_index (const vector <int> numbers) {
  int left_sum = 0;
  int right_sum = std::accumulate(numbers.begin(), numbers.end(), 0);
  for (unsigned long i{0}; i < numbers.size(); i++) {
    right_sum -= numbers[i];
    if (left_sum == right_sum) {
      return i;
    }
    left_sum += numbers[i];
  }
  return -1;
}
________________________
#include <vector>
using namespace std;

int find_even_index (const vector <int> numbers) 
{
    int ret = -1;
    int sum_left = 0;
    int sum_right = 0;

    for(int i = 0; i < int(numbers.size()); ++i)
    {
        for(int j = (numbers.size() - 1); j > i ; --j)
        {
            sum_right += numbers[j];

        }
        if(sum_left == sum_right)
        {
            return i;
        }
        sum_left += numbers[i];
        sum_right = 0;
    }
    return ret;
}
________________________
#include <vector>
using namespace std;

int find_even_index (const vector <int> numbers) {
  int res = -1;
  for(size_t i = 0; i < numbers.size(); i++) {
    int left = 0;
    int right = 0; 
    // sum of left
    for (size_t j = 0; j < i; j++) {
      left += numbers[j];
    }
    // sum of right
    for (size_t j = i + 1; j < numbers.size(); j++) {
      right += numbers[j];
    }

    if (left == right) return i;
  }
  return res;
}
