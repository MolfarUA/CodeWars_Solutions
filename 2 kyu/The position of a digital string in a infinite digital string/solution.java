public class InfiniteDigitalString {
  private static class Position implements Comparable<Position> {
    final long number;
    final int usedDigits;

    Position(long number, int usedDigits) {
      this.number = number;
      this.usedDigits = usedDigits;
    }

    @Override
    public int compareTo(Position other) {
      long d = number - other.number;
      if (d != 0)
        return Long.signum(d);
      return other.usedDigits - usedDigits;
    }

    boolean yieldsString(String s) {
      String numStr = Long.toString(number);
      int d = numStr.length() - usedDigits;
      if (d < 0 || !s.startsWith(numStr.substring(d)))
        return false;
      long num = number;
      d = usedDigits;
      int sLen = s.length();
      while (d < sLen) {
        numStr = Long.toString(++num);
        int e = Math.min(numStr.length(), sLen - d);
        if (!s.startsWith(numStr.substring(0, e), d))
          return false;
        d += e;
      }
      return true;
    }

    long linearPos() {
      long t = 1;
      int n = 1;
      long digitCount = 0;
      while (true) {
        long t1 = t * 10;
        if (number < t1)
          break;
        digitCount += (t1 - t) * n;
        n++;
        t = t1;
      }
      digitCount += (number - t) * n;
      return digitCount + n - usedDigits;
    }
  }

  private static Position testCandidate(String s, Position best, long number, int usedDigits) {
    Position p = new Position(number, usedDigits);
    return (best == null || best.compareTo(p) > 0) && p.yieldsString(s) ? p : best;
  }

  public static long findPosition(final String s) {
    if (!s.matches("\\d+"))
      return -1L;
    Position best = null;
    int sLen = s.length();
    // There is a number that resides in s completely
    for (int numLen = 1; numLen <= sLen; numLen++)
      for (int sPos = 0; sPos <= sLen - numLen; sPos++) {
        if (s.charAt(sPos) == '0')
          continue;
        long num = Long.parseLong(s.substring(sPos, sPos + numLen));
        if (sPos > 0)
          num--;
        int ud = Long.toString(num).length();
        if (sPos > 0) {
          if (ud <= sPos)
            continue;
          ud = sPos;
        }
        best = testCandidate(s, best, num, ud);
      }
    // There is no such number, but s is a part of a single number
    if (s.charAt(0) == '0')
      best = testCandidate(s, best, Long.parseLong('1' + s), sLen);
    // There is no such number, but s is made up of two consecutive numbers
    for (int sPos = 1; sPos < sLen; sPos++) {
      if (s.charAt(sPos) == '0')
        continue;
      String endPart = s.substring(0, sPos);
      endPart = Long.toString(Long.parseLong('1' + endPart) + 1).substring(1);
      String begPart = s.substring(sPos);
      int begLen = begPart.length();
      for (int endPos = Math.max(1, begLen - sPos + 1); endPos <= begLen; endPos++)
        if (endPart.startsWith(begPart.substring(endPos))) {
          String union = begPart.substring(0, endPos) + endPart;
          best = testCandidate(s, best, Long.parseLong(union) - 1, sPos);
        }
    }
    return best.linearPos();
  }  
}
___________________________________________________
public class InfiniteDigitalString {

    private final String s;

    public InfiniteDigitalString(String s) {
        this.s = s;
    }

    public long findPosition() {
        long position = Long.MAX_VALUE;
        for (int a = 0; a <= s.length() - 1; a++) {
            for (int b = a + 1; b <= s.length(); b++) {
                String beginning = a == 0 ? "" : s.substring(0, a);
                String token = s.substring(a, b);
                String end = b == s.length() ? "" : s.substring(b, s.length());

                if (token.startsWith("0")) continue;

                if (isBeginningMatched(token, beginning) && isEndMatched(token, end)) {
                    long newPosition = position(Long.parseLong(token));
                    if (newPosition < position) {
                        position = newPosition - a;
                    }
                }
            }
        }

        for (int i = 1; i < s.length(); i++) {
            long newPosition = findOverlappingPosition(s.substring(0, i), s.substring(i, s.length()));
            if (newPosition < position) {
                position = newPosition;
            }
        }

        if (position == Long.MAX_VALUE) position = position(Long.parseLong("1" + s)) + 1;

        return position;
    }

