59568be9cc15b57637000054

import java.math.BigInteger;

public class Immortal {
  /** set true to enable debug */
    static boolean debug = false;

    static BigInteger intervalSum(long a, long b) {
        if (b < a) return BigInteger.ZERO;
        BigInteger bigA = BigInteger.valueOf(a);
        BigInteger bigB = BigInteger.valueOf(b);
        return ((bigA.add(bigB)).multiply(bigB.subtract(bigA).add(BigInteger.ONE))).shiftRight(1);
    }

    static BigInteger calculate(long n, long m, long k, long delta) {
        if (m > n) return calculate(m, n, k, delta);
        long nH = java.lang.Long.highestOneBit(n);
        long mH = (m < nH) ? m :nH;
        BigInteger result = intervalSum(Math.max(0, delta - k), delta + nH - k - 1).multiply(BigInteger.valueOf(mH));
        if (n > nH) result = (result.add(calculate(n - nH, mH, k, delta + nH)));
        if (m > mH) result = (result.add(calculate(nH, m - mH, k, delta + mH)));
        if (n > nH && m > mH) result = result.add(calculate(n - nH, m - mH, k, delta + (mH^nH)));
        return result;
    }

    static long elderAge(long n, long m, long k, long newp) {
        return calculate(n, m, k, 0).mod(BigInteger.valueOf(newp)).longValue();
    }
}
_____________________________________________________
import java.math.BigInteger;

public class Immortal {
  /** set true to enable debug */
    static boolean debug = false;
  
    static long elderAge(long maxCol, long maxRow, long loss, long time) {

        BigInteger total = new BigInteger("0");
        long row = 0, col = 0;
        long len = Long.MAX_VALUE;

        while (len > 0) {
            len = largestPossibleSquare(row, col, maxRow, maxCol);
            // Full square fits
            if (maxRow - row >= len && maxCol - col >= len) {
                total = total.add(calculateSum(row, col, len + row, len, loss))
                        .add(calculateSum(col + len, row, maxCol, len, loss))
                        .add(calculateSum(row + len, col, maxRow, len, loss));
                row += len;
                col += len;
            } else if (maxCol - col < len) { // Right side of the square is cut off
                total = total.add(calculateSum(col, row, maxCol, len, loss));
                row += len;
            } else if (maxRow - row < len) { // Bottom of the square is cut off
                total = total.add(calculateSum(row, col, maxRow, len, loss));
                col += len;
            }
        }

        return total.mod(BigInteger.valueOf(time)).longValue();
    }

    // Size of the largest full or not full square from row and col
    static long largestPossibleSquare(long row, long col, long maxRow, long maxCol) {
        long len = Math.max(maxRow - row, maxCol - col);
        len = (long) (Math.log(len) / Math.log(2));
        len = (long) Math.pow(2, len);
        return len;
    }

    // Calculate sum of a full or not full square from row and col
    static BigInteger calculateSum(long row, long col, long max, long size, long loss) {
        long start = (row ^ col) - loss;
        start = start > 0 ? start : 0;
        long end = ((row + size - 1) ^ col) - loss;
        end = end > 0 ? end : 0;
        long length = end - start + 1;

        return new BigInteger("0")
                .add(BigInteger.valueOf(start))
                .add(BigInteger.valueOf(end))
                .multiply(BigInteger.valueOf(length))
                .divide(BigInteger.valueOf(2))
                .multiply(BigInteger.valueOf(max - row));
    }
}
______________________________________________________________
import java.util.ArrayList;
import java.util.List;

public class Immortal {
    private static final long MAXIMUM_ALLOWED_POWER_OF_TWO  = 1L << 62L;

    public static boolean debug = false;

    public static long elderAge(long n, long m, long k, long mod) {
        long mx = Math.max(n, m);
        long mn = Math.min(n, m);

        long answer = 0;
        for (Pair<Long, Long> horizontal : calculateRanges(mx)) {
            for (Pair<Long, Long> vertical : calculateRanges(mn)) {
                long distance = Math.max(horizontal.second - horizontal.first, vertical.second - vertical.first);
                long numberOfLines = Math.min(horizontal.second - horizontal.first, vertical.second - vertical.first) + 1;

                long lower = (horizontal.first & ~distance) ^ (vertical.first & ~distance);
                long upper = lower + distance;

                long lineSum = calculateRangeSum(lower, upper, k, mod);
                long blockSum = mulMod(lineSum, numberOfLines, mod);

                answer = (answer + blockSum) % mod;
            }
        }
        return answer;
    }

    private static List<Pair<Long, Long>> calculateRanges(long value) {
        List<Pair<Long, Long>> ranges = new ArrayList<>();
        long powerOfTwo = MAXIMUM_ALLOWED_POWER_OF_TWO;
        long offset = 0;

        while (value > 0) {
            while (powerOfTwo > value) powerOfTwo /= 2;

            ranges.add(new Pair<>(offset, offset + powerOfTwo - 1));
            offset += powerOfTwo;
            value -= powerOfTwo;
        }

        return ranges;
    }

