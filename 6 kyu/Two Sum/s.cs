using System;
public class Kata
{
  public static int[] TwoSum(int[] numbers, int target)
  {
     for (int i = 0; i < numbers.Length; i++)
         for (int j = i + 1; j < numbers.Length; j++)
             if (numbers[i] + numbers[j] == target)
                return new int[] { i, j };
                
     return new int[0];
  }
}
________________________________
public class Kata
{
  public static int[] TwoSum(int[] numbers, int target)
  {
    for(int i = 0; i < numbers.Length - 1; i++)
    {
      for(int u = i + 1; u < numbers.Length; u++)
      {
        if(numbers[i] + numbers[u] == target)
          return new int[]{ i, u };
      }
    }
    return null;
  }
}
________________________________
using System;
using System.Collections.Generic;

public class Kata
{
  public static int[] TwoSum(int[] numbers, int target)
  {
    var targets = new Dictionary<int, int>();

    for (var i = 0; i < numbers.Length; i++) {
      int match = target - numbers[i];
      if (targets.ContainsKey(match)) {
        return new int[] {i, targets[match]};
      }
      targets[numbers[i]] = i;
    }

    throw new ArgumentException("Bad numbers");
  }
}
________________________________
using System;
using System.Linq;

public class Kata
{
  public static int[] TwoSum(int[] numbers, int target)
  {
    int[] arr = new int[2];
    Random rand = new Random();
    while(true)
    {
      arr[0] = rand.Next(0, numbers.Length);
      arr[1] = rand.Next(0, numbers.Length);
      if(arr[0] == arr[1]) continue;
      if(numbers[arr[0]] + numbers[arr[1]] == target) break;
    }
    return arr.OrderBy(a => a).ToArray();
  }
}
