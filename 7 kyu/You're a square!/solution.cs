using System;

public class Kata
{
  public static bool IsSquare(int n)
  {
    return Math.Sqrt(n) % 1 == 0;
  }
}
__________________________________
using System;

public class Kata {
  public static bool IsSquare(int n) 
    => (Math.Sqrt(n) % 1 == 0);
}
__________________________________
using System;

public class Kata
{
  public static bool IsSquare(int n)
  {
    return Math.Abs(Math.Sqrt(n) - (int)Math.Sqrt(n)) < double.Epsilon;
  }
}
__________________________________
using System;

public class Kata
{
  public static bool IsSquare(int n)
  {
  bool sqr;
  double result;
  double result2;
    if (n >= 0)
    {
    result = Math.Sqrt(n);
    result2 = Math.Round(result);
    if (result2 == result)
       sqr = true;
    else
       sqr = false;
    }
    else
    {
    sqr = false;
    }
    return sqr;
  }
}
