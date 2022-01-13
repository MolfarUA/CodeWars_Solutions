using System.Collections;

using static System.Math;

public class PiApprox
{
    public static ArrayList iterPi(double epsilon)
    {
        var sum = 0.0;
        var i = 0;

        do
        {
            sum += (i % 2 == 0 ? 4.0 : -4.0) / (2 * i + 1);
            ++i;
        }
        while (Abs(PI - sum) >= epsilon);

        return new ArrayList { i, Round(sum, 10) };
    }
}
________________________________________
using System;
using System.Collections;

public static class PiApprox
{
  public static ArrayList iterPi(double epsilon)
  {
    double myPi = 0.0;
    int i = 0;
    while (Math.Abs(myPi - Math.PI) > epsilon)
      myPi += 4 * Math.Pow(-1, i) / (2 * i++ + 1);
    return new ArrayList {i, Math.Round(myPi, 10, MidpointRounding.AwayFromZero)};
  }
}
________________________________________
using System;
using System.Collections;
public class PiApprox
        {
            public static ArrayList iterPi(double epsilon)
            {
                 double myPI = 0d;
            double sum = 0d;
            int n = 0;
            while (Math.Abs(Math.PI - myPI) > epsilon)
            {
                sum = sum + Math.Pow(-1,n) / (2 * n + 1);
                n++;
                myPI = 4 * sum;
            }
           
            return new ArrayList{n, Math.Round(myPI,10)};
            }
        }
________________________________________
using System.Collections;
using System;
public class PiApprox
        {
            public static ArrayList iterPi(double epsilon)
            {
                double pp = 0 , ci = (1/epsilon>=100000 ? 1/epsilon+1 : 1/epsilon);
                for ( double i=0 , db=1 ; i<ci ; i++ , db+=2 ) pp+=( i%2==1 ? -1/db : 1/db );
                return new ArrayList{ Math.Round(ci,0) , Math.Round(pp*4,10) };
            }
        }
________________________________________
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public class PiApprox
        {
            public static ArrayList iterPi(double epsilon)
            {
                ArrayList res = new ArrayList { };
                double n = 1.0; double value = 0; int counter = 0;
                while (Math.Abs((Math.PI - 4 * value)) > epsilon)
                {
                    value += 1.0 / n;
                    n = -n;
                    if (n > 0) n += 2.0;
                    if (n < 0) n -= 2;
                    counter += 1;
                }
                res.Add(counter); res.Add(Math.Round(4 * value, 10));
                return res;
            }
        }
