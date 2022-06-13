#include <algorithm>

class Kata
{
public:
    std::vector<int> sortArray(std::vector<int> array)
    {
        std::vector<int> odds;
        std::copy_if(array.begin(), array.end(), std::back_inserter(odds), [] (int x) {return x % 2;});
        std::sort(odds.begin(), odds.end());
        for (int i = 0, j = 0; i < array.size(); i++) if (array[i] % 2) array[i] = odds[j++];
        return array;
    }
};
_______________________________________________
class Kata
{
public:
    std::vector<int> sortArray(std::vector<int> array)
    {
      for (int i=0; i<array.size(); i++) {
          if(array[i] &1){
            for (int j=i+1; j<array.size(); j++) {
                if(array[j] & 1 && array[j] < array[i]){
                    std::swap(array[i], array[j]);
                }
            }
          }
        }
        return array;
    }
};
_______________________________________________
#include <string>
#include <algorithm>
#include <cinttypes>
#include <cmath>
#include <vector>
using namespace std;

class Kata
{
  vector<int> helpArray{};
public:
  vector<int> sortArray(std::vector<int> arr)
  {
    for (auto& val:arr) {
      if (val % 2 == 1)
        helpArray.push_back(val);
    }
    sort(begin(helpArray), end(helpArray));
    int ind = 0;
    for (auto& val:arr) {
      if (val % 2 == 1)
        val = helpArray[ind++];
    }
    return arr;
  }

};
_______________________________________________
#include <cstdint>
#include<string>
#include<algorithm>
#include<cmath>
#include<iostream>
#include<vector>
using namespace std;


class Kata
{
public:
  std::vector<int> sortArray(std::vector<int> array)
  {
    vector<int>v;
    for (size_t i = 0; i < array.size(); i++)
    {
      if (array[i] % 2 != 0)
        v.push_back(array[i]);
    }
    sort(v.begin(), v.end());
    int ind = 0;
    for (size_t i = 0; i < array.size(); i++)
    {
      if (array[i] % 2 != 0) {
        array[i] = v[ind];
        ind++;
      }
    }
    return array;
  }
};
