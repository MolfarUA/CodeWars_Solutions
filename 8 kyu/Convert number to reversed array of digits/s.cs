using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution
{
  class Digitizer
  {
    public static long[] Digitize(long n)
    {
      return n.ToString()
              .Reverse()
              .Select(t => Convert.ToInt64(t.ToString()))
              .ToArray();
    }
  }
}
________________________
using System.Linq;

class Digitizer
{
  public static long[] Digitize(long n)
  {
    return $"{n}".Select(c => (long) c - '0').Reverse().ToArray();
  }
}
________________________
using System;
using System.Collections.Generic;

namespace Solution
{
  class Digitizer
  {
    public static long[] Digitize(long n)
    {
      char[] array = n.ToString().ToCharArray();
      long[] res = new long[array.Length];
      int len = res.Length - 1;
      for(int i = 0; i < len + 1; i++){
        res[i] = int.Parse(array[len - i].ToString());
      }
      return res;
    }
  }
}
________________________
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution
{
  class Digitizer
  {
    public static long[] Digitize(long num)
    {
       string str = num.ToString();
            long[] array = num.ToString().Select(o => Convert.ToInt64(o) - 48).ToArray();
            Array.Reverse(array, 0, array.Length);
        return array;
            
    }
  }
}
