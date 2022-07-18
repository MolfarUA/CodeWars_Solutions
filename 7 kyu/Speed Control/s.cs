56484848ba95170a8000004d


using System;
using System.Linq;

public class GpsSpeed 
{
    public static int Gps(int s, double[] x) 
    {
      if(x.Length > 2)
      {
        var averageSpeeds = x.Skip(1).Select((distance, index) => ((distance - x[index]) / s) * 3600);
        return Convert.ToInt32(Math.Floor(averageSpeeds.Max()));
      }
      
      return 0;
    }
}
_____________________________
using System.Linq;

public class GpsSpeed
{
  public static int Gps(int s, double[] x)
  {
    return (int) (x.Length < 2 ? 0 : x.Zip(x.Skip(1), (a, b) => b - a).Max() * 3600 / s);
  }
}
_____________________________
using System;

public class GpsSpeed {
    
    public static int Gps(int s, double[] x) {        
        if(x.Length <= 1)
          return 0;
        
        double max = x[0];
        
        for(int i=1; i<x.Length; i++)
            max = Math.Max(max, x[i] - x[i-1]);        
        
        return (int) Math.Ceiling(3600.0 * max / s);
    }
}
_____________________________
using System.Linq;
using static System.Math;

public class GpsSpeed
{  
    public static int Gps(int s, double[] x)
    {
        return x.Length <= 1 ? 0 : (int)Floor(Enumerable.Range(0, x.Length - 1).Select(i => Abs(x[i] - x[i + 1]) * 3600 / s).Max());
    }
}
