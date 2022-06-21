5263c6999e0f40dee200059d


using System.Collections.Generic;
using System.Linq;

public class Kata
{
  public static List<string> GetPINs(string observed)
  {
    var result = new List<string>
    {
      ""
    };
    
    foreach (var c in observed)
    {
      result =
        (from r in result
         from a in AdjacentKeys[c]
         select $"{r}{a}").ToList();
    }
    
    return result;
  }
  
  public static Dictionary<char, IEnumerable<string>> AdjacentKeys =
    new Dictionary<char, IEnumerable<string>>()
  {
    { '1', new[] { "1", "2", "4" } },
    { '2', new[] { "1", "2", "3", "5" } },
    { '3', new[] { "2", "3", "6" } },
    { '4', new[] { "1", "4", "5", "7" } },
    { '5', new[] { "2", "4", "5", "6", "8" } },
    { '6', new[] { "3", "5", "6", "9" } },
    { '7', new[] { "4", "7", "8" } },
    { '8', new[] { "5", "7", "8", "9", "0" } },
    { '9', new[] { "6", "8", "9" } },
    { '0', new[] { "8", "0" } }
  };
}
______________________________
using System.Collections.Generic;
using System.Linq;

public class Kata
{
    public static List<string> GetPINs(string observed)
    {
      var adjacent = new Dictionary<char, List<string>>
      {
        {'0', new List<string> {"0", "8"}},
        {'1', new List<string> {"1", "2", "4"}},
        {'2', new List<string> {"1", "2", "3", "5"}},
        {'3', new List<string> {"2", "3", "6"}},
        {'4', new List<string> {"1", "4", "5", "7"}},
        {'5', new List<string> {"2", "4", "5", "6", "8"}},
        {'6', new List<string> {"3", "5", "6", "9"}},
        {'7', new List<string> {"4", "7", "8"}},
        {'8', new List<string> {"0" ,"5", "7", "8", "9"}},
        {'9', new List<string> {"6", "8", "9"}}
      };
      
      return CartesianN(observed.Select(c => adjacent[c]));
    }
    
    public static List<string> CartesianN(IEnumerable<List<string>> xss) 
      => xss.Aggregate(new List<string>(), (acc, cur) => !acc.Any() ? cur : Cartesian(acc, cur));
    
    public static List<string> Cartesian(List<string> xs, List<string> ys) 
      => xs.SelectMany(x => ys, (x, y) => $"{x}{y}").ToList();
}
______________________________
using System.Collections.Generic;

public class Kata
{
    public static List<string> GetPINs(string observed)
    {  
        var variations = new List<string>() { "" };
        foreach (var digit in observed)
        {
            variations = Helper.Expound(variations, digit);
        }
        return variations;
    }
    
    internal static class Helper
    {
        internal static IDictionary<char, List<string>> _digits = new Dictionary<char, List<string>>()
            {
                {'1', new List<string>() { "1", "2", "4" } },
                {'2', new List<string>() { "1", "2", "3", "5" }},
                {'3', new List<string>() { "2", "3", "6" }},
                {'4', new List<string>() { "1", "4", "5", "7" }},
                {'5', new List<string>() { "2", "4", "5", "6", "8" }},
                {'6', new List<string>() { "3", "5", "6", "9" }},
                {'7', new List<string>() { "4", "7", "8" }},
                {'8', new List<string>() { "5", "7", "8", "9", "0" }},
                {'9', new List<string>() { "6", "8", "9", }},
                {'0', new List<string>() { "8", "0" }}
            };

        internal static List<string> Expound(List<string> list, char digit)
        {
            var newList = new List<string>();
            foreach (var item in list)
            {
                var options = _digits[digit];
                foreach (var option in options)
                {
                    newList.Add(item + option);
                }
            }
            return newList;
        }
    }
}
