52597aa56021e91c93000cb0


using System.Linq;
public class Kata
{
  public static int[] MoveZeroes(int[] arr)
  {
     return arr.OrderBy(x => x==0).ToArray();
  }
}
_____________________________
using System.Linq;
public class Kata
{
  public static int[] MoveZeroes(int[] arr)
  {
    return arr.Where(x=>x!=0).Concat(arr.Where(x=>x==0)).ToArray();
  }
}
_____________________________
using System.Collections.Generic;

public class Kata
{
  public static int[] MoveZeroes(int[] arr)
  {
    var ret = new int[arr.Length];
    var index = 0;
    
    foreach (var item in arr)
    {
      if (item == 0) continue;
      ret[index] = item;
      index++;
    }
    return ret;
  }
}
