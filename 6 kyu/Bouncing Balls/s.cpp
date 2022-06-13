#include <cmath>

using namespace std;
class Bouncingball
{
public:
    static int bouncingBall(double h, double bounce, double window) {
        if (h <= 0 || bounce <= 0 || bounce >= 1 || window >= h) return -1;
        return (int)floor(log(window / h) / log(bounce)) * 2 + 1;
    }
};
_______________________________________________
using namespace std;
class Bouncingball
{
public:
    static int bouncingBall(double h, double bounce, double window)
    {
        if (h <= 0 || bounce <= 0 || bounce >=1 || window >= h) return -1;
        int count = 1;
        while (true){
            h *= bounce;
            if (h <= window) break;
            count += 2;
        }
        return count;
    }
};
_______________________________________________
using namespace std;

class Bouncingball
{
public:
    static int bouncingBall(double h, double bounce, double window);
};

int Bouncingball::bouncingBall(double h, double bounce, double window)
{
    if ((h <= 0) || (window >= h) || (bounce <= 0) || (bounce >= 1))
        return -1;
    int seen = -1;
    while (h > window)
    {
        seen += 2;
        h = h * bounce;
    }
    return seen;
}
_______________________________________________
using namespace std;
class Bouncingball
{
public:
    static int bouncingBall(double h, double bounce, double window);
};

int Bouncingball::bouncingBall(double h, double bounce, double window) {

  int result = -1;
  if(h <= 0 || bounce <= 0 || bounce >= 1 || window >= h) {
    return result;
  }else {
    result = 0;
    do {
      h = h*bounce;
      result+=2; // mom sees the ball always twice (2n - 1)
      std::cout << h << endl;
    }while(h > window); // must be strictly greater 
    
    result -= 1; // remove the last rebound 
  }
  return result;
  
}
_______________________________________________
using namespace std;
class Bouncingball
{
public:
    static int bouncingBall(double h, double bounce, double window)
    {
      if ( h <= 0 || bounce <= 0 || bounce >= 1 || window >= h )
        return -1;
      int number = 0;
      while( h > window )
      {
        h *= bounce;
        number += ( h <= window ) ? 1 : 2;
      }
      return number;  
    }
};

