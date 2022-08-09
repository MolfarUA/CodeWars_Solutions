57f780909f7e8e3183000078


package kata

func Grow(arr []int) int{
  result := 1
  
  for _, n := range arr {
    result *= n
  }
  
  return result
}
_______________________
package kata

func Grow(arr []int) int {
  v := arr[0]

  for _, val := range arr[1:] {
    v *= val
  }

  return v
}
_______________________
package kata

func Grow(arr []int) int{
  var prod int
  prod = 1
  for i:=0; i < len(arr); i++ {
    prod *= arr[i]
  }
  return prod
}