    private long findOverlappingPosition(String beginning, String end) {
        if (end.startsWith("0")) return Long.MAX_VALUE;
        String incremented = increment(beginning);
        if (incremented.length() != beginning.length()) throw new IllegalStateException("Incremented is invalid.");

        long position = position(Long.parseLong(end + incremented)) - beginning.length();

        for (int i = 1; i < incremented.length(); i++) {
            String head = incremented.substring(0, i);
            String tail = incremented.substring(i, incremented.length());

            if (end.endsWith(head)) {
                if (beginning.startsWith("0") && (end.equals(head) || end.equals("1"))) continue;
                String token = end + tail;
                long newPosition = position(Long.parseLong(token)) - beginning.length();
                if (newPosition < position) position = newPosition;
            }
        }

        return position;
    }

    private String increment(String token) {
        String result = String.valueOf(Long.parseLong(token) + 1);
        if (result.length() == token.length()) {
            return result;
        } else if (result.length() > token.length()) {
            return result.substring(1);
        } else {
            for (int i = result.length(); i < token.length(); i++) result = "0" + result;
            return result;
        }
    }

    private boolean isBeginningMatched(String token, String beginning) {
        String s = beginning;
        if (beginning.isEmpty()) return true;

        long t = Long.parseLong(token) - 1;
        String tail = String.valueOf(t);
        while (tail.length() <= s.length() && t >= 1) {
            if (t <= 0) return false;
            if (s.endsWith(tail)) {
                s = s.substring(0, s.length() - tail.length());
                t--;
                tail = String.valueOf(t);
            } else {
                return false;
            }
        }

        return s.isEmpty() || (t > 0 && String.valueOf(t).endsWith(s));
    }

    private boolean isEndMatched(String token, String end) {
        String s = end;
        if (end.isEmpty()) return true;

        long t = Long.parseLong(token) + 1;
        String head = String.valueOf(t);
        while (head.length() <= s.length()) {
            if (s.startsWith(head)) {
                s = s.replaceFirst(head, "");
                t++;
                head = String.valueOf(t);
            } else {
                return false;
            }
        }

        return s.isEmpty() || String.valueOf(t).startsWith(s);
    }

    private long position(long n) {
        int length = String.valueOf(n).length();
        long position = 0;
        for (int i = 1; i <= length - 1; i++) {
            position += i * (9 * Math.pow(10, i - 1));
        }

        position += length * (n - Math.pow(10, length - 1));
        return position;
    }

    public static long findPosition(final String s) {
        System.out.println("input: " + s);
        return new InfiniteDigitalString(s).findPosition();
    }
}
___________________________________________________
import java.util.Arrays;
import java.util.TreeSet;
public class InfiniteDigitalString {

    private static final byte anyNumber = -1;

    public static long findPosition(final String s) {
        byte[] seq = s.getBytes();
        for (int i = 0; i < seq.length; i++) {
            seq[i] -= '1' - 1;
        }
        for (int numLength = 1; numLength <= seq.length; numLength++) {
            TreeSet<Long> results = new TreeSet<>();
            for (int offset = 0; offset < numLength; offset++) {
                if (seq[offset] == 0) // first num not 0
                    continue;
                byte[] numberBeforeChange = Arrays.copyOfRange(seq, offset, offset + numLength);
                if (offset + numLength > seq.length)
                    Arrays.fill(numberBeforeChange, seq.length - offset, numLength, anyNumber);
                byte[] number = changeAny(seq, numberBeforeChange, offset);
                if (checkNumber(seq, number, offset))
                    results.add(getPositionByNumber(number, offset)); // wait for return
            }
            if (!results.isEmpty())
                return results.first();
        }
        // if not match the seq must filled by 0 ,then shift 1 before
        byte[] number = new byte[seq.length + 1];
        number[0] = 1;
        System.arraycopy(number, 1, seq, 0, seq.length);
        return getPositionByNumber(number, -1);
    }

    private static boolean checkNumber(byte[] seq, byte[] number, int offset) {
        // seq    number offset
        // 11213  12     1
        // po n    i
        int prev = offset - 1, next = offset + number.length;
        byte[] prevNumber = minusOne(number.clone()), nextNumber = number.clone();
        // check left
        // the count of left number in seq (offset) is less then number.length
        for (int i = 1; prev >= 0; prev--, i++) {
            int p = prevNumber[prevNumber.length - i];
            if (p != anyNumber && seq[prev] != p)
                return false;
        }
        // check right
        for (int i = 0; next < seq.length; next++, i = (i + 1) % nextNumber.length) {
            if (i == 0)
                nextNumber = addOne(nextNumber);
            if (nextNumber[i] != seq[next])
                return false;
        }
        return true;
    }

