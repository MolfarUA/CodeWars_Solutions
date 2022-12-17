57873ab5e55533a2890000c7
  
  
#include <regex>
#include <string>

std::string correct(std::string timeString)
{ 
	if (timeString.empty())
		return timeString;
	std::regex reg("(\\d\\d):(\\d\\d):(\\d\\d)");
	std::cmatch cm;
	if (std::regex_match(timeString.c_str(), cm, reg)) {
		int hours = atoi(cm[1].first);
		int minutes = atoi(cm[2].first);
		int seconds = atoi(cm[3].first);
		minutes += seconds / 60;
		hours += minutes / 60;
		seconds %= 60;
		minutes %= 60;
		hours %= 24; 

		char result[9];		
		sprintf(result, "%02d:%02d:%02d", hours, minutes, seconds);
		return std::string(result);
	}
	return "";
}
_________________________________
#include <regex>
#include <string>

std::string correct(std::string timeString)
{ 
    std::regex mask("(\\d\\d):(\\d\\d):(\\d\\d)");
    std::cmatch cm;
    
    if (std::regex_match(timeString.c_str(),cm,mask))
    {
      int h = atoi(cm[1].first);
      int m = atoi(cm[2].first);
      int s = atoi(cm[3].first);
      
      m += s/60;
      h += m/60;
      s %= 60;
      m %= 60;
      h %= 24;
      
      char result[9];
      sprintf(result,"%02d:%02d:%02d",h,m,s);
      return std::string(result);
      
    }
    
    return "";
}
_________________________________
std::string correct(std::string timeString)
{
  char res[9]{};
  if (unsigned int h, m, s; sscanf(timeString.data(), "%u:%u:%u", &h, &m, &s) == 3) {
    m += s / 60;
    h += m / 60;
    sprintf(res, "%.2u:%.2u:%.2u", h % 24, m % 60, s % 60);
  }
  return res;
}
