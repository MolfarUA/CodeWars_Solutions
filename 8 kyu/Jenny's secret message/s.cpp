55225023e1be1ec8bc000390


std::string greet(std::string name) 
{
  return "Hello, " + ( name == "Johnny" ? "my love" : name) + "!";
}
__________________________________
std::string greet(std::string name) 
{
  if(name == "Johnny") {
    return "Hello, my love!";
  }
  return "Hello, " + name + "!";
}
__________________________________
using namespace std;
#include<string>
string greet(string name)
{
  if (name == "Johnny")
  {
    return "Hello, my love!";
  }
  else
  {
    return "Hello, " + name + "!";
  }
}
__________________________________
std::string greet(std::string name) 
{
  bool isLoyal("Johnny");
  
  if(name == "Johnny" && isLoyal) {
    return "Hello, my love!";
  }
  
  else if (!isLoyal) {
    return "I don't want to see you again, just leave me alone!";
  }
 
  return "Hello, " + name + "!";
}
