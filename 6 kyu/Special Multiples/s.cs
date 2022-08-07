55e785dfcb59864f200000d9


using System;
using System.Linq;
public class CountMultiples 
{
//An unnessarily complex prime generator - nice for use with Linq though
private static System.Collections.Generic.IEnumerable<long> genPrimes()
        {
            System.Func<long, bool> isPrime = (num) => {
                for (long i = 3; i < System.Math.Sqrt(num) + 1; i += 2)
                    if (num % i == 0)
                        return false;
                return true;
            };
            yield return 2;
            for (long i = 3; i < long.MaxValue; i += 2)
                if (isPrime(i))
                    yield return i;
        }

    public static long CountSpecMult(long n, long mxval) 
    {
        //Get the first n primes as an array
        var primes = genPrimes().Take((int)n).ToArray();
        //multiply them together into a single divisor
        var primeProd = primes.Aggregate((x, y) => { return x * y; });
        return mxval / primeProd;
    }
}
_________________________________
using System.Collections.Generic;
using System.Linq;

public class CountMultiples 
{
    public static long CountSpecMult(long n, long mxval) 
    {  
        return mxval / GetPrimes(n).Aggregate((acc, val) => acc * val);
    }
    
    public static List<long> GetPrimes(long n)
    {
       List<long> result = new List<long>();
       
       long current = 2;
       while(result.Count() < n){
         if(!result.Any(r => current % r == 0))
           result.Add(current);
         
         current++;
       }
       
       return result;
    }
    
}
_________________________________
using System.Linq;

public class CountMultiples
{
  public static long CountSpecMult(long n, long mxval)
  {
    return (long) (mxval / new double[] {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}.Take((int) n).Aggregate(1d, (x, y) => x * y));
  }
}
