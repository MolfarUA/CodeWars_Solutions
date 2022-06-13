package kata

func FindNb(m int) int {
  for n := 1 ; m > 0 ; n++ {
    m -= n*n*n
    if m == 0 { return n }
  }
  return -1
}
_________________________________________
package kata

import (
  "math"
)

func FindNb(m int) int {
  if m < 0 { return -1 }
  
  discriminant := 1 + 8 * math.Sqrt(float64(m))
  
  if discriminant < 0 { return -1 }
  
  x := (-1 + math.Sqrt(discriminant)) / 2
  
  if x < 0 || x != math.Trunc(x) { return -1 }
  
  return int(x)
}
_________________________________________
package kata

import "math"

func FindNb(m int) int {
  n := -0.5 + math.Sqrt(0.25 + 2*math.Sqrt(float64(m)));
  if n - float64(int(n)) != 0 { return -1 }
  return int(n)
}
_________________________________________
package kata

func FindNb(m int) int {
  sum := 0
  for i := 1;; i++ {
    sum += i*i*i
    if sum == m {
      return i
    } else if sum > m {
      return -1
    }
  }
}
