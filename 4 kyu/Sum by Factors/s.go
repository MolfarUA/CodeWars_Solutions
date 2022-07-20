54d496788776e49e6b00052f


package kata

import (
  "fmt"
  "sort"
)

func SumOfDivided(lst []int) string {
  var sums = make(map[int]int)

  for _, n := range lst {
    positiveN := n
    if n < 0 {
      positiveN = n * -1
    }
    for i := 2; i*i <= positiveN; i++ {
      if positiveN%i == 0 {
        sums[i] += n
        for positiveN%i == 0 {
          positiveN /= i
        }
      }
    }
    if positiveN > 1 {
      sums[positiveN] += n
    }
  }

  keys := []int{}
  for key := range sums {
    keys = append(keys, key)
  }
  sort.Ints(keys)

  result := ""
  for _, key := range keys {
    result += fmt.Sprintf("(%d %d)", key, sums[key])
  }
  return result
}
________________________________________________
package kata

import (
  "fmt"
  "math"
)

func SumOfDivided(lst []int) (res string) {
  primes := getPrimesInRange(getAbsMax(lst))
  var sum, flag int
  for _, i := range primes {
    sum, flag = 0, 0
    for _, l := range lst {
      if (l % i) == 0 {
        sum += l
        flag = 1
      }
    }
    if flag == 1 {
      res = fmt.Sprintf("%v(%v %v)", res, i, sum)
    }
  }
  return
}

func getAbsMax(lst []int) int {
  i := getIntAsAbosulteFloat(lst[0])
  for _, n := range lst {
    if getIntAsAbosulteFloat(n) > i {
      i = getIntAsAbosulteFloat(n)
    }
  }
  return int(i)
}

func getIntAsAbosulteFloat(i int) float64 {
  return math.Abs(float64(i))
}

func getPrimesInRange(limit int) (p []int) {
  p = []int{2}
  for i := 3; i <= limit; i += 2 {
    isPrime := true
    for j := 3; j < (i / 2); j += 2 {
      if i%j == 0 {
        isPrime = false
        break
      }
    }
    if isPrime == true {
      p = append(p, i)
    }
  }
  return
}
________________________________________________
package kata

import (
  "sort"
  "strconv"
)

func PrimeFactors(n int) (pfs []int) {
  if n < 0 {
    n *= -1
  }
  // Get the number of 2s that divide n
  for n%2 == 0 {
    pfs = append(pfs, 2)
    n = n / 2
  }

  // n must be odd at this point. so we can skip one element
  // (note i = i + 2)
  for i := 3; i*i <= n; i = i + 2 {
    // while i divides n, append i and divide n
    for n%i == 0 {
      pfs = append(pfs, i)
      n = n / i
    }
  }

  // This condition is to handle the case when n is a prime number
  // greater than 2
  if n > 2 {
    pfs = append(pfs, n)
  }

  return
}

func SumOfDivided(lst []int) string {
  result := make(map[int]int)
  for _, v := range lst {
    repeat := 0
    pfs := PrimeFactors(v)
    for _, f := range pfs {
      if repeat == 0 || repeat-f != 0 {
        result[f] += v
      }
      repeat = f
    }
  }

  var keys []int
  for k, _ := range result {
    keys = append(keys, k)
  }
  sort.Ints(keys)

  s := ""
  for _, v := range keys {
    s += "(" + strconv.Itoa(v) + " " + strconv.Itoa(result[v]) + ")"
  }
  return s
}
