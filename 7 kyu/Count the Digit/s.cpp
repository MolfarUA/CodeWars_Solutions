566fc12495810954b1000030
  
  
class CountDig
{
public:
    static int nbDig(int n, int d);
};

int CountDig::nbDig(int n, int d) { 
  int count = 0;
  for (int k = 0; k <= n; ++k) {
    int m = k*k;
    do {
      if ((m % 10) == d) count += 1;
      m /= 10;
    } while(m);
  }
  return count;
}
____________________________
namespace CountDig
{
  int nbDig(int n, int d)
  {
    std::string digits;
    for (int k = 0; k <= n; ++k)
      digits += std::to_string(k * k);
  
    return std::count(digits.begin(), digits.end(), std::to_string(d)[0]);
  }
}
____________________________
class CountDig
{
public:
    static int nbDig(int n, int d)
    {
      std::string ret;
      do
        ret += std::to_string(n * n);
      while (n-- > 0);
      return count(ret.cbegin(), ret.cend(), d + '0');
    }
};
