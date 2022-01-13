#include <stdbool.h>
#include <math.h>

bool is_square(int n) {

    // <---- hajime!
    
    int s = sqrt(n);
    return n == s * s;

}
__________________________________
#include <stdbool.h>
#include <math.h>

bool is_square(int n) 
{
    int num;
    if(n>=0)
    {
        num = sqrt(n);
        if((num*num)== n)
            return true;
        else
            return false;
            
    }
    else
      return false;
}
__________________________________
#include <stdbool.h>
#include <math.h>

bool is_square(int n) {
  if (n < 0){return false;}
  float c = sqrt(n);
  int b = c;
  if (b < c){
    return false;
  }
  else return true;
}
__________________________________
#include <math.h>

_Bool is_square(int n)
{
    double unused;
    return modf(sqrt(n), &unused) == 0;
}
__________________________________
#include <stdbool.h>
#include <math.h>

bool is_square(int n) {

  unsigned int a; // declaring a variable a.
  a = sqrt(n);  // variable a is the square root of n.
  
  if(a*a == n){      // checks if a^2 is equal to n or less. If it is equal, return true.
    return true;   
    }
  else {             // if a*a is not equal to n, returns false.
    return false;
    }
}
