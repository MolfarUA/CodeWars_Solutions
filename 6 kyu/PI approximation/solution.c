#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define M_PI 3.14159265358979323846

char* iterPi(double epsilon) {
    // your code
  static char ans[200];
  double aprox = 4.;
  double aux;
  int iteration = 1;
  int n = 1;
  while (fabs(aprox-M_PI) >= epsilon){
    n *= -1;
    aux = (double)(2*iteration + 1);
    aprox += (4*n / aux);
    iteration++;
  } 
  sprintf(ans, "[%d, %.10f]", iteration, aprox);
  return ans;
}
________________________________________
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define M_PI 3.14159265358979323846

char *iterPi(double epsilon)
{
    double sum = 0;
    char *result = (char *) malloc((sizeof(double) + sizeof(double) + 5) * sizeof(char));
    int sign = 1;
    double i = 1;

    for ( i = 0; fabs(M_PI - sum*4) >= epsilon; i++)
    {
        sum += sign * 1.0 / (i*2+1);
        sign = -sign;
    }

    sprintf(result, "[%.0f, %.10lf]", i, sum*4);
    
    result = (char *) realloc(result, strlen(result)+1);

    return result;
}
________________________________________
#define M_PI 3.14159265358979323846
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

char* iterPi(double epsilon) {
  char* ret = calloc(100, sizeof(char));
  double pi = 0;
  int denominator = 1;
  bool state = true;
  int iters = 0;
  while(fabs(pi*4 - M_PI) > epsilon) {
    if(state) pi += ((double)1)/denominator;
    else pi -= ((double)1)/denominator;
    state = !state;
    denominator += 2;
    iters++;
  }
  sprintf(ret, "[%d, %.10f]", iters, pi * 4);
  return ret;
}
________________________________________
#define _GNU_SOURCE
#include <stdio.h>
#include <math.h>

const double Pi = 3.14159265358979323846;

char *iterPi (double epsilon)
{
  double approx_pi = 0;
  long long i = 0;
  long long sign = +1, denominator = 1;

  for (; fabs(Pi - 4.0 * approx_pi) > epsilon; i++) {
    approx_pi += sign * (1.0 / denominator);
    sign = -sign;
    denominator += 2;
  }

  char *result;

  asprintf(&result, "[%llu, %.10f]", i, 4.0 * approx_pi);
  return result;
}
________________________________________
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define M_PI 3.14159265358979323846

char* iterPi(double epsilon) {
    double pi = 4;
    int iterNr = 1;
    
    for(
      double sign = -4, i = 3;
      fabs(pi - M_PI) > epsilon; 
      i += 2, iterNr += 1, sign *= -1)
        pi += sign / i;
  
    char * fmt = malloc(log10(iterNr) + 18);
    sprintf(fmt, "[%d, %1.10f]", iterNr, pi); 
    return fmt;
}
