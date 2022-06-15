public class Kata
{
  public static bool IsValidWalk(string[] walk)
  {
    if (walk.Length != 10) return false;
    var x = 0; var y = 0;
    foreach (var dir in walk)
    {
        if (dir == "n") x++;
        else if (dir == "s") x--;
        else if (dir == "e") y++;
        else if (dir == "w") y--;
    }
    return x == 0 && y == 0;
  }
}
__________________________________________
using System.Linq;

public class Kata
{
  public static bool IsValidWalk(string[] walk)
  {
    return walk.Count(x => x == "n") == walk.Count(x => x == "s") && walk.Count(x => x == "e") == walk.Count(x => x == "w") && walk.Length == 10;
  }
}
__________________________________________
public class Kata
{
  public static bool IsValidWalk(string[] walk)
  {
    if (walk.Length != 10) return false;
    var ns = 0;
    var ew = 0;
    for (var n = 0; n < walk.Length; n++)
    {
        switch (walk[n])
        {
            case "n":
                ns++;
                break;
            case "s":
                ns--;
                break;
            case "e":
                ew++;
                break;
            case "w":
                ew--;
                break;
        }
    }
    return ns == 0 && ew == 0;
  }
}
__________________________________________
using System.Linq;

public class Kata
{
  public static bool IsValidWalk(string[] walk)
  {
    return walk.Count() == 10 &&
        walk.Count(c => c == "n") == walk.Count(c => c == "s") &&
        walk.Count(c => c == "w") == walk.Count(c => c == "e");
  }
}
