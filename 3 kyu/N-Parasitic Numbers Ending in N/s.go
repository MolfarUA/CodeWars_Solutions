55df87b23ed27f40b90001e5


package kata

const alpha = "0123456789abcdef"

func CalculateSpecial(lastDigit, base int) string {
    result := []byte{}
    dividend, divisor, digit := lastDigit, lastDigit * base - 1, 0
    for digit != lastDigit || dividend != lastDigit {
      dividend *= base
      digit = dividend / divisor
      dividend %= divisor
      result = append(result, alpha[digit])
    }
  return string(result)
}
____________________________
package kata

import "math/big"

func CalculateSpecial(lastDigit, base int) string {
  LastDigit := big.NewInt(int64(lastDigit))
	Base := big.NewInt(int64(base))
	M := big.NewInt(int64(lastDigit))
	D := big.NewInt(int64(base*lastDigit - 1))
	LastDigitSquare := big.NewInt(int64(lastDigit * lastDigit))
	for l := 1; l < 1240; l++ {
		A := new(big.Int).Sub(M, LastDigitSquare)
		Mod := new(big.Int).Mod(A, D)
		if Mod.IsInt64() && Mod.Int64() == 0 {
			Div := new(big.Int).Div(A, D)
			Div.Mul(Div, Base)
			Div.Add(Div, LastDigit)
			return Div.Text(base)
		}
		M.Mul(M, Base)
	}
	return ""
}
____________________________
package kata
import (
        "math/big"
       )

func CalculateSpecial(ld, b int) string {
	i := 0
	bigLD := big.NewInt(int64(ld))
	num := big.NewInt(int64(ld))

	if ld*ld < b {
		num = big.NewInt(int64((10*ld + 1) * ld))
	}
	zerof := false
	last := big.NewInt(int64(0))
	for true {
		num.Mul(bigLD, num)
		if len(num.Text(b)) > 1 {
			if num.Text(b)[1:2] == "0" {
				zerof = true
			}
			l := len(num.Text(b)) / 2
			firstHalf := num.Text(b)[l:]
			secondHalf := num.Text(b)[:l]

			for firstHalf == secondHalf {
				num, _ = new(big.Int).SetString(firstHalf, b)
				l = len(num.Text(b)) / 2
				firstHalf = num.Text(b)[l:]
				secondHalf = num.Text(b)[:l]
			}
		}
		num.Add(shiftL(zerof, *num, b), bigLD)
		test := big.NewInt(0)
		if last.Text(b) == test.Mul(num, bigLD).Text(b) {
			num.Add(shiftLSpecial(*last, b), bigLD)
		}
    
		last.Add(num, big.NewInt(int64(0)))
		if last.Mul(last, bigLD).Text(b) == shiftR(*num, b).Text(b) {
			l := len(num.Text(b)) / 2
			firstHalf := num.Text(b)[l:]
			secondHalf := num.Text(b)[:l]

			for firstHalf == secondHalf {
				num, _ = new(big.Int).SetString(firstHalf, b)
				l = len(num.Text(b)) / 2
				firstHalf = num.Text(b)[l:]
				secondHalf = num.Text(b)[:l]
			}

			return num.Text(b)
		}
		i++
		zerof = false
	}
	return "error"
}

func shiftL(zero bool, num big.Int, base int) *big.Int {

	str := num.Text(base)
	if zero {
		str = "0" + str
	}
	chunk := str[1:len(str)]
	str2 := chunk + "0"
	res, _ := new(big.Int).SetString(str2, base)
	return res
}

func shiftLSpecial(num big.Int, base int) *big.Int {
	str := num.Text(base)
	str2 := str + "0"
	res, _ := new(big.Int).SetString(str2, base)
	return res
}

func shiftR(num big.Int, base int) *big.Int {
	str := num.Text(base)
	tail := str[len(str)-1:]
	chunk := str[:len(str)-1]
	str2 := tail + chunk
	res, _ := new(big.Int).SetString(str2, base)
	return res
}
____________________________
package kata

import (
  "math/big"
  "fmt"
)

 /*
  Strategy:
  N is n-parasitic (special) in base b:

  => n * N = n * b^(len(N)-1) + (N-n) / b
  substitute len(N) = l

  N(nb - 1) = n*b^l - n

  for l := (2..)
    if (n*b^l - n) % (nb - 1) == 0
      => N = (n*b^l - n) / (nb - 1)
  */

func pow(n *big.Int, p int64) *big.Int  {
  res := big.NewInt(1)
  for p > 0 {
    res.Mul(res, n)
    p--
  }
  return res
}

func CalculateSpecial(lastDigit, base int) string {
  
  parasitic := big.NewInt(0)
  zero := big.NewInt(0)
  n, b := big.NewInt(int64(lastDigit)), big.NewInt(int64(base))
  
  for l := int64(2); true; l++ {
    
    num := pow(b, l)
    num.Mul(n, num)
    num.Sub(num, n)
    
    den := big.NewInt(0)
    den.Mul(n,b)
    den.Sub(den, big.NewInt(1))
  
    mod := big.NewInt(0)
    mod.Mod(num, den)  
    if mod.Cmp(zero) == 0 {
      parasitic = parasitic.Div(num, den)
      break
    }
  }
  
  switch base {
  case 8:
    return fmt.Sprintf("%0o", parasitic)
  case 16:
    return fmt.Sprintf("%0x", parasitic)
  default:
    return fmt.Sprintf("%d",  parasitic)
  }
}
