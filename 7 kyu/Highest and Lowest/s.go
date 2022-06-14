package kata

import (
  "strings"
  "strconv"
  "fmt"
)

func HighAndLow(in string) string {
  var tmpH, tmpL int
  for i, s := range strings.Fields(in) {
    n, _ := strconv.Atoi(string(s))
    if i == 0 {
      tmpH = n
      tmpL = n
    }

    if n > tmpH {
      tmpH = n
    }

    if n < tmpL {
      tmpL = n
    }
  }
  return fmt.Sprintf("%d %d", tmpH, tmpL)
}
______________________________
package kata

import (
  "fmt"
  "sort"
  "strconv"
  "strings"
)

func HighAndLow(in string) string {
  numStrings := strings.Fields(in)
  var nums = []int{}
  
  for _, i := range numStrings {
    j, _ := strconv.Atoi(i)
    nums = append(nums, j)
  }
  sort.Ints(nums)
  return fmt.Sprintf("%d %d", nums[len(nums)-1], nums[0])
}
______________________________
package kata

import (
  "strings"
  "strconv"
)

func HighAndLow(in string) string {
  d := strings.Fields(in)
  min := 0
  max := 0
  
  for i, s := range d {
      n, _ := strconv.Atoi(s)
      if i == 0 || n < min { min = n }
      if i == 0 || n > max { max = n }
  }
  
  return strconv.Itoa(max) + " " + strconv.Itoa(min)
}
______________________________
package kata

import (
  "fmt"
  "math"
  "strconv"
  "strings"
)

func HighAndLow(in string) string {
  // Code here or
  spt := strings.Split(in," ")
  min := math.MaxInt32
  max := math.MinInt32
  for _, value := range spt {
    cvt,_ := strconv.Atoi(value)
    if cvt < min {
      min = cvt
    }
    if cvt > max {
      max = cvt
    }
  }
  
  return fmt.Sprintf("%d %d",max,min)
}
