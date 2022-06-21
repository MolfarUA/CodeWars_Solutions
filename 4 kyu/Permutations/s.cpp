5254ca2719453dcc0b00027d
  
  
#include <algorithm>
#include <string>
#include <vector>

std::vector<std::string> permutations(std::string s)
{
    std::sort(s.begin(), s.end());
    std::vector<std::string> result;
    do
    {
        result.push_back(s);
    }
    while (std::next_permutation(s.begin(), s.end()));
    return result;
}
______________________________
#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<string> permutations(string s) {
    vector<string> result{};
    std::sort(s.begin(), s.end());
    do 
    {
        result.push_back(s);
    } while(std::next_permutation(s.begin(), s.end()));
  
  return result;
}
______________________________
#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<string> permutations(string s) {
  if (s.length() == 0) return vector<string> {""};
  vector<string> result;
  for (int i = 0; i < s.length(); i++) {
    string first = string(1, s[i]), rest = s.substr(0, i) + s.substr(i + 1, string::npos);
    vector<string> subset = permutations(rest);
    for (int j = 0; j < subset.size(); j++) if (find(result.begin(), result.end(), first + subset[j]) == result.end()) result.push_back(first + subset[j]);
  }
  return result;
}
