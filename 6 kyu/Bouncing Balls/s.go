package kata

func BouncingBall(h, bounce, window float64) int {
    if h < 0 || bounce <= 0 || 1 <= bounce || h < window {
        return -1
    }
    
    var count int = -1
    for ; h > window; h *= bounce {
        count += 2 
    }
    
    return count
}
_______________________________________________
package kata

func BouncingBall(h, bounce, window float64) int {
  if h <= window || bounce <= 0 || bounce >= 1 {
    return -1
  } else {
    return 2 + BouncingBall((h*bounce), bounce, window)
  }
}
_______________________________________________
package kata

import "math"

func BouncingBall(h, bounce, window float64) int {
    if !(h > 0 && 0 < bounce && bounce < 1 && window < h) {
        return -1
    }
    return int(math.Ceil(math.Log(window / h) / math.Log(bounce))) * 2 - 1
}
_______________________________________________
package kata

func BouncingBall(h, bounce, window float64) int {
  // your code
  if h <= 0 || bounce <= 0 || bounce >= 1 || window >= h {
    return -1
  }
  count := 1
  bHeight := h*bounce
  for  bHeight > window {
    bHeight = bHeight * bounce
    count += 2
  }
  return count
}
_______________________________________________
package kata

func BouncingBall(h, bounce, window float64) int {
  if h <= 0 || bounce <= 0 || bounce >= 1 || window >= h {
    return -1
  }
  var result = 1
  
  var bounceHeight = h * bounce
  
  for bounceHeight > window {
    result += 2
    bounceHeight = bounceHeight * bounce
  }
  
  return result
}
