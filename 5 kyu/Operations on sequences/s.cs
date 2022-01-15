using System;
using System.Numerics;                  

public class ProdSeq
{
    public static BigInteger[] solve(int[] arr) 
    {
        BigInteger a = 1;
        BigInteger b = 0;
        for (int i = 0; i < arr.Length; i += 2)
        {
          BigInteger temp = a;
          a = BigInteger.Abs(arr[i] * a + arr[i + 1] * b);
          b = BigInteger.Abs(arr[i + 1] * temp - arr[i] * b);
        }
        return new BigInteger[]{a,b};
    }
}
_____________________________________
using System;
using System.Numerics;                  

public class ProdSeq
{
        public static BigInteger[] solve(int[] arr)
        {
            // your code
            BigInteger[] a = new BigInteger[2];
            a[0] = arr[0]; a[1] = arr[1];
            for (int i = 2; i < arr.Length; i += 2)
            {
                var x = a[0];
                var y = a[1];
                a[0] = x * arr[i] - y * arr[i + 1] >= 0 ? x * arr[i] - y * arr[i + 1] : -x * arr[i] + y * arr[i + 1];
                a[1] = x * arr[i + 1] + y * arr[i];
            }
            return a;
        }
}
_____________________________________
using System;
using System.Numerics;                  
using System.Linq;

public class ProdSeq
{
    public static BigInteger[] h(BigInteger[] a) {
        BigInteger p = BigInteger.Subtract(BigInteger.Multiply(a[0], a[2]), BigInteger.Multiply(a[1], a[3]));
        BigInteger q = BigInteger.Add(BigInteger.Multiply(a[0], a[3]), BigInteger.Multiply(a[1], a[2]));
        return new BigInteger[2]{BigInteger.Abs(p), BigInteger.Abs(q)};
    }
    public static BigInteger[] solve(int[] arr) {
        BigInteger[] bigs = arr.Select(i => new BigInteger(i)).ToArray();
        BigInteger[] r = h(new BigInteger[]{bigs[0], bigs[1], bigs[2], bigs[3]});
        for (int i = 4; i < bigs.Length; i += 2) {
            r = h(new BigInteger[4]{r[0], r[1], bigs[i], bigs[i + 1]});
        }
        return r;
    }
}
_____________________________________
using System;
using System.Numerics;                  

public class ProdSeq
{
    public static BigInteger[] solve(int[] arr)
        {
            BigInteger num1 = 1;
            BigInteger num2 = 0;
            for (int i = 0; i < arr.Length; i += 2) 
            { 
            (num1, num2) = (num1 * arr[i] + num2 * arr[i + 1],
                    BigInteger.Abs(num1 * arr[i + 1] - num2 * arr[i])); 
            }
            return new BigInteger[] { num1, num2 };
        }
}
_____________________________________
using System;
using System.Numerics;
using System.Collections.Generic;
using System.Linq;
  
public class ProdSeq
{
         public static BigInteger[] solve(int[] arr) {
        // (x^2+y^2)(w^2+v^2) = (xw+vy)^2 + (xv-yw)^2;
        //x^2*w^2 + x^2*v^2 + y^2*w^2 + v^2*y^2
        //(xw + vy)^2 = (x^2*w^2 + 2*x*y*w*v + v^2*y^2)
        //eliminate 2*x*y*w*v
        //add x^2*v^2 and y^2*w^2
        //x^2*v^2 - 2*x*y*w*v + y^2*w^2
        //(xv-yw)^2
        //(xw+vy)^2 + (xv-yw)^2

        BigInteger[] p = new BigInteger[2];    
        p[0] = arr[0];
        p[1] = arr[1];

        for(int i=2;i<arr.Length;i=i+2)
        {
             BigInteger tmp = p[0]*arr[i+1] + p[1]*arr[i];
             p[1] = BigInteger.Abs(p[0]*arr[i] - p[1]*arr[i+1]);
             p[0] = tmp;
        }
        return p;
     }
}
_____________________________________
using System;
using System.Numerics;                  
public class ProdSeq
{
  public static BigInteger[] solve(int[] arr) {
    BigInteger a = 1;
    BigInteger b = 0;
    for (int i = 0; i < arr.Length; i += 2) (a, b) = (a * arr[i] + b * arr[i+1], BigInteger.Abs(a * arr[i+1] - b * arr[i]));
    return new BigInteger[] { a, b };
  }
}
