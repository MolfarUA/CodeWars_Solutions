using System;
using System.Linq;

public class Kata
{
  public static string PigIt(string str)
  {
    return string.Join(" ", str.Split(' ').Select(w => w.Any(char.IsPunctuation) ? w : w.Substring(1) + w[0] + "ay"));
  }
}

###################
using System.Text.RegularExpressions;

public class Kata
{
  public static string PigIt(string str)
  {
      return Regex.Replace(str, @"((\S)(\S+))", "$3$2ay");
  }
}

####################
using System;
using System.Linq;
using System.Text.RegularExpressions;

public class Kata
{
  public static string PigIt(string str) => Regex.Replace(str, @"\w+", word => word.Value.MoveFirstLetter().AddAy());  
}

static class WordExtensions
{
  public static string AddAy(this string word)
  {
    return word+"ay";
  }
  
  public static string MoveFirstLetter(this string word)
  {
    return new string(word.Skip(1).Concat(word.Take(1)).ToArray());
  }
}

####################
using System.Linq;
public class Kata
{
  static string[] array={".",",","!","?"};
  public static string PigIt(string str)
  {
    return string.Join(' ', str.Split(' ').Select(x=> {
      if(array.Contains(x))
        return x;
      else
        return (x+x[0]+"ay").Remove(0,1);
      }));
  }
}

##################
using System;
using System.Linq;

public class Kata
{
  public static string PigIt(string str) //"Pig latin is cool"; // igPay atinlay siay oolcay
        {
          string outString = "";
            string[] words = str.Split(' ');
            bool dig = words.Contains("!");
            string[] finalWords = new string[words.Length];
            for(int i=0; i<words.Length; i++)
            {
                if(words[i]=="!") { continue; }
                Word_Rewriter(words[i], out finalWords[i]);
            }
            foreach(string word in finalWords)
            {
                outString += word;
            }
            if(dig) { outString += "!"; }
            return outString.Trim();

            void Word_Rewriter(string word, out string reword)
            {
                reword="";
                for(int i=1; i<word.Length; i++)
                {
                    reword += word[i];
                }
                reword += word[0]+"ay ";
            }
        }
}

#######################
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;

public class Kata
{
    public static string PigIt(string str)
    {
        string[] ss = str.Split();

        for (int i = 0; i < ss.Length; i++)
        {
            if(char.IsLetterOrDigit(ss[i][0]))
            {
                ss[i] = ss[i] + ss[i][0].ToString();
                ss[i] = ss[i].Remove(0, 1);
                ss[i] += "ay";
            }
        }

        str = "";
        foreach (var item in ss)
        {
            str += item + " ";
        }

        return str.Trim();
    }


    public static void Main()
    {
    }
}
