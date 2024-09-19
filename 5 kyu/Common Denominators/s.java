
class Fracts {
    
    static long gcd(long a, long b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    static long lcm(long a, long b) {
        return a * b / gcd(a, b);
    }

    public static String convertFrac(long[][] lst) {
        long lcmall = 1;
        long[][] newlst = new long[lst.length][2];
        for  (int i = 0; i < lst.length; i++) {
            long g = gcd(lst[i][0], lst[i][1]);
            newlst[i][0] = lst[i][0] / g;
            newlst[i][1] = lst[i][1] / g;
        }
        for (long[] item : newlst) {
            lcmall = lcm(lcmall, item[1]);
        }
        String result = "";
        for (long[] item : newlst) {
            result += "(" + (item[0] * lcmall / item[1]) + "," + lcmall + ")";
        }
        return result;
    }
}
################################
import java.util.Arrays;
import java.util.stream.Collectors;

public class Fracts {

    public static String convertFrac(long[][] lst) {
        final Long dividor = Arrays.stream(lst)
                .map(pair -> new Long[]{pair[0], pair[1]})
                .map(Fracts::divideByGreatestCommonDivider)
                .map(longs -> longs[1])
                .reduce(1L, Fracts::leastCommonMultiple);

        return Arrays.stream(lst)
                .map(pair -> pair[0] * dividor / pair[1])
                .map(aLong -> String.format("(%d,%d)", aLong, dividor))
                .collect(Collectors.joining());
    }

    private static Long greatestCommonDivider(Long a, Long b) {
        return b == 0 ? a : greatestCommonDivider(b, a % b);
    }

    private static Long[] divideByGreatestCommonDivider(Long[] pair) {
        Long gcd = greatestCommonDivider(pair[0], pair[1]);
        return new Long[]{pair[0] / gcd, pair[1] / gcd};
    }

    private static Long leastCommonMultiple(Long a, Long b) {
        return Math.abs(a * b) / greatestCommonDivider(a, b);
    }
}
################################
import java.util.ArrayList;
import java.util.List;

public class Fracts {
  public static String convertFrac(long[][] lst) {
        if (lst.length == 0) {
            return "";
        }
        List<Long> first = new ArrayList<>();
        List<Long> second = new ArrayList<>();
        for (long[] longs : lst) {
            long a = longs[0];
            long b = longs[1];
            for (int i = (int)a; i > 0; i --) {
                if (a % i == 0 && b % i == 0) {
                    a = a / i;
                    b = b / i;
                    break;
                }
            }
            first.add(a);
            second.add(b);
        }
        Long count = second.get(0);
        for (int i = 1; i < first.size(); i++) {
            long a = second.get(i);
            long min = Math.min(count, a);
            for (int j = (int)min; j > 0; j --) {
                if (a % j == 0 && count % j == 0) {
                    a = a / j;
                    count = count / j;
                    count = a * count * j;
                    break;
                }
            }
        }
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < first.size(); i++) {
            stringBuilder.append("(")
                    .append(first.get(i) * (count / second.get(i)))
                    .append(",")
                    .append(count)
                    .append(")");
        }
        return stringBuilder.toString();
    }

}
