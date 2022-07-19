55eea63119278d571d00006a


using System;
using System.Linq;

public class Kata
{
  public static int NextId(int[] ids)
  {
    int i = 0;
    while (ids.Contains(i))
    {
      i++;
    }
    
    return i;
  }
}
______________________
using System;
using System.Linq;

public class Kata
{
  public static int NextId(int[] ids)
  {
    return Enumerable.Range(0,ids.Length+1).Except(ids).Min();
  }
}
______________________
using System;
using System.Linq;

public class Kata
{
  public static int NextId(int[] ids)
  {
    var f= Enumerable.Range(0, ids.Max()).Except(ids);
           return f.Count() == 0 ? ids.Max() + 1 : f.First();
  }
}
