559b8e46fa060b2c6a0000bf
  
  
class Diagonal {
public:
    using ull = unsigned long long;
    static ull diagonal(int n, int p) {
      ull steps = n + 1 - p, 
        k = 1, 
        i = 1, 
        sum = 0;
      
      while (steps--) {
        sum += k;
        k = k * ++p / i++;
      }
      
      return sum;
    }
};
_____________________________
#include <numeric>

typedef unsigned long long ull;
class Diagonal
{
public:
    static ull diagonal(int n, int p);
    
private:
    static ull comb(int n, int p);
    static void reduce(ull& x, ull& y);
};


ull Diagonal::diagonal(int n, int p)
{
    return comb(n + 1, p + 1);
}

ull Diagonal::comb(int n, int p)
{
    p = std::min(p, n - p);
    
    ull a = 1, b = 1;
    for (int i = 0; i < p; ++i) {
        a *= n - i;
        b *= i + 1;
        reduce(a, b);
    }
    
    return a / b;
}

void Diagonal::reduce(ull& x, ull& y)
{
    ull g = std::gcd(x, y);
    x /= g;
    y /= g;
}
_____________________________
#include <numeric>

typedef unsigned long long ull;
class Diagonal
{
public:
    static ull diagonal(int n, int p);
};


ull Diagonal::diagonal(int n, int p)
{
    ++n;
    ++p;    
    p = std::min(p, n - p);
    
    ull a = 1, b = 1;
    for (int i = 0; i < p; ++i) {
        a *= n - i;
        b *= i + 1;
        
        ull g = std::gcd(a, b);
        a /= g;
        b /= g;
    }
    
    return a / b;
}
