package kata

import (
  "math"
  "fmt"
)

func IterPi(epsilon float64) (int, string) {
  n, v := 1.0, 1.0
  for math.Abs(math.Pi - 4*v) > epsilon {
    v += math.Pow(-1, n)/(2*n + 1)
    n += 1
  }
  return int(n), fmt.Sprintf("%.10f", 4*v)
}
________________________________________
package kata

import (
    "math"
    "fmt"
)

func IterPi(epsilon float64) (int, string) {
    const PI = 3.14159265358979323846
    var divisor float64 = 1.0
    var sign float64 = 1.0
    var count int = 0
    var sum float64 = 0.0
    for ; math.Abs(sum - PI) > epsilon ; {
        sum += sign * 4.0 / divisor
        divisor += 2.0
        sign *= -1.0
        count += 1
    }
    return count, fmt.Sprintf("%.10f", sum)
}
________________________________________
package kata
import ("math";"fmt")
func IterPi(epsilon float64) (int, string) {
  n, p4  := 1, 1.0 
  for i, one:=3.0,-1.0; math.Abs(math.Pi-4*p4)>epsilon; i += 2 {
    p4 += one/i;
    one = -one
    n++
  }
  return n,fmt.Sprintf("%1.10f",4*p4)
}
________________________________________
package kata

import (
  "math"
  "fmt"
  "strconv"
)

func LeibnizTerm(n int) float64 {
  power := math.Pow(-1, float64(n + 1))
  term := 1 / float64(2 * n - 1)
  return power * term
}

func IterPi(epsilon float64) (int, string) {
  i := 1
  result := 0.0
  fmt.Println(math.Pi, i)
  
  for math.Abs(result - math.Pi) > epsilon {
    result += 4 * (LeibnizTerm(i))
    i++
  }
  return i - 1, strconv.FormatFloat(result, 'f', 10, 64)
}
________________________________________
package kata
import "math"
import "fmt"

func IterPi(epsilon float64) (int, string) {
  var pi4 = 1.0
  var sign = -1.0
  var iterations = 1
  var denom = 3.0
  for math.Abs(4.0 * pi4 - math.Pi) >= epsilon {
    pi4 = pi4 + sign * (1.0 / denom)
    sign = sign * (-1.0)
    denom = denom + 2.0
    iterations = iterations + 1
  }
  return iterations, fmt.Sprintf("%.10f", 4.0 * pi4)
}

