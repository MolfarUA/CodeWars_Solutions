55aa075506463dac6600010d


using System;
using System.Collections.Generic;
using System.Linq;

public class SumSquaredDivisors 
{
  
  public static string listSquared(long m, long n)
  {
    List<string> result = new List<string>();
    for(int i = (int)m; i <= n; i++)
    {
      int sum = GetDivisors(i).Select(x => x*x).Sum();
      if(IsSquare(sum))
      {
        result.Add(string.Format("[{0}, {1}]", i, sum));
      }
    }
    return "[" + string.Join(", ", result) + "]";
  }
  
  private static bool IsSquare(int num)
  {
    return Math.Sqrt(num) % 1 == 0;
  }
  
  private static List<int> GetDivisors(int num)
  {
    List<int> divs = new List<int>();
    for(int i = 1; i <= num; i++)
    {
      if(num % i == 0)
        divs.Add(i);
    }
    return divs;
  }
}
________________________________
using System;
using System.Collections.Generic;
public class SumSquaredDivisors 
{
  
  public static string listSquared(long m, long n)
  {
            var result = new List<string>();

            for (long number = m; number <= n; number++)
            {
                var divisors = new List<int>();
                long sum = 0;
                for (int div = 1; div <= number; div++)
                {
                    if (number % div == 0)
                        sum += (div * div);
                }

                if (Math.Sqrt(sum) % 2 == 0 || sum == 1)
                    result.Add(string.Format("[{0}, {1}]",number,sum));
            }
            return string.Format("[{0}]", string.Join(", ", result));
  }
}
________________________________
using System;
public class SumSquaredDivisors
{

    public static string listSquared(long m, long n)
    {
        string output = "[";

        for (long i = m; i <= n; i++)
        {

            long sum = 0;
            for (long j = 1; j <= Math.Sqrt(i); j++)
            {
                if (i % j == 0)
                {
                    sum += j * j;
                    if (j != i / j) { sum += (i / j) * (i / j); }
                }

            }
            if (Math.Sqrt(sum) % 1 == 0)
            {
                output += String.Format("[{0}, {1}], ", i, sum);
            }
        }
        if (output == "[") { return "[]"; }
        return output.Substring(0, output.Length - 2) + "]";
    }
}
