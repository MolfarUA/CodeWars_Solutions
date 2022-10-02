5547cc7dcad755e480000004
  
  
#include <vector>

using namespace std;

class RemovedNumbers
{
public:
  static vector<vector<long long>> removNb(long long n);
};

vector<vector<long long> > RemovedNumbers::removNb(long long n)
{
    vector<vector<long long> >  result;
    
    long long  total = (n + 1) * n / 2;
    
    for( long long a = n/2; a <= n; ++a )
    {
         long long  b = (total - a) / (a + 1);
         
         if( total == (a * b + a + b) )
         {
             vector<long long>  one_pair;
            
             one_pair.push_back( a );
             one_pair.push_back( b );
            
             result.push_back( one_pair );
         }
        
    }
    
    return result;
}
______________________________
#include <vector>

class RemovedNumbers
{
public:
  static std::vector<std::vector<long long>> removNb(long long n)
  {
    std::vector<std::vector<long long>> retVec;
    long long sum = (n*n+n)/2;
    for(long long i=n/2; i<=n; i++)
      if((sum-i)%(1+i)==0){
        retVec.push_back(*new std::vector<long long>{i, (sum-i)/(1+i)});
      }
    return retVec;
  }
};
______________________________
#include <vector>

using namespace std;

class RemovedNumbers
{
public:
  static vector<vector<long long>> removNb(long long n);
};

vector<vector<long long>> RemovedNumbers::removNb(long long n)
{
  long long s = static_cast<long long>(n * (n + 1) / 2.0);
  vector<vector<long long>> res;
  long long i = static_cast<long long>(n / 2);
  while (i <= n)
  {
    long long b = static_cast<long long>(s - i);
    if (b % (i + 1) == 0)
    {
      vector<long long> c = {i, static_cast<long long>(b / (i + 1))};
      res.push_back(c);
    }
    i += 1;
  }
  return res;
}
