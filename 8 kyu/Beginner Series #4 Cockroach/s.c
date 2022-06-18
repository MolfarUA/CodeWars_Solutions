55fab1ffda3e2e44f00000c6


int cockroach_speed(double s)
{
    return s / 0.036;
}
__________________________
#include<math.h>
int cockroach_speed(double s)
{ int p= ( s * 27.77777778);
  if( s == 0)  
    return 0; 
  else 
    return  round (p);
}
__________________________
#include <math.h>
int cockroach_speed(double s)
{
    return (s >= 0 ? (floor(s * 100000) / 3600) : 0);
}
__________________________
int cockroach_speed(double s)
{
    return s*27.77778;
}
__________________________
int cockroach_speed(double s)
{
    return s * 1000 / 36;
}
__________________________
#include <math.h>
int cockroach_speed(double s)
{
  int y = floor(s * 250 / 9);
  return y;
}
