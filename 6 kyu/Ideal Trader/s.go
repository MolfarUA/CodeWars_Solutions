610ab162bd1be70025d72261


package kata

func IdealTrader(prices []float64) (o float64) {
  if len(prices) <= 1 {
    return 1
  }
  o = 1
  for i := 1; i < len(prices); i++ {
    if prices[i - 1] > prices[i] {
      continue
    }
    
    o *= prices[i] / prices[i - 1]
  }
  
  return
}
__________________________________
package kata

func IdealTrader(prices []float64) float64 {
  r, x := 1.0, prices[0]
  for i := 1; i < len(prices); i++ {
    y := prices[i]
    if y > x {
      r *= y / x
    }
    x = y
  }
  return r
}
__________________________________
package kata

func max(a float64, b float64) float64 {
  if a > b { return a } else { return b }
}

func IdealTrader(prices []float64) float64 {
  k := float64(1)
  for i, e := range prices {
    if i + 1 < len(prices) {
      if e > prices[i+1] { continue }
      k *= max(e / prices[i+1], prices[i+1] / e)
    }
  }
  return k
}
__________________________________
package kata

func IdealTrader(prices []float64) float64 {
  profit := 1.0
  for i := 1; i < len(prices); i++ {
    if prices[i] > prices[i-1] {
      profit *= prices[i] / prices[i-1]
    }
  }
  return profit
}
