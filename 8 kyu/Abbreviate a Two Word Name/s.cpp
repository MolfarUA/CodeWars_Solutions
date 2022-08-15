57eadb7ecd143f4c9c0000a3
  
  
#include <string>

std::string abbrevName(std::string name)
{
  std::string ret;
  ret.push_back(toupper(name[0]));
  ret.push_back('.');
  ret.push_back(toupper(name[name.find(' ') + 1] ));
  return ret;
}
_________________________
std::string abbrevName(std::string name)
{
  std::string s = "";
  s += toupper(name[0]);
  s += '.';
  s += toupper(name[name.find(' ')+1]);
  return s;
}
_________________________
#include <cctype>

std::string abbrevName(std::string name) {
  const char a = std::toupper(name[0]);
  const char b = std::toupper(name[name.find(' ') + 1]);
  return std::string({a, '.', b});
}
