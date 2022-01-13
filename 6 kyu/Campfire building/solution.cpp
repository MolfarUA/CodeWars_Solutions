#include <cmath>

long sqrtl(long x)
{
    return static_cast<long>(std::sqrt(x) + 1e-6);
}

bool is_perfect_square(long x)
{
    long t = sqrtl(x);
    return t * t == x;
}

bool is_constructable(long a)
{
    long m = sqrtl(a);
    for (long x = 0; x <= m; ++x) {
        if (is_perfect_square(a - x * x)) return true;
    }
    return false;
}
__________________________________
#include <cmath>

bool is_constructable(long a)
{
  long side = sqrt(a);
  for (long i = side; i >= 0; --i)
  {
    long temp = a - i * i;
    if (pow(long(sqrt(temp)), 2) == temp) return true;
  }
  return false;
}
__________________________________
bool is_constructable(long a)
{
    for(int i = 0; i*i <= a; i++){
        for(int j = i; j*j <= a; j++){
            if(i*i + j*j == a) return true;
        }
    }
    return false;
}
__________________________________
#include <cmath>
int rrenja(long num);

bool is_constructable(long a)
{
  for(int i = 0; i < sqrt(a); i++){

       long n = a - pow(i, 2);

       if(rrenja(n)){
           return true;
           break;
       }
    }
  
  return false;
}

int rrenja(long num){
    
    double a = sqrt(num);
    
    if(a == round(a)){
        return 1; 
    }
    else return 0; 
}
__________________________________
#include <math.h>
#include <functional>

bool is_constructable(long a){  
  if (a==1 || a== 2) return true;
  for(long i=1; 2*i <= a; i++){    
    std::function<bool(long)> isSquare = [](long x) {return (sqrt(double(x)) - floor(sqrt(double(x)))==0);};    
    if(i*i==a || isSquare(a-i*i)) return true;
  }
  return false;
}
