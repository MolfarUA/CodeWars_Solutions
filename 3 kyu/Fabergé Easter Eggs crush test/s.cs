54cb771c9b30e8b5250011d4


using System.Numerics;
public class Faberge
{
    public static BigInteger Height(int n, int m)
    {
      BigInteger c = m;
      BigInteger a = 0;
      for(int i=1; i<=n; i++)
      {
        c/=i;   a+=c;   m--;   c*=m;
      }
      return a;
    }
}
_________________________
using System.Numerics;

public class Faberge
{
    public static BigInteger Height(BigInteger n, BigInteger m)
    {
        BigInteger h = 0;
        BigInteger t = 1;
        for (var i = 1; i < n + 1; i++)
        {
            t = (t * (m - i + 1) + i - 1) / i;
            h += t;
        }
        return h;
    }
}
_________________________
using System;
using System.Numerics;

public class Faberge
{
    public static BigInteger Height(int n, int m)
    {
        /*return walk(new BigInteger(n), BigInteger.One, BigInteger.Zero);
        BigInteger walk(BigInteger x, BigInteger t, BigInteger h) {
          if (x == 0) return h;
          var e = (t * (m - n + x)) / (n + 1 - x);
          return walk(x - 1, e, h + e);
        }*/
        var x = new BigInteger(n);
        var t = BigInteger.One;
        var h = BigInteger.Zero;
        while (x != 0) {
          var e = (t * (m - n + x)) / (n + 1 - x);
          x--;
          t = e;
          h += e;
        }
        return h;
    }
}
_________________________
using System;
using System.Numerics;
using System.Collections.Generic;

public class Faberge
{
    public static BigInteger Height(int n, int m)
    {   
        if (m<=n){return BigInteger.Pow(2,m)-1;}
        if (n==0){return 0;}
        BigInteger total = 0;
        BigInteger toAdd = BigInteger.Pow(2,n);
        BigInteger adds = 1;
        for (int i=0; i<n; i++)
        {
          total+=toAdd;
          toAdd=(toAdd*(m-n+i))/(2*(i+1));
          adds=(adds*(m-n+i))/(i+1);
        }
        total+=(adds-1);     
        return total;
    }
}
_________________________
using System;
using System.Numerics;
using System.Collections.Generic;
using System.Linq;

public class Faberge
{
    public static BigInteger Height(int eggCount, int tryCount)
    {      
      return PascalRow(tryCount)
          .Take(eggCount + 1)
          .Aggregate(BigInteger.MinusOne, (x,y) => x + y);
    }
    
    private static IEnumerable<BigInteger> PascalRow(int rowNumber)
    {
      BigInteger value = 1;
      
      for (int i=0; i<=rowNumber; i++)
      {
        yield return value;
        value *= (rowNumber - i);
        value /= (1 + i);
      }
      
      while (true)
      {
        yield return 0;
      }
    }
}
_________________________
using System;
using System.Numerics;
public class Faberge
{
    public static BigInteger Height(int n, int m)
    {
        if (n == 0 || m == 0)
            {
                return 0;
            }
            var sum = new BigInteger(m);
            var coeff = new BigInteger(m);
            for (var i = 1; i < n; i++)
            {
                coeff = coeff*(m - i)/(i + 1);
                sum += coeff;
            }
            return sum;
    }
}
_________________________
using System.Numerics;
public class Faberge
{
    public static BigInteger Height(int n, int m)
    {
      BigInteger h = 0, sk = 1;   
      for(int i=1; i<=n; i++){
        sk=sk*m/i;
        h+=sk;
        m--;
      }
      return h;
    }
}
