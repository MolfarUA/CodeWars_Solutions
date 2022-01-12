using System.Collections.Generic;
using System.Linq;

public static class SumOfK 
{
  public static int? chooseBestSum(int t, int k, List<int> ls) =>
    ls.Combinations(k)
      .Select(c => (int?) c.Sum())
      .Where(sum => sum <= t)
      .DefaultIfEmpty()
      .Max();

  // Inspired by http://stackoverflow.com/questions/127704/algorithm-to-return-all-combinations-of-k-elements-from-n
  public static IEnumerable<IEnumerable<int>> Combinations(this IEnumerable<int> ls, int k) =>
    k == 0 ? new[] { new int[0] } :
      ls.SelectMany((e, i) =>
        ls.Skip(i + 1)
          .Combinations(k - 1)
          .Select(c => (new[] {e}).Concat(c)));
}
_______________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class SumOfK 
{
  public static int? chooseBestSum(int t, int k, List<int> ls)
  {
    var _ls = ls.Where(x => x <= t);
    return _ls.Count() == 0 ? null : _ls.Select((x, i) => x + (k > 1 ? chooseBestSum(t-x, k-1, _ls.Skip(i+1).ToList()) : 0)).Max();
  }
}
_______________________________________
using System;
using System.Collections.Generic;

public static class SumOfK
{
    public static int? chooseBestSum(int t, int k, List<int> ls)
    {
        return Best(t, k, ls, 0, 0);
    }

    public static int? Best(int t, int k, List<int> ls, int Start, int Sum)
    {
        if (k == 0)
            return (Sum <= t) ? (int?)Sum : null;

        if (Start >= ls.Count)
            return null;

        int? S1 = Best(t, k - 1, ls, Start + 1, Sum + ls[Start]);
        int? S2 = Best(t, k, ls, Start + 1, Sum + 0);

        if (S1 == null && S2 == null)
            return null;
        if (S1 == null)
            return S2;
        if (S2 == null)
            return S1;
        return (int?)Math.Max(S1.Value, S2. Value);
    }
}
_______________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class SumOfK 
{
    public static int? chooseBestSum(int t, int k, List<int> ls)
    {
      return ls.Combinations(k).Select(x => (int?)x.Sum()).Where(x => x <= t).Max();
    }
    
    // thanks to https://stackoverflow.com/a/44845484
    public static IEnumerable<IEnumerable<int>> Combinations(this IEnumerable<int> input, int size)
    {
      return size == 0 ? new[] { new int[0] } :
        input.SelectMany((e, i) =>
          input.Skip(i + 1).Combinations(size - 1).Select(c => (new[] { e }).Concat(c)));
    }
}
_______________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class SumOfK 
{
    public static int? chooseBestSum(int t, int k, List<int> ls) 
    {
        var s = new List<int>(Combinations<int>(ls, k).Select(c => c.Sum()));
        var rv = s.OrderByDescending(i => i).Where(i => i <= t).FirstOrDefault();
        return rv == default(int) ? null : (int?)rv;
    }
    
    public static IEnumerable<IEnumerable<T>> Combinations<T>(IEnumerable<T> elements, int k)
    {
      return k == 0 ? new[] { new T[0] } :
        elements
          .SelectMany((e, i) => Combinations(elements.Skip(i + 1), k - 1)
              .Select(c => c.Concat(new[] { e })));
    }
}
