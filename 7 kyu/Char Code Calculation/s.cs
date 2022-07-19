57f75cc397d62fc93d000059


using System.Linq;

public class Kata
{
  public static int Calc(string s)
  {
    return string.Concat(s.Select(x => (int) x)).Count(x => x == '7') * 6;
  }
}
__________________________________
using System;
using System.Linq;

public class Kata
{
    public static Int32 Calc(String s)
    {
        return string.Join("", string.Join("", s.Select(c => (int)c)).ToCharArray().Where(c => c == '7')).Length * 6;
    }
}
__________________________________
using System;
using System.Linq;

public class Kata
{
  public static Int32 Calc(String s)
  {
    return string.Concat(s.Select(c => (int)c)).Count(c => c == '7') * 6;
  }
}

