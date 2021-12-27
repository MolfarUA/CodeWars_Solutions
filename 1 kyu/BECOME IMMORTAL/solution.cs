using System;

public static class Immortal
{
  /// set true to enable debug
  public const bool Debug = true;

  public static long ElderAge(long m, long n, long l, long t)
  {
    long small = Math.Min(m, n);
    long big = Math.Max(m, n);
    long power = (long) Math.Pow(2, Math.Floor(Math.Log(big, 2)));
    long rows = Math.Min(power, small);
    long first = Math.Max(0, -l);
    long terms = Math.Max(0, power - l - 1);
    long x = (terms - first + 1);
    long y = first + terms;

    if (x % 2 > 0) y = (long) Math.Floor((double) (y / 2));
    else if (y % 2 > 0) x = (long) Math.Floor((double) (x / 2));

    long series = y <= 0 ? 0 : ((y % t) * (x % t)) % t;

    long sum = (((series % t) * (rows % t)) % t)
      + (big > power ? ElderAge(big - power, rows, l - power, t) : 0)
      + (small > rows ? ElderAge(power, small - rows, l - rows, t) : 0)
      + (small > rows && big > power ? ElderAge(big - power, small - rows, l, t) : 0);
      
    return sum % t;
  }
}
_____________________________________________________
using System;
using System.Collections.Generic;
using System.Numerics;

public static class Immortal
{
  /// set true to enable debug
  public const bool Debug = true;

  public static long ElderAge(long m, long n, long L, long T)
  {
    return (long)BigInteger.ModPow(myElderAge(m, n, 0, L), 1, T);    
  }
  
  public static BigInteger myElderAge(long ColumnLen, long RowLen, long Shift, long L)
  {
    long n;
    long m;
    // always consider columns as max length. so...
    if (ColumnLen > RowLen)
    {
      m = ColumnLen;
      n = RowLen;
    }
    else
    {
      m = RowLen;
      n = ColumnLen;
    }

    if (n == 0 || m == 0 || L >= (Math.Pow(2, Math.Ceiling(Math.Log(m, 2))) - 1 + Shift))
      return 0;
    // if we have a n*m matrix which m equal power of 2 so
    // we can calculate sum of all matrix members by using this formula
    // p*(p+1)/2 where each row is contain {1,2,3,...,P}
    //just it is neccessery to consider shift-Value and L-Value
    else if (Math.Pow(2, Math.Floor(Math.Log(m, 2))) == m)
    {
      BigInteger rowSum = BigInteger.Multiply((m - 1 + Shift - L), (m + Shift - L)) / 2;
      BigInteger extraPart = L < Shift ? BigInteger.Multiply((Shift - 1 - L), (Shift - L)) / 2 : 0;
      return n * (rowSum - extraPart);
    }
    else
    {                         
      List<long> nList = new List<long>();
      List<long> mList = new List<long>();

      // break column and row to powers of 2   
      long q = (long)Math.Pow(2, Math.Floor(Math.Log(m, 2)));
      mList.AddRange(new long[] { q, m - q });                
      if (n > q)
      {
        long p = (long)Math.Pow(2, Math.Floor(Math.Log(n, 2)));
        nList.AddRange(new long[] { p, n - p });
      }
      //when "n" is less or equal than "m", so there is no need to break it
      else 
        nList.AddRange(new long[] { n, 0 });
                
      // TL:TopLeft , TR:TopRight , BL:BottomLeft, BR:BottomRight
      long newShift;
      newShift = Shift + 0;
      BigInteger TL = myElderAge(nList[0], mList[0], newShift, L);

      newShift = Shift + q;
      BigInteger TR = myElderAge(nList[0], mList[1], newShift, L);

      newShift = Shift + q;
      BigInteger BL = myElderAge(nList[1], mList[0], newShift, L);

      newShift = Shift + 0;
      BigInteger BR = myElderAge(nList[1], mList[1], newShift, L);

      return BigInteger.Add(BigInteger.Add(BigInteger.Add(TL, TR), BL), BR);
    }
  }  
}
__________________________________________________
using System;
using System.Collections.Generic;
using System.Numerics;

public static class Immortal
{
  /// set true to enable debug
  public const bool Debug = true;

  public static long ElderAge(long m, long n, long L, long T)
  {
    return (long)BigInteger.ModPow(myElderAge(m, n, 0, L), 1, T);    
  }
  
