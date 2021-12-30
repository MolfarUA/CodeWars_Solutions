package kata

func DigitalRoot(n int) int {
    return (n - 1) % 9 + 1
}

________________________________
package kata

func getSum(n int) int {
  if n > 0 && n < 10 {
    return n
  } else if n <= 0 {
    return 0
  }

  return getSum(n/10) + getSum(n%10)
}

func DigitalRoot(n int) int {
  if n >= 0 && n < 10 {
    return n
  }
  return DigitalRoot(getSum(n))
}

________________________________
package kata

import (
  "strconv"
  "strings"
)

func DigitalRoot(num int) int {
  // ...
  stringSlice := strings.Split(strconv.Itoa(num), "")
  if len(stringSlice) == 1 {
    return num //if the number just have one digit, return the number
  }
//   Provided that we have more one digit
  for len(stringSlice) > 1 {
    sum := 0
    for _, v := range stringSlice {
      elem, _ := strconv.Atoi(v)
      sum += elem
    }
    stringSlice = strings.Split(strconv.Itoa(sum), "")
  }
//   convert the first element in the slice of string to an integer
  ans, _ := strconv.Atoi(stringSlice[0])
  
  return ans
}
