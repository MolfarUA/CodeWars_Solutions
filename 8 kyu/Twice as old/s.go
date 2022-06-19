5b853229cfde412a470000d0


package kata
import "math"

func TwiceAsOld(dadYearsOld int, sonYearsOld int) int { 
  return int(math.Abs(float64(dadYearsOld - (sonYearsOld * 2))))
}
______________________________
package kata
func TwiceAsOld(dadYearsOld, sonYearsOld int) int { 
  x := dadYearsOld - sonYearsOld * 2 
  if x >= 0 { return x }
  return -x 
}
______________________________
package kata
import "math"
func TwiceAsOld(dadYearsOld, sonYearsOld int) int { 
  return int(math.Abs(float64(dadYearsOld - 2 * sonYearsOld)));
}
______________________________
package kata

func TwiceAsOld(dadYearsOld, sonYearsOld int) (years int) {
  switch {
  case dadYearsOld > (sonYearsOld * 2):
    for dadYearsOld != (sonYearsOld * 2) {
      dadYearsOld += 1
      sonYearsOld += 1
      years += 1
    }
  case dadYearsOld < (sonYearsOld * 2):
    for dadYearsOld != (sonYearsOld * 2) {
      dadYearsOld -= 1
      sonYearsOld -= 1
      years += 1
    }
  }

  return
}
______________________________
package kata

func TwiceAsOld(dadYearsOld, sonYearsOld int) int { 
  years := 2*sonYearsOld -dadYearsOld
  if years >=0 {return years } else {return -years}
  
}
______________________________
package kata

func TwiceAsOld(dadYearsOld, sonYearsOld int) int {
    var result = ( 2 * sonYearsOld - dadYearsOld)

  if result < 0 {
    return -result
  }
  return result
}
