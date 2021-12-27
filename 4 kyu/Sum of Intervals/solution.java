package cw;

import java.util.Arrays;
import java.util.stream.IntStream;

public class Interval {

    public static int sumIntervals(int[][] intervals) {
        return intervals == null ? 0 : (int) Arrays.stream(intervals)
            .flatMapToInt(interval -> IntStream.range(interval[0], interval[1]))
            .distinct()
            .count();
    }
}

________________________
package cw;

import java.util.Arrays;
import java.util.stream.IntStream;

public class Interval {

    public static int sumIntervals(int[][] intervals) {
        return intervals == null ? 0 : (int) Arrays.stream(intervals)
            .flatMapToInt(interval -> IntStream.range(interval[0], interval[1]))
            .distinct()
            .count();
    }
}

_____________________
package cw;

import java.util.Comparator;

public class Interval {

  public static int sumIntervals(int[][] intervals) {
    if (intervals == null) return 0;
    else if (intervals.length == 0) return 0;
    else if (intervals[0].length == 0) return 0;
    java.util.Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
    int sum = 0, min = intervals[0][0], max = intervals[0][1];
    for (int[] interval : intervals) {
      if (min < interval[0] && max >= interval[0]) {
        if (max < interval[1]) max = interval[1];
      } else if (max < interval[0]) {
        sum += (max - min);
        min = interval[0];
        max = interval[1];
      }
    }
    sum += (max - min);
    return sum;
  }
}

__________________________
package cw;
import java.util.*;
public class Interval {

    public static int sumIntervals(int[][] intervals) {
        if(intervals == null)
        {
          return 0;
        }
        HashSet<Integer> ints = new HashSet<Integer>();
        for(int i=0; i<intervals.length; i++)
        {
          for(int j=intervals[i][0]; j<intervals[i][1]; j++)
          {
            ints.add(j);
          }
        }
        return ints.size();
    }
}

_________________
package cw;
import java.util.*;

public class Interval {

    public static int sumIntervals(int[][] intervals) 
    {
        if (intervals == null)
          return 0;
          
        Set<Integer> set = new HashSet<Integer>();
        for(int i = 0; i < intervals.length; i++)
            for(int j = intervals[i][0]; j < intervals[i][1]; j++)
                set.add(j);
        
        return set.size();
    }
}
