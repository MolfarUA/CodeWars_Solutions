57cfdf34902f6ba3d300001e


package kata

import (
  "sort"
  "strings"
)

func TwoSort(arr []string) string {
  sort.Strings(arr)
  chars := strings.Split(arr[0], "")
  return strings.Join(chars, "***")
}
___________________________
package kata
import (
  "strings"
  "sort"
)
func TwoSort(arr []string) string {
  sort.Strings(arr)
  return strings.Join(strings.Split(arr[0],""), "***")
}
___________________________
package kata
import "sort"
func TwoSort(arr []string) (parola string) {
  sort.Strings(arr)
  for pos, char := range arr[0]{
    if pos !=  (len(arr[0])-1) {
      parola += string(char)
      parola += "***"
    }else{
      parola += string(char)
    }
  }
  return parola
}
