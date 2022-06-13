public class BouncingBall {
  
  public static int bouncingBall(double h, double bounce, double window) {
    if(h <= 0 || bounce <= 0 ||bounce >= 1 || window >= h) return -1;
    int result = -1;
  
    do{
      result+=2;
      h*=bounce;
    }while(h>window);
  
    return result;
  }
}
_______________________________________________
public class BouncingBall {
  
  public static int bouncingBall(double h, double bounce, double window) {
    if (h <= 0 || bounce <= 0 || bounce >= 1 || window >= h || window <= 0) return -1;
    return 2 + bouncingBall(h * bounce, bounce, window);
  }
}
_______________________________________________
using System;

public class BouncingBall {
  
  public static int bouncingBall(double h, double bounce, double window) {
      if (h <= 0 || bounce < 0 || bounce > 1 || window >= h)
        return -1;
        
      return (int) Math.Ceiling(Math.Log(window / h, bounce)) * 2 - 1;
  }
}
_______________________________________________
public class BouncingBall {
  
  public static int bouncingBall(double h, double bounce, double window) {
      if (h > 0 && (bounce > 0 && bounce < 1) && window < h)
      {
          var ret = 0;
          while(h > window)
          {
              h = h * bounce;
              if(ret == 0)
                ret++;
              else
                ret = ret + 2;
          }
          return ret;
      }
      return -1;           
  }
}
_______________________________________________
public class BouncingBall {
  
  public static int bouncingBall(double h, double bounce, double window) {
            if(h > 0 && window < h && bounce > 0 && bounce < 1)
            {
                int count = 0;
                while(h > window)
                {
                    h *= bounce;
                    count++;
                }
                return count * 2 - 1;
            }
            else
            {
                return -1;
            }
  }
}
