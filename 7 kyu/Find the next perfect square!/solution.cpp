#include <cmath>    
long int findNextSquare(long int sq) {
  if(sqrt(sq) != (int)sqrt(sq)){return -1;}
  return  pow(sqrt(sq) + 1,2);
}

_______________________________________
#include <cmath>

long int findNextSquare(long int sq) {
  auto sqrt = std::sqrt(sq);

  return std::modf(sqrt, &sqrt) == 0 ? std::pow(sqrt + 1, 2) : -1;
}

_______________________________________
#include <cmath>
using namespace std; 

long int findNextSquare(long int sq) 
{
 if (sqrt(sq) == floor(sqrt(sq))) return pow(sqrt(sq)+1,2);  return -1 ;
}

_______________________________________
#include <math.h>
long int findNextSquare(long int sq) {
  long int a,n,i;
  i=sqrt(sq);
  for(a = i; a <= sq; a++)
    {
        if (a*a > sq) return-1;
        if (sq == a * a)
        {
         a++;
         return a=a*a;    
        }
    }
}

_______________________________________
#include <cmath>

long int findNextSquare(long int sq) {
    // Return the next square if sq if a perfect square, -1 otherwise
    double sq_root = sqrt(sq);
      if (ceil(sq_root) != floor(sq_root))
        return -1;
    else
        return (sq_root + 1) * (sq_root + 1);
}

_______________________________________
#include <cmath>

long int findNextSquare(long int sq) {
  double base = sqrt(sq);
  if (floor(base) - base != 0)
  {
    return -1;
  }
  return round(pow(base + 1, 2));
}
