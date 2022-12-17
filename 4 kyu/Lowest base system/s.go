58bc16e271b1e4c5d3000151


package kata
     
import (
	"regexp"
	"strconv"
)

func GetMinBase(n uint64) uint64 {

	strn := strconv.FormatUint(n,10);
  if len(strn)>9 && regexp.MustCompile("^1[0]*2?$").MatchString(strn){
    return n-1
  }
  base:= loopMinBase(n,1,1000)
  if(base!=1){
	return uint64(base)
  }
  if len(strn)>9 && ! regexp.MustCompile("^[10]*$|0001$").MatchString(strn){ 
    return n-1
  }
  return loopMinBase(n,1000,n)
}


func loopMinBase(n uint64, base uint64,limit uint64) uint64{
	completed := false
	for !completed { 
	if(base>=limit){	
		return 1
	}
		base++
		nPrime := n
		completed = true
			for nPrime > 0 { 
				r := nPrime % base   
				if(r!=1){
				completed = false
				break;
		}
			nPrime = nPrime / base
			}
		}
		return base
}
______________________________________
package kata

import "math"

func GetMinBase(n uint64) uint64 {
  for k := uint64(math.Floor(math.Log2(float64(n)))); k >= 2; k-- {
    b := uint64(math.Floor(math.Pow(float64(n), 1.0 / float64(k))))
    var a = n
    for a % b == 1 {
      a = (a - 1) / b
    }
    if a == 0 {
      return b
    }
  }
  return n - 1
}
______________________________________
package kata


import "math"

func GetMinBase(n uint64) uint64 {
  maxK := uint64(math.Ceil(math.Log2(float64(n)))) + 1
  for k := maxK ; k > 1 ; k-- {
    for b := uint64(math.Ceil(math.Pow(float64(n), 1.0 / float64(k)))) + 1 ; b > 1 ; b-- {
      var s uint64
      for i, t := uint64(0), uint64(1) ; i <= k ; i, t = i + 1, t * b {
        s += t
      }
      if s == n { return b }
      if s < n { break }
    }
  }
  return n - 1
}
