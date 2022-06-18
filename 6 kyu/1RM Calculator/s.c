595bbea8a930ac0b91000130

#include <math.h>

int calculate_1RM(int w, int r) {

    if(r == 0) return 0;
    if(r == 1) return w;
    
    double Epley       = w * (1 + (r / 30.0));
    double McGlothin   = (100.0 * w) / (101.3 - (2.67123 * r));
    double Lombardi    = w * pow(r, 0.10);
    
    double calculation = Epley;
    
    if(McGlothin > Epley) {
        calculation = McGlothin;
    }
    if(Lombardi > calculation) {
        calculation = Lombardi;
    }
    return (int)round(calculation);
}
_______________________________
#include <math.h>

int calculate_1RM(int w, int r) {
  if(r<=1) return r*w;
  float e = (float)w + r*w/30.0;
  float m = 100*w / (101.3-2.67123*r);
  float l = w * pow(r, 0.1);
  int rm =(e>=m)?(int)(e+0.5):(int)(m+0.5);
  rm = (l>rm)?(int)(l+0.5):rm;
  return rm;
}
_______________________________
#include <math.h>

double max(double a, double b) {
  return a > b ? a : b;
}

int calculate_1RM(int w, int r) {
  if (r == 0) return 0;
  if (r == 1) return w;
  return round(max(w * (1 + r / 30.0), max(100.0 * w / (101.3 - 2.67123 * r), w * pow(r, 0.1))));
}
_______________________________
#include <math.h>

int calculate_1RM(int w, int r) {
double rm[3] = {w * (1. + r/30.), (100. * w) / (101.3 - 2.67123 * r), w * pow(r, 0.10)}, m = rm[0] > rm[1] ? rm[0] : rm[1];
return (r ? r == 1 ? w : round(m > rm[2] ? m : rm[2]) : 0);
}
_______________________________
#include <math.h>

#define MAX(a, b) (a > b ? a : b)
#define MAX3(a, b, c) MAX(a, MAX(b, c))

double epley(int w, int r) { return w * (1.0 + (r / 30.0)); }
double mcglothin(int w, int r) { return (100.0 * w) / (101.3 - 2.67123 * r); }
double lombardi(int w, int r) { return w * pow(r, 0.1); }

int calculate_1RM(int w, int r) {
  return r == 0   ? 0
         : r == 1 ? w
                  : round(MAX3(epley(w, r), mcglothin(w, r), lombardi(w, r)));
}
