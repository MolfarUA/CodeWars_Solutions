std::vector<double> averages(std::vector<int> numbers)
{
    std::vector<double> result;
    
    for (int i=1; i<numbers.size(); i++)
    {
        result.push_back((numbers[i-1] + numbers[i]) / 2.0f);
    }

    return result;
}
____________________________
std::vector<double> averages(std::vector<int> numbers)
{
    std::vector<double> result;
    if (numbers.size() < 2) return result;
    result.resize(numbers.size()-1);
    for(int i = 0; i< result.size(); ++i)
      result[i] = (numbers[i]+numbers[i+1])/2.0;
    return result;
}
____________________________
#include <algorithm>
#include <iterator>
#include <vector>

std::vector<double> averages(const std::vector<int>& numbers) {
  std::vector<double> result;
  if (!numbers.empty()) {
    std::transform(numbers.begin(), numbers.end() - 1, numbers.begin() + 1, std::back_inserter(result),
      [](auto a, auto b) { return 0.5 * (a + b); }
    );
  }
  return result;
}
____________________________
std::vector<double> averages(std::vector<int> numbers)
{
    std::vector<double> result;
    
    for(int i = 1; i < numbers.size(); i++){
        result.push_back((numbers[i-1]+numbers[i])/2.0);
    }
    
    return result;
}
____________________________
#include <vector>

std::vector<double> averages(std::vector<int> numbers)
{
    std::vector<double> result;
    for(int i = 1; i < numbers.size(); i++)
      result.push_back((numbers[i] + numbers[i - 1]) / 2.0);
    return result;
}
