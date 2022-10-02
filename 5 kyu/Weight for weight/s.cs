55c6126177c9441a570000cc


using System.Linq;

public class WeightSort 
{
    public static string orderWeight(string s)
    {
        return string.Join(" ", s.Split(' ')
            .OrderBy(n => n.ToCharArray()
            .Select(c => (int)char.GetNumericValue(c)).Sum())
            .ThenBy(n => n));
    }
}
_____________________________
using System;
using System.Linq;

public static class WeightSort {
  
  public static string orderWeight(string strng) {
    var values = strng.Split(' ');
    return string.Join(" ", values.OrderBy(s => s.Sum(c => c - 48)).ThenBy(s => s));
  }
}
_____________________________
using System;
using System.Linq;

public class WeightSort 
{
  public static string orderWeight(string strng)    
    => string.Join(" ", strng.Split().OrderBy(s => s.Sum(char.GetNumericValue)).ThenBy(x => x));
}
