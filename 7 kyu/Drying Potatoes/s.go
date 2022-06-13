package kata

func Potatoes(p0, w0, p1 int) int {
    return w0 * (100 - p0) / (100 - p1)
}
_______________________________________________
package kata

func Potatoes(p0, w0, p1 int) int {
    return (100 - p0) * w0 / (100 - p1)
}
_______________________________________________
package kata

const percent = 100

func Potatoes(p0, w0, p1 int) int {
  return int(float64(w0) * (float64(percent-p0) / float64(percent-p1)))
}
_______________________________________________
package kata

import (
    "math"
)

func Potatoes(p0, w0, p1 int) int {
    return int(math.Floor(float64(w0)  * (100.0 - float64(p0)) / (100.0 - float64(p1))))
}
_______________________________________________
package kata

func Potatoes(p0, w0, p1 int) int {
    matter := float64(w0) * (100 - float64(p0)) / 100
    return int(matter * (100 / (100 - float64(p1))))
}
