using System.Collections.Generic;

public static class Kata
{
  public static IEnumerable<T> UniqueInOrder<T>(IEnumerable<T> iterable) 
  {
    T previous = default(T);
    foreach(T current in iterable)
    {
      if (!current.Equals(previous))
      {
        previous = current;
        yield return current;
      }
    }
  }
}
_____________________________________________
using System.Collections.Generic;
using System.Linq;

public static class Kata
{
  public static IEnumerable<T> UniqueInOrder<T>(IEnumerable<T> iterable) 
  {
    var retList = new List<T>();
    foreach (var element in iterable) if (!element.Equals(retList.LastOrDefault())) retList.Add(element);
    return retList;
  }
}
_____________________________________________
using System.Collections.Generic;

public static class Kata
{
  public static IEnumerable<T> UniqueInOrder<T>(IEnumerable<T> iterable) 
  {
    var e = iterable.GetEnumerator();
    if (e.MoveNext())
    {
      var c = e.Current;
      while (e.MoveNext())
      {
        if (!e.Current.Equals(c)) yield return c;
        c = e.Current;
      }
      yield return c;
    }
  }
}
_____________________________________________
using System.Collections.Generic;
using System.Linq;
public static class Kata
{
  public static IEnumerable<T> UniqueInOrder<T>(IEnumerable<T> iterable) 
  {
    return iterable.Where((x, i) => i == 0 || !Equals(x, iterable.ElementAt(i-1)));
    
  }
}
_____________________________________________
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Linq;
using System;

public static class Kata
{
  public static IEnumerable<T> UniqueInOrder<T>(IEnumerable<T> iterable) 
  {
    Object prev = null;
    foreach (var el in iterable) {
      if (!el.Equals(prev)) yield return el;
      prev = el;
    } 
  }
}
