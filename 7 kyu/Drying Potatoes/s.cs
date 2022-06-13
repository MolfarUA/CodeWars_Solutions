public class DryPotatoes
{

    public static int Potatoes(int p0, int w0, int p1)
    {
        return w0 * (100 - p0) / (100 - p1);
    }
}
_______________________________________________
public class DryPotatoes
{
  public static int Potatoes(int p0, int w0, int p1) => (100 - p0) * w0 / (100 - p1);
}
_______________________________________________
public class DryPotatoes
{

    public static int Potatoes(int p0, int w0, int p1)
    {
        int w1 = w0 * (100 - p0) / (100 - p1);
      return w1;
    }
}
_______________________________________________
using System;

public class DryPotatoes
{
    public static int Potatoes(int p0, int w0, int p1)
    {
        double result = (100-p0)*w0 /(100-p1);
        result = result%1>=0.99?Math.Ceiling(result):Math.Floor(result);
        return (int)result;
    }
}
_______________________________________________
public class DryPotatoes
{

    public static int Potatoes(int p0, int w0, int p1)
    {
        // your code
     double suhoiProcent = 100 - (double)p0;
      double suhoiVes = ((double)w0 / 100) * suhoiProcent;
      double procentPosleSushki = 100 - (double)p1;
      double suhoePosleSushki = suhoiVes / procentPosleSushki;
     double itog = suhoePosleSushki * 100;
      return (int)itog;
    }
}
