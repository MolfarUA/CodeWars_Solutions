54d7660d2daf68c619000d95

using namespace std;
#include <numeric>
#include<math.h>
class Fracts
{

public:
   static unsigned long long LCM(unsigned long long n1,unsigned long long n2)
   {
//      int m=max(n1,n2);
//      if(m%n1==0&&m%n2==0)return m;
//      while(!(m%n1==0&&m%n2==0))m++;
     unsigned long long m=(n1*n2)/gcd(n1,n2);
     return m;
     
   }
    
    static string convertFrac(vector<vector<unsigned long long>> &lst)
    {
      unsigned long long lcm=1;
      for(int i=0;i<lst.size();i++)
      {
        lcm=LCM(lcm,lst[i][1]);
      }
      //vector<vector<unsigned long long>> res;
      string res="";
      for(int i=0;i<lst.size();i++)
      {
        unsigned long long n=(lcm/(lst[i][1]))*lst[i][0];
        res+="("+to_string(n)+","+to_string(lcm)+")";
        
      }
      return res;

      
      
    }
};

##################################
#include <string>
#include <iostream>

typedef unsigned long long ull;

class Fracts
{
public:
  static ull GCD(ull a, ull b) {
    ull gcd;
    ull rem;
    
    ull high, low;
    if (a > b) {
      high = a;
      low = b;
    } else {
      high = b;
      low = a;
    }
    rem = low;
    
    do {
      gcd = rem;
      rem = high % low;
      high = low;
      low = rem;
    } while (rem != 0);
    
    std::cout << "A | B -> GCD" << std::endl
      << a << " | " << b << " -> " << gcd
      << std::endl;
    return gcd;
  };
  
  static ull LCM(ull a, ull b) {
    // Abs
    if (a < 0) {a *= -1;};
    if (b < 0) {b *= -1;};
      
    // Handle trivial case
    if (a == b) {
      return 1;
    }
    
    return a * b / Fracts::GCD(a, b);
  };
  
  static std::string convertFrac(std::vector<std::vector<ull>> &lst) {
    ull D = 1;
    std::string res;

    // Iterate denominators to find common Denominator
    for (auto itr = lst.begin(); itr != lst.end(); itr++) {
      ull curr_d = (*itr)[1];
      D = Fracts::LCM(D, curr_d);
    }

    // Build up result string
    auto D_str = std::to_string(D);
    auto stringify_N = [=](ull N) -> std::string {
      return "(" + std::to_string(N) + "," + D_str + ")";
    };

    for (auto itr = lst.begin(); itr != lst.end(); itr++) {
      ull multiplicand = D / (*itr)[1];
      res += stringify_N((*itr)[0] * multiplicand);
    }

    return res;
  };
};

###################################
#include "iostream"
class Fracts {
private:
    static unsigned long long gcd(unsigned long long a, unsigned long long b) {
        while (b != 0) {
            unsigned long long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    static unsigned long long  lcm(unsigned long long a, unsigned long long b) {
        return (a * b) / gcd(a, b);
    }
public:
    static std::string convertFrac(std::vector<std::vector<unsigned long long>> &lst) {
      for (unsigned long long i = 0; i < lst.size(); i++) {
          unsigned long long gcd_tmp = gcd(lst[i][0], lst[i][1]);
          if (gcd_tmp != 1) {
              lst[i][0] /= gcd_tmp;
              lst[i][1] /= gcd_tmp;
          }
      }
      unsigned long long lcm_tmp = lcm(lst[0][1], lst[1][1]);
      for (unsigned long long i = 1; i < lst.size(); i++) {
          lcm_tmp = lcm(lcm_tmp, lst[i][1]);
      }
      std::string result = "";
      for (unsigned long long i = 0; i < lst.size(); i++) {

          result += "(" + std::to_string(lst[i][0] * (lcm_tmp / lst[i][1])) + "," + std::to_string(lcm_tmp) + ")";
      }
      return result;
    }
};
