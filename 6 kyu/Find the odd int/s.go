package kata

func FindOdd(seq []int) int {
    res := 0
    for _, x := range seq {
        res ^= x
    }
    return res
}
_______________________________
package kata

func FindOdd(seq []int) int {
    // your code here
    
    m := make(map[int]int)
    
    for _, e := range seq {
      m[e]++
    }
    
    for k, v := range m{
      if v % 2 != 0 {
        return k
      }  
    }
    return 0
}
_______________________________
package kata

func FindOdd(seq []int) (res int) {
    for _, n := range seq {
        res ^= n
    }
    return
}
_______________________________
package kata

func FindOdd(seq []int) int {
  var m map[int] int
  m = make(map[int] int)
  for i:=0;i<len(seq);i++{
    m[seq[i]]++
  }
  for i:=0;i<len(seq);i++{
    if m[seq[i]]%2==1{
      return seq[i]
    }
  }
  return -1
}
_______________________________
package kata

func FindOdd(seq []int) int {
  m := map[int]bool{}
  for _, n := range seq {
    m[n] = !m[n]
  }
  for _, n := range seq {
    if m[n] {
      return n
    }
  }
  return 0
}
_______________________________
package kata

func FindOdd(seq []int) int {
  oddMap := make(map[int]bool)
  for _, n := range seq {
    oddMap[n] = !oddMap[n]
  }
  for n, odd := range oddMap {
    if odd {
      return n
    }
  }
  return -1
}
