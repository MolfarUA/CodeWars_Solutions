package kata

// ChooseBestSum is a recursive function to find the kvvalues in ls that
// sum to the greatest number <= t. returns -1 if not possible.
func ChooseBestSum(t, k int, ls []int) int {
  outerbest := -1
  for i, d := range ls {
    // not enough remaining values for this d to work
    if len(ls) < k {
      continue
    }
    // recursively choose best from t-d, until final level k=1
    if k > 1 {
      innerbest := ChooseBestSum(t-d, k-1, ls[i+1:])
      // if no best available at lower level, this d cant work
      if innerbest < 0 {
        continue
      }
      d += innerbest
    }
    if d <= t && d > outerbest {
      outerbest = d
    }
  }
  return outerbest
}
_______________________________________
package kata

func ChooseBestSum(t, k int, ls []int) int {
  if len(ls) < k || t < 0 {
    return -1
  }
  if k == 0 {
    return 0
  }
  skip := ChooseBestSum(t, k, ls[1:])
  take := ChooseBestSum(t - ls[0], k-1, ls[1:])
  if take > -1 {
    take += ls[0]
  }
  return max(skip, take)
}

func max(a, b int) int {
  if a > b {
    return a
  }
  return b
}
_______________________________________
package kata

func FindAllSums(k, i, s int, ls, rs *[]int) int {
  if k < 1 {return 0}
  for; i <= len(*ls)-k; i++ {
    if k == 1 {
      *rs = append(*rs, s+(*ls)[i])
    }else{
      FindAllSums(k-1,i+1,s+(*ls)[i],ls,rs)
    }
  }
  return 1
}

func ChooseBestSum(t, k int, ls []int) int {
  rs, r := make([]int, 0, 256), -1
  FindAllSums(k,0,0,&ls,&rs)
  for _, sum := range rs {
    if sum > r && sum <= t {r = sum}
  }
return r
}
_______________________________________
package kata

func max(a, b int) int {
  if a > b { return a }
  return b
}

func ChooseBestSum(t, k int, ls []int) (ret int) {
  if k > len(ls) { return -1 }
  if k == 1 {
    ret = -1
    for _, v := range ls {
      if v <= t && v > ret { ret = v }
    }
    return ret
  }
  if k == len(ls) {
    sum := 0
    for _, v := range ls { sum += v }
    if sum > t { return -1 }
    return sum
  }
  sub1 := ChooseBestSum(t, k, ls[1:])
  if sub1 == t || t <= ls[0] { return sub1 }
  sub2 := ChooseBestSum(t - ls[0], k - 1, ls[1:])
  if sub2 < 0 { return sub1 }
  return max(sub1, sub2 + ls[0])
}
