using System;
using System.Collections.Generic;
using System.Linq;
public class SumDigPower {
    
    public static long[] SumDigPow(long a, long b) 
    {
        List<long> values = new List<long>();
        for (long x = a; x <= b; x++)
        {
          if (x.ToString().Select((c, i) => Math.Pow(Char.GetNumericValue(c), i + 1)).Sum() == x)
            values.Add(x);
        }
        return values.ToArray();
    }
}
_____________________________________________
using System;
using System.Collections.Generic;
public class SumDigPower {
    
    public static long[] SumDigPow(long a, long b)
      {
        if (b < a)
          return new long[0];
        List<long> result = new List<long>();
        for (long i = a; i <= b; i++)
        {
          if (IsEureka(i))
            result.Add(i);
        }
        return result.ToArray();
      }

      public static bool IsEureka(long num)
      {
        int digitCount = 0;
        long i = num;
        while (i > 0)
        {
          digitCount++;
          i /= 10;
        }
        if (digitCount == 1)
          return true;
        long sum = 0;
        i = num;
        while (i > 0)
        {
          sum += (long)Math.Pow(i % 10, digitCount--);
          if (sum > num)
            return false;
          i /= 10;
        }
        return sum == num;
      }
}
_____________________________________________
using System;
using System.Linq;

public class SumDigPower
{
  public static long[] SumDigPow(long a, long b)
  {
    return Enumerable.Range((int) a, (int) (b - a))
        .Where(x => (long) x.ToString().Select((c, i) => Math.Pow(c - '0', i + 1)).Sum() == x)
        .Select(Convert.ToInt64).ToArray();
  }
}
_____________________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class SumDigPower {
    
    public static long[] SumDigPow(long a, long b) 
    {
        List<long> r = new List<long>();
        for(long l = a; l<=b; l++){
          int n = 1;
          long sum = 0;
          foreach(char c in (""+l)){
            sum+=(long)Math.Pow(Int64.Parse(""+c), n);
            n++;
          }
          if(sum==l){
            r.Add(l);
          }
        }
        return r.ToArray();
    }
}
_____________________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class SumDigPower {
    
    public static long[] SumDigPow(long a, long b) 
    {
        List<long> ls = new List<long>();
        for (long n = a; n <= b; n++) //remember <= since it's inclusive
        {
          var digitsPow = n.ToString() //seperate digits
                        .Select(x => x-'0') //convert chars into ints
                        .Select((x, i) => Math.Pow(x, i+1)) //raise ints to power of digit position
                        .Sum();
          
          if (digitsPow == n) ls.Add(n);
        }
        return ls.ToArray();
    }
}
