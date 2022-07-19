561e9c843a2ef5a40c0000a4


using System;
class GapInPrimes 
{
    public static bool IsP(long n){
        if (n%2==0) return false;
        for (long i=3;i<=Math.Sqrt(n);i+=2) if (n%i==0) return false;
        return true;
    }
    public static long[] Gap(int g, long m, long n) 
    {
        long p=0;
        for (;m<=n;m++){
          if (IsP(m)){
            if (m-p==g) return new long[]{p,m};
            p=m;
          }
        }
        return null;
    }        
}
__________________________________
using System;
using System.Collections.Generic;

class GapInPrimes 
{
    private static bool IsPrimeNumber(long number)
    {
      int sqrtNumber = (int)(Math.Sqrt(number));
      for (int i = 2; i <= sqrtNumber; i++)
      {
        if (number % i == 0)
          return false;
      }
      return true;
    }
  
    public static long[] Gap(int g, long m, long n)
    {
      var primeNumbers = new List<long>();
      for (long i = m; i <= n; i++)
      {
        if (IsPrimeNumber(i))
        {
          primeNumbers.Add(i);
        }
      }
      for (long i = 0; i <= primeNumbers.Count-2; i++)
      {
        if (primeNumbers[(int)i] + g == primeNumbers[(int)i + 1])
          return new long[] { primeNumbers[(int)i], primeNumbers[(int)i + 1] };       
      }
      return null;
    }
 
}
__________________________________
using System;

public class GapInPrimes
{
    public static long[] Gap(int g, long m, long n)
    {
        long first = 0;
        long second = 0;
        for (long i = m; i <= n; i++)
        {
            if (IsPrime(i))
            {
                if (first == 0)
                {
                    first = i;
                }
                else
                {
                    second = i;
                    if (second - first == g)
                    {
                        break;
                    }

                    (first, second) = (second, 0);
                }
            }
        }

        return second == 0 ? null : new[] {first, second};
    }

    public static bool IsPrime(long number)
    {
        if (number <= 1) return false;
        if (number == 2) return true;
        if (number % 2 == 0) return false;

        var boundary = (long) Math.Floor(Math.Sqrt(number));

        for (long i = 3; i <= boundary; i += 2)
            if (number % i == 0)
                return false;

        return true;
    }
}