    private static long calculateRangeSum(long lower, long upper, long k, long mod) {
        lower = Math.max(0, lower - k);
        upper = Math.max(0, upper - k);

        long left = lower + upper;
        long right = upper - lower + 1;

        if (left % 2 == 0) left /= 2;
        else right /= 2;

        return mulMod(left, right, mod);
    }

    private static long mulMod(long left, long right, long mod) {
        long answer = 0;
        long operand = left;

        while (right != 0) {
            if ((right & 1) == 1) answer = (answer + operand) % mod;
            operand = (operand + operand) % mod;
            right >>= 1;
        }

        return answer;
    }

    private static class Pair<T, K> {
        public final T first;
        public final K second;

        public Pair(T first, K second) {
            this.first = first;
            this.second = second;
        }
    }
}
__________________________________________________
import java.math.BigInteger;

import static java.lang.Math.log;
import static java.lang.Math.max;
import static java.lang.Math.min;
import static java.lang.Math.pow;
import static java.math.BigInteger.ZERO;
import static java.math.BigInteger.valueOf;

public class Immortal {
  /** set true to enable debug */
  static boolean debug = false;

  private static double log2(final long n) {
        return log(n) / log(2);
    }

    private static BigInteger sum(final long n, final BigInteger mod) {
        final BigInteger bn = valueOf(n);
        return bn.multiply(bn).add(bn).divide(valueOf(2)).mod(mod);
    }

    private static BigInteger sumRange(final long from, final long to, final BigInteger mod) {
        return sum(to, mod).subtract(sum(from - 1, mod));
    }

    private static BigInteger test(final long fromA, final long fromB, final long toA, final long toB, final long lim, final BigInteger mod) {
        if (fromA >= toA || fromB >= toB) {
            return ZERO;
        }
        final long rangeA = toA - fromA;
        final long rangeB = toB - fromB;
        final long max = max(rangeA, rangeB);
        final long min = min(rangeA, rangeB);
        final long side = (long) pow(2, (long) log2(max));

        final BigInteger lines = valueOf(min(min, side));
        BigInteger sum = ZERO;
        final long max1 = max(0, (fromA ^ fromB) - lim);
        if (rangeB >= rangeA) {
            long toL = max(0, (fromA ^ (fromB + side - 1)) - lim);
            sum = sum.add(lines.multiply(sumRange(max1, toL, mod)));
            sum = sum.add(test(fromA, fromB + side, toA, toB, lim, mod));
            sum = sum.add(test(fromA + side, fromB, toA, fromB + side, lim, mod));
        } else {
            long toL = max(0, (fromB ^ (fromA + side - 1)) - lim);
            sum = sum.add(lines.multiply(sumRange(max1, toL, mod)));
            sum = sum.add(test(fromA + side, fromB, toA, toB, lim, mod));
            sum = sum.add(test(fromA, fromB + side, fromA + side, toB, lim, mod));
        }

        return sum.mod(mod);
    }

    static long elderAge(final long n, final long m, final long k, final long newp) {
        System.out.println(n + " " + m + " " + k + " " + newp);
        return test(0, 0, n, m, k, valueOf(newp)).longValue();
    }
}
___________________________________________________
public class Immortal {
  /** set true to enable debug */
  static boolean debug = false;

  static long elderAge(long n, long m, long k, long newp) {
    return solve(m, n, k, newp);
  }

  private static long solve(long m, long n, long k, long MOD) {
        return solve(0,0, m - 1, n - 1, k, MOD);
  }

  private static long solve(long left, long top, long right, long bottom, long K, long MOD) {
        if (left > right || top > bottom) return 0L;
        if (right - left < bottom - top) {
            long t1 = left;
            long t2 = right;
            left = top;
            right = bottom;
            top = t1;
            bottom = t2;
        }
        long width = right - left + 1;
        long height = bottom - top + 1;

        long areaWidth = nearestLessOrEqualPowerOfTwo(width);
        long areaHeight = Math.min(height, areaWidth);
        long min = (left ^ top) - K;
        long max = min + areaWidth - 1;
        if (min < 0) {
            min = 0;
        }
        if (width == 1) {
            return min;
        }

        long areaSum = 0;
        if (min < max) {
            long count = max - min + 1;
            areaSum = count % 2 == 0 ?
                    (((((min % MOD) * (count % MOD)) % MOD) + ((((count / 2) % MOD) * ((count - 1) % MOD)) % MOD)) % MOD) :
                    ((((min % MOD) * (count % MOD)) % MOD) + (((((count - 1) / 2) % MOD) * (count % MOD)) % MOD) % MOD);
            areaSum = (areaSum * (areaHeight % MOD) % MOD);
        }

        // Recursion
        if (height > areaHeight) {
            long subSumA = solve(left, top + areaHeight, right, bottom, K, MOD);
            areaSum = (areaSum + subSumA) % MOD;
        }
        if (width > areaWidth) {
            long subSumB = solve(left + areaWidth, top, right, top + areaHeight - 1, K, MOD);
            areaSum = (areaSum + subSumB) % MOD;
        }
        return areaSum;
    }

    private static long nearestLessOrEqualPowerOfTwo(long a) {
        if (a >= 1L << 62) return 1L << 62;
        long res = 1;
        while (res << 1 <= a) {
            res <<= 1;
        }
        return res;
    }
}
