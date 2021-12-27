using System.Linq;

public class Kata
{
  public static int DuplicateCount(string str)
  {
    return str.ToLower().GroupBy(c => c).Where(g => g.Count() > 1).Count();
  }
}
_______________________
using System;
using System.Linq;

public class Kata
{
  public static int DuplicateCount(string str)
  {
    return str.ToLower().GroupBy(c => c).Count(c => c.Count() > 1);
  }
}
________________
using System;
using System.Linq;

public class Kata
{
  public static int DuplicateCount(string str)
  {  
    return str.ToUpperInvariant()
              .ToCharArray()
              .GroupBy(c => c)
              .Where(c => c.Count() > 1)
              .Select(c => c.First())
              .Count();
  }
}
______________________
using System;

public class Kata
{
  public static int DuplicateCount(string str)
  {
    int repeatTimes = 0;
    str = str.ToLower();
    for (char i = 'a'; i <= 'z'; i++)
    {
      if (str.IndexOf(i)!=(-1))
      {
        if (str.IndexOf((char)i) != str.LastIndexOf((char)i))
          repeatTimes++;
      }
    }
    for (char i = '0'; i <= '9'; i++)
    {
      if (str.IndexOf(i)!=(-1))
      {
        if (str.IndexOf((char)i) != str.LastIndexOf((char)i))
          repeatTimes++;
      }
    }
    return repeatTimes;
  }
}
______________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;



public class Kata
{
    public static int DuplicateCount(string str)
    {
        str = string.Join("", str.OrderBy(e => e));
        int count = 0;

        for (int i = 1; i < str.Length-1; i++)
        {    
            if(i == 1) if (str[i] == str[i + 1] || str[i] == str[i - 1]) count++;
            if (str[i] == str[i+1] && str[i] != str[i-1]) count++;
        }
        return count;
    }

    static void Main()
    {
        DuplicateCount("aabbcde");
    }
}
