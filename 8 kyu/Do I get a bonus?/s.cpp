56f6ad906b88de513f000d96
  
  
#include<string>
using namespace std;

string bonus_time(int salary, bool bonus)
{
    return "$" + to_string(salary) + (bonus ? "0" : "");
}
__________________________
#include<string>
using namespace std;

string bonus_time(int salary, bool bonus)
{

 return (bonus) ? ("$" + to_string(salary*10)) : ("$" + to_string(salary));
    
}
__________________________
#include <string>
#include <sstream>

std::string bonus_time (int salary, bool bonus)
{
  std::ostringstream oss;
  
  oss << '$' << (bonus ? 10 * salary : salary);
  
  return oss.str();
}

