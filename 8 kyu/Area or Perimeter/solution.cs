public class MathCheck {
    public static int AreaOrPerimeter(int l, int w) => (l == w) ? l * w : 2 * (l + w);
        
    }
#############
public class MathCheck {
    public static int AreaOrPerimeter(int l, int w) {
        return l == w ? l * w : (l + w) * 2;
    }
}
###########
public class MathCheck 
{
    public static int AreaOrPerimeter(int l, int w) => l == w ? l * w : l + l + w + w;
}
############
using System;
using System.Linq;
public class MathCheck {
  public static int AreaOrPerimeter(int l, int w) => l!=w ? 2*l + 2*w: l*w;
}
#############
public class MathCheck {
    public static int AreaOrPerimeter(int l, int w) {
        if(l==w){
          return l*w;
        }
      else
        {
        int p=2*l+2*w;
        
        return p;
      }
    }
}
###############
using System;
public class MathCheck {
    public static int AreaOrPerimeter(int l, int w) => l == w ? (int) Math.Pow(l, 2) : 2 * l + 2 * w;
}
###########
public class MathCheck {
    public static int AreaOrPerimeter(int l, int w) {
        if (l != w)
            {
                int per = (l+w)*2;
                return per;
            }
            return l * w;
    }
}
