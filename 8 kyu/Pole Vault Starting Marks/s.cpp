5786f8404c4709148f0006bf
  
  
#include <math.h>
double startingMark(double bodyHeight)
{
   //assuming linear relationship between body height and starting mark
   double a = (10.67 - 9.45) / (1.83 - 1.52); 
   double b = 10.67 - a * 1.83;
   return round(100 * (bodyHeight * a + b)) / 100;
}
____________________________________
#include <math.h>
double startingMark(double b){ return round((3.935483870967741 * b + 9.45 - 3.935483870967741 * 1.52) * 100) / 100;}
____________________________________
#include <cmath>

double startingMark(double h) {
    double r = 122/31.0 * (h - 1.83) + 10.67;
    return floor( r * 100.00 + 0.5 ) / 100.00;
}
