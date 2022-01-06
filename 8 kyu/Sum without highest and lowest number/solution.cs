using System;
using System.Linq;

public static class Kata
{
    public static int Sum(int[] numbers)
    {
        return numbers == null || numbers.Length < 2
            ? 0
            : numbers.Sum() - numbers.Max() - numbers.Min();
    }
}
________________________________________
using System;
using System.Linq;

public static class Kata
{
    public static int Sum(int[] numbers)
    {
        if (numbers == null || numbers.Length < 2) 
        {
            return 0;
        }
    
        int min = int.MaxValue;
        int max = int.MinValue;
        int sum = 0;
        
        foreach(var x in numbers) 
        {
            if (x > max) max = x;
            if (x < min) min = x;
            sum += x;
        }
        
        return sum - min - max;
    }
}
________________________________________
using System.Linq;

public static class Kata
{
  public static int Sum(int[] n) => (n?.Length ?? 0) > 1 ? n.Sum() - n.Max() - n.Min() : 0;
}
