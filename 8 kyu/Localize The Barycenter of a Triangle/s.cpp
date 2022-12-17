5601c5f6ba804403c7000004
  
  
#include <utility>
#include <math.h>

using point =  std::pair<double, double>;
std::pair<double, double> barTriang(point p1, point p2, point p3) {
  //your code here
    point result{};

   result.first = (p1.first + p2.first + p3.first)/3;
   result.second = (p1.second + p2.second + p3.second)/3;

   result.first = round(result.first * 10000) / 10000;
   result.second = round(result.second * 10000) / 10000;


  return result;
}
__________________________________
#include <utility>
#include <cmath>

using point = const std::pair<double, double>;
std::pair<double, double> barTriang(point p1, point p2, point p3) {
  double x_bc = std::round((std::get<0>(p1) + std::get<0>(p2) + std::get<0>(p3)) / 3 * 10000) / 10000;
  double y_bc = std::round((std::get<1>(p1) + std::get<1>(p2) + std::get<1>(p3)) / 3 * 10000) / 10000;
  return {x_bc, y_bc};
}
__________________________________
#include <utility>

#include <cmath>

using point = const std::pair<double, double>;
double r(double a)
{
  return std::round(a * 10000.0)/ 10000.0;
}
std::pair<double, double> barTriang(point p1, point p2, point p3) {
  //your code here
  return { r((p1.first + p2.first + p3.first ) / 3.0), r((p1.second + p2.second + p3.second) / 3.0)};
}
