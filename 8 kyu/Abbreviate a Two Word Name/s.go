57eadb7ecd143f4c9c0000a3


package kata

import "strings"

func AbbrevName(name string) string{
  words := strings.Split(name, " ")
  return strings.ToUpper(string(words[0][0])) + "." + strings.ToUpper(string(words[1][0]))
}
_________________________
package kata
import "strings"
func AbbrevName(name string) string{
  var x = strings.Index(name, " ")
  return strings.ToUpper(string(name[0])+"."+string(name[x+1]))

}
_________________________
package kata
import "strings"

func AbbrevName(name string) string{
  var parts []string
  for _, part := range strings.Split(name, " ") {
    parts = append(parts, strings.ToUpper(part[:1]))
  }
  return strings.Join(parts, ".")
}
