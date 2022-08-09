57f780909f7e8e3183000078


using System.Linq;

public class Kata
{
  public static int Grow(int[] x)
  {
    return x.Aggregate((a,b) => a*b);
  }
}
_______________________
using System.Linq;

public class Kata
{
  public static int Grow(int[] x)
  {
    var sum = 1;
    for(var i = 0; i < x.Length; i++)
    {
      sum *= x[i];
    }
    return sum;
  }
}
_______________________
using System.Linq;
public class Kata
{
  public static int Grow(int[] x)
  {
     return x.Aggregate((p, next) => p * next);
  }
}
