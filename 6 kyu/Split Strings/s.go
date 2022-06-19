515de9ae9dcfc28eb6000001


package kata

func Solution(str string) []string {
  var res []string
  if len(str) % 2 != 0 {
    str += "_"
  }
  for i := 0; i < len(str); i+=2 {
    res = append(res, str[i:i+2])
  }
  return res
}
________________________________
package kata

import "regexp"

func Solution(str string) []string {
  return regexp.MustCompile(".{2}").FindAllString(str+"_",-1)
}
________________________________
package kata

func Solution(str string) []string {
  var result []string
  l := len(str)
  if l % 2 != 0 {str +="_"}
  
  for i:=0; i<l; i+=2 {
     result = append(result, str[i:i+2])
  }
  
  return result
}
________________________________
package kata;
func Solution(s string) (r []string) {
  for i := 0; i < len(s); i+=2 {
    if i > len(s)-2 {
      r = append(r, s[i:] + "_");
    } else {
      r = append(r, s[i:i+2]);
    }
  }
  return;
}
________________________________
package kata

import "regexp"

func Solution(str string) []string {
  str += "_" 
  re := regexp.MustCompile(`.{2}`)
  return re.FindAllString(str, -1)
}
