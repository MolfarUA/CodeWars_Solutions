#include <string>

std::string createPhoneNumber(const int arr [10]){
  char buf[15];
  snprintf(buf, sizeof(buf), "(%d%d%d) %d%d%d-%d%d%d%d%d", arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9]);
  return buf;
}
_______________________________
#include <string>

std::string createPhoneNumber(const int digits[10]) {
  std::string res = "(...) ...-....";
  for (unsigned is = 0, id = 0; is < res.length(); is++)
    if (res[is] == '.')
      res[is] = '0' + digits[id++];
  return res;
}
_______________________________
#include <string>

std::string createPhoneNumber(const int arr [10]){
  std::string a = "(";
  for(int i = 0; i <10; i++){
    if(i == 3)
      a += ") ";
    if(i == 6)
      a += "-";
    a += std::to_string(arr[i]);
  }
  return a;
}
_______________________________
#include <string>
using namespace std;
std::string createPhoneNumber(const int arr [10]){
  string number = "";
  for (int i = 0; i < 10; i++)
    number += to_string(arr[i]);
    
  number.insert(0, "(");
  number.insert(4, ") ");
  number.insert(9, "-");
  
  return number;
}
_______________________________
#include <string>
#include <sstream>
#include <iomanip>

std::string createPhoneNumber(const int arr [10])
{
  std::stringstream ss;
  
  ss
    << "(" << arr[0] << arr[1] << arr[2] << ") "
    << arr[3] << arr[4] << arr[5] << "-"
    << arr[6] << arr[7] << arr[8] << arr[9];
  
  
  return ss.str();
}
