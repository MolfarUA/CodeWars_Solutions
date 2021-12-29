using System;
using System.Linq;

public class Mixing 
{
  public static string Mix(string s1, string s2)
  {
     var s1Group = s1.Where(c => char.IsLower(c) && char.IsLetter(c)).GroupBy(a => a, b => b).Select(a => new { letter = a.Key, count = a.Count() });

     var s2Group = s2.Where(c => char.IsLower(c) && char.IsLetter(c)).GroupBy(a => a, b => b).Select(a => new { letter = a.Key, count = a.Count() });
     
     var s12Group = s1Group.Concat(s2Group).GroupBy(a => a.letter, b => b);
     
     var sGrouped = s12Group.Select(a => new {count = a.OrderByDescending((p => p.count)).First().count, 
                                         letter = a.Key, 
                                         winner = s1.Count(i => i == a.Key) > s2.Count(i => i == a.Key) 
                                         ? "1" : s1.Count(i => i == a.Key) < s2.Count(i => i == a.Key) ? "2" : "="});
                    
     return string.Join("/", sGrouped.Where(o => o.count > 1).OrderByDescending(o => o.count)
     .ThenBy(o => int.Parse(o.winner == "=" ? "3" : o.winner))
     .ThenBy(o => o.letter).Select(gz => gz.winner + ":" + new string(gz.letter, gz.count)));
  }
}

__________________________________________________
using System.Linq;

public class Mixing 
{
  public static string Mix(string s1, string s2)
  {
    return string.Join("/", (s1 + s2).Distinct()
      .Where(c => char.IsLower(c) && MaxCount(s1, s2, c) > 1)
      .Select(c => new { Prefix = Prefix(s1, s2, c), Value = new string(c, MaxCount(s1, s2, c)) })
      .OrderByDescending(x => x.Value.Length)
      .ThenBy(x => x.Prefix[0])
      .ThenBy(x => x.Value)
      .Select(x => x.Prefix + x.Value));
  }

  private static int MaxCount(string s1, string s2, char c)
  {
    var c1 = s1.Count(x => x == c);
    var c2 = s2.Count(x => x == c);
    return c1 > c2 ? c1 : c2;
  }

  private static string Prefix(string s1, string s2, char c)
  {
    var c1 = s1.Count(x => x == c);
    var c2 = s2.Count(x => x == c);
    return c1 == c2 ? "=:" : c1 > c2 ? "1:" : "2:";
  }
}

__________________________________________________
using System;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public class Mixing
{
    public static string Mix(string s1, string s2)
    {
        var l1 = from x in Regex.Replace(s1, "[^a-z]", "").ToList()
                 group x by x into g
                 where g.Count() > 1
                 select new { ch = g.Key, count = g.Count() };

        var l2 = from x in Regex.Replace(s2, "[^a-z]", "").ToList()
                 group x by x into g
                 where g.Count() > 1
                 select new { ch = g.Key, count = g.Count() };

        return string.Join("/", (from x in l1.Select(a => a.ch).Union(l2.Select(a => a.ch))
                                 join y in l1 on x equals y.ch into y_
                                 from y in y_.DefaultIfEmpty()
                                 join z in l2 on x equals z.ch into z_
                                 from z in z_.DefaultIfEmpty()
                                 select new
                                 {
                                     count = y == null ? z.count : (z == null ? y.count : Math.Max(y.count, z.count)),
                                     ch = y == null ? z.ch : y.ch,
                                     symbol = y == null ? '2' : (z == null ? '1' :
                                     (y.count > z.count ? '1' : (y.count == z.count ? '=' : '2')))
                                 })
                             .OrderByDescending(a => a.count)
                             .ThenBy(a => a.symbol)
                             .ThenBy(a => a.ch)
                             .Select(a => a.symbol + ":" + string.Concat(Enumerable.Repeat(a.ch, a.count))));
    }
}

__________________________________________________
using System;
using System.Linq;

public class Mixing 
{
  public static string Mix(string s1, string s2)
  {
      return string.Join("/", Enumerable.Range('a', 'z')
          .Select(p => Tuple.Create((char)p, s1.Count(q => q == p), s2.Count(q => q == p)))
          .Where(p => p.Item2 > 1 || p.Item3 > 1)
          .Select(p => Tuple.Create(p.Item1, p.Item2 < p.Item3 ? 2 : p.Item2 > p.Item3 ? 1 : 5, Math.Max(p.Item2, p.Item3)))
          .OrderByDescending(p => p.Item3)
          .ThenBy(p => p.Item2)
          .ThenBy(p => p.Item1)
          .Select(t => (t.Item2 == 5 ? "=" : t.Item2.ToString()) + ":" + new string(t.Item1, t.Item3)));
  }
}

__________________________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class Mixing 
{
  public static string Mix(string s1, string s2)
  {
      var matches = new List<Match>();
  
      for (var i = 97; i <= 122; i++)
      {
          matches.Add(new Match(s1, s2, (char) i));
      }
      
      return String.Join("/", matches.Where(x => x.Text != null)
                                     .OrderBy(x => x.Highest)
                                     .OrderByDescending(x => x.Occurences)
                                     .Select(x => x.Text)
                                     .ToArray());
  }
}

public class Match
{
    public Match(string s1, string s2, char c)
    {
        var n1 = s1.Count(x => x==c);
        var n2 = s2.Count(x => x==c);
        Occurences = Math.Max(n1, n2);
        Highest = n1 > n2 ? 1 : n1 < n2 ? 2 : 3;
        
        if (Occurences > 1)
        {
            Text = Highest == 3 ? "=" : Highest.ToString();
            Text += ":" + new String(c, Occurences);
        }
    }
    
    public int Occurences { get; private set; }
    public int Highest { get; private set; }
    public string Text { get; private set; }    
}

__________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Mixing 
{
  public static string Mix(string s1, string s2)
  {
    char[] lowerCaseletters = new char[] { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' };

    Dictionary<char, int> d1 = new Dictionary<char, int>();
    Dictionary<char, int> d2 = new Dictionary<char, int>();

    var s11 = s1.Where(x => lowerCaseletters.Contains(x));
    var s22 = s2.Where(x => lowerCaseletters.Contains(x));

    foreach (var letter in s11) { if (!d1.ContainsKey(letter)) { d1.Add(letter, 1); } else { d1[letter]++; } }
    foreach (var letter in s22) { if (!d2.ContainsKey(letter)) { d2.Add(letter, 1); } else { d2[letter]++; } }

    foreach (var item in d1.Where(item => item.Value < 2).ToList()) d1.Remove(item.Key);
    foreach (var item in d2.Where(item => item.Value < 2).ToList()) d2.Remove(item.Key);

    foreach (var item in d1.Keys.ToList()) { if (d2.Keys.Contains(item)) { if (d1[item] > d2[item]) { d2.Remove(item); } else if (d1[item] < d2[item]) { d1.Remove(item); } } }

    List<string> res = new List<string>();
    foreach (var item in d1.Keys.ToList()) { if (d2.Keys.Contains(item)) { res.Add($"=:{new string(item, d1[item])}"); d2.Remove(item); d1.Remove(item); } else { res.Add($"1:{new string(item, d1[item])}"); } }
    foreach (var item in d2.Keys.ToList()) { res.Add($"2:{new string(item, d2[item])}"); }


    return string.Join("/", res.OrderByDescending(x=>x.Length).ThenBy(y=>y[0]).ThenBy(z=>z[2]));
  }
}
