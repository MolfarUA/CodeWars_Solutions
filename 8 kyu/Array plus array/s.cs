5a2be17aee1aaefe2a000151


using System.Linq;

public static class Kata
{
  public static int ArrayPlusArray(int[] arr1, int[] arr2)
  {
    return arr1.Sum()+arr2.Sum();
  }
}
_________________________
using System;
using System.Linq;
public static class Kata
{
  public static int ArrayPlusArray(int[] arr1, int[] arr2)
  {
    return arr1.Sum() + arr2.Sum();
  }
}
_________________________
public static class Kata
{
  public static int ArrayPlusArray(int[] arr1, int[] arr2)
  {
    var result = 0;
    
    foreach(var number in arr1)
      result += number;
      
    foreach(var number in arr2)
      result += number;
      
    return result;
  }
}
