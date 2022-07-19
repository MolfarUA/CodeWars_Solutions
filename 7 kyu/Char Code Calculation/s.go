57f75cc397d62fc93d000059


package kata

func Calc(s string) int {
    n := 0
    for _,c := range s {
        if (c/10) == 7 {n++}
        if (c%10) == 7 {n++}
    }
    return 6*n
}
__________________________________
package kata

import "fmt"

func Calc(s string) int {
  t := ""
  for _, value := range s {
    t = fmt.Sprintf("%v%v", t, value)
  }
  o := 0
  for _, value := range t {
    value = value - '0'
    if value == 7 {
      o = o + 6
    }
  }
  
  return o
}
__________________________________
package kata
import "fmt"
import "strings"

func DigitSum(s string) int {
  sum := 0
  for _,x := range(s) {sum += int(x)-48}
  return sum
}

func Convert(s string) string {
  r := ""
  for _,x := range(s) {r += fmt.Sprintf("%d", int(x))}
  return r
}

func Calc(s string) int {
  return DigitSum(Convert(s)) - DigitSum(strings.Replace(Convert(s), string('7'), string('1'), -1))
}
