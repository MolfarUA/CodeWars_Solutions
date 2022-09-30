55b2549a781b5336c0000103


#include <math.h>

int compare_powers(const int n1[2], const int n2[2]) {
  double d = log(n2[0]) * n2[1] - log(n1[0]) * n1[1];
  return (d > 0) - (d < 0);
}
________________________________
#include <math.h>
int compare_powers(const int n1[2], const int n2[2]) {
  double l1 = n1[1]*log(n1[0]), l2 = n2[1]*log(n2[0]);
  return (l2>l1)-(l1>l2);
}
________________________________
int compare_powers(const int n1[2], const int n2[2]) {
 return (log2(n1[0])*n1[1] == log2(n2[0])*n2[1])? 0: (log2(n1[0])*n1[1] > log2(n2[0])*n2[1])? -1: 1;
}
________________________________
#include <math.h>

int compare_powers(const int n1[2], const int n2[2]) {
  float a = log(n1[0]) * n1[1], b = log(n2[0]) * n2[1];
  return a > b ? -1 : (a != b);
}
