package kata
import (
  "strings"
)
func FirstNonRepeating(str string) string {
    for _, c := range str {
        if strings.Count(strings.ToLower(str), strings.ToLower(string(c))) < 2 {
            return string(c)
        }
    }
    return ""
}
_______________________________________________
package kata

func FirstNonRepeating(str string) string {
  seen := make(map[rune]int)

  for _, r := range str {
    seen[r|32]++
  }

  for _, r := range str {
    if seen[r|32] == 1 {
      return string(r)
    }
  }

  return ""
}
_______________________________________________
package kata

import (
  "strings"
  "unicode"
)
  
func FirstNonRepeating(str string) string {
  lowerString := strings.ToLower(str)

  for _, r := range str {
    if strings.Count(lowerString, string(unicode.ToLower(r))) < 2 {
      return string(r)
    }
  }

  return ""
}
_______________________________________________
package kata

import "strings"

func FirstNonRepeating(str string) string {
  s := strings.ToLower(str)

  for i := 0; i < len(s); i++ {
    st := string(s[i])
    if strings.Index(s, st) == strings.LastIndex(s, st) {
      return string(str[i])
    }
  }
  return ""
}
