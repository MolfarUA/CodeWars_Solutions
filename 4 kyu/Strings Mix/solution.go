package kata

import (
  "strings"
  "sort"
  
)

func Mix(s1, s2 string) string {
    alphabase := "abcdefghijklmnopqrstuvwxyz"
    result := []string{}
    for _, c := range alphabase {
      nb_s1 := strings.Count(s1, string(c))
      nb_s2 := strings.Count(s2, string(c))
      if nb_s1 > 1 || nb_s2 > 1 {
          if nb_s1 == nb_s2 {
               result = append(result, "=:" + strings.Repeat(string(c), nb_s1))
          }
          if nb_s1 > nb_s2 {
               result = append(result, "1:" + strings.Repeat(string(c), nb_s1))
          }
          if nb_s1 < nb_s2 {
               result = append(result, "2:" + strings.Repeat(string(c), nb_s2))
          }
      }
    }
    sort.Slice(result, func(i, j int) bool {
        if len(result[i]) == len(result[j]) {
            return result[i] < result[j]
        }
        return len(result[i]) > len(result[j])
    })
    return strings.Join(result, "/")
}

__________________________________________________
package kata

import (
  "sort"
  "strings"
)

type pair struct {
  name   string
}

type pairList []pair

func (e pairList) Len() int {
  return len(e)
}

func (e pairList) Less(i, j int) bool {
  a := len(e[i].name)
  b := len(e[j].name)
  if a > b {
    return true
  } else if a == b {
    return 0 > strings.Compare(e[i].name, e[j].name)
  } else {
    return false
  }
}

func (e pairList) Swap(i, j int) {
  e[i], e[j] = e[j], e[i]
}

func Mix(s1, s2 string) string {
  var arr [128]int
  for i := 0; i < len(s1); i++ {
    arr[s1[i]]++
  }
  var brr [128]int
  for i := 0; i < len(s2); i++ {
    brr[s2[i]]++
  }
  pairs := make([]pair, 0, 26)
  size := 0
  for i := 'a'; i <= 'z'; i++ {
    if arr[i]>1 || brr[i] > 1 {
      var s uint8
      c := 1
      if arr[i] == brr[i] {
        s = '='
        c = arr[i]
      } else if arr[i] > brr[i] {
        s = '1'
        c = arr[i]
      } else {
        s = '2'
        c = brr[i]
      }
      var sb strings.Builder
      for j := 0; j < c; j++ {
        sb.WriteByte(byte(i))
      }
      pairs = append(pairs, pair{name: string(s)+":"+sb.String()})
      size++
    }
  }
  sort.Sort(pairList(pairs))
  var sb strings.Builder
  for i := 0; i < len(pairs); i++ {
    sb.WriteString(string(pairs[i].name))
    if i != len(pairs)-1 {
      sb.WriteByte('/')
    }
  }
  return sb.String()
}

__________________________________________________
package kata

import (
  "sort"
  "fmt"
)

type result struct {
  str        string
  countRune  int
  compareStr int
}

type resultArray []result

func (a resultArray) Len() int { return len(a) }
func (a resultArray) Less(i, j int) bool {
  if a[i].countRune > a[j].countRune {
    return true

  } else if a[i].countRune == a[j].countRune {
    if a[i].compareStr < a[j].compareStr {
      return true
    } else if a[i].compareStr == a[j].compareStr {
      if a[i].str < a[j].str {
        return true
      }
    }
  }
  return false
}
func (a resultArray) Swap(i, j int) { a[i], a[j] = a[j], a[i] }
func (a resultArray) String() string {
  var resultStr string
  for _, v := range a {
    resultStr += v.str
  }
  if len(a) > 0 {
    return resultStr[:len(resultStr)-1]
  }
  return ""
}

func Mix(s1, s2 string) string {
  fmt.Println(s1)
  fmt.Println()
  fmt.Println(s2)
  resM := make(map[rune]int)
  var res resultArray
  m1 := accountStr(s1)
  m2 := accountStr(s2)
  for k, v := range m1 {
    resM[k] += v
  }
  for k, v := range m2 {
    resM[k] += v
  }

  for k := range resM {
    if m1[k] > m2[k] {
      res.appendResult(1, m1[k], k)
    } else if m1[k] < m2[k] {
      res.appendResult(2, m2[k], k)
    } else {
      res.appendResult(3, m2[k], k)
    }
  }
  sort.Sort(res)

  return res.String()
}

func (r *resultArray) appendResult(stringNumber, runeCount int, symbol rune) {

  if runeCount < 2 {
    return
  }
  var resultStr string

  switch stringNumber {
  case 1:
    resultStr += "1:"
  case 2:
    resultStr += "2:"
  case 3:
    resultStr += "=:"
  }

  for i := 0; i < runeCount; i++ {
    resultStr += string(symbol)
  }
  resultStr += "/"
  *r = append(*r, result{resultStr, runeCount, stringNumber})

}

func accountStr(s string) (res map[rune]int) {
  res = make(map[rune]int)
  for _, c := range s {
    if c >= 'a' && c <= 'z' {
      res[c]++
    }
  }
  return
}

__________________________________________________
package kata

import  (
    re  "regexp"
        "sort"
    sc  "strconv"
        "strings"
        )

func Mix(str ...string) string {
  cull := re.MustCompile(`[^a-z]*`)
  mS := make(map[string][]byte)
  for i, s := range str {
    sI := cull.ReplaceAll([]byte(s), nil)
    for len(sI) != 0 {
      pI := []byte(sc.Itoa(i+1)+":")
      pE, chr := []byte(`=:`), string(sI[0])
      iso := re.MustCompile(`[^`+ chr +`]*`)
      del := re.MustCompile(`[`+ chr +`]*`)
      sO := iso.ReplaceAll(sI, nil)
      sI = del.ReplaceAll(sI, nil)
      if len(sO) < 2 {continue}
      curr, prev := len(sO) + 2, len(mS[chr])
      if curr > prev {mS[chr] = append(pI, sO...)}
      if curr == prev {mS[chr] = append(pE, sO...)}
    }
  }
  sS, swap := []string {}, true
  for _, v := range mS {sS = append(sS, string(v))}
  sort.Strings(sS)
  for swap {
    swap = false
    for i := 1; i < len(sS); i++ {
      if len(sS[i]) > len(sS[i-1]) {
        swap, sS[i], sS[i-1] = true, sS[i-1], sS[i]
      } 
    }
  }
  return strings.Join(sS, "/")
}

__________________________________________________
package kata

import (
  "strings"
  "sort"
)

func Mix(s1, s2 string) string {
  // your code
  m1, m2 := map[rune]string{}, map[rune]string{}
  
  for _, r := range s1 {
    if r >= 'a' && r <= 'z' {
      m1[r] += string(r)
    }
  }
  for _, r := range s2 {
    if r >= 'a' && r <= 'z' {
      m2[r] += string(r)
    }
  }
  
  var res []string
  for k, v1 := range m1 {
    if len(v1) <= 1 {
      continue
    }
    prefix := "1:"
    if v2, ok := m2[k]; ok {
      if len(v1) == len(v2) {
        prefix = "=:"        
      } else if len(v1) < len(v2) {
        continue
      }
      delete(m2, k)
    }
    res = append(res, prefix+v1)
  }
  for _, v := range m2 {
    if len(v) <= 1 {
      continue
    }
    res = append(res, "2:"+v)
  }
  
  sort.Slice(res, func(i, j int) bool {
    if len(res[i]) == len(res[j]) {
      return res[i] < res[j]
    }
    return len(res[i]) > len(res[j])
  })
  
  return strings.Join(res, "/")
}
