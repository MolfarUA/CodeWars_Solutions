59568be9cc15b57637000054

import 'dart:math';

/** set true to enable debug */
bool debug = false;

BigInt max(BigInt a, BigInt b) { return a > b ? a : b; }
BigInt clog2(BigInt a) { BigInt b = BigInt.one; while (b < a) b *= BigInt.two; return b; }
BigInt rsum(BigInt a, BigInt b) { return ((a + b) * (b - a + BigInt.one)) ~/ BigInt.two; }

int elderAge(int m, int n, int k, int p) {
  return helper(BigInt.from(m), BigInt.from(n), BigInt.from(k), BigInt.from(p)).toInt();
}

BigInt helper(BigInt m, BigInt n, BigInt k, BigInt p) {
  if (m == BigInt.zero || n == BigInt.zero) return BigInt.zero;
  if (m > n) { BigInt o = m; m = n; n = o; }
  BigInt x = clog2(m);
  BigInt y = clog2(n);
  if (k > y) return BigInt.zero;
  if (x == y) return ((m + n - y) * rsum(BigInt.one, y - k - BigInt.one) + helper(y - n, x - m, k, p)) % p;
  x = y ~/ BigInt.two;
  BigInt phi = m * rsum(BigInt.one, y - k - BigInt.one) - (y - n) * rsum(max(BigInt.zero, x - k), y - k - BigInt.one);
  if (k <= x) phi += (x - k) * (x - m) * (y - n) + helper(x - m, y - n, BigInt.zero, p);
  else phi += helper(x - m, y - n, k - x, p);
  return phi % p;
}
______________________________________
bool debug = false;

int mul(int x, int y, int m) {
  return (x % m) * (y % m) % m;
}

int elderAge(int m, int n, int l, int t) {
  if (m < n) return elderAge(n, m, l, t);
  var k = 1 << m.bitLength;
  if (m <= 0 || n <= 0 || l >= k) return 0;
  k = n > 1 ? k >> 1 : m;
  var r = n < k ? n : k, s = 0;
  if (k > l) {
    if (l >= 0) {
      var x = k - l;
      var y = x - 1;
      if (x.isEven) x ~/= 2; else y ~/= 2;
      s = mul(mul(x, y, t), r, t);
    }
    else {
      var x = k, y = k - 1;
      if (x.isEven) x ~/= 2; else y ~/= 2;
      s = mul(mul(x, y, t) - mul(l, k, t), r, t);
    }
  }
  s += elderAge(m - k, r, l - k, t);
  s += elderAge(k, n - r, l - k, t);
  s += elderAge(m - k, n - r, l, t);
  return s % t;
}
______________________________________________
import 'dart:math' as math;

/** set true to enable debug */
bool debug = false;

BigInt bigIntPow(BigInt x) {
  var p = BigInt.one;
  while (p < x) {
    p <<= 1;
  }
  return p;
}

BigInt bigIntRangeSum(BigInt l, BigInt r) =>
    (l + r) * (r - l + BigInt.one) ~/ BigInt.two;

BigInt bigIntMax(BigInt a, BigInt b) => a > b ? a : b;

BigInt bigIntElderAge(BigInt m, BigInt n, BigInt k, BigInt newp) {
  if (m == BigInt.zero || n == BigInt.zero) {
    return BigInt.zero;
  }
  if (m > n) {
    var t = m;
    m = n;
    n = t;
  }
  var lm = bigIntPow(m);
  var ln = bigIntPow(n);
  if (k > ln) {
    return BigInt.zero;
  }

  if (lm == ln) {
    return ((bigIntRangeSum(BigInt.one, ln - k - BigInt.one) * (m + n - ln) +
            bigIntElderAge(ln - n, lm - m, k, newp))) %
        newp;
  }
  if (lm < ln) {
    lm = ln ~/ BigInt.from(2);
    var tmp = bigIntRangeSum(BigInt.one, ln - k - BigInt.one) * m -
        (ln - n) *
            bigIntRangeSum(bigIntMax(BigInt.zero, lm - k), ln - k - BigInt.one);

    if (k <= lm) {
      tmp += (lm - k) * (lm - m) * (ln - n) +
          bigIntElderAge(lm - m, ln - n, BigInt.zero, newp);
    } else {
      tmp += bigIntElderAge(lm - m, ln - n, k - lm, newp);
    }
    return tmp % newp;
  }
  return BigInt.zero;
}

int elderAge(int m, int n, int k, int newp) => bigIntElderAge(
        BigInt.from(m), BigInt.from(n), BigInt.from(k), BigInt.from(newp))
    .toInt();
______________________________________________
import 'dart:math';

bool debug = false;

int elderAge(int n, int m, int k, int newp) {
  var findMax = max(n, m);
  var findMin = min(n, m);

  var sq = pow(2.0, (log(findMax.toDouble()) / log(2)).floor()).toInt();

  var sMin = min(sq, findMin);
  var kInv = max(0, -k);
  var maxMod = max(0, sq - k - 1);

  var dCase = maxMod - kInv + 1;
  var sCase = maxMod + kInv;
  if (dCase % 2 > 0) {
    sCase = (sCase.toDouble() / 2).floor().toInt();
  } else if (sCase % 2 > 0) {
    dCase = (dCase.toDouble() / 2).floor().toInt();
  }

  var diff;
  if (sCase <= 0) {
    diff = 0;
  } else {
    diff = ((sCase % newp) * (dCase % newp)) % newp;
  }
  var acc = ((diff % newp) * (sMin % newp)) % newp;
  if (findMax > sq) {
    acc += elderAge(findMax - sq, sMin, k - sq, newp);
  }
  if (findMin > sMin) {
    acc += elderAge(sq, findMin - sMin, k - sMin, newp);
  }
  if ((findMin > sMin) & (findMax > sq)) {
    acc += elderAge(findMax - sq, findMin - sMin, k, newp);
  }
  return acc % newp;
}
