#include <string>
#include <vector>
#include <algorithm>
#include <iostream>
#include <iterator>
#include <unordered_set>

using namespace std;
template <typename T> std::vector<T> uniqueInOrder(const std::vector<T>& iterable){
    vector<T> res;

    unique_copy (iterable.begin(), iterable.end(), std :: back_inserter(res));
    return res;
}
std::vector<char> uniqueInOrder(const std::string& iterable){
    vector<char> res;

    unique_copy (iterable.begin(), iterable.end(), std :: back_inserter(res));
    return res;
}
_____________________________________________
#include <string>
#include <vector>

template <typename T> std::vector<T> uniqueInOrder(const std::vector<T>& iterable){
  std::vector<T> result;
  for (const auto& c : iterable) if (result.empty() || c != result.back()) result.push_back(c);
  return result;
}

std::vector<char> uniqueInOrder(const std::string& iterable) {
  std::vector<char> result;
  for (auto c : iterable) if (result.empty() || c != result.back()) result.push_back(c);
  return result;
}
_____________________________________________
#include <string>
#include <vector>

template <typename T> std::vector<T> uniqueInOrder(const std::vector<T>& iterable){
  std::vector<T> to_return;
  for(int i = 0; i < iterable.size(); i++){
    if(to_return.empty() || to_return.back() != iterable.at(i)){
      to_return.push_back(iterable.at(i));
    }
  }
  return to_return;
}
std::vector<char> uniqueInOrder(const std::string& iterable){
  return uniqueInOrder(std::vector<char> (iterable.begin(), iterable.end()));
}
_____________________________________________
#include <string>
#include <vector>

template <typename T> std::vector<T> uniqueInOrder(const std::vector<T>& iterable)
{
  std::vector<T> unique_in_order(iterable.size());
  auto lead_it{ iterable.cbegin() };
  auto target_it{ unique_in_order.begin() };
  auto END{ iterable.cend() };
  while(lead_it < END)
  {
    *target_it = *lead_it;
    while(lead_it < END 
          && *lead_it == *target_it)
          ++lead_it;
    ++target_it;
  }
  unique_in_order.resize(target_it - unique_in_order.begin());
  return unique_in_order;
}

std::vector<char> 
uniqueInOrder(const std::string& iterable)
{
  std::vector<char> tmp(iterable.begin(), iterable.end());
  return uniqueInOrder(tmp);
}
_____________________________________________
#include <string>
#include <vector>

template <typename T> std::vector<T> uniqueInOrder(const std::vector<T>& iterable){
  std::vector<T> output;
  unique_copy(iterable.begin(), iterable.end(), std::back_inserter(output));
  return output;
}
std::vector<char> uniqueInOrder(const std::string& iterable){
  std::vector<char> output;
  unique_copy(iterable.begin(), iterable.end(), std::back_inserter(output));
  return output;
}
