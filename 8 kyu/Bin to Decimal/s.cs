57a5c31ce298a7e6b7000334


using System;

namespace Solution
{
  public static class Program
  {
    public static int binToDec(string s)
    {
      return Convert.ToInt32(s, 2);
    }
  }
}
_________________________
using System;

namespace Solution
{
  public static class Program
  {
    public static int binToDec(string s) => Convert.ToInt32(s, 2);
    
  }
}
_________________________
using System;

namespace Solution
{
    public static class Program
    {
        public static int binToDec(string s)
        {
            byte RADIX = 2;
            return Convert.ToInt32(s, RADIX);
        }
    }
}
