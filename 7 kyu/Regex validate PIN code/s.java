import java.util.regex.*;

public class Solution {

  public static boolean validatePin(String pin) {
    return pin.matches("\\d{4}|\\d{6}");
  }

}
____________________________
public class Solution {

  public static boolean validatePin(String pin) {
    return pin.matches("[0-9]{4}|[0-9]{6}");
  }

}
____________________________
public class Solution {

  public static boolean validatePin(String pin) {

    if (pin == null || (pin.length() != 4 && pin.length() != 6)) {
      return false;
    }
    
    for (int i = 0; i < pin.length(); i++) {
      if (!Character.isDigit(pin.charAt(i))) {
        return false;
      }
    }
    return true;

  }

}
____________________________
public class Solution {
  public static boolean validatePin(String pin) {
    return pin.matches("\\d{4}|\\d{6}");
  }
}
____________________________
public class Solution {

    private static final int[] SIZES = {4, 6};
    private static final char RANGE_FIRST_CHAR = '0';
    private static final char RANGE_LAST_CHAR = '9';

    public static boolean validatePin(String pin) {
        if (pin == null) {
            return false;
        }
        final int length = pin.length();
        final int sizesLength = SIZES.length;
        for (int i = 0; i < sizesLength; i++) {
            if (SIZES[i] != length) {
                continue;
            }
            for (int j = 0; j < length; j++) {
                final char ch = pin.charAt(j);
                if (!isValidChar(ch)) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    
    private static boolean isValidChar(final char ch) {
        if (ch < RANGE_FIRST_CHAR || ch > RANGE_LAST_CHAR) {
            return false;
        }
        return true;
    }
}
