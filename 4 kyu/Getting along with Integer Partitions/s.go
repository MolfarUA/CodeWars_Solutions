55cf3b567fc0e02b0b00000b


package kata

import "fmt"
import "sort"

func removeDuplicates(elements []int) []int {
  // Use map to record duplicates as we find them.
  encountered := map[int]bool{}
  result := []int{}

  for v := range elements {
    if encountered[elements[v]] == true {
      // Do not add duplicate.
    } else {
      // Record this element as an encountered element.
      encountered[elements[v]] = true
      // Append to result slice.
      result = append(result, elements[v])
    }
  }
  // Return the new slice.
  return result
}

func ruleAsc(n int) []int {
  res := make([]int, 0)
  a := make([]int, n + 1)
  k := 1
  a[1] = n
  for k != 0 {
    x := a[k - 1] + 1
    y := a[k] - 1
    k -= 1
    for x <= y {
      a[k] = x
      y -= x
      k += 1
    }
    a[k] = x + y
    product := 1
    for j := 0; j <= k; j++ {
      product *= a[j]
    }
    res = append(res, product)
  }
  sort.Ints(res)
  res = removeDuplicates(res)
  return res
}

func Part(n int) string {
  partition := ruleAsc(n)
  r := partition[len(partition) - 1] - partition[0]
  sum := 0
  for i := 0; i < len(partition); i++ {
    sum += partition[i]
  }
  mean := float64(sum) / float64(len(partition))
  median := 0.0
  if len(partition) % 2 != 0 {
    median = float64(partition[len(partition) / 2])
  } else if len(partition) != 1 {
    median = float64(partition[len(partition) / 2 - 1] + partition[len(partition) / 2]) / 2.0
  } else {
    median = float64(partition[0])
  }
  return fmt.Sprintf("Range: %v Average: %.2f Median: %.2f", r, mean, median)
}
_____________________________
package kata

import (
  "sort"
  "fmt"
)

const MAXINTEGER = 50

// Column of table is min value in partition, from 1 to n/2
// Item of table is products of partitions whoes min value equal to column number
var table = [MAXINTEGER][][]int{}

func initTable(n int) int {
  if n != 0 && len(table[n-1]) == 0 {
    initTable(n - 1)
  }

  maxColumn := (n + 1) / 2
  table[n] = make([][]int, maxColumn+1)
  table[n][0] = []int{n + 1}

  count := 0
  for i := 1; i <= maxColumn; i++ {
    // partitions whoes min value is i contain (n-i+1 * i) and table[n-i][j] (j >= i)

    previous := 0
    for j := len(table[n-i]) - 1; j >= i; j-- {
      previous += len(table[n-i][j])
    }

    // addtional 1 is n-i+1 * i
    table[n][i] = make([]int, 0, previous+1)
    table[n][i] = append(table[n][i], (n-i+1)*i)
    count++

    for j := len(table[n-i]) - 1; j >= i; j-- {
      for _, v := range table[n-i][j] {
        table[n][i] = append(table[n][i], v*i)
        count++
      }
    }
  }

  return count
}

func merge(columns [][]int, count int) []int {
  prod := make([]int, 0, count)
  m := make(map[int]bool, count)

  for _, c := range columns {
    for _, v := range c {
      m[v] = true
    }
  }

  for k := range m {
    prod = append(prod, k)
  }

  return prod
}

func average(prod []int) float64 {
  sum := 0.0
  for _, v := range prod {
    sum += float64(v)
  }

  return sum / float64(len(prod))
}

func median(prod []int) float64 {
  l := len(prod)

  if l%2 == 0 {
    return float64(prod[l/2]+prod[l/2-1]) / 2.0
  }

  return float64(prod[l/2])
}

func Part(n int) string {
  n -= 1
  count := initTable(n)
  prod := merge(table[n], count)
  sort.Ints(prod)

  return fmt.Sprintf("Range: %d Average: %.2f Median: %.2f",
    prod[len(prod)-1]-1, average(prod), median(prod))
}
