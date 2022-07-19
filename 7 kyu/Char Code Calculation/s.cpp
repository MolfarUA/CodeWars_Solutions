57f75cc397d62fc93d000059
  
  
#include <string>

int calc(const std::string& x) {
  int s = 0;
  for (char c : x) s += (c % 10 == 7 ? 6 : 0) + (c / 10 % 10 == 7 ? 6 : 0);
  return s;
}
__________________________________
#include <string>

int calc(const std::string& x) {
 std::vector<int> vec;
  for (auto zz : x)
  {
    int c = zz;
    vec.emplace_back(c % 10);
    vec.emplace_back(c / 10);
  }
  std::vector<int> newvec{vec};
  int rem = 0;
  std::replace(newvec.begin(), newvec.end(), 7, 1);
  for (int it = 0; it < vec.size(); ++it)
     rem += vec[it] - newvec[it];

  return rem;
}
__________________________________
#include <string>

int calc(const std::string& x) {
  std::string total1;
  std::string total2;
  int sum1 = 0;
  int sum2 = 0;
  
  for (char c : x) {
    total1 += std::to_string(int(c));
  }
  
  for (char& c : total1) {
    sum1 += int(c);
    
    if (c == '7') {
      c = '1';
    }
    
    total2 += c;
    sum2 += int(c);
  }
  
  return sum1 - sum2;
}
__________________________________
#include <string>

int calc(const std::string& x) {
  int total1 = 0;
  int total2 = 0;

  for (auto& letter : x)
  {
    total1 += int(letter) / 10 + int(letter) % 10;
    int num1 = (int(letter) / 10 != 7 ? int(letter) / 10 : 1);
    int num2 = (int(letter) % 10 != 7 ? int(letter) % 10 : 1);
    total2 += (num1 + num2);
  }
  return total1 - total2;
}
