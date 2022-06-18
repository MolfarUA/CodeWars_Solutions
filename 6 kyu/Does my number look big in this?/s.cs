using System;
using System.Linq;

public class Kata
{
  public static bool Narcissistic(int value)
  {
    var str = value.ToString();
    return str.Sum(c => Math.Pow(Convert.ToInt16(c.ToString()), str.Length)) == value;
  }
}
________________________
using System.Linq;
using System;
public class Kata
{
  public static bool Narcissistic(int value)
  {
    var lstInt = value.ToString().Select(x => int.Parse(x.ToString())).ToList();
    double resultTemp = 0;
    
    lstInt.ForEach(x =>
    {
        resultTemp += Math.Pow(x, lstInt.Count);
    });
    
    return resultTemp == value;
  }
}
________________________
using System.Linq;
using System.Collections.Generic;

public class Kata
{
  private static HashSet<int> nNums = new HashSet<int>
  {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
    153, 370, 371, 407,
    1634, 8208, 9474,
    54748, 92727, 93084,
    548834,
    1741725, 4210818, 9800817, 9926315,
    24678050, 24678051, 88593477,
    146511208, 472335975, 534494836, 912985153,
  };

  public static bool Narcissistic(int value) =>
    nNums.Contains(value);
}
________________________
using System;
using System.Linq;

public class Kata
{
  public static bool Narcissistic(int value)
  {
    return $"{value}".Sum(c => Math.Pow(c - '0', $"{value}".Length)) == value;
  }
}
