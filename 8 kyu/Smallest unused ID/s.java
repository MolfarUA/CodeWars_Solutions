55eea63119278d571d00006a


import java.util.stream.IntStream;

public class Kata {
  public static int nextId(int[] ids) {
    return IntStream.range(0, ids.length + 1).filter(id -> !IntStream.of(ids).anyMatch(x -> x == id)).findFirst().getAsInt();
  }
}
______________________
public class Kata {
    public static int nextId(int[] ids) {
        int minId = 0;
        for (int i = 0; i < ids.length;) {
            if (minId == ids[i]) {
                minId += 1;
                i = 0;
            } else {
                i++;
            }
        }
        return minId;
    }
}
______________________
public class Kata {
    public static int nextId(int[] ids) {
      int largest = 0;
      int smallest = -1;
    
      for (int num: ids) {
        if (num > largest) largest = num;
      } // O(n)
      
      boolean arr[] = new boolean[largest+1];
      
      for(int i = 0; i < arr.length; i++) {
        arr[i] = false;
      }  // O(n)
      
      for (int num: ids) {
        arr[num] = true;
      } // O(n)
      
      for(int i = 0; i < arr.length; i++) {
        if (arr[i] == false) {
          smallest = i; 
          break;
        }
      } // O(n)
      
      if (smallest == -1)  smallest = arr.length;
      
      
      return smallest; // time complexity = O(n)
    }
}
