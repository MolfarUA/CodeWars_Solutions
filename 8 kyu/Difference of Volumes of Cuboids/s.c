58cb43f4256836ed95000f97



#include <stdlib.h>

int find_difference(const int a[3], const int b[3]) {
    return abs(a[0]*a[1]*a[2]-b[0]*b[1]*b[2]); 
}
________________________
int cube(const int x[3])
{
  return x[0] * x[1] * x[2];
}

int find_difference(const int a[3], const int b[3]) 
{
  return abs(cube(a) - cube(b));  
}
________________________
int find_difference(const int a[3], const int b[3]) {
     
  float volume1 = (a[0]*a[1]*a[2]);
  float volume2 = (b[0]*b[1]*b[2]);
  return (volume2>volume1) ? volume2 - volume1 : volume1 - volume2;
   
}
