using System;

public class Sum
{
  public int GetSum(int a, int b)
  {
    return (a + b) * (Math.Abs(a - b) + 1) / 2;
  }
}

_______________________________________
  using System;
  public class Sum
  {
    public int GetSum(int a, int b)
        {
            int max = Math.Max(a, b);
            int min = Math.Min(a, b);
            int result = 0;
            for (int i = min; i <= max; i++)
            {
                result += i;
            }
            return result;
        }
 }
 
_______________________________________
  using System;
  using System.Linq;
  public class Sum
  {
     public int GetSum(int a, int b)
     {
       //Good Luck!
        return Enumerable.Range(Math.Min(a,b), Math.Max(b,a)-Math.Min(b,a)+1).Sum();
     }
  }
  
_______________________________________
using System.Linq;
using static System.Math;

public class Sum
{
   public int GetSum(int a, int b)
   {
     return Enumerable.Range(a < b ? a : b, Abs(a - b) + 1).Sum();
   }
}

_______________________________________
using System;
  public class Sum
  {
     public int GetSum(int a, int b)
     {
         int min,max;
         if (a>b)
         {
             max=a;
             min=b;
         }
         else
         {
             max=b;
             min=a;
         }
         int result=0;
         while (min<=max)
         {
             result+=min;
             min++;
         }
         
       return result;
     }
  }
