5842df8ccbd22792a4000245


using System;
using System.Linq;

public static class Kata 
{
    public static string ExpandedForm(long num) 
    {
            var str = num.ToString();
            return String.Join(" + ", str
                .Select((x, i) => char.GetNumericValue(x) * Math.Pow(10, str.Length - i - 1))
                .Where(x => x > 0));
    }
}
_________________________
using System;

public static class Kata 
{
    public static string ExpandedForm(long num) 
    {
      string numString = num.ToString();
      string blah = "";      
      for (int i = 0; i < numString.Length; i++)
      {
        if (numString[i] != '0')
        {
          blah += numString[i];
          blah += new String('0', numString.Length - i - 1);
          blah += " + ";
        }
      }
      return blah.Substring(0, blah.Length - 3);
    }
}
_________________________
using System.Linq;

public static class Kata
{
  public static string ExpandedForm(long n)
  {
    return string.Join(" + ", $"{n}".Select((c, i) => c + new string('0', $"{n}".Length - i - 1)).Where(x => x[0] != '0'));
  }
}
