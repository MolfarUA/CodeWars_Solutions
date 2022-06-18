544675c6f971f7399a000e79


package kata
import "strconv"
func StringToNumber(str string) int {
  n, err := strconv.Atoi(str)
  if err != nil {panic(err)}
  return n
}
_______________________
package kata

import "strconv"

var StringToNumber = strconv.Atoi
_______________________
package kata

import "strconv"

func StringToNumber(str string) int {
  ret, _ := strconv.Atoi(str)
  return ret
}
_______________________
package kata

import (
  "strconv"
)


func StringToNumber(str string) (int, error) {
  return strconv.Atoi(str)
}
_______________________
package kata


func StringToNumber(str string) int {
  sign,num:=+1,0
  for i,ch := range str {
    if i==0 && ch=='-' { 
      sign=-1 
    }else{
      num*=10
      num+=int(ch-'0')
    }
  }
  return sign*num
}
