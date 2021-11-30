#include <iomanip>

std::string seriesSum(int n)
{
    float num = 0,divider = 1;
    for (int i = 0; i < n; ++i)
    {
      num += (1.0/divider);
      divider  += 3;
    }
    
    std::ostringstream ss;
    ss << std::fixed << std::setprecision(2) << num;
    return ss.str();
}
#########################
std::string seriesSum(int n)
{
    float sum = 0;
    char str[3];
    for(auto i = 0; i < n; i++) sum += 1./(3*i+1);
    sprintf(str, "%.2f", sum);
    return str;
}
####################
#include <iomanip>

using namespace std;

string seriesSum(int n)
{
    double ret = 0.0;
    double base = 1.0;
    while (n--) {
      ret += 1 / base;
      base += 3;
    }
    stringstream retss;
    retss << setprecision(2) << fixed << ret;
    return retss.str();
}
######################
#include <iomanip>
#include <algorithm>

std::string seriesSum(int n)
{
  float f = 0.0;
  for (int i = 0; i < n; i++) {
    f += 1.0/double(1 + 3*i);
  }
  std::stringstream ss;
  ss << std::fixed << std::setprecision(2) << f;
  return ss.str();
}
######################
std::string seriesSum(int n)
{
    double sum = 0.0;
    for (int index = 0; index < n; ++index) {
      sum += 1.0 / (3 * index + 1);
    }
    std::string result = std::to_string(sum + 0.005);
    return result.substr(0, result.find('.') + 3);
}
####################
using namespace std;
std::string seriesSum(int n)
{
    // Happy Coding ^_^
    
    double value = 0.00;
    double one = 1.00;
    int bottom = 1;
    double temp;
    
    for (int ii = 0; ii < n; ii++){
      temp = one / bottom;
      value +=temp;
      bottom+=3;
    }
    
    value = value * 100;
    value +=0.5;
    value = value / 100;
    return to_string(value).substr(0,4);
    
    
}
#####################
#include <cmath>
#include <sstream>
#include <iomanip>
std::string seriesSum(int n)
{
    double sum = 0.0;
    for (double i = 1.0; i < 1+n*3; i += 3.0)
    {
        sum += 1.0/i;
    }
    std::ostringstream result;
    result << std::fixed << std::setprecision(2) << std::floor(sum*100.0 + 0.5) / 100.0;
    
    return result.str();
}
###################
using namespace std;
string seriesSum(int n)
{
    double res = 0;
    for (int i = n-1; i >= 0; --i)
      res += 1. / (1 + 3 * i);
    char str[64];
    sprintf(str, "%.2f", res);
    return string(str);
}
###########
#include <string>
#include <sstream>
#include <iomanip>

//Series: 1 + 1/4 + 1/7 + 1/10 + 1/13 + 1/16 +...
std::string seriesSum(int n)
{
    double result = 0.00;
    for(int i = 0; i < n; i++){
        result += 1.0 / ((i * 3) + 1);
    }
    
    std::stringstream ss;
    ss << std::fixed << std::setprecision(2) << result;
    return ss.str();
    
    
}
#################
#include <cmath>

std::string seriesSum(int n)
{
  if (n == 0) 
    return {"0.00"};
  double answer = 0.;
  for (int i = n; i > 0; --i) {
    answer += 1. / (1 + (i - 1) * 3);
  }
  auto ret = std::to_string((int)std::round(answer * 100));
  return std::move(ret.insert(ret.size() - 2, 1, '.'));
}
