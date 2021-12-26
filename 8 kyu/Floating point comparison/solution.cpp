#include <cmath>
using namespace std;

bool approx_equals(double a, double b) {
  return abs(a - b) < 0.001;
}

###################
#include <cmath>
using namespace std;

bool approx_equals(double a, double b) {
  return abs(a - b) <= 1e-3;
}

#######################
#include <cmath>
using namespace std;

bool approx_equals(double a, double b, float epsilon = 0.001f) {
  return fabs(a-b) < epsilon;
  //return round(a*1000) == round(b*1000);
}

#####################
#include <cmath>
using namespace std;

bool approx_equals(double a, double b) {
  float diff;
  
  if (a>=b){
  diff = a-b;
    }
  
  if (b>a){
    diff = b-a;
  }
  
  if (diff <= 0.001){
    return true;
  }
  else {
      return false;
}
}

######################
#include <cmath>
using namespace std;

bool approx_equals(double a, double b) {
  if(abs(a - b) < 0.001){
    return true; 
  }
  return false; 
}

################
#include <cmath>
using namespace std;

bool approx_equals(double a, double b) {
//   return trunc(a*1000) == trunc(b*1000);
  return abs(a - b) < 0.001;
}
