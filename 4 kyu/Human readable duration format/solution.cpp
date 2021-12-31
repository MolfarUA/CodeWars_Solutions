#include <string>
#include <vector>

std::string format_duration(int seconds) {
  if (seconds == 0) return "now";
  
  std::vector<std::string> times;
  auto add = [&] (auto text, auto time) {
    if (time == 0) return;
    times.push_back(std::to_string(time) + text + (time > 1 ? "s" : ""));
  };
  add(" year",    seconds / 31536000);    
  add(" day",    (seconds / 86400) % 365);    
  add(" hour",   (seconds / 3600) % 24);    
  add(" minute", (seconds / 60) % 60);    
  add(" second",  seconds % 60);    
  
  std::string result = times[0];
  for (auto i = 1; i < times.size() - 1; i ++) result.append(", " + times[i]);
  if (times.size() > 1) result.append(" and " + times.back());
  
  return result;
}

___________________________________________________
#include <iostream>
#include <string>
#include <cmath>
using namespace std;
std::string format_duration(int seconds) {
int gs = seconds;
  int years = gs/(3.154e7);
  int days = (gs-years*31536000)/86400;
int ngs = gs - ((24 * 3600 * days) + (31536000 * years));
  int hours = (ngs / 3600);
int nngs = ngs - (3600 * hours);
  int minutes = nngs / 60;
int nnngs = nngs - (60 * minutes);
  int secs = nnngs;
string strdays = to_string(days);
string strhours = to_string(hours);
string strminutes = to_string(minutes);
string strsecs = to_string(secs);
string stryears = to_string(years);
string sy, sd, sh, sm, ss;
  if (years == 0 && days == 0 && hours == 0 && minutes == 0 && secs == 1)
    {return "1 second";}
    else if (years == 0 && days == 0 && hours == 0 && minutes == 1 && secs == 0)
      {return "1 minute";}
    else if (years == 0 && days == 0 && hours == 1 && minutes == 0 && secs == 0)
      {return "1 hour";}
    else if (years == 0 && days == 1 && hours == 0 && minutes == 0 && secs == 0)
      {return "1 day";}
    else if (years == 1 && days == 1 && hours == 0 && minutes == 0 && secs == 0)
      {return "1 year";}
    else if (years == 0 && days == 0 && hours == 0 && minutes == 0 && secs == 0)
      {return "now";}
  
  if (years == 1) {sy = "1 year";}
    else if (years>1) {sy = stryears + " years";}
  if (days == 1) {sd = "1 day";}
    else if (days>1) {sd = strdays + " days";}
  if (hours == 1) {sh = "1 hour";}
    else if (hours>1) {sh = strhours + " hours";}
  if (minutes == 1) {sm = "1 minute";}
    else if (minutes>1) {sm = strminutes + " minutes";}
  if (secs == 1) {ss = "1 second";}
    else if (secs>1) {ss = strsecs + " seconds";}

  if (years == 0 && days == 0 && hours == 0 && minutes != 0 && secs != 0)
    {sm = sm + " and ";}
    else if (years == 0 && days == 0 && hours != 0 && minutes != 0 && secs != 0)
      {sh = sh + ", "; sm = sm + " and ";}
    else if (years == 0 && days != 0 && hours != 0 && minutes != 0 && secs != 0)
      {sd = sd + ", "; sh = sh + ", "; sm = sm + " and ";}
    else if (years != 0 && days != 0 && hours != 0 && minutes != 0 && secs != 0)
      {sy = sy + ", "; sd = sd + ", "; sh = sh + ", "; sm = sm + " and ";}
    else if (years == 0 && days == 0 && hours == 0 && minutes == 0 && secs == 0)
      {return "1 year";}
    else if (years == 0 && days != 0 && hours == 0 && minutes != 0 && secs != 0)
      {sd = sd + ", "; sm = sm + " and ";}
    else if (years == 0 && days != 0 && hours == 0 && minutes != 0 && secs != 0)
      {sd = sd + ", "; sm = sm + " and ";}
    else if (years == 0 && days != 0 && hours != 0 && minutes == 0 && secs != 0)
      {sd = sd + ", "; sh = sh + " and ";}
    else if (years == 0 && days != 0 && hours != 0 && minutes != 0 && secs == 0)
      {sd = sd + ", "; sh = sh + " and ";}
    else if (years == 0 && days != 0 && hours == 0 && minutes == 0 && secs != 0)
      {sd = sd + " and ";}
    else if (years == 0 && days != 0 && hours != 0 && minutes == 0 && secs == 0)
      {sd = sd + " and ";}
    else if (years == 0 && days == 0 && hours != 0 && minutes != 0 && secs == 0)
      {sh = sh + " and ";}
    else if (years == 0 && days != 0 && hours == 0 && minutes != 0 && secs == 0)
      {sd = sd + " and ";}
    else if (years != 0 && days != 0 && hours != 0 && minutes != 0 && secs == 0)
      {sy = sy + ", "; sd = sd + ", "; sh = sh + " and ";}
  if (years == 0 && days == 0 && hours == 0 && minutes == 0 && secs == 0)
      {return "now";}
  return sy + sd + sh + sm + ss;
}

___________________________________________________
#include <string>
#include <vector>

std::string format_duration(int s) {
    if(s == 0){ return "now"; }
    std::vector<std::pair<std::string, int>> data =
    {{"year",(s/60/60/24/365)},{"day",(s/60/60/24)%365},{"hour",(s/60/60)%24},{"minute",(s/60)%60},{"second",s%60}};
    std::vector<std::string> tvec;
    for(auto &c:data){
        if(c.second != 0){
            tvec.push_back(std::to_string(c.second) + " " + c.first + (c.second > 1? "s":""));
        }
    }
    std::string result;
    size_t size = tvec.size();
    for(int i = 0; i != size; i++){
        result += tvec[i] + (i==size-1?(""):(i == size-2?(" and "):(", ")));
    }
    return result;
}
