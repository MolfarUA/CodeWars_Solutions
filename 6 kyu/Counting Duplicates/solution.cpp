#include <string>
#include <unordered_map>
#include <algorithm>

#include <cctype>

std::size_t duplicateCount(const char* in) {
  std::unordered_map<char, unsigned> counts;
  for (const char* c = in; *c != '\0'; ++c) {
    ++counts[tolower(*c)];
  }
  return std::count_if(cbegin(counts), cend(counts), [](const auto& count) {
      return count.second > 1;
    });
}

__________________
#include <map>
size_t duplicateCount(const std::string& in); // helper for tests

size_t duplicateCount(const char* in)
{
  std::map<char,int> characters;
  for(int i = 0; in[i] != 0; i++){
    characters[std::tolower(in[i])]++;
  }
  return std::count_if(characters.begin(),characters.end(),
      [](auto &i){ return i.second > 1 ? true : false;});
}

_____________________
size_t duplicateCount(const std::string& in); // helper for tests

size_t duplicateCount(const char *in)
{
  if (in == NULL)
    return 0;

  std::string in_s(in);
  std::map<char, int> dups;
  size_t ret_size = 0;

  for (auto &it : in_s)
    dups[tolower(it)]++;

  for (auto &it : dups)
  {
    if (it.second > 1)
      ret_size++;
  }

  return ret_size;
}
________________________
#include <algorithm>
#include <array>

size_t duplicateCount(const std::string& in); // helper for tests

size_t duplicateCount(const char* in)
{
    std::array<int,255> occurences = {};
    for(auto i = 0; i < strlen(in); ++i)
    {
       occurences[std::tolower(in[i])]++;
    }
    return std::count_if(occurences.begin(),occurences.end(), [](int times) { return times > 1;});
}
____________________
size_t duplicateCount(const std::string& in); // helper for tests

#include<iostream>
#include<string>
#include<vector>
#include<utility>
#include<algorithm>

size_t duplicateCount(const char* in)
{
  std::string cped = in;
  std::vector < std::pair < char, int >> vecOfPair;
  std::pair < char, int > prs;
  size_t ans = 0;
  std::string result;
  char prev;

  ///Replase all capital symbols///
  for (int i = 0; i < cped.size(); i++)
  {
    cped[i] = (char)tolower(cped[i]);
  }

  ///Sort given string///
  std::sort(begin(cped), end(cped));

  ///Find all unic symbols///
  prev = cped[0];
  result += cped[0];
  for (int i = 1; i < cped.size(); i++)
  {
    if (cped[i] != prev)
    {
      prev = cped[i];
      result += cped[i];
    }
  }

  cped.clear();
  cped = in;

  ///Create vector of pair{symbol, count of this symbols(0)}///
  for (int i = 0; i < (int)result.size(); i++)
  {
    prs.first = result[i];
    prs.second = 0;
    vecOfPair.push_back(prs);
  }

  ///Fill vector of pair with count of symbols///
  for (int i = 0; i < (int)vecOfPair.size(); i++)
  {
    for (int j = 0; j < (int)cped.size(); j++)
    {
      if (vecOfPair[i].first == cped[j] || vecOfPair[i].first == toupper(cped[j]) || toupper(vecOfPair[i].first) == cped[j])
      {
        vecOfPair[i].second++;
      }
    }
    if (vecOfPair[i].second > 1)
    {
      ans++;
    }
  }
  return ans;
}
