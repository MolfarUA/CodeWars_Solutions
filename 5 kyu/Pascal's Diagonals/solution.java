public class PascalDiagonals {

    public static long[] generateDiagonal(int n, int l) {
        long[] result = new long[l];
        if(l > 0) {
            result[0] = 1;
        }
        for(int i = 1; i < l; i++)
        {
            result[i] =  ( result[i-1] *  (n + i) /  i);
        }
        return result;
    }

}
_______________________________
import java.util.Arrays;
import java.math.BigInteger;
public class PascalDiagonals {

  public static long[] generateDiagonal(int n, int l) {
        if (l == 0) {
            return new long[]{};
        }
        long[] result = new long[l];
        if(n == 0){
            Arrays.fill(result,1);
            return result;
        }
        result[0] = 1;
        long coef = 1;
        BigInteger ak = BigInteger.ONE;
        for (int i = 1; i < l; i++) {
            coef = coef * i;
            ak = ak.multiply(BigInteger.valueOf(n + i));
            result[i] = ak.divide(BigInteger.valueOf(coef)).longValue();
        }
        return result;
  }

}
_______________________________
public class PascalDiagonals {

  public static long[] generateDiagonal(int n, int l) {
    long[] diagonal = new long[l];
    if (l == 0) return diagonal;
    diagonal[0] = 1;
    for (int x=1; x<l; x++) {
      diagonal[x] = diagonal[x-1]*(n+x)/x;
    }
    return diagonal;
  }

}
_______________________________
public class PascalDiagonals {

  public static long[] generateDiagonal(int n, int l) {
    long[] result = new long[l];    
    if (l > 0) {         
      result[0] = 1;
      for (int i = 1; i < l; ++i)
        result[i] = result[i-1] * (n + i) / i;          
    }
    return result;
  }  
}
_______________________________
import java.math.BigInteger;
import java.util.Arrays;
public class PascalDiagonals {

  public static long[] generateDiagonal(int n, int l) {
  
    BigInteger ret[] = new BigInteger[l];
    
    for(int line = 1; line <= l+n; line++) 
    { 
          
    BigInteger C= new BigInteger("1");
    for(int i = 1; i <= line; i++) 
    {  
        if(i-1==n){ret[line-1-n]=C;}
        C = C.multiply(new BigInteger(""+line).subtract(new BigInteger(i+""))).divide(new BigInteger(""+i));  
    } 
    } 
    
    long[] retl = new long[l];
    
    for(int i=0; i<l;i++) {
      
      retl[i] = ret[i].longValue();
    }  
    return retl; 
  }

}
