public class Sum
{
  public int GetSum(int a, int b)
  {
    return (a + b) * (Math.abs(a - b) + 1) / 2;
  }
}

_______________________________________
  public class Sum
  {
    public int GetSum(int a, int b) {
      int res = 0;
      for (int i = Math.min(a, b); i <= Math.max(a, b); i++) {
        res += i;
      }
      return a == b ? a : res;
    }
  }

_______________________________________
import java.util.stream.IntStream;
  
  public class Sum {
     public int GetSum(int a, int b) {
       return IntStream.range(Math.min(a, b), Math.max(a, b) + 1).sum();
     }
  }

_______________________________________
  public class Sum
  {
     public int GetSum(int smaller, int bigger)
     {
        if(bigger<smaller) {
          return GetSum(bigger,smaller);
        }
        else
        {
          /* use Euler's formula to sum up all numbers from 0 to bigger 
          /  and subtract the sum of numbers from 0 to smaller (exclusive)
          */
          return (bigger+smaller)*(bigger-smaller+1)/2;
        }
     }
  }
