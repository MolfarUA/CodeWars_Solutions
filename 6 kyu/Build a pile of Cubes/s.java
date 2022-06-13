public class ASum {
  
  public static long findNb(long m) {
    long mm = 0, n = 0;
    while (mm < m) mm += ++n * n * n;
    return mm == m ? n : -1;
  } 
}
_________________________________________
public class ASum {
  
   public static long findNb(long m) {
        long volume = 0;
        final int cubic = 3;
        long numberOfCubes = 0;
        int i = 1;
        while (volume != m) {
            volume += (long) Math.pow(i, cubic);
            i++;
            numberOfCubes++;
            if (volume > m) {
                return -1;
            }
        }
        return numberOfCubes;
    }
}
_________________________________________
public class ASum {
  
  public static long findNb(long m) {
    long n = 0;
        for (int i = 1; i <= m / 2; i++) {
            m = m - (long)Math.pow(i, 3);
            n++;
            if (m == 0) {
                break;
            }
        }
        return (m == 0) ? n : -1;
  } 
}
_________________________________________
public class ASum {
  public static long findNb(long m) {
    long total = 0;                   // Set total at 0; will be tallying this up
    long n = 0;                       // Set n to start cubing at 0 (increments in while loop)
    
    while (total < m) {               // While the total is less than the expected total passed in as parameter...
      n += 1;                         // Increase n by 1, otherwise, stuck at 0 forever
      total += (n * n * n);           // Total is equal to n cubed and add to existing total until no longer less than m
    }

    return (total == m) ? n : -1;     // If the total ends up equal to m, return n, else return -1
  }
}

