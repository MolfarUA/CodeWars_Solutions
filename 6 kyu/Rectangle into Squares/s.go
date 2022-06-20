55466989aeecab5aac00003e


package kata

func SquaresInRect(lng int, wdth int) []int {
    var res []int
    if (lng == wdth) { return res}
    for lng != wdth {
        if lng < wdth {
            wdth, lng = lng, wdth
        }
        res = append(res, wdth)
        lng = lng - wdth
    }
    res = append(res, wdth)
    return res
}
______________________________
package kata

func SquaresInRect(lng int, wdth int) []int {
  var res []int
  if lng == wdth {
    return nil
  }
  
  for lng > 0 {
    if wdth > lng {
      wdth, lng = lng, wdth
    }
   
    lng -= wdth
    res = append(res, wdth)
  }
  
  return res
}
______________________________
package kata

func SquaresInRect(lng int, wid int) (sizes []int) {
    if lng == wid || lng * wid <= 0 { return nil}
  
    hi := max(lng, wid)
    lo := min(lng, wid)
  
    for {
      if hi == lo || lo == 0 { break }
      
      seg := make([]int, hi / lo)
      for i := range seg { seg[i] = lo }
      
      newHi := lo
      lo = hi - (lo * len(seg))
      hi = newHi
      
      sizes = append(sizes, seg...)
      
      continue
    }
  
    return sizes
}

func max(x, y int) int {
    if x < y {
        return y
    }
    return x
}

func min(x, y int) int {
    if x > y {
        return y
    }
    return x
}
