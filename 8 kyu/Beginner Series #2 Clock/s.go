55f9bca8ecaa9eac7100004a


package kata

func Past(h, m, s int) int {
    return (h*3600000 + m*60000 + s*1000)    
}
__________________________
package kata

func Past(h, m, s int) int {
    return (h*60*60+m*60+s)*1000
}
__________________________
package kata

const MS_PER_SEC = 1000
const MS_PER_MIN = MS_PER_SEC * 60
const MS_PER_HOUR = MS_PER_MIN * 60

func Past(h, m, s int) int {
  return h*MS_PER_HOUR + m*MS_PER_MIN + s*MS_PER_SEC
}
__________________________
package kata

  func Past(h, m, s int) int {
    milliseconds := s
    milliseconds += m * 60
    milliseconds += h * 3600
    milliseconds *= 1000

    return milliseconds

  }
__________________________
package kata

func Past(h, m, s int) int {

      result := ((h * 3600) + (m * 60) + s) * 1000
      return result
   
}
__________________________
package kata

import "time"

func Past(h, m, s int) int {
  return int((time.Hour * time.Duration(h) + time.Minute * time.Duration(m) + time.Second * time.Duration(s)) / time.Millisecond)
}
