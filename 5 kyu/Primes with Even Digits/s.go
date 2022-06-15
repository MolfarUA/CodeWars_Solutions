package kata

func isPrime(n int) bool{
  switch n % 10 {
  case 1,3,7,9:
    for  i := 3; i * i < n + 1; {
      if n % i == 0{
        return false
      }
      i += 2
    }
    return true
  }
  return false
}

func evenCount(n int) (evenCount int){
  for i := n/10; i > 0; i /= 10{
    ost := i % 10
    if ost % 2 == 0{evenCount++}
  }
  return 
} 

func F(n int) (primeNumber int) {
  var maxEvenCount int
  var positionCount int
  start := n
  if n % 2 == 0 {
    start--
  } else {
    start-=2
  }
  for i:=n; i > 0; i/=10{
    positionCount++
  }
  for i:=start; i > start/2; i -= 2{
    if positionCount - evenCount(i) <= 2{
      if isPrime(i){
        even := evenCount(i)
        if even > maxEvenCount{
          maxEvenCount = even
          primeNumber = i
        }
      }
    }
  }
  return
}
____________________________________________
package kata

func isPrime(n int) bool{
  switch n % 10 {
  case 1,3,7,9:
    for  i := 3; i * i < n + 1; {
      if n % i == 0{
        return false
      }
      i += 2
    }
    return true
  }
  return false
}

func evenCount(n int) (evenCount int){
  for i := n/10; i > 0; i /= 10{
    ost := i % 10
    if ost % 2 == 0{evenCount++}
  }
  return 
} 

func F(n int) (primeNumber int) {
  var maxEvenCount int
  var positionCount int
  start := n
  if n % 2 == 0 {
    start--
  } else {
    start-=2
  }
  for i:=n; i > 0; i/=10{
    positionCount++
  }
  for i:=start; i > start/2; i -= 2{
    if positionCount - evenCount(i) <= 2{
      if isPrime(i){
        even := evenCount(i)
        if even > maxEvenCount{
          maxEvenCount = even
          primeNumber = i
        }
      }
    }
  }
  return
}
____________________________________________
package kata

import "strconv"

func IsPrime(n int) bool {
  if n <= 2 || n % 2 == 0 {
    return n == 2
  }
  for d := 3; d * d <= n; d += 2 {
    if n % d == 0 {
      return false
    }
  }
  return true
}

func CountEven(n int) int {
  e := 0
  for n > 0 {
    if n % 2 == 0 {
      e++
    }
    n /= 10
  }
  return e
}

func F(n int) int {
  s := strconv.Itoa(n)
  max := len(s) - 1
  if s[0] == '1' {
    max -= 1
  }
  e, r := 0, 0
  for p := n - 1 - n % 2; p >= 2; p -= 2 {
    if IsPrime(p) {
      k := CountEven(p)
      if k == max {
        return p
      }
      if k > e {
        e, r = k, p
      }
    }
  }
  return r
}
____________________________________________
package kata

import (
  "strconv"
)
var evenDigits = map[rune]bool{ '0': true, '2':   true, '4': true, '6': true, '8': true }

func F(n int) int {
  for k := n - 1 ; ; k-- {
    s := strconv.Itoa(k)
    if s[0] == '1' {
      s = s[1:len(s) - 1]
    } else {
      s = s[0:len(s) - 1]
    }
    if check(s) && isPrime(k) {
      return k
    }
  }
  return 0
}

func check(s string) bool {
    for _,c := range s {
      if !evenDigits[c] {return false}
    }
  return true
}

func isPrime(n int) bool {
  if (n%2)==0||(n%3)==0||(n%5)==0||(n%7)==0 {return false}
  c := [8]int{4, 2, 4, 2, 4, 6, 2, 6}
  p := 7
  i := 0
  for p*p <= n {
    if (n%p)==0 {return false}
    p += c[i]
    i = (i+1)%8
  }
 return true
}
