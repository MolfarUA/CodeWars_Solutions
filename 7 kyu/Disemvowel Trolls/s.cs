using System;
using System.Text.RegularExpressions;

public static class Kata
{
  public static string Disemvowel(string str)
  {
    return Regex.Replace(str,"[aeiou]", "", RegexOptions.IgnoreCase);
  }
}
______________________________
using System;
using System.Linq;

public static class Kata
{
  public static string Disemvowel(string str)
  {
    return string.Concat(str.Where(ch => !"aeiouAEIOU".Contains(ch)));
  }
}
______________________________
using System;

public static class Kata
{
   public static string Disemvowel(string str)
  { 
    string[] vowels = {"a","e","i","o","u","A","E","I","O","U"}; 
    for (int i = 0; i < vowels.Length; i++)
    {
      str = str.Replace(vowels[i],"");  
    }
        return str;
    }
}
______________________________
using System;
using System.Text.RegularExpressions;

public static class Kata
{
  public static string Disemvowel(string str)
  {
    return Regex.Replace(str, "[euioa]", "", RegexOptions.IgnoreCase);;
  }
}
______________________________
using System;

public static class Kata
{
  public static string Disemvowel(string str)
  {
    string strNew = "";

            string[] strings = str.Split('a', 'u', 'e', 'i', 'o', 'A', 'U', 'E', 'I', 'O');

            foreach (var item in strings)
            {
                strNew += item;
            }
            
    return strNew;
  }
}
