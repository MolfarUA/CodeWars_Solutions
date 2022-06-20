55466989aeecab5aac00003e


import java.util.*;
public class SqInRect {
  public static List<Integer> sqInRect(int lng, int wdth) {
    if (lng == wdth) return null;
    List<Integer> squares = new ArrayList<Integer>();
    int area = lng * wdth;
    while (area > 0) {
      squares.add(Math.min(lng,wdth));
      if (wdth > lng)wdth = wdth - lng;
      else lng = lng - wdth;
      area = lng * wdth;
    }
    return squares;
  }
}
______________________________
import java.util.*;

public class SqInRect {
  
  private static void recurse(int l, int w, List<Integer> result) {
    int min = Math.min(l, w);
    int max = Math.max(l, w);
    if (min == 0) {
      return;
    }
    result.add(min);
    recurse(max - min, min, result);
  }
  
  public static List<Integer> sqInRect(int lng, int wdth) {
    List<Integer> result = new ArrayList<Integer>();
    recurse(lng, wdth, result);
    if (result.size() == 1) {
        // Dagnabit boys, we been given a square, and we don't do no RE-GU-LAR quadrilaterals roun' here!
        return null;
    }
    return result;
  }
}
______________________________
import java.util.*;

public class SqInRect {
  public static List<Integer> sqInRect(int min, int max) {
    if (max == min) {
      return null;
    }
    List<Integer> sqInRect = new ArrayList<>();
    for (; max > 0 && min > 0; max -= min) {
      if (min > max) {
        int foo = max;
        max = min;
        min = foo;
      }
      sqInRect.add(min);
    }
    return sqInRect;
  }
}
