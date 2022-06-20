5ab6538b379d20ad880000ab


public class Solution {
    public static int areaOrPerimeter (int a, int b) {
        return a == b ? a * b : 2 * ( a + b );
    }
}
________________________
public class Solution {
    public static int areaOrPerimeter (int l, int w) {
       if( l == w){
         return l*l;
       } else if (l != w){
         return (2*l + 2*w);
       }
      return 0;
    }
}
________________________
public class Solution {
    public static int areaOrPerimeter (int l, int w) {
        int output;
        
        if (l == w)
            output = l*w;
        else 
            output = (l+w)*2;
      
      return output;
    }
}
