55f9bca8ecaa9eac7100004a


int past(int h, int m, int s) {
    return h * 3600000 + m * 60000 + s * 1000;
}
__________________________
int past(int h, int m, int s) {

  return(3600 * h + 60 * m + s) * 1000;
}
__________________________
int past(int h, int m, int s) {
  int result = 0;

   if (h != 0 || m!= 0 || s!= 0){
     return h*3600000 + m*60*1000 + s*1000;
     
   } 
  else{
    return result;//  <----  hajime!

}
  }
__________________________
#include <stdio.h>
int past(int h, int m, int s) {
  return ((h * 3600000) + (m * 60000) + (s * 1000));
}
__________________________
#include <math.h>
int past(int h, int m, int s) {
    
  0 <= h <= 23;
  0 <= m <= 59;
  0 <= s <= 59;
  return 3.6 * pow(10, 6) * h + 60000 * m + 1000 * s;
 

}
__________________________
int past(int h, int m, int s) 
{
  int res;
  h = h*3600000;
  m = m*60000;
  s = s*1000;
  
  res = h+m+s;
  
  return (res);
  //1s = 1 000ms
  //1m = 60 000ms
  //1h = 3 600 000ms
}
__________________________
int past(int h, int m, int s) 
{
  int hConversion = h * 60 * 60 * 1000;
  int mConversion = m * 60 * 1000;
  int sConversion = s * 1000;
  
  int result = hConversion + mConversion + sConversion;
  
  return result;
}
