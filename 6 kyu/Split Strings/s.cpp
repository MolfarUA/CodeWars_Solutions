515de9ae9dcfc28eb6000001
  
  
std::vector<std::string> solution(const std::string &s) {
    std::vector <std::string> res;
    for (int i = 0; i < s.length(); i += 2) res.push_back(s.substr(i, 2));
    if (s.length() % 2) res[res.size() - 1] += "_";
    return res;
}
________________________________
#include <string>
#include <vector>
#include <regex>

std::vector<std::string> solution(const std::string &s)
{
    std::regex r{".."};
    auto str = s + '_';
    return {std::sregex_token_iterator(str.begin(), str.end(), r), {}};
}
________________________________
#include <string>
#include <vector>

std::vector<std::string> solution(const std::string &s)
{
    std::string String = s;
  std::vector<std::string> Vector;
  int Size = String.size();
  
  
  
  if (Size % 2 != 0)
  {
    String.push_back('_');
  }

  Size = String.size();

  for (size_t i = 0; i < Size/2; i++)
  {
    std::string substr = String.substr(0, 2);
    Vector.push_back(substr);
    String.erase(0, 2);
  }

  


  return Vector;
}
________________________________
#include <string>
#include <vector>
using namespace std;
std::vector<std::string> solution(const std::string &s)
{
//          ／＞　　フ
//　　　　　| 　n　n 彡
//　 　　　／`ミ＿xノ
//　　 　 /　　　 　 |
//　　　 /　 ヽ　　 ﾉ
//　 　 │　　|　|　|
//　／￣|　　 |　|　|
//　| (￣ヽ＿_ヽ_)__)
//　＼二つ
// ITS CAT FOR YOU
    vector <string> result;
    for (int i = 0; i < s.size(); i += 2) result.push_back(s.substr(i, 2));
    if (s.size() % 2) result[result.size() - 1] += "_";
    return result;
}
________________________________
#include <string>
#include <vector>

std::vector<std::string> solution(const std::string &s) {
    std::string ss = s;
    std::vector<std::string> res;
    while (ss.length() > 1) {
        res.push_back(ss.substr(0, 2));
        ss.erase(0, 2);
    }
    if (ss.length() == 1) {
        res.push_back(ss + "_");
    }
    return res;
}
