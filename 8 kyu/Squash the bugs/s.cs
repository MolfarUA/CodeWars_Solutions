56f173a35b91399a05000cb7


using System.Linq;

public static class Kata
{
  public static int FindLongest(string str) => str.Split().Max(x => x.Length);
}
__________________________
using System;

public static class Kata
{
    public static int FindLongest(string str) {

      var spl = str.Split(" ");
      int longest = 0;

      for (var i = 0; i < spl.Length; i++) {
          if (spl[i].Length > longest) 
          {
              longest = spl[i].Length;
          }
      }
      return longest;
    }
}
__________________________
using System;

public static class Kata
{
    public static int FindLongest(string str) {

            string[] spl = str.Split(' ');
            var longest = 0;

            for (int i = 0; i < spl.Length; i ++) { 
            if (spl[i].Length > longest) {
                longest = spl[i].Length;
            }
        }
            return longest;
      }
}
