53ee5429ba190077850011d4


class Java {
  public static int doubleInteger(int i) {
    return i*2;
  }
}
__________________________
class Java {
  public static int doubleInteger(int i) {
    // Double the integer and return it!
    return i<<1;
  }
}
__________________________
interface Java {
  static int doubleInteger(int i) {
    return i + i;
  }
}
__________________________
class Java {
  public static int doubleInteger(int i) {
    long result = i * 2;
    if (result > Integer.MAX_VALUE) return Integer.MAX_VALUE;
    if (result < Integer.MIN_VALUE) return Integer.MIN_VALUE;
    
    return (int) result;
  }
}
