import java.math.BigInteger;
import java.util.Arrays;

public class ProdSeq {
    public static BigInteger[] solve(int[] arr) {
        BigInteger a,A,B,C,D;
      A=BigInteger.valueOf(arr[0]*arr[2] + arr[1]*arr[3]);  
      B=(BigInteger.valueOf(arr[0]*arr[3] - arr[2]*arr[1])).abs();
  
      for(int i=4;i<arr.length;i+=4)
      {
            C = BigInteger.valueOf(arr[i]*arr[i+2] + arr[i+1]*arr[i+3]);  
            D = (BigInteger.valueOf(arr[i]*arr[i+3] - arr[i+2]*arr[i+1])).abs();
            
            a=A;
            A = A.multiply(C).add(B.multiply(D));
            B = (a.multiply(D).subtract(B.multiply(C))).abs();
      }
      
      return new BigInteger[] {A,B};
    }
}
_____________________________________
import java.math.BigInteger;
import java.util.Arrays;
import java.lang.Math;

public class ProdSeq {
  public static BigInteger[] solve(int[] arr) {
    BigInteger A = BigInteger.valueOf(arr[0] * arr[2] + arr[1] * arr[3]);
    BigInteger B = BigInteger.valueOf(arr[0] * arr[3] - arr[1] * arr[2]);
    
    for (int i = 4; i < arr.length; i +=2) {
      BigInteger oldA = A;
      A = A.multiply(BigInteger.valueOf(arr[i])).add(B.multiply(BigInteger.valueOf(arr[i+1])));
      B = oldA.multiply(BigInteger.valueOf(arr[i+1])).subtract(B.multiply(BigInteger.valueOf(arr[i])));
    }
    
    BigInteger[] res = {A.abs(), B.abs()};
    return res;
  }
}
_____________________________________
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;import java.util.Arrays;

public class ProdSeq {
    public static BigInteger[] solve(int[] arr)
    {
  BigInteger[] result = new BigInteger[2];
    result[0] = BigInteger.valueOf(arr[0]);
    result[1] = BigInteger.valueOf(arr[1]);
    for(int i = 2; i<arr.length;i=i+2)
    {
      BigInteger n3 = BigInteger.valueOf(arr[i]);
      BigInteger n4 = BigInteger.valueOf(arr[i+1]);
      BigInteger p1 = result[0].multiply(n3);
      BigInteger p2 = result[1].multiply(n4);
      BigInteger p3 = result[0].multiply(n4);
      BigInteger p4 = result[1].multiply(n3);
      result[0] =p1.add(p2);
      result[1]=p3.subtract(p4);
      if(result[1].compareTo(BigInteger.ZERO)==-1)
      {
        result[1] = result[1].negate();
      }
      

    }
    return result;
    }
}
_____________________________________
import java.math.BigInteger;
import java.util.Arrays;

public class ProdSeq {
    private static BigInteger[] h(BigInteger[] a) {
        BigInteger x = a[0], y = a[1], z = a[2], t = a[3];
        BigInteger p = x.multiply(z).subtract(y.multiply(t));
        BigInteger q = x.multiply(t).add(y.multiply(z));
        BigInteger[] res = new BigInteger[]{p.abs(), q.abs()};
        return res;
    }
    public static BigInteger[] solveAux(BigInteger[] arr) {
        if (arr.length == 4)
            return h(arr);
        BigInteger[] a1 = h(Arrays.copyOfRange(arr, 0, 4));
        BigInteger[] a2 = Arrays.copyOfRange(arr, 4, arr.length);  
        BigInteger[] a = new BigInteger[a1.length + a2.length];
        System.arraycopy(a1, 0, a, 0, a1.length);
        System.arraycopy(a2, 0, a, a1.length, a2.length);
        return solveAux(a);
    }
    public static BigInteger[] solve(int[] arr) {
        BigInteger[] bigs = Arrays.stream(arr).mapToObj(BigInteger::valueOf).toArray(BigInteger[]::new);
        return solveAux(bigs);
    }
}
