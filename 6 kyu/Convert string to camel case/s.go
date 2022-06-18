package kata

import (
  "regexp"
  "strings"
)

func ToCamelCase(s string) string {
  words := regexp.MustCompile("-|_").Split(s, -1)

  for i, w := range words[1:] {
    words[i+1] = strings.Title(w)
  }

  return strings.Join(words, "")
}
________________________
package kata

import (
  "strings"
)

func ToCamelCase(s string) string {
  if s == "" {return ""}
  result := strings.Title(strings.Replace(strings.Replace(s, "-", " ", -1), "_", " ", -1))
  result = s[:1] + result[1:]
  result = strings.Replace(result, " ", "", -1)
  return result
}
________________________
package kata

import (
  "regexp"
  "strings"
)

func ToCamelCase(s string) string {
  return regexp.MustCompile("[-_](.)").ReplaceAllStringFunc(s, func(w string) string {
    return strings.ToUpper(w[1:])
  })
}
________________________
package kata
import(
  "strings"
  "regexp"
  )
func ToCamelCase(s string) string {
  ss:=regexp.MustCompile("[_-]").Split(s,-1)
  css:=ss[0]
  for i := 1 ; i<len(ss);i++ {
    css+=strings.Title(ss[i])
  }
  return css
}
________________________
package kata
import "regexp"
import "strings"
func ToCamelCase(s string) string {
  return regexp.MustCompile(`[-_]\w`).ReplaceAllStringFunc(s, func (x string) string { return strings.ToUpper(string(x[1])) })
}
