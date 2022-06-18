using System;
public class Kata
{
  public static string FindNeedle(object[] haystack)
  {
    return "found the needle at position " + Array.IndexOf(haystack,"needle");
  }
}
________________________
using System;
public class Kata
{
  public static string FindNeedle(object[] haystack)
  {
    return $"found the needle at position {Array.IndexOf(haystack, "needle")}";
  }
}
________________________
using System;
public class Kata
{
  public static string FindNeedle(object[] haystack)
  {
    for(int i = 0 ; i < haystack.Length; i++)
    {
        string text = haystack[i] as string;
        if(text != null && text == "needle") 
        {
          return "found the needle at position " +i.ToString();
        }   
      
    }
    return null;
  }
}
________________________
using System;
public class Kata
{
  public static string FindNeedle(object[] haystack)
  {
            string res = "";
            for (int i = 0; i < haystack.Length; i++)
                if (haystack[i] != null && haystack[i].ToString() == "needle")
                    res = $"found the needle at position {i}";

            return res;
  }
}
________________________
using System;
public class Kata
{
  public static string FindNeedle(object[] haystack)
  {
    for(int i = 0; i<haystack.Length; i++)
    {
      if(haystack[i] == "needle")
        return "found the needle at position " + i;
    }
    return "Needle not there";
  }
}
