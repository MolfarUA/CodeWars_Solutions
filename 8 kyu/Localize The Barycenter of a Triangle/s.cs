5601c5f6ba804403c7000004


using System;

public class Barycenter
{
  public static Double[] BarTriang(Double[] x, Double[] y, Double[] z)
  {
    return new Double[]{
      Math.Round((x[0] + y[0] + z[0]) / 3, 4),
      Math.Round((x[1] + y[1] + z[1]) / 3, 4)
    };
  }
}
__________________________________
using System;

public class Barycenter
{
	public static double[] BarTriang(double[] x, double[] y, double[] z)
	{
		return new double[]{ Math.Round( ( x[0] + y[0] + z[0] ) / 3, 4 ), Math.Round( ( x[1] + y[1] + z[1] ) / 3, 4) };
  }
}
__________________________________
using System.Linq;
using System;
public class Barycenter
{
	public static double[] BarTriang(double[] x, double[] y, double[] z)
	{
		return Enumerable.Range(0,2).Select(i=>Math.Round((x[i]+y[i]+z[i])/3,4)).ToArray();
  }
}
__________________________________
using System;
public class Barycenter
{
	public static double[] BarTriang(double[] x, double[] y, double[] z)
	{
      double[] answer = new double[2];
      answer[0] = Math.Round((x[0]+y[0]+z[0])/3.0D,4); 
      answer[1] = Math.Round((x[1]+y[1]+z[1])/3.0D,4); 
      return answer;
	}	
}
