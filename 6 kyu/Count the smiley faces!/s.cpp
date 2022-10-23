583203e6eb35d7980400002a


#include <regex>

int countSmileys(std::vector<std::string> arr)
{
  int count = 0;
  std::regex smiles_regex("[:|;](-|~)?[)|D]");
  
  for (auto &smile : arr) {
    if (std::regex_match(smile, smiles_regex))
      count++;
  }

  return count;
}
__________________________
#include <vector>
#include <string>
#include <regex>

int countSmileys(std::vector<std::string> arr)
{
  std::regex expr("[:;][-~]?[)D]");

    return static_cast<int>(std::count_if(arr.begin(), arr.end(),
            [&expr](auto const &v){
        return std::regex_match(v, expr);
    }));
}
__________________________
int countSmileys(std::vector<std::string> arr)
{
  int sum=0;
  for(std::string s : arr)
    if((s[0]==':' || s[0]==';') && (s[s.size()-1]==')' || s[s.size()-1]=='D') && (s.size()==2 || s.size()==3 && (s[1]=='-' || s[1]=='~')))
      sum++;
      
  return sum;
}
