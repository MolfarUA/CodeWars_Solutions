563f037412e5ada593000114


using System;

public class Kata
{
  public static Int32 CalculateYears(Double Principal, Double Interest, Double Tax, Double DesiredPrincipal)
  {
    var years = 0;
    while (Principal < DesiredPrincipal){
      Principal += Principal * Interest * (1 - Tax);
      years++;
    }
    return years;
  }
}
_________________________
using System;

public class Kata
{
  public static int CalculateYears(double p, double i,  double t, double d)
    {
      int x = 0;
      double amtAdd = 0;
    for(x = 0; p < d; x++){
        p += p*i - ((p*i)*t);
      } 
    return x;
    }
  }
_________________________
using System;

public class Kata
{
  public static int CalculateYears(double p, double i,  double t, double d)
    {
      int x = 0;
      double amtAdd = 0;
    for(x = 0; p < d; x++){
        amtAdd = p*i;
        amtAdd = amtAdd - (amtAdd*t);
        p += amtAdd;
      } 
    return x;
    }
  }
