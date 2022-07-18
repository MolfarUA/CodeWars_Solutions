56484848ba95170a8000004d


int gps(int s, double* x, int sz) {
  double max = 0.;
  
  for (int i = 1; i < sz; i++) {
    double temp = x [i] - x[i - 1];
    if (temp > max) max = temp;
  }
  return (s > 0) ? (max * 3600.) / (double) s : 0;
}
_____________________________
#include <math.h>

int hourlySpeed(double delta_distance, int s) {
  return (3600 * delta_distance) / s;
}

int gps(int s, double* x, int sz) {
  int maxAvarageSpeed = 0, avarageSpeed = 0;
  
  for (int i = 0; i < (sz - 1); i++) {
    avarageSpeed = hourlySpeed(fabs(x[i] - x[i + 1]), s);
    if (avarageSpeed > maxAvarageSpeed)
      maxAvarageSpeed = avarageSpeed;
  }
  
  return maxAvarageSpeed;
}
_____________________________
int gps(int s, double* x, int sz) {
  int max = 0;  
  for(int i = 1; i < sz; ++i) if(3600*(x[i]-x[i-1])/s > max) max = 3600*(x[i]-x[i-1])/s;
  return max;
}
