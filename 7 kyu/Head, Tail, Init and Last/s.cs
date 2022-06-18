using System.Linq;
using System.Collections.Generic;

public static class ArrayMethods
{
  public static TSource Head<TSource>(this List<TSource> list) => list[0];
  public static List<TSource> Tail<TSource>(this List<TSource> list) => list.Skip(1).ToList();
  public static List<TSource> Init<TSource>(this List<TSource> list) => list.Take(list.Count - 1).ToList();
  public static TSource Last_<TSource>(this List<TSource> list) => list[^1];
}
_____________________________
using System.Collections.Generic;
using System.Linq;

public static class ArrayMethods
{
  public static TSource Head<TSource>(this List<TSource> list)
  {
    return list.First();
  }
  
  public static List<TSource> Tail<TSource>(this List<TSource> list)
  {
    return list.Skip(1).ToList();
  }

  public static List<TSource> Init<TSource>(this List<TSource> list)
  {
    return list.Take(list.Count - 1).ToList();
  }
  
  public static TSource Last_<TSource>(this List<TSource> list)
  {
    return list.Last();
  }
}
_____________________________
using System.Collections.Generic;
using System.Linq;

public static class ArrayMethods {
  public static TSource Head<TSource>(this List<TSource> ls) => ls.First();
  public static List<TSource> Tail<TSource>(this List<TSource> ls) => ls.Skip(1).ToList();
  public static List<TSource> Init<TSource>(this List<TSource> ls) => ls.SkipLast(1).ToList();
  public static TSource Last_<TSource>(this List<TSource> ls) => ls.Last();
}
