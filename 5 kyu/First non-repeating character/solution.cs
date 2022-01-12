using System;
using System.Linq;

public class Kata
{
  public static string FirstNonRepeatingLetter(string s)
  {
    return s.GroupBy(char.ToLower)
            .Where(gr => gr.Count() == 1)
            .Select(x => x.First().ToString())
            .DefaultIfEmpty("")
            .First();
  }
}
_______________________________________________
using System;
using System.Linq;

public class Kata
{
  public static string FirstNonRepeatingLetter(string s)
  {
    var ret = s.GroupBy(z => char.ToLower(z)).Where(g => g.Count() == 1).FirstOrDefault();
    return (ret != null) ? ret.First().ToString() : string.Empty;
  }
}
_______________________________________________
using System;
using System.Linq;

public class Kata
{
  public static string FirstNonRepeatingLetter(string s)
  {
    return s.GroupBy(c => c.ToString(), StringComparer.InvariantCultureIgnoreCase)
            .Where(g => g.Count() == 1)
            .Select(g => g.Key)
            .DefaultIfEmpty("")
            .FirstOrDefault();
  }
}
_______________________________________________
public class Kata
{
  public static string FirstNonRepeatingLetter(string s)
  {
    string lowInputString = s.ToLower();
           for (int i = 0; i < s.Length; i++)
           {
               if (lowInputString.IndexOf(lowInputString[i]) == lowInputString.LastIndexOf(lowInputString[i]))
                   return s[i].ToString();
           }
           return "";
  }
}
