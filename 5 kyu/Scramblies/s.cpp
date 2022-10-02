55c04b4cc56a697bb0000048
  
  
#include <algorithm>
#include <string>

bool scramble(std::string s1, std::string s2) {
  std::sort(begin(s1), end(s1));
  std::sort(begin(s2), end(s2));
  return std::includes(begin(s1), end(s1), begin(s2), end(s2));
}
______________________________
#include<string>

bool scramble(const std::string& s1, const std::string& s2){
    std::map<char,int> idx;
    for (auto &i : s1) idx[i]++;
    for (auto &i : s2) if (idx[i]-- == 0) return false;
    return true;
}
______________________________
#include <unordered_map>
#include <algorithm>

bool scramble(const std::string &s1, const std::string &s2){
    std::unordered_map<char, unsigned> m1, m2;
    
    for(auto c : s1) ++m1[c];
    for(auto c : s2) ++m2[c];
    
    return std::all_of(m2.begin(), m2.end(), [&](const std::pair<char, unsigned> &p) {
        return m1[p.first] >= p.second;
    });
}
