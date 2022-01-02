#include <string>
#include <algorithm>

std::string makeUpperCase (const std::string& input_str)
{
  std::string str = input_str;
  std::transform(str.begin(), str.end(),str.begin(), ::toupper);
  return str;
}
_____________________________________________
#include <string>

std::string makeUpperCase (const std::string& input_str)
{
  std::string new_str = "";
  for (int i = 0; i < input_str.length(); i++)
  {
    std::string sub_str = "";
    sub_str = input_str.substr(i, 1);
    
    if (sub_str == "a")
    {
      new_str += "A";
    }
    else if (sub_str == "b")
    {
      new_str += "B";
    }
    else if (sub_str == "c")
    {
      new_str += "C";
    }
    else if (sub_str == "d")
    {
      new_str += "D";
    }
    else if (sub_str == "e")
    {
      new_str += "E";
    }
    else if (sub_str == "f")
    {
      new_str += "F";
    }
    else if (sub_str == "g")
    {
      new_str += "G";
    }
    else if (sub_str == "h")
    {
      new_str += "H";
    }
    else if (sub_str == "i")
    {
      new_str += "I";
    }
    else if (sub_str == "j")
    {
      new_str += "J";
    }
    else if (sub_str == "k")
    {
      new_str += "K";
    }
    else if (sub_str == "l")
    {
      new_str += "L";
    }
    else if (sub_str == "m")
    {
      new_str += "M";
    }
    else if (sub_str == "n")
    {
      new_str += "N";
    }
    else if (sub_str == "o")
    {
      new_str += "O";
    }
    else if (sub_str == "p")
    {
      new_str += "P";
    }
    else if (sub_str == "q")
    {
      new_str += "Q";
    }
    else if (sub_str == "r")
    {
      new_str += "R";
    }
    else if (sub_str == "s")
    {
      new_str += "S";
    }
    else if (sub_str == "t")
    {
      new_str += "T";
    }
    else if (sub_str == "u")
    {
      new_str += "U";
    }
    else if (sub_str == "v")
    {
      new_str += "V";
    }
    else if (sub_str == "w")
    {
      new_str += "W";
    }
    else if (sub_str == "x")
    {
      new_str += "X";
    }
    else if (sub_str == "y")
    {
      new_str += "Y";
    }
    else if (sub_str == "z")
    {
      new_str += "Z";
    }
    else
    {
      new_str += sub_str;
    }
  }
  return new_str;
}
_____________________________________________
#include <string>

std::string makeUpperCase (const std::string& input_str)
{
  std::string temp = input_str;
  for(int i = 0; i < temp.length(); i++){
    temp[i] = toupper(temp[i]);
  }
  return temp;
}
_____________________________________________
#include <string>

std::string makeUpperCase (const std::string& input_str)
{
    std::string s = "";
    for(int i = 0; i < input_str.size();i++)
    {
        if((input_str[i] >= 97)&&(input_str[i] <= 122))
            s += input_str[i] - 32;
        else s += input_str[i];
    }
    return s;
}
