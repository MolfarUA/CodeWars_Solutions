#include <string>

std::string to_camel_case(std::string text)
{
  for(int i = 0; i < text.size(); ++i)
  {
    if(text[i] == '-' || text[i] == '_')
    {
      text.erase(i,1);
      text[i] = toupper(text[i]);
    }
  }
  return text;
}
________________________
#include <string>


std::string to_camel_case(std::string text) {
  if (text == "") return "";
  std::string capText = "";
  if(!isupper(text[0])) {
    capText = capText + text[0];
  } else {
      capText.push_back(toupper(text[0]));
  }
  for (int i = 1; i < text.size(); i++) {
    if (text[i] == '_' || text[i] == '-') {
      i++;
      capText.push_back(toupper(char(text[i])));
    } else {
      capText = capText + text[i];
    }
  }
  return capText;
}
________________________
#include <string>

std::string to_camel_case(std::string text) {
  int i=0;
  std::string new_text;
  while(i<(int)text.size()){
    if(text[i]=='_'||text[i]=='-'){
      new_text+=toupper(text[i+1]);
      i++;
    }else{
      new_text+=text[i];
    }
    i++;
  }
  return new_text;;
}
________________________
#include <string>


std::string to_camel_case(std::string text) {
  // TODO: Your code goes here!
  
  std::string CamelCase = ""; //Return this
  unsigned long marker = 0; ; //Position
  bool toUpper = false;       //Make capital
  
  while(marker < text.size()){  //For the entire word
    if(text[marker]=='-'||text[marker]=='_'){ //Condition for capital
      marker++;                               //Go to next letter
      toUpper = true;                         //Make it capital
    }
    
    if(toUpper)
      CamelCase += toupper(text[marker]);
    else
      CamelCase += text[marker];
    
    marker++;
    toUpper = false;
  }
  
  return CamelCase;
}
