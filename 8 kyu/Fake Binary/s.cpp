#include <string>

std::string fakeBin(std::string str){
  for (int i = 0; i < str.length(); i++)
  {
    str[i] = ((str[i] - '0') > 4) ? '1' : '0';
  }
  return str;
}
__________________________________
#include <string>
#include <algorithm>

std::string fakeBin(std::string str){
  std::transform(str.cbegin(), str.cend(), str.begin(), [](auto const & c){
    return c >= '5' ? '1' : '0';
  });
  return str;
}
__________________________________
#include <string>
#include <regex>
using namespace std;
string fakeBin(string str){
str = regex_replace(str, regex("[1234]"), "0");
str = regex_replace(str, regex("[56789]"), "1");
  return str;
}
__________________________________
#include <string>

std::string fakeBin(std::string str){
  for (auto &s : str)
  {
    s = s < '5'?'0':'1';
  }
  return str;
}
__________________________________
#include <string>

std::string fakeBin(std::string str){
  std::transform(str.begin(), str.end(), str.begin(), [](auto ch) {return ch < '5' ? '0' : '1';});
  return str;
}
