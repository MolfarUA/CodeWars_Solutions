package kata

import "fmt"

func CreatePhoneNumber(n [10]uint) string {
  return fmt.Sprintf("(%d%d%d) %d%d%d-%d%d%d%d", n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], n[8], n[9])
}
_______________________________
package kata

import (
  "fmt"
  "strings"
)

func ArrayToString(numbers interface{}) string {
  return strings.Trim(strings.Replace(fmt.Sprint(numbers), " ", "", -1), "[]")
}

func CreatePhoneNumber(numbers [10]uint) string {
  str := ArrayToString(numbers)
  return fmt.Sprintf("(%s) %s-%s", str[0:3], str[3:6], str[6:10])
}
_______________________________
package kata

import (
  "fmt"
  "strings"
)

func CreatePhoneNumber(numbers [10]uint) string {
  var test string = strings.Trim(strings.Replace(fmt.Sprint(numbers), " ", "", -1), "[]")
  return fmt.Sprintf("(%s) %s-%s", test[0:3], test[3:6], test[6:10])  
}
_______________________________
package kata

import "fmt"

func CreatePhoneNumber(numbers [10]uint) string {
  tmp := make([]interface{}, len(numbers))
  for i, val := range numbers {
    tmp[i] = val
  }
  return fmt.Sprintf("(%d%d%d) %d%d%d-%d%d%d%d", tmp...)
}
_______________________________
package kata

import (
  "fmt"
)

func str(numbers []uint) string {
  s := ""
  for _, n := range numbers {
    s += fmt.Sprintf("%v", n)
  }
  return s
}

func CreatePhoneNumber(numbers [10]uint) string {
  return fmt.Sprintf("(%v) %v-%v", str(numbers[0:3]), str(numbers[3:6]), str(numbers[6:10]))
}
_______________________________
package kata

import ("fmt")

func CreatePhoneNumber(numbers [10]uint) string {
  stringNumbers := make([]interface{}, len(numbers))
  for idx, num := range numbers {
    stringNumbers[idx] = num
  }
  return fmt.Sprintf("(%d%d%d) %d%d%d-%d%d%d%d", stringNumbers...)
}
