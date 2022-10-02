55c04b4cc56a697bb0000048


using System;
using System.Linq;
public class Scramblies 
{
    
    public static bool Scramble(string str1, string str2) 
    {
        return str2.All(x=>str1.Count(y=>y==x)>=str2.Count(y=>y==x));
    }

}
______________________________
using System;
using System.Linq;

public class Scramblies 
{
  public static bool Scramble(string str1, string str2)
  {
    var possible = str1.ToList();

    foreach (var c in str2)
    {
      if (!possible.Remove(c))
        return false;
    }

    return true;
  }
}
______________________________
using System.Linq;

public class Scramblies 
{
    
    public static bool Scramble(string str1, string str2) 
    {
        return str2.GroupBy(c => c).All(g => str1.Where(c => c == g.Key).Count() >= g.Count());
    }

}
