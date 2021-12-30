int digital_root(int Z) {
    return --Z % 9 + 1;
}

________________________________
int digital_sum(int n)
{
  int sum = 0;
  while (n > 0)
  {
    sum += n % 10;
    n /= 10;
  }
  
  return sum;
}

int digital_root(int n)
{
  while (n >= 10)
    n = digital_sum(n);  
  return n;
}

________________________________
int digital_root(int n)
{
  return (n-1) % 9 +1;
}

________________________________
int digital_root(int n)
{
  int digitRoot = 0;
  while(n)
  {
    digitRoot += n%10;
    n = n/10;
  }
  
  return (digitRoot > 9) ? digital_root(digitRoot) : digitRoot;
}

________________________________
int digital_root(int n)
{
  if(n < 10) 
    return n;
  return digital_root(n % 10 + digital_root(n / 10));
}

________________________________
#include <numeric>                                          //^^
int digital_root(int n){
  if (n / 10 == 0)
    return n % 10;
  std::string s = std::to_string(n);
  return digital_root(accumulate(s.begin(), s.end(), 0, [](auto a, auto b) {return a + (b-'0');}));
}
