57cfdf34902f6ba3d300001e


using System;
using System.Linq;

public class Kata
{
  public static string TwoSort(string[] s)
  {
     return string.Join("***", s.OrderBy(a => a, StringComparer.Ordinal).First().ToArray());
  }  
}
___________________________
using System;

public class Kata
{
  public static string TwoSort(string[] s)
  {
    System.Array.Sort(s, StringComparer.Ordinal);
    char[] c = s[0].ToCharArray();
    return string.Join("***", c);
  }  
}
___________________________
using System;
using System.Linq;

public class Kata
{
  public static string TwoSort(string[] s)
  {
    Array.Sort(s, StringComparer.Ordinal);

    var word = s[0];

    var newWord = string.Join("***", word.AsEnumerable());
            
    return newWord;
  }  
}
