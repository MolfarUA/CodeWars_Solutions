55e785dfcb59864f200000d9


package kata

var primes = [20]int{2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71}

func CountSpecMult(n int, maxVal uint64) uint64 {
  i, x := 0, uint64(1)
  for i < n {
    x *= uint64(primes[i])
    i++
  }
  return maxVal / x
}
_________________________________
package kata

import (
  "math"
)

func CountSpecMult(n int, maxVal uint64) uint64 {
  p, prod := uint64(3), uint64(2)
  for _i := 1 ; _i < n ; _i++ {
    p = nextPrime(p)
    prod *= p
    p += 2
  }
  return maxVal / prod
}


func nextPrime(n uint64) uint64 {
  var x uint64
  for true {
    s := uint64(math.Sqrt(float64(n)))
    for x = uint64(3) ; x <= s ; x += uint64(2) {
      if n % x == 0 {
        n += uint64(2)
        break
      }
    }
    if x > s {return n}
  }
  return 0
}
