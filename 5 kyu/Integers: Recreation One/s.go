55aa075506463dac6600010d


package kata

import "math"

func ListSquared(m, n int) [][]int {
    res := make([][]int, 0)
    for i := m; i <= n; i++ {
      s := 0
      for j := 1; j <= i; j++ {
        if i % j == 0 {
          s += j*j
        }
      }
      if math.Mod(math.Sqrt(float64(s)), 1.) == 0 {
        res = append(res, []int{i, s})
      }
    }
    return res
}
________________________________
package kata

import "math"

func ListSquared(m, n int) [][]int {
  res := [][]int{}
  
  for i := m; i <= n; i++ {
    if i == 1 {
      res = append(res, []int{1, 1})
      continue
    }

    sum := 1 + (i * i)
    
    for j := 2; j <= (i / 2); j++ {
      if (i % j) == 0 {
        sum += j * j
      }
    }
    
    sqrt := int(math.Round(math.Sqrt(float64(sum))))
    
    if (sqrt * sqrt) == sum {
      res = append(res, []int{i, sum})
    }
  }

  return res
}
________________________________
package kata

import "math"

func ListSquared(m, n int)  [][]int {
  res := make([][]int,0)
  for i := m; i <= n; i++ {
    sumSqrDiv := sumSqrDiv(i)
    if sqrIsInt(sumSqrDiv) {
      res = append(res, []int{i, sumSqrDiv})
    }
  }
  return res
}

func sumSqrDiv(num int) int {
  divisors := divs(num)
  return sumSqrs(divisors)
}

func divs(num int) []int {
  divs := make([]int, 0)
  for i := 1; i <= num; i++ {
    if num % i == 0 {
      divs = append(divs, i)
    }
  }
  return divs
}

func sumSqrs(nums []int) int {
  sum := float64(0)
  for _, val := range nums {
    sum += math.Pow(float64(val),2)
  }
  return int(sum)
}

func sqrIsInt(num int) bool {
  sqr := math.Sqrt(float64(num))
  return sqr == float64(int(sqr))
}
