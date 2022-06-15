public class Kata {
  public static double[] averages(final int[] numbers) {
    final double res[] = new double[(numbers == null || numbers.length == 0) ? 0 : numbers.length - 1];
    for (int i = 0; i < res.length; i++) res[i] = (numbers[i]+numbers[i+1]) / 2.0;
    return res;
  }
}
____________________________
import java.util.stream.IntStream;

public class Kata
{
    public static double[] averages(int[] numbers)
    {
        return numbers == null || numbers.length<2 
                ? new double[0] 
                : IntStream.range(0, numbers.length-1).mapToDouble(i -> (numbers[i] + numbers[i+1])/2d).toArray();
    }
}
____________________________
public class Kata
{
  public static double[] averages(int[] numbers)
  {
    if (numbers == null || numbers.length < 2) return new double[] {};
    double [] ans = new double [numbers.length - 1];
    for (int i = 0; i < ans.length; i++) ans[i] = (numbers[i] + numbers[i + 1]) / 2.0;
    return ans;
  }
}
____________________________
import static java.util.stream.IntStream.range;

class Kata {
  static double[] averages(int[] nums) {
    return nums != null ? range(0, nums.length - 1).mapToDouble(i -> (nums[i] + nums[i + 1]) / 2.).toArray() : new double[0];
  }
}
____________________________
import java.util.*;

public class Kata
{
  public static double[] averages(int[] numbers)
  {
    if(numbers == null || numbers.length <= 1) return new double[0];
    double[] averageArr = new double[numbers.length-1];
        for(int i = 0; i < averageArr.length; i++){averageArr[i] = (double) (numbers[i] + numbers[i + 1]) / 2;}
        return averageArr;
  }
}
