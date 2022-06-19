515de9ae9dcfc28eb6000001


using System.Collections.Generic;
using System.Linq;

public class SplitString
{
  public static string[] Solution(string str)
  {
    if (str.Length % 2 == 1)
    str += "_";
  
    List<string> list = new List<string>();
    for (int i = 0; i < str.Length; i += 2)
    {
      list.Add(str[i].ToString() + str[i+1]);
    }
    
    return list.ToArray();
  }
}
________________________________
using System.Linq;

public class SplitString
{
  public static string[] Solution(string str)
  {
    if (str.Length%2 != 0)
      str += "_";
    return Enumerable.Range(0, str.Length)
      .Where(x => x%2 == 0)
      .Select(x => str.Substring(x, 2))
      .ToArray();
  }
}
________________________________
using System.Linq;
using System.Text.RegularExpressions;

public class SplitString
{
  public static string[] Solution(string str)
  {
    return Regex.Matches(str + "_", @"\w{2}").Select(x => x.Value).ToArray();
  }
}
________________________________
using System.Linq;


public class SplitString
{
  public static string[] Solution(string str)
  {
    str = (str.Length % 2 == 0) ? str : str + "_";
    return 
     Enumerable
      .Range(0, str.Length / 2) 
      .Select( i => str.Substring( 2*i, 2))
      .ToArray();
  }
}
________________________________
using System;
using System.Text.RegularExpressions;
using System.Linq;
public class SplitString
{
  public static string[] Solution(string s)
  {
    if (s.Length % 2 != 0) {
      s += "_";
    }
    return Regex.Matches(s, "([a-zA-Z_]{2})").OfType<Match>().Select(m => m.Value).ToArray();
  }
}
