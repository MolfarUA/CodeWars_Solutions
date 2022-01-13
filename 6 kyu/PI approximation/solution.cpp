#define M_PI 3.14159265358979323846  /* pi */

#include <cmath>
#include <iomanip>
#include <sstream>

using namespace std;

class PiApprox
{
    public: 
       static string iterPi(double epsilon){
         int denominator = 1, counter = 0;
         double currPi = 0;
         
         ostringstream stream;
         
         while(true){
           if(fabs(currPi * 4 - M_PI) < epsilon){
             break;
           }
     
           currPi = currPi + 1.0/denominator;
           
           denominator = (denominator > 0) ? 0 - denominator - 2 : 0 - denominator + 2;
           
           counter++;
         }
         
         stream << "[" << counter << ", " << fixed << setprecision(10) << currPi * 4 << "]";
         
         return stream.str();
       }
};
________________________________________
#define M_PI 3.14159265358979323846  /* pi */

using namespace std;
class PiApprox
{
    public: static string iterPi(double epsilon){
      char res [20];
      double pi = 4.0;
      int count = 1;
      double n = 3;
      
      while(pi - M_PI > epsilon || M_PI - pi > epsilon){
        double k = n;
        if(count % 2 != 0)
          k = (-1) * k;
        pi += 4 / k;
        n += 2;
        count += 1;
      }
      sprintf(res, "[%d, %11.10f]", count, pi);
      return res;
    };
};
________________________________________
#include <sstream>
#include <cmath>
#include <iomanip>
#define M_PI 3.14159265358979323846  /* pi */
using namespace std;
class PiApprox
{
    public: static string iterPi(double epsilon);
};

string PiApprox::iterPi(double epsilon) {
  double n = 1;
  double sum = 0;
  int sign = 1;
  int i = 0;
  while (abs(4 * sum - M_PI) >= epsilon) {
    sum += sign / n;
    n += 2;
    sign = -sign;
    i++;
  }
  sum *= 4;
  
  stringstream ss;
  ss << setprecision(11) << sum;
  string str;
  ss >> str;
  
  return "[" + to_string(i) + ", " + str + "]";
}
________________________________________
#define M_PI 3.14159265358979323846  /* pi */
using namespace std;

#include <sstream>
#include <iomanip>

class PiApprox
{
  
    public:
  
    static inline double own_abs(double x) { return x < 0 ? -x : x; }
  
    static string iterPi(double epsilon) {
      
      double pi_val = 0.0, mul = 4.0, denom = 1.0;
      int iter = 0;
      
      do {
          pi_val += mul / denom;
          mul = -mul;
          denom += 2.0;
          ++iter;
      } while (own_abs(pi_val - M_PI) >= epsilon);

      std::ostringstream strm;
      strm << "[" << iter << ", " << std::setprecision(11) << pi_val << "]";
        
      return strm.str();
    }
};
