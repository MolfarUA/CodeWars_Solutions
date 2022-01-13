class StockList
{
public:
  static std::string stockSummary(std::vector<std::string> &lstOfArt, std::vector<std::string> &categories);
};

std::string StockList::stockSummary(std::vector<std::string> &lstOfArt, std::vector<std::string> &categories)
{
  if (lstOfArt.empty() || categories.empty()) return "";
  std::unordered_map<std::string, int> record;
  for (auto category : categories) {
    record[category] = 0;
  }
  
  for (auto art : lstOfArt) {
    std::string key = art.substr(0, 1); 
    if (record.count(key) > 0) {
      size_t pos = art.find(" ");
      int num = stoi(art.substr(pos+1, art.size()-pos));
      record[key] += num;
    }
  }
  
  std::string res;
  for (auto category : categories) {
    res += "(" + category + " : " + std::to_string(record[category]) + ") - ";
  }
  if (record.size() > 0) {
    res = res.substr(0, res.size()-3);
  }
  
  return res;
}
________________________________________
#include <math.h>

class StockList
{
public:
  static std::string stockSummary(std::vector<std::string> &lstOfArt, std::vector<std::string> &categories);
  static int getAmount(std::string name);
};

std::string StockList::stockSummary(std::vector<std::string> &lstOfArt, std::vector<std::string> &categories)
{
  if(lstOfArt.empty() || categories.empty())
    return "";
  
  std::map<std::string, int> ret;
  std::string retString = "";
  
  for (auto cats : categories)
  {
    ret[cats] = 0;
    for (auto arts : lstOfArt)
    {
      if(arts[0] == cats[0])
        ret[cats] += getAmount(arts);
    }
  }
  
  /* care no sorting => not for (auto map : ret), but */
  for (auto cats : categories)
  {
    if(cats != *categories.begin())
    {
      retString+= " - ";
    }
    retString += ("(" + cats + " : " + std::to_string(ret[cats]) + ")");
    
  }
  
  return retString;
}

int StockList::getAmount(std::string name)
{
  int pos = 0, ret = 0, div = 0;
  
  while(name[pos++] != ' '){}
  div = name.length() - pos;
  
  for(int i = pos; i < (int)name.length(); i++)
  {
    ret += (((int)name[i] - 48) * pow(10,--div));
  }
  return ret;
}
_______________________________________
#include <sstream>
#include <string>
class StockList
{
public:
  static std::string stockSummary(std::vector<std::string> &lstOfArt, 
                                  std::vector<std::string> &categories)
  {
    if(lstOfArt.size() == 0 || categories.size() == 0)
    {
      return "";
    }
    std::string ret;
    std::vector<std::pair<std::string, int>> countBook;
    for(auto &val:categories)
    {
      countBook.push_back({val, 0});
    }
    for(auto &val:lstOfArt)
    {
      std::string tmp(1, val[0]);
      for(unsigned long i = 0; i < countBook.size(); ++i)
      {
        if(tmp == countBook[i].first)
        {
          std::stringstream ss(val); 
          std::string s; 
          std::getline(ss, s, ' ');
          std::getline(ss, s, ' ');
          countBook[i].second += std::stoi(s);
          break;
        }
      }
    }
    for(auto &val:countBook)
    {
      ret += "(" + val.first + " : " + std::to_string(val.second) + ") - ";
    }
    ret = ret.substr(0, ret.size()-3);
    std::cout << ret << std::endl;
    return ret;
  }
};
________________________________________
#include<map>

class StockList
{
public:
  static std::string stockSummary(std::vector<std::string> &L, std::vector<std::string> &M) {
    if (L.size() == 0 || M.size() == 0) {
      return "";
    }
    
    std::map<char,int> data_map;
    
    for (std::string letter : M) {
      data_map.insert(std::pair<char,int>(letter[0], 0));
      for (std::string data : L) {
        if (data[0] == letter[0]) {
          std::string count_str = data.substr(data.find(" ") + 1);
          int count = std::stoi(count_str);
          std::map<char,int>::iterator it = data_map.find(letter[0]);
          if (it == data_map.end()) {
            throw std::runtime_error("Unable to find key: " + letter);
          } else {
            it->second += count;
          }
        }
      }
    }
    
    std::string result = "";
    for (std::string letter : M) {
      std::map<char,int>::iterator it = data_map.find(letter[0]);
      result += "(" + std::string(1, it->first) + " : " + std::to_string(it->second) + ")" + " - ";
    }
    
    return result.substr(0, result.length() - 3);
  }
};
