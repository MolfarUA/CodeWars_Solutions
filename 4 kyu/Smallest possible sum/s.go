52f677797c461daaf7000740


package kata

func Solution(ar []int) int {
    result := ar[len(ar) - 1]
    
    for i := len(ar) - 2; i >= 0; i-- {
      result = gcd(ar[i], result)
    }
    
    return result * len(ar)
}

func gcd(x int, y int) int { 
    for y != 0 {
        x, y = y, x % y
    }
      
    return x
}
_______________________________
package kata

func Solution(ar []int) int {
    if len(ar) == 0 {
        return 0
    }
    x := ar[0]
    for _, y := range ar[1:] {
        for y != 0 {
            x, y = y, x % y
        }
    }
    return x*len(ar)
}
_______________________________
package kata

func Solution(ar []int) int {
  res := ar[0]
  for i := 1; i < len(ar); i++ {
    res = gcd(ar[i], res)
  }
  return res * len(ar)
}

func gcd(x, y int) int {
  if x == 0 {
    return y
  }
  return gcd(y%x, x)
}
