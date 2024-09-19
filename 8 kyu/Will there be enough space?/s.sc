5875b200d520904a04000003

using System;

public static class Kata
{
  public static int Enough(int cap, int on, int wait) => Math.Max(on + wait - cap, 0);
}
__________________________
using System;

public static class Kata
{
  public static int Enough(int cap, int on, int wait)
  {
    return cap - (on + wait) > 0 ? 0 : Math.Abs(cap - (on + wait));
  }
}
_________________________
using System;

public static class Kata
{
  public static int Enough(int cap, int on, int wait)
  {
    int remainingPlace = cap-on;
    
    if(remainingPlace < wait)
    {
      return wait-remainingPlace;
    }
    return 0;
  }
}
