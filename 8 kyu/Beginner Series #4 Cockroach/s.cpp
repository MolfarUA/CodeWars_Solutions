55fab1ffda3e2e44f00000c6
  
  
int cockroach_speed(double s)
{
    return s / 0.036;
}
__________________________
#include <cmath>

int cockroach_speed(double s)
{
  return static_cast<int>(std::floor((s * 100000.0) / 3600.0));
}
__________________________
#include <cmath>
int cockroach_speed(double s) {
    return floor(s*1e5/3600);
}
__________________________
#include <cmath>

int cockroach_speed(double kph) {
    double cps = kph * 27.7778;
    return floor(cps);
}
__________________________
#include <cmath>
using namespace std;

int cockroach_speed(const double& s){
  return s*pow(10,5)/pow(60,2);
}
