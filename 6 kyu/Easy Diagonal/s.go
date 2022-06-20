559b8e46fa060b2c6a0000bf


package kata

import "math/big"

func Diagonal(n, p int) int {
  var z big.Int
  return int(z.Binomial(int64(n+1), int64(p+1)).Int64())
}
_____________________________
package kata
func Diagonal(n, p int) int { 
  return nChooseK(n+1,p+1)
}
func nChooseK(n, k int) int {
  if k > n {    return 0
  }
  if k*2 > n {    k = n - k
  }
  if k == 0 {   return 1
  }
  result := n
  for i := 2; i <= k; i++ {
    result *= (n - i + 1)
    if result%i != 0 {      panic("err")
    }
    result /= i
  }
  return result
}
_____________________________
package kata

import "math/bits"

func mul(x [2]uint64, y uint64) [2]uint64 {
  p, q := bits.Mul64(x[1], y)
  return [2]uint64{p + x[0]*y, q}
}

func div(x [2]uint64, y uint64) [2]uint64 {
  aq, ar := bits.Div64(0, x[0], y)
  bq, _ := bits.Div64(ar, x[1], y)
  return [2]uint64{aq, bq}
}

func Diagonal(n, p int) int {
  nn := uint64(n + 1)
  rr := uint64(p + 1)
  if rr > nn/2 {
    rr = nn - rr
  }
  r := [2]uint64{0, 1}
  for i := nn; i >= nn-rr+1; i-- {
    r = mul(r, i)
  }
  for i := rr; i > 1; i-- {
    r = div(r, i)
  }
  return int(r[1])
}
