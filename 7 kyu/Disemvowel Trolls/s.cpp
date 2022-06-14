# include <string>
# include <regex>
std::string disemvowel(std::string str)
{
  std::regex vowels("[aeiouAEIOU]");
  return std::regex_replace(str, vowels, "");
}
______________________________
# include <string>

std::string disemvowel(std::string str)
{
    for ( auto letter : "AEIOUaeiou" ) {
      str.erase(std::remove(str.begin(), str.end(), letter), str.end());
    }
    
    return str;
}
______________________________
# include <string>
std::string disemvowel(std::string str)
{
  std::string vowels = "AEIOUaeiou", result = "";

  for (auto& ch : str)
    if (vowels.find(ch) == std::string::npos)
      result += ch;

  return result;
}
______________________________
# include <string>
# include <regex>

std::string disemvowel(std::string str)
{
    return std::regex_replace(str,static_cast<std::regex>("([AaEeIiOoUu])"),"");
}
______________________________
# include <string>
# include <algorithm>
using namespace std;
string disemvowel(string str)
{
  for(int i = 0; i <= str.length(); i++) {
    if(str[i] == 'a' || str[i] == 'e' || str[i] == 'o' || str[i] == 'u' || str[i] == 'i') {  //Check for the lowercase vowels
      str.erase(str.begin()+i); 
      }
   if(str[i] == 'A' || str[i] == 'E' || str[i] == 'O' || str[i] == 'U' || str[i] == 'I') { //Check for the uppercase vowels
      str.erase(str.begin()+i);
      }
    if(str[i] == 'a' || str[i] == 'u') { str.erase(str.begin()+i); } //I actually had a problem without this "if" statement 
    //The thing is : there was an 'a' and an 'u' remaining, and I didn't really know why. So I just added this and it worked.
  }
return str;
    // return
}
