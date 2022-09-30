55b2549a781b5336c0000103


using System;

public class Kata {
    public static int ComparePowers( int[] a, int[] b ) {
        var l1 = Math.Log10( a [ 0 ] )*a [ 1 ];
        var l2 = Math.Log10( b [ 0 ] )*b [ 1 ];
        return l2.CompareTo( l1 );
    }
}
________________________________
using System;
class Kata
{
    public static int ComparePowers(int[] a, int[] b)
    {
        double h=Math.Log(Convert.ToInt64(b[0]),Convert.ToInt64(a[0]));
        double right = Convert.ToInt64(b[1])*h;
        double left = Convert.ToInt64(a[1]);
        return right>left?1:right==left?0:-1;
    }
}
________________________________
using System;
class Kata
{
  public static int ComparePowers(int[] left, int[] right) => (Math.Log10(right[0]) * right[1]).CompareTo(Math.Log10(left[0]) * left[1]);
}
