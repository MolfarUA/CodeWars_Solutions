57aa218e72292d98d500240f


#include <math.h>

float heron(int a, int b, int c) {
  float s = (a+b+c)/2.;
  return sqrt((s * (s - a) * (s - b) * (s - c)));

}
________________________
#include <math.h>

float heron(int a, int b, int c) {
    double s = (a + b + c) / 2.0;
    return sqrt(s * (s - a) * (s - b) * (s - c));
}
________________________
#include <math.h>
float heron(int a, int b, int c) {float s= (float)(a+b+c)/2.0;
return sqrt(s*(s-a)*(s-b)*(s-c));}
