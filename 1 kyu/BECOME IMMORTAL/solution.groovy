59568be9cc15b57637000054

class Immortal {
  /**
   * set true to enable debug
   */
  static boolean debug = false

  def static elderAge(long m, long n, long l, long t) {
    long small = Math.min(m, n);
    long big = Math.max(m, n);
    long power = Math.pow(2, Math.floor(Math.log(big) / Math.log(2)));
    long rows = Math.min(power, small);
    long first = Math.max(0, -l);
    long terms = Math.max(0, power - l - 1);
    long x = (terms - first + 1);
    long y = first + terms;

    if (x % 2 > 0) y = Math.floor(y / 2);
    else if (y % 2 > 0) x = Math.floor(x / 2);

    long series = y <= 0 ? 0 : ((y % t) * (x % t)) % t;

    long sum = ((series % t) * (rows % t)) % t;
    sum += big > power ? elderAge(big - power, rows, l - power, t) : 0;
    sum += small > rows ? elderAge(power, small - rows, l - rows, t) : 0;
    sum += small > rows && big > power ? elderAge(big - power, small - rows, l, t) : 0;

    return sum % t;
  }

}
_________________________________
class Immortal {
  private static long p = (int) 1e9

  /**
   * set true to enable debug
   */
  static boolean debug = false

  private static int log2(long x) {
    int ans = 0
    while (true) {
      x = x >> 1
      if (x == 0) break
      ans++
    }
    return ans
  }

  private static long mul(long x, long y, long z) {
    if (z == 2) {
      if ((x & 1) != 0) y >>= 1
      else if ((y & 1) != 0) x >>= 1
      else throw new RuntimeException("shit")
    }
    return x % p * (y % p) % p
  }

  private static long sumTimes(long first, long n, long k, long t) {
    first -= k
    if (first < 1) {
      n -= 1 - first
      first = 1
    }
    if (n <= 0) return 0
    return mul(mul(first + first + n - 1, n, 2L), t, 1)
  }

  def static elderAge(long n, long m, long k, long newp) {
    if (n == 0 || m == 0) return 0
    if (k < 0) k = 0
    if (n < m) {
      long tmp = n
      n = m
      m = tmp
    }
    p = newp
    if (n == m && (n & -n) == n) return sumTimes(1, n - 1, k, m)
    int N = log2(n), M = log2(m)
    long centerWidth = 1L << N, centerHeight = 1L << M
    if (N == M) {
      long rightWidth = n - centerWidth, bottomHeight = m - centerHeight
      long bottomSum = sumTimes(centerHeight, centerWidth, k, bottomHeight)
      return ((sumTimes(centerWidth, centerHeight, k, rightWidth) + bottomSum) % p + (elderAge(rightWidth, bottomHeight, k, p) + elderAge(centerWidth, centerHeight, k, p)) % p) % p
    } else {
      long leftWidth = 1L << N
      long leftSum = sumTimes(0, leftWidth, k, m)
      long rightSum = elderAge(n - leftWidth, m, k - leftWidth, p)
      if (leftWidth > k) {
        rightSum += mul(mul(leftWidth - k, m, 1), n - leftWidth, 1)
        rightSum %= p
      }
      return (leftSum + rightSum) % p
    }
  }
}
