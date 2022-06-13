#include <string>

std::string boolean_to_string(bool b){
  return b ? "true" : "false";
}
_________________________________
#include <sstream>
#include <iomanip>

std::string boolean_to_string(bool b){
  std::ostringstream oss;
  oss << std::boolalpha << b;
  return oss.str();
}
_________________________________
std::string boolean_to_string(bool b){
  //Your code here
  if (b) {
    return "true"; 
  } else { 
    return "false";
  }
}
_________________________________
std::string boolean_to_string(bool b){
  
  std::string tmp;
  
  if(b == 1)
  {
    tmp = "true";
  }
  else
  {
    tmp = "false";
  }
  
  return tmp;
}
_________________________________
#include <string>

std::string boolean_to_string(bool b) {
    return b == 1 ? "true" : "false";
}
_________________________________
#include <string>

std::string boolean_to_string(bool b){
  //Your code here
  std::string text{""};
  if(b == 1 || b == true)
    text = "true";
  else if(b==0 || b == false)
    text = "false";
  
  return text;
}
_________________________________
#include <string>
using namespace std;

string boolean_to_string(bool b){
  string truth_value;
  if (b == true) truth_value = "true";
  else truth_value = "false";
  return truth_value;
}
_________________________________
