using System;
using System.Linq;

public static class Kata
{
  public static string Order(string words)
        {
            if (string.IsNullOrEmpty(words)) return words;
            return string.Join(" ", words.Split(' ').OrderBy(s => s.ToList().Find(c => char.IsDigit(c))));
        }
}

_____________________________________________
using System;
using System.Linq;

public static class Kata
{
  public static string Order(string words)
  {
    return string.Join(" ", words.Split().OrderBy(w => w.SingleOrDefault(char.IsDigit)));
  }
}

_____________________________________________
using System;
using System.Text;
using System.Linq;
using System.Text.RegularExpressions;
public static class Kata
{
  public static string Order(string words)
  {
    if (words == null) return words;
    var orderedWords = words.Split(" ")
                            .OrderBy(x => Regex.Match(x, @"\d").Value);
                      
    return string.Join(" ", orderedWords);
  }
}

_____________________________________________
using System;

public static class Kata
{
  public static string Order(string words)
  {    
    if (words == "")
      return words;
    
    string[] splited = words.Split(' ');  
    string result = "";
    for (int i = 1; i < 10; i++)
      {
        foreach (string word in splited)
          {
            if (word.Contains(Convert.ToString(i)))
            {   
              if (result == "")
                result += word;
              else  
                result += " " + word;
            }
          }
      }
    return result;
  }
}

_____________________________________________
using System;
using System.Linq;

public static class Kata
{
  public static string Order(string words)
  {
    if (words == "")
            return words;
        var stringArray = words.Split(" ");
        var returnString = new string[stringArray.Length];
        foreach (var i in stringArray)
            returnString[i.Where(n => Char.IsDigit(n)).First() - '1'] = i;
        return String.Join(" ", returnString);
  }
}
