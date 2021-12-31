public class Hamming {
  
  public static long hamming(int n) {
    long[] h = new long[n];
    h[0] = 1;
    long x2 = 2, x3 = 3, x5 = 5;
    int i = 0, j = 0, k = 0;
 
    for (int index = 1; index < n; index++) {
      h[index] = Math.min(x2, Math.min(x3, x5));
      if (h[index] == x2) x2 = 2 * h[++i];
      if (h[index] == x3) x3 = 3 * h[++j];
      if (h[index] == x5) x5 = 5 * h[++k];
    }
    
    return h[n - 1];
  }
}

___________________________________________________
import java.util.ArrayList;

public class Hamming {

  public static long hamming(int n) {
  long[] h = new long[n];
    h[0] = 1;
    long x2 = 2, x3 = 3, x5 = 5;
    int i = 0, j = 0, k = 0;
 
    for (int index = 1; index < n; index++) {
      h[index] = Math.min(x2, Math.min(x3, x5));
      if (h[index] == x2) x2 = 2 * h[++i];
      if (h[index] == x3) x3 = 3 * h[++j];
      if (h[index] == x5) x5 = 5 * h[++k];
    }
    
    return h[n-1];
  }
  
}

___________________________________________________
public class Hamming {

  public static long hamming(int n) {
        long[] dp = new long[n + 1];
        dp[1] = 1;
        int p2 = 1, p3 = 1, p5 = 1;
        for (int i = 2; i <= n; i++) {
            long num2 = dp[p2] * 2, num3 = dp[p3] * 3, num5 = dp[p5] * 5;
            dp[i] = Math.min(Math.min(num2, num3), num5);
            if (dp[i] == num2) {
                p2++;
            }
            if (dp[i] == num3) {
                p3++;
            }
            if (dp[i] == num5) {
                p5++;
            }
        }
        return dp[n];
    }
  
}

___________________________________________________
import java.util.TreeSet;
public class Hamming {
  private static Long[] ham;
  private static void initHam() {
    TreeSet<Long> treeHam = new TreeSet<Long>();
    treeHam.add((long) 1);
    long nextLowestHam = 1;
    while (treeHam.size() < 5000) {
      treeHam.add(nextLowestHam * 2);
      treeHam.add(nextLowestHam * 3);
      treeHam.add(nextLowestHam * 5);
      nextLowestHam = treeHam.higher(nextLowestHam);
    }
    ham = treeHam.toArray(new Long[0]);
  }
  public static long hamming(int n) {
    if (ham == null) {
      initHam();
    }
      return ham[n-1];
  }
  
}

___________________________________________________
public class Hamming {

  public static long hamming(int n) 
  {
    long hamm[]=new long[n];
    hamm[0]=1;
    long a=2,b=3,c=5;
    int i=0,j=0,k=0;
    for(int id=1;id<n;id++)
    {
      hamm[id]=Math.min(a,Math.min(b,c));
      if(hamm[id]==a)
        a=2*hamm[++i];
      if(hamm[id]==b)
        b=3*hamm[++j];
      if(hamm[id]==c)
        c=5*hamm[++k];
    }
    return hamm[n-1];
  }
  
}

___________________________________________________
import java.util.Arrays;

public class Hamming {
  
  public static long hamming(int n) {
    long[] nums = new long[n];
        for (int i = 0; i < n; i++) {
            nums[i] = 1;
        }
    
        long[] bases = {2, 3, 5};
        long[] candidates = {2, 3, 5};
        int[] candidates_indexes = {0, 0, 0};

        for (int i = 1; i < n; i++) {
            long nextN = Arrays.stream(candidates).min().getAsLong();
            nums[i] = nextN;

            for (int j = 0; j < candidates.length; j++) {
                if (candidates[j] == nextN) {
                    candidates_indexes[j] += 1;
                    candidates[j] = bases[j] * nums[candidates_indexes[j]];
                }
            }
        }
        return nums[n - 1];
  }  

//  public static long hamming(int n) {
//    if (n > 0 && n < 7) return n;
//         int counterHam = 6;
//         long numberOfHam = 6;
//         while (counterHam < n) {
//             numberOfHam++;
//             if (isNumberOfHamming(numberOfHam)) {
//                 counterHam++;
//             }
//         }
//         return numberOfHam;
//   }
  
//    public static boolean isNumberOfHamming(long numberOfHam) {
//         long res = numberOfHam;

//         while (res != 1) {
//             if (res % 2 == 0)  res /= 2;
//             else if (res % 3 == 0)  res /= 3;
//             else if (res % 5 == 0)  res /= 5;
//             else return false;
//         }
//         return true;
//     }
  
}
