package kata
import (
  "strconv"
)

type Hack struct {}

func (h *Hack) MatchString(s string) bool {
  if i, err := strconv.ParseUint(s, 2, 64); err == nil {
        return i % 7 == 0
  }
  
  return false
}

var Solution = Hack{}

__________________________________
package kata
import "regexp"
var Solution = regexp.MustCompile(`^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$`)

_______________________________
package kata
import "regexp"
var q1q4 = "1(01*00)*01*01|0((0|11)|10(01*00)*01*01)"
var q4q4 = "1((0|11)|10(01*00)*01*01)"
var q4q0 = "110(01*00)*1"
var q1q1 = "(" + q1q4 + ")(" + q4q4 + ")*0"
var q1q0a = "1(01*00)*1|010(01*00)*1"
var q1q0b = "(" + q1q4 + ")(" + q4q4 + ")*(" + q4q0 + ")"
var q1q0 = "(" + q1q1 + ")*((" + q1q0a + ")|(" + q1q0b + "))"
var q0q0 = "0|1(" + q1q0 + ")"
var Solution = regexp.MustCompile("^(0|1(" + q1q0 + "))(" + q0q0 + ")*$")

_________________________
package kata
import "regexp"
var Solution = regexp.MustCompile("^(0|(10((0|11)(1|00))*(10|(0|11)01)|11)(01*0(0|101|1(1|00)((0|11)(1|00))*(10|(0|11)01)))*1)+$")
