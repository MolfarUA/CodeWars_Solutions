package kata

import (
  "strings"
)

func MakeUpperCase(str string) string {
    return strings.ToUpper(str)
}
_____________________________________________
package kata

import "strings"

var MakeUpperCase = strings.ToUpper
_____________________________________________
package kata

func MakeUpperCase(str string) string {
  res := make([]byte, len(str))
  for i := 0; i < len(str); i++ {
    c := str[i]
    if c >= 97 && c <= 122 {
      res[i] = c - 32
    } else {
      res[i] = c
    }
  }
  return string(res)
}
_____________________________________________
package kata

func MakeUpperCase(str string) string {
    STR := ""
    for _, i := range str {
      if i >= 97 && i <= 123 {
        STR += string(i-32)
      } else {
        STR += string(i)
      }
    }
    return STR 
}
