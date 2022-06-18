576757b1df89ecf5bd00073b


public class Kata
{
  public static string[] TowerBuilder(int nFloors)
  {
    var result = new string[nFloors];
    for(int i=0;i<nFloors;i++)
      result[i] = string.Concat(new string(' ',nFloors - i - 1),
                                new string('*',i * 2 + 1),
                                new string(' ',nFloors - i - 1));
    return result;
  }
}
_____________________________
using System;
public class Kata
{
  public static string[] TowerBuilder(int nFloors)
  {
            string[] tower = new string[nFloors];
            int spaces = nFloors - 1;
            for (int floor = 0; floor < nFloors; floor++,spaces--)
            {
                int asterisk = floor * 2 + 1;
                tower[floor] = new String(' ', spaces) + new String('*', asterisk) + new String(' ', spaces);
            }            
            return tower;
  }
}
_____________________________
using System.Linq;
public class Kata
{
  public static string[] TowerBuilder(int nFloors)
  {
      return Enumerable.Range(1, nFloors).Select(i => string.Format("{0}{1}{0}", i == nFloors ? "" : new string(' ', nFloors - i), new string('*', 2 * i - 1))).ToArray();
  }
}
_____________________________
using System;
using System.Linq;

public class Kata
{
  public static string[] TowerBuilder(int nFloors)
  {
    return Enumerable.Range(1, nFloors).Select(
      x => new String(' ', nFloors - x)
      + new String('*', x * 2 - 1)
      + new String(' ', nFloors - x)).ToArray();
  }
}
_____________________________
using System.Linq;

public class Kata
{
  public static string[] TowerBuilder(int nFloors)
  {
    return Enumerable.Range(0, nFloors).Select(x => new string('*', x * 2 + 1).PadLeft(nFloors + x).PadRight(nFloors * 2 - 1)).ToArray();
  }
}
_____________________________
using System.Linq;

public class Kata
{
    public static string FloorBuilder(int nFloor, int nFloors)
        => new string(' ', nFloors - nFloor) +
            new string('*', 2 * nFloor - 1) + 
            new string (' ', nFloors - nFloor);

    public static string[] TowerBuilder(int nFloors)
        => Enumerable.Range(1, nFloors)
            .Select(n => FloorBuilder(n, nFloors))
            .ToArray();
}
