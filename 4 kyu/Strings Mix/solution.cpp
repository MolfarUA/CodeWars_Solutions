#include <sstream>
#include <vector>
#include <algorithm>

class Mix {
private:
    struct Letter {
        char letter {'a'};
        std::pair<int,int> freq {0, 0};
        char maxChar {'a'};
        int maxFreq {0};
    };
    
public:
    static std::string mix(const std::string &s1, const std::string &s2) {
        std::vector<Letter> alphabet(26);
        for (int i = 0; i < 26; i++) {
            alphabet[i].letter      = i + 'a';
            alphabet[i].freq.first  = std::count(s1.begin(), s1.end(), alphabet[i].letter);
            alphabet[i].freq.second = std::count(s2.begin(), s2.end(), alphabet[i].letter);
            alphabet[i].maxFreq = (alphabet[i].freq.first > alphabet[i].freq.second) ? alphabet[i].freq.first : alphabet[i].freq.second;
            if      (alphabet[i].freq.first >  alphabet[i].freq.second)   alphabet[i].maxChar = '1';
            else if (alphabet[i].freq.first <  alphabet[i].freq.second)   alphabet[i].maxChar = '2';
            else if (alphabet[i].freq.first == alphabet[i].freq.second)   alphabet[i].maxChar = '=';
        }        
        auto sortingFunction = [](Letter &a, Letter &b) {
            if (a.maxFreq > b.maxFreq)  return true;
            if (a.maxFreq < b.maxFreq)  return false;
            if (a.maxChar < b.maxChar)  return true;
            if (a.maxChar > b.maxChar)  return false;
            if (a.letter  < b.letter)   return true;
            else                        return false;
        };
        std::sort(alphabet.begin(), alphabet.end(), sortingFunction);
        std::stringstream ss;
        for (int i = 0; i < 26; i++) {
            if (alphabet[i].freq.first > 1 || alphabet[i].freq.second > 1) {
                ss << alphabet[i].maxChar << ':';
                ss << std::string(alphabet[i].maxFreq, alphabet[i].letter) << '/';
            }
        }
        std::string result = ss.str();
        return result.substr(0, result.length()-1);
    }
};

__________________________________________________
#include <vector>
using namespace std;
class Mix
{
public:
  static std::string mix(const std::string &s1, const std::string &s2) {
    string rv;
    int aFreq[26] = {0}, bFreq[26] = {0};
    vector<pair<string, string>> table;
    for(auto c : s1) if(islower(c)) aFreq[c - 'a']++;
    for(auto c : s2) if(islower(c)) bFreq[c - 'a']++;
    for(int i = 0; i < 26; i++) {
      int frequency = max(aFreq[i], bFreq[i]);
      if(frequency <= 1) continue;
      string stringLoc = "=";
      if(aFreq[i] != bFreq[i]) stringLoc = ((aFreq[i] > bFreq[i]) ? "1" : "2");
      table.push_back(make_pair(string(frequency, ((char)('a' + i))), stringLoc));
    }
    sort(table.begin(), table.end(), [](pair<string, string> a, pair<string, string> b) {
      if (a.first.length() != b.first.length()) return (a.first.length() > b.first.length());
      return (a.second + ":" + a.first < b.second + ":" + b.first);
    });
    for(auto x : table)
      rv += x.second + ":" + x.first + "/";
    return rv.substr(0, rv.length() - 1);      
  }
};

__________________________________________________
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

class Mix
{
private:
  static bool compare(const std::string &s1, const std::string &s2);
  static std::vector<std::string> split(const std::string &s);
  static std::string join(const std::vector<std::string>& vec);
public:
  static std::string mix(const std::string &s1, const std::string &s2);
};

bool Mix::compare(const std::string &s1, const std::string &s2)
{
    int w1 = s1.length(); int w2 = s2.length();
    if (w1 == w2) return s1 < s2;
    return w1 > w2;
}
std::vector<std::string> Mix::split(const std::string &s)
{
    std::vector<std::string> out;
    std::istringstream ss(s);
    std::string next;
    while (std::getline(ss, next, '/'))
        out.push_back(next);
    return out;
}
std::string Mix::join(const std::vector<std::string>& vec)
{
    std::string s = "";
    for (unsigned int i = 0; i < vec.size(); i++)
        if (i < vec.size() - 1) s += vec[i] + "/";
        else s += vec[i];
    return s;
}

std::string Mix::mix(const std::string &s1, const std::string &s2)
{
    std::vector<int> alpha1(26);
    for (unsigned int i = 0 ; i < alpha1.size() ; i++) alpha1[i] = 0;
    std::vector<int> alpha2(26);
    for (unsigned int i = 0 ; i < alpha1.size() ; i++) alpha2[i] = 0;
    for (unsigned int i = 0; i < s1.length(); i++)
    {
        int c = static_cast<int>(s1[i]);
        if (c >= 97 && c <= 122)
            alpha1[c - 97]++;
    }
    for (unsigned int i = 0; i < s2.length(); i++)
    {
        int c = static_cast<int>(s2[i]);
        if (c >= 97 && c <= 122)
            alpha2[c - 97]++;
    }
    std::string res = "";
    for (int i = 0; i < 26; i++)
    {
        int sm = std::max(alpha1[i], alpha2[i]);
        if (sm > 1)
        {
            if (sm > alpha1[i])
            {
                std::string r1 = std::string(sm, static_cast<char>(i + 97));
                res += "2:" + r1 + "/";
            }
            else
            {
                std::string r2 = std::string(sm, static_cast<char>(i + 97));
                if (sm > alpha2[i])
                    res += "1:" + r2 + "/";
                 else
                    res += "=:" + r2 + "/";
            }
        }
    }
    if (res.length() == 0)
        return "";
    std::vector<std::string> lstr = split(res.substr(0, res.length() - 1));
    std::sort (lstr.begin(), lstr.end(), compare);
    res = join(lstr);
    return res;
}

__________________________________________________
#include <algorithm>
#include <map>
#include <numeric>
#include <sstream>

class Mix
{
public:
  static std::map<char, int> histogram(const std::string& s) {
    std::map<char, int> hist;
    for (const char& c : s) {
      if (c >= 'a' && c <= 'z') {
        ++hist[c];
      }
    }
    
    return hist;
  }
  
  static std::vector<std::string> find_maximums(std::map<char,int>& h1, std::map<char, int>& h2) {
    std::vector<std::string> substrings;
    for (char c = 'a'; c <= 'z'; ++c) {
      if (h1[c] > 1 || h2[c] > 1) {
        std::stringstream tmp;
        tmp << (h1[c] > h2[c] ? "1" : (h2[c] > h1[c] ? "2" : "=")) << ":";
        for (int counter = 0; counter < std::max(h1[c], h2[c]); ++counter) {
          tmp << c;
        }
        substrings.push_back(tmp.str());
      }
    }
    return substrings;
  }

  static std::string mix(const std::string &s1, const std::string &s2) {
    std::map<char, int> h1 = histogram(s1), h2 = histogram(s2);
    
    std::vector<std::string> substrings = find_maximums(h1, h2);
    
    if (substrings.empty())
      return "";
    
    std::sort(std::begin(substrings),
              std::end(substrings),
              [] (const auto& s1, const auto& s2) {
                return std::make_tuple(-s1.size(), s1) < std::make_tuple(-s2.size(), s2);
              });
    
    return std::accumulate(std::next(std::begin(substrings)),
                           std::end(substrings),
                           substrings[0],
                           [] (const auto& s1, const auto& s2) {
                             return s1 + "/" + s2;
                           });
  }
};
