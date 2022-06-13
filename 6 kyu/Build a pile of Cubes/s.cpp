class ASum
{
  public:
  static long long findNb(long long m)
  {
      long long i = 1;
      long long sum = 0;
      do {
          sum += i * i * i;
          if (m == sum) return i;
          i++;
      } while (sum < m);
      return -1;
  }
};
_________________________________________
class ASum {
public:
    static long long findNb(long long m) {
        long long n = 1;
        while ((m -= n * n * n++) > 0);
        return m == 0 ? --n : -1;
    }
};
_________________________________________
class ASum
{
  public:
  static long long findNb(long long m);
};

long long ASum::findNb(long long m){
  long long V=1;
  long long i=1;
  while(V<m){
    i++;
    V=V+(i*i*i);
  }
  std::cout<< V-m;
  if (V==m) {return i;}
  return -1;
};
_________________________________________
class ASum
{
  public:
  static long long findNb(long long m)
  {
    long long n = 0, mCalc = 0;

    while (mCalc < m)
      mCalc += ++n*n*n;
    
    if (mCalc == m)
      return n;
    else
      return -1;
  }
};
