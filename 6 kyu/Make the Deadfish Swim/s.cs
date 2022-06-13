using System.Collections.Generic;

public class Deadfish
{
  public static int[] Parse(string program)
  {
    var output = new List<int>();
    
    int value = 0;
    
    foreach (var instruction in program)
    {
      switch (instruction)
      {
        case 'i':
          ++value;
          break;
        case 'd':
          --value;
          break;
        case 's':
          value *= value;
          break;
        case 'o':
          output.Add(value);
          break;
      }
    }
    
    return output.ToArray();
  }
}
__________________________________________
using System.Linq;
using System.Collections.Generic;

public class Deadfish
{
  public static int[] Parse(string data, int i = 0)
  {
    return data.Aggregate(new List<int>(), (a, c) =>
    {
        if (c == 'i') i++;
        else if (c == 'd') i--;
        else if (c == 's') i *= i;
        else if (c == 'o') a.Add(i);
        return a;
    }).ToArray();
  }
}
__________________________________________
using System.Collections.Generic;

public class Deadfish
{
  public static int[] Parse(string data)
  {
    int i = 0;
    List<int> result = new List<int>();
    
    foreach(char c in data)
    {
      if(c == 'i') i++;
      else if(c == 'd') i--;
      else if(c == 's') i*= i;
      else if(c == 'o') result.Add(i);      
    }
    return result.ToArray();
  }
}
