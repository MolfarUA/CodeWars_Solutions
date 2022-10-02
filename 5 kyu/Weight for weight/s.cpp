55c6126177c9441a570000cc
  
  
#include <numeric>
#include <string>
#include <iterator>
#include <algorithm>
#include <sstream>

class WeightSort
{
public:
    static std::string orderWeight(const std::string &strng) {
      std::vector<std::string> inputs;
      std::istringstream iss(strng);
      std::copy(std::istream_iterator<std::string>(iss), 
                std::istream_iterator<std::string>(),
                std::back_inserter(inputs));
      std::sort(inputs.begin(), inputs.end(),
                [](const std::string& s1, const std::string& s2) {
                  auto sum_func = [](const char c, int acc) { return acc + static_cast<int>(c-'0'); };
                  int s1sum = std::accumulate(s1.begin(), s1.end(), 0, sum_func);
                  int s2sum = std::accumulate(s2.begin(), s2.end(), 0, sum_func);
                  if (s1sum == s2sum)
                    return s1 < s2;
                  else
                    return s1sum < s2sum;
                });
      std::ostringstream oss;
      std::copy(inputs.begin(), inputs.end(), std::ostream_iterator<std::string>(oss, " "));
      std::string s = oss.str();
      return s.substr(0, s.size()-1);
    }
};
_____________________________
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

class WeightSort
{
private:
    static std::vector<std::string> split(const std::string &s);
    static int weightStrNb(const std::string &strng);
    static bool compare(const std::string &s1, const std::string &s2);
    static std::string join(const std::vector<std::string>& vec);
public:
    static std::string orderWeight(const std::string &strng);
};

std::vector<std::string> WeightSort::split(const std::string &s)
{
    std::vector<std::string> out;
    std::istringstream ss(s);
    std::string next;
    while (std::getline(ss, next, ' '))
        out.push_back(next);
    return out;
}
int WeightSort::weightStrNb(const std::string &s)
{
    int dsum = 0;
    for (unsigned int i = 0; i < s.length(); i++)
        dsum += s[i] - '0';
    return dsum;
}
bool WeightSort::compare(const std::string &s1, const std::string &s2)
{
    int w1 = weightStrNb(s1); int w2 = weightStrNb(s2);
    if (w1 == w2) return s1 < s2;
    return w1 < w2;
}
std::string WeightSort::join(const std::vector<std::string>& vec)
{
    std::string s = "";
    for (unsigned int i = 0; i < vec.size(); i++)
        if (i < vec.size() - 1)
            s += vec[i] + " ";
        else s += vec[i];
    return s;
}

std::string WeightSort::orderWeight(const std::string &strng)
{
    std::vector<std::string> lstr = split(strng);
    std::sort (lstr.begin(), lstr.end(), compare);
    return join(lstr);
}
_____________________________
class WeightSort
{
public:
    static std::string orderWeight(const std::string &strng) {
      std::vector<std::pair<std::string, int>> list;
      std::stringstream ss(strng);
      for (std::string s; ss >> s;) {
          int sum = 0;
          for (char i : s) sum += i - '0';
          list.emplace_back(s, sum);
      }
      std::sort(list.begin(), list.end(), [](auto& left, auto& right) {
          return left.second == right.second ? left.first < right.first : left.second < right.second; });
      std::string result;
      for (auto& i : list) result += i.first + (&i != &list.back() ? " " : "");
      return result;
    }
};
