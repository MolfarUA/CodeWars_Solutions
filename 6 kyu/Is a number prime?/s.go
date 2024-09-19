package kata

import "math"

func IsPrime(n int) bool {
  if n < 2 {
    return false
  }
  for i:=2; i<=int(math.Sqrt(float64(n))); i++ {
    if n%i == 0 {
      return false
    }
  }
  return true
}
_______________________
package kata

import (
	"math"
)

func IsPrime(n int) bool {
	if n <= 1 {
		return false
	}
	if n == 2 {
		return true
	}
	if n%2 == 0 {
		return false
	}

	for i := 3; i <= int(math.Sqrt(float64(n))); i += 2 {
		if n%i == 0 {
			return false
		}
	}

	return true
}
_______________________
package kata
import "math"
func IsPrime(n int) bool {
  if n < 2 {
    return false
  }
  
  for x := 2; float64(x) <= math.Sqrt(float64(n)); x++ {
    if n % x == 0 {
      return false
    }
  }
  
  return true
}
_______________________
package kata

import "math"

func IsPrime(n int) bool {
  switch {
   case n < 0, n==0, n == 1: return false
   case n == 2, n==3: return true
  }
  
  for v:=2; v <= int(math.Sqrt(float64(n))); v++ {
    if n % v == 0 {
      return false
    }
  }
  
  return true
}
