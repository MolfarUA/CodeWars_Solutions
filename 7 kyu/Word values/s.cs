598d91785d4ce3ec4f000018


using System.Linq;

public class Kata
{
  public static int[] WordValue(string[] a)
  {
    return a.Select((x, i) => x.Sum(c => c != 32 ? c - 96 : 0) * ++i).ToArray();
  }
}
_____________________________
using System;
using System.Linq;

public class Kata
{
  public static int[] WordValue(string[] a) => a.Select((s, i) => (i + 1) * s.ToCharArray().Aggregate(0, (t, c) => t + 1 + "abcdefghijklmnopqrstuvwxyz".IndexOf(c))).ToArray();
}
_____________________________
using System.Linq;

public class Kata
{
  public static int[] WordValue(string[] a)
  {
    return a.Select((w, i) => w.Where(c => char.IsLetter(c)).Sum(c => c - 'a' + 1) * (i + 1)).ToArray();
  }
}
