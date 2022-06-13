using System;
using System.Linq;
public class Kata {
  public string Convert(string i, string s, string t)
  {
        var a= i.Select((x,n)=>s.IndexOf(x)*(long)Math.Pow(s.Length,i.Length-1-n)).Sum();
        string rs;
        for (rs="";a>0;a/=t.Length) rs=t[(int)(a%t.Length)]+rs;
        return i=="0" ? t[0]+"" : rs;
  }
}
__________________________________________
using System;
using System.Linq;

public class Kata
{
  public string Convert(string input, string source, string target)
  {
    var result = "";
    var num = input.Select((c, i) => source.IndexOf(c) * (long) Math.Pow(source.Length, input.Length - i - 1)).Sum();

    do
    {
        result = target[(int) (num % target.Length)] + result;
    } while ((num /= target.Length) > 0);

    return result;
  }
}
__________________________________________
using System;
using System.Linq;
using System.Text;

public class Kata {
  public string Convert(string input, string source, string target)
  {
       var result = "";
            var num = input.Select((c, i) => source.IndexOf(c) * (long) Math.Pow(source.Length, input.Length - i - 1))
                .Sum();

            do
            {
                result = target[(int) (num % target.Length)] + result;
            } while ((num /= target.Length) > 0);

            return result;
  }
}
__________________________________________
using System;
using System.Linq;
using System.Text;

public class Kata {
  public class Alphabet
{
   public const string BINARY = "01";
   public const string OCTAL = "01234567";
   public const string DECIMAL = "0123456789";
   public const string HEXA_DECIMAL = "0123456789abcdef";
   public const string ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz";
   public const string ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
   public const string ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
   public const string ALPHA_NUMERIC = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
}
  public string Convert(string input, string source, string target)
  {
    var result = "";
    var num = input.Select((c,i) => source.IndexOf(c) * (long)Math.Pow(source.Length,input.Length - i - 1)).Sum();
    do{
      result = target[(int) (num % target.Length)] + result;
    }while ((num /= target.Length) > 0);
    return result;
  }
  
}
__________________________________________
using System;
using System.Linq;
using System.Text;
using System.Collections.Generic;

public class Kata {
  public string Convert(string input, string source, string target)
  {
        var sourceBase = source.Length;
        var targetBase = target.Length;
        long num = 0; int i = 1;
        foreach (char c in input)
        {
            var pow = (long) Math.Pow(sourceBase, input.Length - (i++));
            num += source.IndexOf(c) * pow;
        }

        if (num == 0) return $"{target[0]}";

        var lst = new List<char>();
        while(num > 0)
        {
            var cur = num % targetBase;
            lst.Add(target[(int)cur]);
            num /= targetBase;
        }
        lst.Reverse();
        return lst.Aggregate(new StringBuilder(), (sb, c) => sb.Append(c)).ToString();
  }
}