    private static byte[] changeAny(byte[] seq, byte[] number, int offset) {
        if (number[number.length - 1] != anyNumber)
            return number;
        int prev = offset;
        for (int i = number.length - 1; i >= 0; i--) {
            if (number[i] == anyNumber)
                prev--;
            else break;
        }
        byte[] changed = Arrays.copyOfRange(seq, prev, offset);
        addOne(changed); // the return val is ignored , Don't care length increase. addOne(99) -> 00
        System.arraycopy(changed, 0, number, number.length - changed.length, changed.length);
        return number;
    }

    private static byte[] minusOne(byte[] number) {
        int i = number.length - 1;
        while (--number[i] == -1) {
            number[i--] = 9;
        }
        if (number[0] == 0)
            return Arrays.copyOfRange(number, 1, number.length);
        return number;
    }

    private static byte[] addOne(byte[] number) {
        int i = number.length - 1;
        while (++number[i] == 10) {
            number[i--] = 0;
            if (i == -1) {
                byte[] num = new byte[number.length + 1];
                System.arraycopy(number, 0, num, 1, number.length);
                num[0] = 1;
                return num;
            }
        }
        return number;
    }

    private static long getPositionByNumber(byte[] number, int offset) {
        long pos = 0;
        long pow = 1;
        for (int bit = 1; bit < number.length; bit++, pow *= 10) {
            pos += pow * 9 * bit;
        }
        number[0]--;
        for (int bit = 0; bit < number.length; bit++, pow /= 10) {
            pos += pow * number[bit] * number.length;
        }
        return pos - offset;
    }
}
___________________________________________________
import java.util.ArrayList;
import java.util.List;

public class InfiniteDigitalString {

  public static long findPosition(final String s) {
    if (Long.parseLong(s) == 0)
      return numIndex(Long.parseLong(1 + s)) + 1;
    for (int l = 1; l <= s.length(); l++) {
      //System.out.println("L: " + l);
      List<Long> poss = new ArrayList<Long>();
      for (int i = 0; i < l + 1; i++) {
        List<String> checks = new ArrayList<String>();
        //System.out.println("I: " + i);
        String sdt = s.substring(0, l - i);
        String end = s.substring(l - i, l);
        long ende = 0;
        try {
          ende = Long.parseLong(end);
        } catch (Exception e) {
        }
        if (ende == 0) {
          checks.add(end+sdt);
        } else {
          checks.add(end + sdt);
          checks.add((Long.parseLong(end) - 1) + sdt);
        }

        //System.out.println("Sdt: " + sdt );
        //System.out.println("End: " + end);
        //System.out.println("End+Sdt: " + end+sdt);
        for (String c : checks) {
          //System.out.println("C: " + c);
          if(c.charAt(0)=='0') {
            //System.out.println("Übersprungen");
            continue;
          }
          String ds = c;
          long num = 0;
          num = Long.parseLong(c);
          while (ds.length() < s.length() + l) {
            num++;
            ds += num;
          }
          int idx = ds.indexOf(s);
          if (idx != -1)
            poss.add(numIndex(Long.parseLong(c)) + idx);
        }
      }
      if (poss.size() > 0) {
        long min = poss.get(0);
        for (int i = 0; i < poss.size(); i++) {
          if (poss.get(i) < min)
            min = poss.get(i);
        }
        return min;
      }
    }
    return -1;
  }

  public static Long numIndex(Long n) {
    //System.out.println("n in numIndex " + n);
    if (n < 10)
      return n - 1;
    long c = 0;
    for (int i = 1; true; i++) {
      //System.out.println("i in numIndex " + i);
      c += i * 9 * Math.pow(10, i - 1);
      //System.out.println("C in numIndex " + c);
      if (n < Math.pow(10, i + 1)) {
        //System.out.println("numIndex: " + (c + (i + 1) * (n - (int) Math.pow(10, i))));
        return c + (i + 1) * (n - (long) Math.pow(10, i));
      }
    }
  }
}
