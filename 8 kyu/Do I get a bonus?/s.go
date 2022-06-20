56f6ad906b88de513f000d96


package kata
import ( "fmt" )


func BonusTime(salary int, bonus bool) string {
  if bonus {
    salary = salary * 10
  }
  return fmt.Sprintf("£%d", salary)
}
__________________________
package kata

import "strconv"

func BonusTime(salary int, bonus bool) string {
  if bonus {
    salary *= 10
  }
  
  return "£" + strconv.Itoa(salary) 
}
__________________________
package kata

import "fmt"

func BonusTime(salary int, bonus bool) string {
  if bonus {
    salary *= 10
  }
  
  return fmt.Sprintf("£%d", salary)
}
