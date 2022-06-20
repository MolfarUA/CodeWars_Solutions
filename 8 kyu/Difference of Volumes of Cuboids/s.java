58cb43f4256836ed95000f97


interface CuboidVolumes {
  static int findDifference(int[] a, int[] b) {
    return Math.abs(a[0] * a[1] * a[2] - b[0] * b[1] * b[2]);
  }
}
________________________
public class CuboidVolumes {
  public static int findDifference(final int[] firstCuboid, final int[] secondCuboid) {
    int vol1 = 1, vol2 = 1;
    for (int i = 0; i < 3; i++) {
      vol1 *= firstCuboid[i];
      vol2 *= secondCuboid[i];
    }
    
    return Math.abs(vol1 - vol2);
  }
}
________________________
public class CuboidVolumes {
  public static int findDifference(final int[] firstCuboid, final int[] secondCuboid) {
    return Math.abs(getMulti(firstCuboid) - getMulti(secondCuboid));
  }
  
  public static int getMulti(int[] arr) {
    int sum = 1;
    for (int i = 0; i < arr.length; i++) {
      sum *= arr[i];
    }
    return sum;
  }
}
