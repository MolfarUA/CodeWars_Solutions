public class Kata
{
  public static bool Plural(double n)
  {
    return n != 1;
  }
}
__________________
public class Kata
{
  public static bool Plural(double n) => (n != 1);
}
__________________
using System;

public class Kata
    {
        public static bool Plural(double n)
        {
            Func<double, bool> result = x => x != 1;
            return result(n);
        }
    }
__________________
public class Kata
{
  public static bool Plural(double n)
  {
    
    
    switch(n)
      {
        case 0:
          return true;
          break;
        
        case 1:
          return false;
          break;
        
        default:
          return true;
          break;
      }
  }
}
__________________
public class Kata{
  public static bool Plural(double n)
    => n<1?true:n>1;
}
