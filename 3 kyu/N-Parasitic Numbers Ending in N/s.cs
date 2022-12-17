55df87b23ed27f40b90001e5


using System.Numerics;
public static class Kata
{
    public static string CalculateSpecial(int d, int b) =>
        CalculateSpecial(d, b, 1);

    public static string CalculateSpecial(int d, int b, BigInteger n) =>
        n % (b * d - 1) != d ? CalculateSpecial(d, b, n * b) :
            convert(d * b * (n - d) / (b * d - 1) + d, b);

    // just getting b-base system representation
    public static string convert(BigInteger x, int b)
        => (x / b > 0 ? convert(x / b, b) : "") + 
            "0123456789abcdef"[(int)(x % b)];

    /* the same non-recursive
    public static string foo(int d, int b)
    {
        int t = b * d - 1, n = 1;
        while (n % t != d) n *= b; // solving b^n == d (mod bd-1)
        return convert(d * b * (n - d) / t + d, b);
    } */
}
____________________________
using System;
using System.Text;
public static class Kata {
  public static string CalculateSpecial(int t, int i) {
    var (l,n,o) = (0,t,new StringBuilder(Convert.ToString(t,i)));
    do {
      l = n*t+l/i;
      n = l%i;
      o.Insert(0,Convert.ToString(n,i));
    } while (l!=t);
    return o.ToString()[1..];
  }
}
____________________________
using System;

public static class Kata
{
  public static string CalculateSpecial(int trailingDigit, int numberBase)
  {
	var divisor = (numberBase * trailingDigit) - 1;
	var x = trailingDigit;
	string result = string.Empty;
	while (true)
	{
		var digit = (x * numberBase) / divisor;
		result = result + Convert.ToString(digit, numberBase);
		if ((result.Length % 2) == 0)
		{
			var mid = result.Length / 2;
			if (result.Substring(0, mid) == result.Substring(mid))
			{
				return result.Substring(mid);
			}
		}
		
		x = (x * numberBase) % divisor;
	}
  }
}
