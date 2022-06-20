559b8e46fa060b2c6a0000bf


using System.Numerics;

public class Diagonal 
{
    public static BigInteger diagonal(int n, int p)
    {
        return Binomial(n + 1, p + 1);
    }
    
    private static BigInteger Binomial(int n, int k)
    {
        if (k == 0) return 1;
        if (k > n / 2) return Binomial(n, n - k);
        return n * Binomial(n - 1, k - 1) / k;
    }
}
_____________________________
using System;
using System.Numerics;
using System.Collections.Generic;


public class Diagonal
    {
      public static BigInteger F(int a)
      {
        BigInteger Ret = 1;
        for (int i = 1; i <= a; i++)
        {
          Ret *= i;
        }
        return Ret;
      }
      public static BigInteger diagonal(int n, int p)
      {
        int k = 2;
        BigInteger Sum = 1;
        if (n > p)
        {
          BigInteger S = p + 1;
          Sum += S;
          for (BigInteger i = p + 2; i <= n; i++)
          {
            S = S * i / k++;
            Sum += S;
          }
        }
        return Sum;
      }
    }
_____________________________
using System;
using System.Numerics;

public class Diagonal 
{
        public static BigInteger diagonal(int n, int p)
        {
            BigInteger result = 1;
            BigInteger multiplier = n - p;
            BigInteger factorial = 1;

            for (int i = 0; i <= p; i++)
            {
                factorial *= i + 1;
                result *= multiplier + 1;
                multiplier++;
            }

            return result / factorial;
        }
}
