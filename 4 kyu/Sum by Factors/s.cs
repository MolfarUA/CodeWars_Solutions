54d496788776e49e6b00052f


using System;
using System.Linq;
using System.Collections.Generic;
public class SumOfDivided {
  public static string sumOfDivided(int[] l) {
      string result ="";
      List<int> primes = new List<int>();
      for (int i =2; i <= l.Max(Math.Abs); i++) 
          if ( primes.All(e=> i%e!=0) && l.Any(e=> e%i ==0) ) {
             primes.Add(i);
             result += $"({i} {l.Where(e=>Math.Abs(e)%i==0).Sum() })";
          }
      return result;
  }
}
________________________________________________
using System;
using System.Linq;

public class SumOfDivided {
  public static string sumOfDivided(int[] lst) =>
    string.Join(string.Empty, getPrimeFactors(lst).Select(p =>
    {
      var sum = lst.Where(i => i % p == 0).Sum();
      return $"({p} {sum})";
    }));
  
  private static int[] getPrimeFactors(int[] lst) {
    var factors = lst
      .SelectMany(i => Enumerable.Range(2, Math.Abs(i)).Where(f => i % f == 0))
      .Distinct();

    return factors
      .Where(p => factors.Count(f => p % f == 0) == 1)
      .OrderBy(p => p)
      .ToArray();
  }
}
________________________________________________
public class SumOfDivided {
  
  public static string sumOfDivided(int[] lst) {
      int[] rem = new int[lst.Length];
      int max = 0;
      string result = "";
      for (int i = 0; i < lst.Length; ++i) {
          rem[i] = System.Math.Abs(lst[i]);
          max = System.Math.Max(max, System.Math.Abs(lst[i]));
      }
      for (int fac = 2; fac <= max; ++fac) {
          bool isFactor = false;
          int tot = 0;
          for (int i = 0; i < lst.Length; ++i) {
              if (rem[i] % fac == 0) {
                  isFactor = true;
                  tot += lst[i];
                  while (rem[i] % fac == 0) {
                      rem[i] /= fac;
                  }
              }
          }
          if (isFactor) {
              result += "(" + fac + " " + tot + ")";
          }
      }
      return result;
  }
}
