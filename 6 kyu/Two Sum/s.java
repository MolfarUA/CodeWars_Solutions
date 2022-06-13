public class Solution
{
    public static int[] twoSum(int[] numbers, int target)
    {
       for(int i = 0; i < numbers.length; i++) {
           for(int j = i + 1; j < numbers.length; j++) {
               if(numbers[i] + numbers[j] == target){
                   return new int[]{i, j};
               }
           }
       }
      return null; 
    }
}
________________________________
public class Solution
{
    public static int[] twoSum(int[] numbers, int target)
    {  
      int[] array = new int[2];
      for(int i=0 ;i< numbers.length;i++){
        for(int j =1;j<numbers.length;j++){
          if(numbers[i]+numbers[j]==target){
            array[0]=i;
            array[1]=j;
            return array;
          }
        }
      } 
      return array;// Do your magic!
    }
}
________________________________
public class Solution
{
    public static int[] twoSum(int[] numbers, int target)
    {
        int[] results = new int[2];
        for (int i = 0; i < numbers.length; i++) {
            for (int j = 0; j < numbers.length; j++) {
                if (target - numbers[i] == numbers[j]) {
                    results[0] = i;
                    results[1] = j;
                }
            }
        }
        return results;
    }
}
________________________________
import java.util.Arrays;
class Solution
{
    public static int[] twoSum(int[] numbers, int target)
    {
        Arrays.sort(numbers);
        for (int indice1 = 0; indice1 < numbers.length; indice1++){
            int indice2 = Arrays.binarySearch(numbers, target-numbers[indice1]);
            if(indice2 > 0 && indice2 != indice1){
                return new int[] {indice1,indice2};
            }
        }
        return null;
    }
}
