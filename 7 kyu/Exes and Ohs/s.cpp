#include <algorithm>
bool XO(const std::string& str)
{
  int xCount = std::count(str.begin(), str.end(), 'x') + std::count(str.begin(), str.end(), 'X');
  int oCount = std::count(str.begin(), str.end(), 'o') + std::count(str.begin(), str.end(), 'O');
  return xCount ==  oCount;
}
__________________________________
#include <string>

bool XO(const std::string& str)
{
  int counter = 0;
  for (int i = 0; i < str.length(); i++)
  {
    if (str[i] == 'x' || str[i] == 'X')
      counter++;

    if (str[i] == 'o' || str[i] == 'O')
      counter--;
  }

  return counter == 0;
}
__________________________________
bool XO(const std::string& str)
{
  int os = 0, xs = 0;
  for (int i = 0; i < str.length(); ++i){
    if (str[i] == 'x' || str[i] == 'X') xs++;
    if (str[i] == 'o' || str[i] == 'O') os++;
  }
  return os == xs;
}
__________________________________
#include <cstdint>

bool XO(const std::string& str)
{
  uint32_t x = 0;
  uint32_t o = 0;
  for(auto c : str) {
    if(std::toupper(c) == 'X') x++;
    if(std::toupper(c) == 'O') o++;
  }
  return x == o;
}
__________________________________
bool XO(const std::string& str)
{
  int balance = 0;
  for (int i = 0; i < str.length(); ++i) {
    switch (str[i]) {
       case 'o':
       case 'O':
          ++balance; 
          break;
       case 'x':
       case 'X':
          --balance; 
          break;
       default:
          break;
    }
  }
  return balance==0;
}
__________________________________
#include <bits/stdc++.h>
using namespace std ;

bool XO(string str)
{
transform(str.begin(),str.end(),str.begin(),::tolower);
return count_if(str.begin(),str.end(),[](char o){return o == 'o';}) == count_if(str.begin(),str.end(),[](char x){return x == 'x';}) ;
}
