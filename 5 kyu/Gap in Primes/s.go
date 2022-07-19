561e9c843a2ef5a40c0000a4


package kata

import "math/big"

func isPrime(n int) bool { return big.NewInt(int64(n)).ProbablyPrime(0) }

func isGap(a, b int) bool {
  if !(isPrime(a) && isPrime(b)) { return false }
  for i := a + 1; i < b; i++ { if isPrime(i) { return false } }
  
  return true
}

func Gap(g, m, n int) (res []int) {
  for i := m; i <= (n - g); i++ {
    if isGap(i, i + g) {
      return []int{i, i + g}
    }
  }
  
  return
}
__________________________________
package kata

import "math/rand"

func Pow(a, b, c int64) int64 {
    a %= c
    if a == 0 {
        return 0
    }
    var res int64 = 1
    for ; b != 0; b >>= 1 {
        if (b & 1) == 1 {
            res = res * a % c
        }
        a = a * a % c
    }
    return res
}

func IsPrime(n int) bool {
    p := int64(n)
    if p == 2 || p == 3 {
        return true
    }
    if p <= 1 || p % 2 == 0 || p % 3 == 0 {
        return false
    }
    for t := 0; t < 20; t++ {
        a := rand.Int63n(2000000000)
        if Pow(a, p - 1, p) > 1 {
            return false
        }
    }
    return true
}

func Gap(g, m, n int) []int {
    if n - m + 1 < g {
        return nil
    }
    lastPrime := -n
    for ; m <= n; m++ {
        if IsPrime(m) {
            if m - lastPrime == g {
                return []int{lastPrime, m}
            }
            lastPrime = m
        }
    }
    return nil
}
__________________________________
package kata

import "math"

func isPrime(n int) bool {
  end := int(math.Sqrt(float64(n)))
  for i := 2; i <= end; i++ {
    if n % i == 0 { return false }
  }
  return true
}

func Gap(g, m, n int) []int {
  for i, last := m, -1; i <= n; i++ {
    if isPrime(i) {
      if last > 0 && i - last == g { return []int{ last, i } }
      last = i
    }
  }
  return nil
}
__________________________________
package kata

import "math"

func Gap(g, m, n int) []int {
  for i, lp, hp := m, 0, 0; i <= n; i++ {
    if isPrime(i) {
      lp = hp
      hp = i
      
      if lp != 0 && hp - lp == g {
        return []int{lp, hp}
      }
    }
  }
  
  return nil
}

func isPrime(x int) bool {
  for c := 2; c <= int(math.Sqrt(float64(x))); c++ {
    if x % c == 0 {
      return false
    }
  }
  
  return true
}
