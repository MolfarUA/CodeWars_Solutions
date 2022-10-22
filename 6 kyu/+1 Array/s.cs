5514e5b77e6b2f38e0000ca9


using System.Linq;

namespace Kata
{
  public static class Kata
  {
    public static int[] UpArray(int[] num)
    {
      if (num.Length == 0 || num.Any(a => a < 0 || a > 9))
        return null;
        
      for (var i = num.Length - 1; i >= 0; i--)
      {
        if (num[i] == 9)
        {
          num[i] = 0;
        }
        else
        {
          num[i]++;
          return num;
        }
      }
      return new []{ 1 }.Concat(num).ToArray(); 
    }
  }
}
_____________________________
using System;
using System.Linq;

namespace Kata
{
  public static class Kata
  {
    public static int[] UpArray(int[] num)
    {
      if (num.Length == 0 || num.Any(x => x < 0 || x.ToString().Length > 1))
      {
        return null;
      }

      for (int i = num.Length - 1; i >= 0; i--)
      {
        num[i] = (++num[i]) % 10;
        if (num[i] > 0)
        {
          return num;
        }
      }
      
      return num.Prepend(1).ToArray();
    }
  }
}
_____________________________
using System;

namespace Kata
{
  public static class Kata
  {
    public static int[] UpArray(int[] num)
    {
      if (num.Length == 0)
                return null;
            bool allnines = true;
            foreach (int i in num )
            {
                if (i > 9 || i < 0)
                    return null;
                if (i != 9)
                    allnines = false;
            }

            if (allnines == true)
            {
                int[] result = new int[num.Length + 1];
                result[0] = 1;
                for (int i = 1; i < result.Length; i++)
                {
                    result[i] = 0;
                }
                return result;
            }

            for (int i = num.Length-1; i > -1; i--)
            {
                if (num[i] + 1 > 9)
                {
                    num[i] = 0;
                    num[i - 1] += 1;
                }
                else 
                {
                    num[i] += 1;
                  break;
                }
            }
            return num;
    }
  }
}
