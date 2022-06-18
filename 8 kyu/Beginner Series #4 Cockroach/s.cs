55fab1ffda3e2e44f00000c6


  using System;
  public class Cockroach
  {
    public static int CockroachSpeed(double x)
      => (int) (x / 0.036);
  }
__________________________
using System;
public class Cockroach
{
    public static int CockroachSpeed(double x)
    {
        return (int) (x *  27.778);
    }
}
__________________________
using System;
public class Cockroach
{
    public static int CockroachSpeed(double x)
    {
        return (int)Math.Floor(x * 1000 / 36);
    }
}
__________________________
  using System;
  public class Cockroach
  {
    const double convertKmHr2CmSec = 27.77777777777778;
    public static int CockroachSpeed(double x)
    {
      return (int)Math.Floor(x * convertKmHr2CmSec);
    }
  }
__________________________
  using System;
  public class Cockroach
  {
    public static int CockroachSpeed(double x)
    {
      return (int)(x * 100000 / 3600);
    }
  }
