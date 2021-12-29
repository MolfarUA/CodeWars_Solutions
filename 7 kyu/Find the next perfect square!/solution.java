public class NumberFun {
  public static long findNextSquare(long sq) {
      long root = (long) Math.sqrt(sq);
      return root * root == sq ? (root + 1) * (root + 1) : -1;
  }
}

_______________________________________
public class NumberFun {
  public static long findNextSquare(long sq) {
      return Math.sqrt(sq) % 1 != 0 ? -1 : (long)Math.pow(Math.sqrt(sq)+1,2);
  }
}

_______________________________________
public class NumberFun {
  public static long findNextSquare(long sq) {
      long result; 
      double d = Math.sqrt(sq);
      
      //if your number d is a integer result will be true, if not will be -1;
      //good luck)!
      if ( d % 1  == 0) {
       result = (long) Math.pow(++d, 2);
      } else result = -1;
      
      return result;
  }
}

_______________________________________
public class NumberFun {
  public static long findNextSquare(long sq) {
      if((long)Math.sqrt(sq) != Math.sqrt(sq)) return -1;
      return sq+(2*(long)Math.sqrt(sq))+1; 
  }
}

_______________________________________
public class NumberFun {
  public static long findNextSquare(long sq) {
      
      double square = Math.sqrt(sq);
      
      if (square % 1 == 0){
          square++;
          return (long) (square*square);
      } else {
          return -1;
      }
  }
}

_______________________________________
import java.math.BigDecimal;

public class NumberFun {
  public static long findNextSquare(long sq) {
        if(!isSquare(sq))
          return -1;
          
        sq++;
        
        for(int i = 0; i < 90000000; i++){
          if(isSquare(sq + i))
            return sq+i;
        }
        
        return -1;
  }
  
  private static boolean isSquare(long in){
    //double sq = Math.sqrt(in);
    BigDecimal bd = new BigDecimal(Math.sqrt(in));

    if(bd.remainder(BigDecimal.ONE) == BigDecimal.ZERO)
      return true;
    
    return false;
  }
}
