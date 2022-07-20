57a5c31ce298a7e6b7000334


package kata
func BinToDec(bin string) int {
  n := 0
  for _, r := range bin {
    n *= 2
    n += int(r-'0')
  }
  return n
}
_________________________
package kata

import "strconv"

func BinToDec(bin string) int {
   r, _ := strconv.ParseInt(bin, 2, 64)
   return int(r)
}
_________________________
package kata

func BinToDec(bin string) int {
  var dec int
  for _, v := range bin {
    dec = dec*2 + int(v-'0')
  }
  return dec
}
_________________________
package kata


func BinToDec(bin string) int {
  cnt := 1
  result := 0
  for i := len(bin) - 1; i >= 0; i-- {
    if bin[i] == '1' {
      result += cnt
    }
    cnt<<=1
  }
  return result
}
