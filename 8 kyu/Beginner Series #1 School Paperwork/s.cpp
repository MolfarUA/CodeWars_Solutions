55f9b48403f6b87a7c0000bd
  
  
int paperwork(int n, int m) {
  return n < 0 || m < 0 ? 0 : n * m;
}
__________________________
int paperwork(int n, int m){
  if(n<1||m<1)
    return 0;
  else return n*m;
}
__________________________
#include <algorithm>

int paperwork(int n, int m){
    return std::max(n, 0) * std::max(m, 0);
}
__________________________
auto paperwork(const int n, const int m) -> int
{
  return n > 0 and m > 0 ? n * m : 0;
}
__________________________
using namespace std;

int paperwork(const int& n,const int& m) {
  return (n > 0 && m > 0) ? m * n : 0;
}
__________________________
int paperwork(int n, int m){
    
  if(m<0 or n<0)
  {
   return 0; 
  }
  else
  {
    return n*m;
  }
}
