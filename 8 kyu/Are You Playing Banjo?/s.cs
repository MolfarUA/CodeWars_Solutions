53af2b8861023f1d88000832


using System;

public class Kata
{
  public static string AreYouPlayingBanjo(string name)
  {
    return string.Format("{0} {1} banjo", name, char.ToLower(name[0]) == 'r' ? "plays" : "does not play");
  }
}
________________________________
using System;

public class Kata
{
  public static string AreYouPlayingBanjo(string name)
  {
      string result = "";
    
      if (name[0] == 'R' || name[0] == 'r')
      {
          result = name + " plays banjo";
      }
      else
      {
          result = name + " does not play banjo";
      }
      
      return result;
  }
}
________________________________
using System;
using System.Globalization;

public class Kata
{
  public static string AreYouPlayingBanjo(string name)
  {
    if (name.StartsWith("R", true, CultureInfo.InvariantCulture))
      return String.Format("{0} plays banjo", name);
    return String.Format("{0} does not play banjo", name);
  }
}
