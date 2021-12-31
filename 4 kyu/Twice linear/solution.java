import java.util.*;

class DoubleLinear {
    
    public static int dblLinear(int n) {
        if (n == 0) return 1;
        SortedSet<Integer> u = new TreeSet<>();
        u.add(1);
        for(int i=0; i<n; i++) {
            int x = u.first();
            u.add(x*2+1);
            u.add(x*3+1);
            u.remove(x);
        }
        return u.first();
    }
    
}

__________________________________________________
class DoubleLinear {
    
    public static int dblLinear (int n) {
        int[] nums = new int[n + 1];
        nums[0] = 1;
        int i = 0, j = 0, k = 1;
        while (k < n + 1) {
            int y = 2 * nums[i] + 1;
            int z = 3 * nums[j] + 1;
            if (y < z) {
                nums[k++] = y;
                i++;
            } else if (z < y) {
                nums[k++] = z;
                j++;
            } else {
                nums[k++] = z;
                i++;
                j++;
            }
        }
        return nums[n];
    }


}

__________________________________________________
import java.util.TreeSet;

public class DoubleLinear {
    
    public static int dblLinear (int n) {
        TreeSet<Integer> set = new TreeSet<Integer>();
        set.add(1);
        
        for(int i=0;i<n;i++) {
          int x = set.pollFirst();
                  
          set.add(2*x + 1);
          set.add(3*x + 1);
        }
        
        return set.pollFirst();
    }    
}

__________________________________________________
import java.util.ArrayDeque;
import java.util.Deque;

public class DoubleLinear {
    
    public static int dblLinear (int n) {
        Deque<Integer>  deque2 = new ArrayDeque<Integer> ((int)n /2);
        Deque<Integer>  deque3 = new ArrayDeque<Integer> ((int)n /2);
        int cnt = 0, h = 1;
        while (true) {
            if (cnt >= n) return h;
            deque2.addLast(2 * h + 1);
            deque3.addLast(3 * h + 1);
            h = Math.min(deque2.peekFirst(), deque3.peekFirst());
            if (h == deque2.peekFirst())
                deque2.removeFirst();
            if (h == deque3.peekFirst())
                deque3.removeFirst();
            cnt++;
        }
    }
}
