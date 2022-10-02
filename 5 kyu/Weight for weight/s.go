55c6126177c9441a570000cc


package kata

import (
  "sort"
  "strings"
)

type byDigitSum []string

func digitSum(s string) int {
  sum := 0

  for _, rune := range s {
    sum += int(rune - '0')
  }

  return sum
}

func (ns byDigitSum) Len() int {
  return len(ns)
}

func (ns byDigitSum) Swap(i, j int) {
  ns[i], ns[j] = ns[j], ns[i]
}

func (ns byDigitSum) Less(i, j int) bool {
  ds1 := digitSum(ns[i])
  ds2 := digitSum(ns[j])

  return ds1 < ds2 || ds1 == ds2 && strings.Compare(ns[i], ns[j]) == -1
}

func OrderWeight(strng string) string {
  ns := strings.Split(strng, " ")
  sort.Sort(byDigitSum(ns))
  return strings.Join(ns, " ")
}
_______________________________
package kata

import (
  "sort"
  "strings"
)

func stringSum(s string) int { // calculates sum of str's digits
  sum := 0
  for _, v := range s {
    sum += int(v) - '0'
  }
  return sum
}

func OrderWeight(s string) string {
  // convert to arr
  arr := strings.Fields(s)
  
  // sort
  sort.SliceStable(arr, func(i, j int) bool { 
    if diff := stringSum(arr[i]) - stringSum(arr[j]); diff == 0  { // if same "weight"
      return arr[i] < arr[j] // just compare the strings directly
    } else {
      return diff < 0 // otherwise compare using weight diff
    }
  })
  
  // convert back to string
  return strings.Join(arr, " ")
}
_______________________________
package kata
import (
  "sort"
  "strings"
)
func OrderWeight(s string) string {
  a := strings.Fields(s)
  sort.Slice(a, func(i, j int) bool {
    si := sum(a[i])
    sj := sum(a[j])
    if si == sj {
      return a[i] < a[j]
    }
    return si < sj
  })
  return strings.Join(a, " ")
}
func sum(s string) int {
  i := 0
  for _, r := range s {
    i += int(r - '0')
  }
  return i
}
