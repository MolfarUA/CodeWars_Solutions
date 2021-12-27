package kata
import "strings"
func duplicate_count(s string) (c int) {
    h := map[rune]int{}
    for _, r := range strings.ToLower(s) {
      if h[r]++; h[r] == 2 { c++ }
    }
    return
}
________________________
package kata

import "strings"

func duplicate_count(s1 string) (c int) {
    m := make(map[rune]int)
    for _,v := range strings.ToLower(s1) {
        m[v]++
        if m[v] == 2 { c++ }
    }      
    return
}
________________________
package kata

import "strings"

func duplicate_count(s1 string) int {
    counter := make(map[string]int)

    for _, s := range s1 {
      sl := strings.ToLower(string(s))
      counter[sl] += 1
    }

    sum := 0
    for _, v := range counter {
      if v > 1 {
        sum += 1
      }
    }

    return sum
}
_____________________
package kata

import "strings"

func duplicate_count(s1 string) (repeatCount int) {
  counters := make(map[rune]int)
  
  for _, letter := range strings.ToLower(s1) {
    if counters[letter] == 1 {
      repeatCount++
    }
    counters[letter]++
  }
  
  return
}
______________________
package kata

import "strings"

func duplicate_count(s1 string) int {
    var m map[byte] int
    var doubles int = 0
    
    m = make(map[byte]int)
    
    var lower string = strings.ToLower(s1)
    
    for i := 0; i < len(lower); i++ {
      m[lower[i]] += 1
      
      if m[lower[i]] == 2 {
        doubles += 1
      } 
    }
    
    return doubles
    
}
