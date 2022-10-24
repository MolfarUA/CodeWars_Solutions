51b6249c4612257ac0000005
  
  
#include <iostream>
#include <string>

using namespace std;

map<char, int> nums = {{'M', 1000}, {'D', 500}, {'C', 100}, {'L', 50}, {'X', 10}, {'V', 5}, {'I', 1}};

int solution(string roman) {
      int res = 0;
      int old = 0;
      
      for(auto a : roman){
          int curr = nums[a];
          res += curr;
          
          if(curr > old){
              res -= 2 * old;
          }
          
          old = curr;
      }
      
      
      return res;
}
__________________________________
#include <iostream>
#include <string>

using namespace std;

int decode(char letter)
{
  switch (letter)
  {
    case 'M':
      return 1000;
    case 'D':
      return 500;
    case 'C':
      return 100;
    case 'L':
      return 50;
    case 'X':
      return 10;
    case 'V':
      return 5;
    case 'I':
      return 1;
  }
}

int solution(string roman) {
  
  int result = 0;
  
  for (size_t i = 0; i < roman.size(); ++i)
    if (i < roman.size() - 1 && decode(roman[i]) < decode(roman[i + 1]))
      result -= decode(roman[i]);
    else result += decode(roman[i]);
    
  return result;
}
__________________________________
#include <iostream>
#include <string>
#include <map>
using namespace std;

int solution(string roman) {
  map <char, int> m = {{'I',1},{'V',5},{'X',10},{'L',50},{'C',100},{'D',500},{'M',1000}};
  map <char, int> a = {{'I',1},{'V',2},{'X',3},{'L',4},{'C',5},{'D',6},{'M',7}};
  int res = 0;
  for(int i = 0 ; i< roman.size(); i++){
    if(a[roman[i]] < a[roman[i+1]]) res -= m[roman[i]];
    else res += m[roman[i]];
  }
  return res;
}
