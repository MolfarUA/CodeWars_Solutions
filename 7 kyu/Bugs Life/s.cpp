5b71af678adeae41df00008c
  
  
#include <cmath>

double shortestDistance (double x, double y, double z) {
  double a = std::max({x,y,z});
  return sqrt(pow((x+y+z-a),2)+pow(a,2));
}
____________________________
#include <vector>
#include <math.h>
#include <algorithm>

double shortestDistance (double x, double y, double z) {
  std::vector<double> candidates;
  candidates.push_back((x + y) * (x + y) + z * z);
  candidates.push_back((x + z) * (x + z) + y * y);
  candidates.push_back((y + z) * (y + z) + x * x);
  return sqrt(*std::min_element(candidates.begin(), candidates.end()));
}
____________________________
#import <cmath>

double shortestDistance (double a, double b, double c) {
  const double maximum = std::max(std::max(a, b), c);
  const double unfolded = a + b + c - maximum;
  return sqrt(unfolded * unfolded + maximum * maximum);
}
