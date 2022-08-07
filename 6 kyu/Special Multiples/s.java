55e785dfcb59864f200000d9


public class CountMultiples {
    
    private static boolean isPrime(long n) {
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        for(long i = 3; i <= Math.sqrt(n) + 1; i += 2) {
            if(n % i == 0) return false;
        }
        return true;
    }
    public static long countSpecMult(long n, long mxval) {
        int i = 2, cnt = 1; long mul = 1;
        while (cnt <= n) {
            if (isPrime(i)) {
                cnt++;
                mul *= i;
            }
            i++;
        }
        return (int)Math.floor(mxval / mul);
    }
}
_________________________________
public class CountMultiples {
    
    public static int[] primes = {2, 3, 5, 7, 11, 13, 17, 19, 23};

    public static long countSpecMult(long n, long mxval) {

        int d = 1;
        for (int i = 0; i < n; i++)
            d *= primes[i];

        return mxval / d;
    }
}
_________________________________
public class CountMultiples {
    
    public static long countSpecMult(long n, long m) {
         return (m/(c(n))); 
      }
      public static long c (long n ) { 
          long sum = 1 ; 
             for (int i =2 ;  ; i++) {  
                 boolean is = true ; 
                 for (int j =2 ; j <=Math.sqrt(i); j++) {  
                    if (i%j == 0 ) is = false; 
                 } 
               if (is == true ) {n--; sum*=i; } 
              if (n==0) return sum ; 
             }
          }
  }
