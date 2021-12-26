#include <string>
#include <regex>
using namespace std;
string pig_it(string Z) {
    regex reg(("(\\w)(\\w*)(\\s|$)"));
    return regex_replace(Z, reg, "$2$1ay$3");
}

####################
#include<iostream>
#include<sstream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

string pig_it(string str)
{
  
  string punctuation = "!.,:;?";
  string result = "";
  stringstream ss;
  ss << str;

  for (char ch; ss.get(ch);) { //read char and whitespace
    
    if (isspace(ch))
      result += ch;
        
    else {
      ss.putback(ch); //read a word from the stream
      string word;
      ss >> word;
      
      if (find(punctuation.begin(), punctuation.end(), word[0]) == punctuation.end()) {
        word.push_back(word[0]);
        word.erase(word.begin());
        word.push_back('a');
        word.push_back('y');
      }
      result += word;
    }
  }

  return result;
}

#################
#include <regex>

std::string pig_it(std::string str)
{
    return std::regex_replace(std::move(str), std::regex{"([a-zA-Z])(\\S*)"}, "$2$1ay");
}

#####################
#include <sstream>

std::string pig_it(std::string str)
{
  std::istringstream is(str);
  std::ostringstream res;
  std::string tmp;
  
  bool first = true;
  while (is >> tmp)
  {
    if (first)
      first = false;
    else
      res << ' ';
    
    if (tmp.size() == 1 && !isalpha(tmp[0]))
    {
      res << tmp;
      continue;
    }

    res << std::string(tmp.begin() + 1, tmp.end()) << *tmp.begin() << "ay";
  }
  
  
  return res.str();
}

#######################
#include <regex>
#include <vector>
#include <iterator>

std::string pig_it(std::string str)
{
  static const std::regex first_letter_middleword_and_maybe_last_letter("([[:alnum:]])([[:alnum:]]*)([[:alnum:]]?)");
  // $01 first letter
  // $02 middle-word
  // $03 last letter
  return std::regex_replace(str, first_letter_middleword_and_maybe_last_letter, "$03$02$01ay");
}

#########################
std::string pig_it(std::string str) {
    std::string res{""};
    std::string word{""};
    char tmp;

    for (int x = 0; x < str.size(); ++x) {
        if (str[x] == '!' || str[x] == '?' || str[x] == ',' || str[x] == '.' ||
            str[x-1] == '!' || str[x-1] == '?' || str[x-1] == ',' || str[x-1] == '.') 
        {
            res.push_back(str[x]);
            continue;
        }

        if (str[x] != ' ')
            word.push_back(str[x]);

        if (str[x] == ' ' || x == str.size()-1) {
            tmp = word[0];
            word.erase(0, 1);
            word.push_back(tmp);
            word.append("ay");

            if (x+1 != str.size())
                word.push_back(' ');

            res.append(word);
            word.clear();
        }
    }

    return res;
}
