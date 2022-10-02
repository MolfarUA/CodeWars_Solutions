5547cc7dcad755e480000004


package kata

func RemovNb(m uint64) [][2]uint64 {
    n := m 
    var sum uint64 = n * (n + 1) / 2
    var res [][2]uint64
    for a := uint64(1); a <= n; a++ {
        if (sum - a) % (a + 1) == 0 {
            b := (sum - a) / (a + 1)
            if b < n {
                res = append(res, [2]uint64{a, b})
            }
        }
    }
    return res
}
______________________________
package kata

func RemovNb(m uint64) (res [][2]uint64) {
  sum := m * (m + 1) / 2
  for i := uint64(1); i <= m; i++ {
    j := (sum - i) / (1 + i)
    if (j <= m) && (((i * j) + i + j) == sum) {
      res = append(res, [2]uint64{i, j})
    }
  }
    
  return
}
______________________________
package kata

func RemovNb(m uint64) (result [][2]uint64) {
  var sum uint64 = (m * (m + 1)) / 2

  for i := uint64(1); i <= m; i++ {
    j := float64(sum-i) / float64(i+1)
    if uint64(j) <= m && j == float64(uint64(j)) {
      result = append(result, [2]uint64{i, uint64(j)})
    }
  }
  return
}
