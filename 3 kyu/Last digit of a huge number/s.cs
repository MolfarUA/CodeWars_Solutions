namespace Solution
{
    using System;
    using System.Linq;

    public class Calculator
    {
        public static int LastDigit(int[] array)
        {
            if (array.Length == 0)
            {
                return 1;
            }

            int number = array.Last();
            
            foreach (int i in array.Reverse().Skip(1))
            {
                int power = number;

                switch (power)
                {
                    case 0:
                        number = 1;
                        break;
                    case 1:
                        number = i;
                        break;
                    case 2:
                        number = i * i;
                        break;
                    default:
                        power = (power - 3) % 4 + 3;
                        int n = i < 3 ? i : (i - 3) % 20 + 3;
                        number = (int)Math.Pow(n, power);
                        break;
                }
            }

            return number % 10;
        }
    }
}
_____________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
namespace Solution 
{
  public class Calculator 
  {
    public static int LastDigit(int[] array) 
    {
      BigInteger t = 1;
      var arr = array.Reverse().ToList();

      foreach(var x in arr)
      {
        if(t < 4)
          t = BigInteger.Pow(x,int.Parse(t.ToString()));
        else
        {
          int exponent = int.Parse(BigInteger.ModPow(t,1,4).ToString()) + 4;
          t = BigInteger.Pow(x,exponent);
        }
      }
      
      return (int)BigInteger.ModPow(t,1,10);
    }
  }
}
_______________________
namespace Solution
{
  using System;
  using System.Linq;
  
  public class Calculator
  {
    public static int LastDigit(int[] a) => Enumerable.Range(0, a.Length).Reverse().Aggregate(1, (p, i) => (int)Math.Pow(i == 0 ? a[i] % 10 : a[i] < 4 ? a[i] : a[i] % 4 + 4, p < 4 ? p : p % 4 + 4)) % 10;
  }
}
______________________
namespace Solution{
  using System;
  public class Calculator {
    public static long LastDigit(int[] a) {
      long b=1;
      for(int i=a.Length; --i>=0;)
        b=(long) Math.Pow(a[i]>9?a[i]%20+20:a[i], b<4?b:(b%4+4));
      return b%10;
    }
  }
}
