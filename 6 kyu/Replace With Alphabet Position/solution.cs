using System.Linq;
public static class Kata
{
  public static string AlphabetPosition(string text)
  {
     return string.Join(" ", text.ToLower().Where(char.IsLetter).Select(x => x - 'a'+1));
  }
}

_______________________________________________
using System.Linq;

public static class Kata
{
  public static string AlphabetPosition(string text)
  {
    return string.Join(" ", text.ToLower()
                                          .Where(c => char.IsLetter(c))
                                          .Select(c => "abcdefghijklmnopqrstuvwxyz".IndexOf(c) + 1)
                                          .ToArray());
  }
}

_______________________________________________
using System.Text;

public static class Kata
{
  public static string AlphabetPosition(string text)
  {
    StringBuilder sb = new StringBuilder(text.Length * 3);
    foreach (char ch in text.ToLower())
    {
        if (ch < 'a' || ch > 'z') continue;
        sb.Append(ch - '`');
        sb.Append(' ');
    }
    return sb.ToString().Trim();
  }
}

_______________________________________________
using System.Linq;

public static class Kata
{
  public static string AlphabetPosition(string text)
  {
    return string.Join(" ", text.Where(char.IsLetter).Select(c => c & 31));
  }
}

_______________________________________________
using System.Collections.Generic;
using System.Text;

public static class Kata
{
    public static string AlphabetPosition(string text)
    {
        var letterPositions = new Dictionary<char, int>
        {
            {'a', 1},
            {'b', 2},
            {'c', 3},
            {'d', 4},
            {'e', 5},
            {'f', 6},
            {'g', 7},
            {'h', 8},
            {'i', 9},
            {'j', 10},
            {'k', 11},
            {'l', 12},
            {'m', 13},
            {'n', 14},
            {'o', 15},
            {'p', 16},
            {'q', 17},
            {'r', 18},
            {'s', 19},
            {'t', 20},
            {'u', 21},
            {'v', 22},
            {'w', 23},
            {'x', 24},
            {'y', 25},
            {'z', 26}
        };

        var convertedLetters = new List<int>();

        foreach (var c in text.ToLower())
        {
            if (letterPositions.ContainsKey(c))
            {
                convertedLetters.Add(letterPositions[c]);
            }
        }

        return string.Join(" ", convertedLetters);
    }
}

_______________________________________________
using System.Collections.Generic;
using System;
public static class Kata
{
  public static string AlphabetPosition(string text)
  {
     string alphabet="abcdefghijklmnopqrstuvwxyz";
     List<string> Nums= new List<string>();
     
     foreach(char c in text)
     {
       if(alphabet.Contains(c.ToString().ToLower()))
         Nums.Add((alphabet.IndexOf(c.ToString().ToLower())+1).ToString());
     }
     
     string result= string.Join(" ", Nums.ToArray());
     
     return result;
  }
}
