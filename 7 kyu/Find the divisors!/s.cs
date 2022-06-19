544aed4c4a30184e960010f4


using System;
using System.Linq;

public class Kata
{
  public static int[] Divisors(int n)
  {
    var div = Enumerable.Range(2, (int) Math.Sqrt(n))
      .Where(x => n % x == 0 && x < n)
      .SelectMany(x => new[] {x, n / x})
      .OrderBy(x => x)
      .Distinct()
      .ToArray();
    
    return div.Any() ? div : null;
  }
}
__________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class Kata
{
  public static int[] Divisors(int n)
  {
    List<int> l = new List<int>();
    for (int i = 2; i <= Math.Sqrt(n); i++) if (n % i == 0) l.Add(i);
    if (l.Count == 0) return null;
    List<int> k = new List<int>(Enumerable.Reverse(l.ToArray().Select(x => n / x).ToArray().Where(x => !l.Contains(x))));
    l.AddRange(k);
    return l.ToArray();
  }
}
__________________________________
using System.Collections.Generic;
using System.Linq.Dynamic;
using System.Linq;
using System;

public class Kata
{
  public static int[] Divisors(int n)
        {
            List<int> divisors = new List<int>();
            int max = (int)Math.Sqrt(n);

            for (int i = 2; i <= max; i++)
            {
                if (n % i == 0)
                {
                    divisors.Add(i);
                    if (i != n / i)
                        divisors.Add(n / i);
                }
            }
            if(divisors.Count() == 0)
              return null;
            else
              return divisors.OrderBy(x => x).ToArray();
        }
}
__________________________________
using System.Linq;
using System;

public class Kata
{
  public static int[] Divisors(int n)
  {
   int[] divisors = Enumerable.Range(2, (int)Math.Sqrt(n)).Where(x => x < n && n % x == 0).SelectMany(x => new[] { x, n / x }).GroupBy(x => x).Select(g => g.First()).OrderBy(x => x).ToArray();
            return divisors.Length != 0 ? divisors : null;
  }
}
__________________________________
using System;
using System.Linq;

public class Kata
{
  public static int[] Divisors(int n) 
  {
    var divisors = Enumerable.Range(2, (int)Math.Sqrt(n))
      .Where(i => n % i == 0 && i < n)
      .SelectMany(i => new[]{i, n / i})
      .OrderBy(i => i)
      .Distinct()
      .ToArray();
    return divisors.Any() ? divisors : null;
  }
}
