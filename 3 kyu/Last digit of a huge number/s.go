package kata

import "math"

func LastDigit(as []int) int {
  var acc int = 1
  
  for i := len(as) - 1; i >=0; i-- {
    exp := acc % 4 + 4
    if (acc < 4) { exp = acc }
    
    base := as[i] % 20 + 20
    if (as[i] < 20) { base = as[i] }
    
    acc = int(math.Pow(float64(base), float64(exp)))
  }
  
  return acc % 10
}
_______________________
package kata

import (
    "fmt"
)

func phi(n int) int {
    var result int
    result = n
    for i := 2; i * i <= n; i++ {
        if n % i == 0 {
            for n % i == 0 {
                n /= i
            }
            result -= result / i
        }
    }
    if n > 1 {
        result -= result / n
    }
    return result
}

func gcd(a, b int) int {
    if a % b == 0 {
        return b
    }
    return gcd(b, a % b)
}

func isCoPrime(a, b int) bool {
    return gcd(a, b) == 1
}

//    Calculates a^b mod m
func modulo(a, b, m int) int {
    res := 1
    for b > 0 {
        if b & 1 == 1 {
            res = (res * a) % m
        }
        b = b >> 1
        a = (a * a) % m
    }
    return res
}
//    Return modulo pattern and the bool code if it loops perfectly.
func getPattern(a, b int) (int, bool) {
    fmt.Printf("Testing pattern for %v mod %v\n", a, b)
    temp := a % b
    cache := make(map[int]bool)
    result := 0
    if isCoPrime(a, b) {
        return phi(b), true
    }
    for {
        if temp == 0 {
            result++
            return result, false
        }
        if _, ok := cache[temp]; ok {
            return result, true
        }
        result++
        cache[temp] = true
        // fmt.Printf("Pattern %v: %v\n", result, temp)
        temp = (temp * a) % b
    }
}
func expModulo(as []int, n int) (int, bool) {
    // return the result, status.
    // status is true if it encountered 0 in the call stack, otherwise false.
    if len(as) == 0 {
        return 1, true
    }
    var result, curN, chain int
    curN = as[0]
    repetition, ok := getPattern(curN, n)
    if curN == 0 {
        fmt.Printf("Special case of 0, checking chain %v\n", as)
        //    Special case of 0, when 0 is the last element or first/middle element
        if len(as) == 1 {
            fmt.Printf("0 is last element, return 0\n")
            return 0, true
        }
        for _, v := range as {
            if v != 0 {
                fmt.Printf("Chain length %v, returning %v\n", chain, (chain + 1) % 2)
                return (chain + 1) % 2, true
            }
            chain++
        }
        fmt.Printf("Chain length %v, returning %v\n", chain, (chain + 1) % 2)
        return (chain + 1) % 2, true
    } else if len(as) > 1 {
        if !ok && as[1] > repetition {
            //    Special case of not perfect loop, terminating the modulo chain in 0
            fmt.Printf("Not perfect loop, returning %v\n", n)
            return n, false
        }
        result, _ = expModulo(as[1:], repetition)
        fmt.Printf("Currently Processing %v -> %v\n", as, result)
        fmt.Printf("Performing modulo (%v, %v, %v)\n", curN, result, n)
        t := modulo(curN, result, n)
        if curN != 0 && t == 0 {
            return n, false
        }
        return modulo(curN, result, n), false
    }
    v := curN % n
    if curN != 0 && v == 0 {
        return n, false
    }
    return curN % n, false
}
func LastDigit(as []int) int {
    res, _ := expModulo(as, 10)
    return res % 10
}
____________________________
package kata

import (
	"math/big"
)

func LastDigit(as []int) int {
	var result = big.NewInt(1)
	for i := len(as) - 1; i >= 0; i-- {
		if result.Cmp(big.NewInt(4)) == -1 {
			result.Exp(big.NewInt(int64(as[i])), result, nil)
		} else {
			result.Exp(big.NewInt(int64(as[i])), result.Add(result.Mod(result, big.NewInt(4)), big.NewInt(4)), nil)
		}
	}

	return int(result.Rem(result, big.NewInt(10)).Int64())
}