  public static BigInteger myElderAge(long ColumnLen, long RowLen, long Shift, long L)
  {
    long n;
    long m;
    // always consider columns as max length. so...
    if (ColumnLen > RowLen)
    {
      m = ColumnLen;
      n = RowLen;
    }
    else
    {
      m = RowLen;
      n = ColumnLen;
    }

    if (n == 0 || m == 0 || L >= (Math.Pow(2, Math.Ceiling(Math.Log(m, 2))) - 1 + Shift))
      return 0;
    // if we have a n*m matrix which m equal power of 2 so
    // we can calculate sum of all matrix members by using this formula
    // p*(p+1)/2 where each row is contain {1,2,3,...,P}
    //just it is neccessery to consider shift-Value and L-Value
    else if (Math.Pow(2, Math.Floor(Math.Log(m, 2))) == m)
    {
      BigInteger rowSum = BigInteger.Multiply((m - 1 + Shift - L), (m + Shift - L)) / 2;
      BigInteger extraPart = L < Shift ? BigInteger.Multiply((Shift - 1 - L), (Shift - L)) / 2 : 0;
      return n * (rowSum - extraPart);
    }
    else
    {                         
      List<long> nList = new List<long>();
      List<long> mList = new List<long>();

      // break column and row to powers of 2   
      long q = (long)Math.Pow(2, Math.Floor(Math.Log(m, 2)));
      mList.AddRange(new long[] { q, m - q });                
      if (n > q)
      {
        long p = (long)Math.Pow(2, Math.Floor(Math.Log(n, 2)));
        nList.AddRange(new long[] { p, n - p });
      }
      //when "n" is less or equal than "m", so there is no need to break it
      else 
        nList.AddRange(new long[] { n, 0 });
                
      // TL:TopLeft , TR:TopRight , BL:BottomLeft, BR:BottomRight
      long newShift;
      newShift = Shift + 0;
      BigInteger TL = myElderAge(nList[0], mList[0], newShift, L);

      newShift = Shift + q;
      BigInteger TR = myElderAge(nList[0], mList[1], newShift, L);

      newShift = Shift + q;
      BigInteger BL = myElderAge(nList[1], mList[0], newShift, L);

      newShift = Shift + 0;
      BigInteger BR = myElderAge(nList[1], mList[1], newShift, L);

      return BigInteger.Add(BigInteger.Add(BigInteger.Add(TL, TR), BL), BR);
    }
  }  
}
_________________________________________________
using System;

public static class Immortal
{
  /// set true to enable debug
  public static bool Debug = false;

  public static long ElderAge(long m, long n, long k, long newp)
        {
            if (m < 1 || n < 1) return 0;
            if (n > m) return ElderAge(n, m, k, newp);
            if (n == 1) return SumRange(0, m, k, newp);
            long ml = HighestOneBit(m);
            long nl = HighestOneBit(n);
            if (ml == nl)
            {
                return ((SumRange(0, ml, k, newp) * (ml % newp)) % newp
                        + (SumRange(ml, 2 * ml, k, newp) * ((m + n - 2 * ml) % newp)) % newp 
                        + ElderAge(m - ml, n - nl, k, newp) 
                ) % newp;
            }
            else
            {
                long delta = Math.Max(0, ml - k); 
                long l1 = Math.Max(0, k - ml); 
                return ((SumRange(0, ml, k, newp) * (n % newp)) % newp
                        + (((delta % newp) * ((m - ml) % newp)) % newp * (n % newp)) % newp
                        + ElderAge(m - ml, n, l1, newp)
                ) % newp;
            }
        }


        private static long SumRange(long a, long b, long k, long newp)
        {
            long maxA = Math.Max(0, a - k);
            long maxB = Math.Max(0, b - k);
            long part1 = maxA + maxB - 1;
            long part2 = maxB - maxA;
            if (part1 % 2 == 0)
                part1 /= 2;
            else
                part2 /= 2;
            return ((part1 % newp) * (part2 % newp)) % newp;
        }

        private static long HighestOneBit(long number)
        {
            long multiplier = 1;
            while (number >= 2)
            {
                multiplier *= 2;
                number /= 2;
            }
            return multiplier;
        }
}
__________________________________
using System;
using System.Numerics;

public class Immortal
{
  public static bool Debug = false;
  
  public static long ElderAge(long n, long m, long k, long newp) =>
    (long)new Immortal() { L = k, T = newp }.RectangleSum(0, 0, n, m);
  
  private long L, T;
  
  private BigInteger RectangleSum(long x, long y, long n, long m)
  {
    if (n < m) (n, m) = (m, n);
    var max = 1L << BitOperations.Log2((ulong)n);
    var sum = SequenceSumWithLoss(x ^ y, max) * BigInteger.Min(m, max);
    if (m > max) sum += RectangleSum(x, y + max, max, m - max);
    if (n > max) sum += RectangleSum(y, x + max, m, n - max);
    return sum % T;
  }
  
  private BigInteger SequenceSumWithLoss(long first, long length) =>
    SequenceSum(Math.Max(first - L, 0), length - Math.Max(L - first, 0));
  
  private BigInteger SequenceSum(BigInteger first, BigInteger length) =>
    length > 0 ? first * length + (length - 1) * length / 2 % T : 0;
}
