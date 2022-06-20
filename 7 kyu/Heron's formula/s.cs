57aa218e72292d98d500240f


using System;

namespace Solution
{
  public static class Program
  {
    public static double heron(double a, double b, double c)
    {
      var s = (a + b + c) / 2;
      return Math.Sqrt(s * (s - a) * (s - b) * (s - c));
    }
  }
}
________________________
using System;

namespace Solution
{
  public static class Program
  {
    public static double heron(double a, double b, double c)
            {
                double p = (a + b + c) / 2;
                return Math.Round(Math.Sqrt(p*((p-a)*(p-b)*(p-c))),1);
            }
  }
}
________________________
using System;

namespace Solution
{
  public static class Program
  {
    public static double heron(double a, double b, double c)
    {
      double s= (a+b+c)/2;
      
      double formula = Math.Sqrt(s * (s - a) * (s - b) * (s - c));
      
      return formula;
    }
  }
}
