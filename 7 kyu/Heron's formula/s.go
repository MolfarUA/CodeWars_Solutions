57aa218e72292d98d500240f


package kata

import "math"


func Heron(a, b, c int) (area float32) {
  var newA, newB, newC float64 = float64(a), float64(b), float64(c)
  var s float64 = (newA + newB + newC) / 2
  var result float64 = math.Sqrt(s * (s - newA) * (s - newB) * (s - newC))
  return float32(result)
}
________________________
package kata
  import "math"

func Heron(a, b, c int) (area float32) {
  
  var s float32 = float32(a+b+c) / 2
  var form float64 = math.Sqrt(float64(s * (s - float32(a)) * (s - float32(b)) * (s - float32(c))))
  return float32(math.Round(form*100) / 100)
}
________________________
package kata

import "math"
func Heron(a, b, c int) (area float32) {
 s := float64(a+b+c) / 2
  res := math.Sqrt(s * (s - float64(a)) * (s - float64(b)) * (s - float64(c)))
  area = float32(math.Trunc(res*100+0.5) / 100)
  return 
}
