539a0e4d85e3425cb0000a88
  
  
class Yoba
{
public:
   Yoba(int n) : _n(n) {}
   Yoba operator() (int n) { return Yoba(_n + n); }
   bool operator== (int n) { return _n == n; }
   int operator+ (int n) { return _n + n; }
   int operator- (int n) { return _n - n; }
   friend bool operator== (int n, const Yoba & y) { return n == y._n; }
   
private:
   int _n;
};

auto add(int n)
{
   return Yoba(n);
}
______________________
class add
{
public:
    add (int x) : _x( x ) { }
    operator int() { return _x; }
    add operator() (int y) { return add(_x + y); }
    friend bool operator==(const int& a, const add& b) { return a == b._x; }

private:
    int _x;
};
______________________
#include <iosfwd>

class add {
  int sum;
public:
  add(int n) : sum(n) { }
  add(const add& adder) = default;
  add& operator=(const add& adder) = default;
  add operator()(int n) const { return add(sum + n); }
  operator int() const { return sum; }
  friend std::ostream& operator<<(std::ostream& os, const add& adder) { return os << adder.sum; }
};

