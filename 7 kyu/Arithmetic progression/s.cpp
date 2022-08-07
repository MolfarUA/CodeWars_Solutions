55caf1fd8063ddfa8e000018
  
  
#include <string>

std::string arithmeticSequenceElements(int a, int r, int n)
{
  std::string result = "";
  
  for(int i=0;i<n;i++) {
    result+= std::to_string(a) + ", ";
    
    a+=r;
  }
  
  
  return result.substr(0, result.size()-2);
}
___________________________
#include <string>

std::string arithmeticSequenceElements(int a, int d, int n) {
  std::string result = std::to_string(a);
  for (int i = 1; i < n; i++)
    result += ", " + std::to_string(a + i * d);
  return result;
}
___________________________
#include <string>

std::string arithmeticSequenceElements(int a, int r, int n)
{
    std::string seq = std::to_string(a);
    while (--n)
        seq.append(", " + std::to_string(a += r));
    return seq;
}
