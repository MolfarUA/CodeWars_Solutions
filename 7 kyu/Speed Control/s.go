56484848ba95170a8000004d


package kata

import "math"

func Gps(s int, segments []float64) int {
  var maxSpeed float64
  for index := 1; index < len(segments); index++ {
    startSegment, endSegment := segments[index-1], segments[index]
    kmPerHour := 3600.0 * (endSegment - startSegment) / float64(s)
    maxSpeed = math.Max(maxSpeed, kmPerHour)
  }
  return int(maxSpeed)
}
_____________________________
package kata

import "math"

func Gps(s int, x []float64) int { //nolint
  if len(x) <= 1 {
    return 0
  }
  sect := sections(x)
  var maxHSpeed float64
  for _, v := range sect {
    if c := (3600 * v) / float64(s); c > maxHSpeed {
      maxHSpeed = c
    }
  }
  return int(math.Floor(maxHSpeed))
}

func sections(x []float64) (sect []float64) {
  for i := 1; i < len(x); i++ {
    sect = append(sect, x[i]-x[i-1])
  }
  return
}
_____________________________
package kata

func Gps(s int, x []float64) int {
    var maxSpeed = 0.0
    
    for i := 0; i < len(x) - 1; i++ {
      deltaDistance := x[i + 1] - x[i]
      avSpeed := (3600 * deltaDistance) / float64(s)
      if maxSpeed < avSpeed {
        maxSpeed = avSpeed
      }
    }
    
    return int(maxSpeed)
}
