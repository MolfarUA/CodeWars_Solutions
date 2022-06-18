56d0a591c6c8b466ca00118b


public class Triangular
{
    public bool isTriangular(int x) {
        return IsSquare(1 + 8L * x);
    }
    static bool IsSquare(long x) {
        long r = (long)System.Math.Sqrt(x);
        return r * r == x;
    }
}
__________________________
using System;

public class Triangular
{
    public bool isTriangular(int T) => Math.Sqrt(8L * T + 1) % 1 == 0;
}
__________________________
using System;
public class Triangular
{
  public bool isTriangular(int T)
  {
    int i = 1;
    while (T > 0) T -= i++;
    return (T == 0);
  }
}
__________________________
public class Triangular
{
    public bool isTriangular(int T) => IsTriangular(T);
    private static bool IsTriangular(long t) => System.Math.Sqrt(8 * t + 1) % 1 == 0;
}
__________________________
using System;
public class Triangular
{
    public bool isTriangular(int T){
        double D = 1 - 4 * (-2L * T);
        return Math.Sqrt(D) == Math.Floor(Math.Sqrt(D));
    }
}
