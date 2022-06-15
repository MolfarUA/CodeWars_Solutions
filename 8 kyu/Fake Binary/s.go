package kata


func FakeBin(x string) string {
  b:=[]byte(x)
  for i,v:=range b{
    if v<'5' {b[i]='0'}else{b[i]='1'}
  }
  return string(b)
}
__________________________________
package kata


func FakeBin(x string) (s string){
//   b := []rune(x) // make([]rune, len(x)):len(x) is in bytes length not rune length so using make is a dilemma
  for _, v := range x {
    s += map[bool]string{true: "0",false:"1"}[v<'5'] // no if: (slow, but fun)
//     b[i] = map[bool]byte{true:'0',false:'1'}[v<'5'] // no if: (slow, but fun)
  }
  return // string(b)
}
__________________________________
package kata

import "strconv"

func FakeBin(x string) string {
  var result string
  for _, v := range x {
    digit, _ := strconv.Atoi(string(v))
    if digit < 5 {
      result += "0"
    } else {
      result += "1"
    }
  }
  return result

}
__________________________________
package kata


func FakeBin(x string) string {
  temp := ""
  for i := 0; i < len(x); i++{
    if x[i] >= 48 && x[i] <= 52{
      temp += "0"
    } else{
      temp += "1"
    }
  }
  return temp
}
