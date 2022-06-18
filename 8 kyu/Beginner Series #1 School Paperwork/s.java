55f9b48403f6b87a7c0000bd


import static java.lang.Math.max;

public class Paper {

  public static int paperWork(int n, int m) {
    return max(m, 0) * max(n, 0);
  }

}
__________________________
public class Paper
{
  public static int paperWork(int n, int m) 
  {
    return n>0&&m>0 ? m*n : 0;
  }
}
__________________________
interface Paper {
  static int paperWork(int n, int m) {
    return n > 0 && m > 0 ? n * m : 0;
  }
}
__________________________
public class Paper
{
  public static int paperWork(int n, int m) 
  {
  if (m <=0 || n <= 0) {
    return 0;
    
  } else if (m >= 1 || n >= 1) {
    return n * m;
    
  }
   return n * m;
  
  }
}
