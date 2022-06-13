using System.Numerics;
using System.Linq;

public class Kata
{
  public static BigInteger[] PowersOfTwo(int n)
  {
    return (from x in Enumerable.Range(0, n+1) select BigInteger.Pow(2, x)).ToArray();
  }
}
___________________________________
using System.Linq;
using System.Numerics;

public class Kata
{
  public static BigInteger[] PowersOfTwo(int n)
  {
    return Enumerable.Range(0, n+1).Select(x => BigInteger.Pow(2, x)).ToArray();
  }
}
___________________________________
using System.Linq;
using System.Numerics;

public class Kata
{
  public static BigInteger[] PowersOfTwo(int n)
  {
    return Enumerable.Range(0, n + 1).Select(i => BigInteger.One << i).ToArray();
  }
}
___________________________________
using System;
using System.Numerics;

public class Kata
{
  public static BigInteger[] PowersOfTwo(int n)
  {
    BigInteger[] result = new BigInteger[n+1];
    
    for(int i = 0; i < result.Length; i++)
    {
      result[i] = (BigInteger)Math.Pow(2,i);
    }
    
    return result;
  }
}
