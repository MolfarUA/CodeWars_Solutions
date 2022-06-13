std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
    for(auto i = 0; i < numbers.size(); i++)
      for(auto j = i+1; j < numbers.size(); j++)  
        if(numbers[i] + numbers[j] == target) return {i, j};
}
________________________________
#include <unordered_map>

std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
    std::unordered_map<int, std::size_t> counterparts;
    for (std::size_t i = 0; i < numbers.size(); ++i) {
        auto it = counterparts.find(numbers[i]);
        if (it != counterparts.end())
            return {it->second, i};
        counterparts.emplace(target - numbers[i], i);
    }
    return {-1, -1};
}
________________________________
std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
  for (auto it1 = numbers.begin(); it1 != numbers.end(); it1++)
  {
    auto it2 = find(it1 + 1, numbers.end(), target - *it1);
    if (it2 != numbers.end())
    {
      return{ it1 - numbers.begin(), it2 - numbers.begin() };
    }
  }
}
________________________________
std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
    for (size_t i = 0; i < numbers.size(); ++i)
        for (size_t j = 0; j < numbers.size(); ++j)
            if (numbers[i] + numbers[j] == target && i != j)
                return {i, j};
}
________________________________
#include <iostream>

using namespace std;

std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
  
  for(int i = 0; i<numbers.size(); i++)
    {
    for(int j=1; j<numbers.size(); j++)
      {
      if(numbers[i]+numbers[j]==target)
        {
        return {i, j};
      }
    }
  }
    
}
________________________________
std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
    
  int index1, index2;
  for(unsigned int i=0; i<numbers.size();++i){
    for(unsigned int j=0; j < numbers.size() ;++j){
      if(numbers[i]+numbers[j]==target && i!=j ){ 
        index1=i;
        index2=j;
      }
     
    }
  }
  return {index1 , index2};
}
________________________________
std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
  for (size_t i = 0; i < numbers.size(); i++)
  {
    for (size_t j = i+1; j < numbers.size(); j++)
    {
       if((numbers[i] + numbers[j])==target)
         return { i, j };
    }
  }
}
