package kata

func Parse(data string) []int{
  output := []int{}
  var val int
  for _, s := range data {
    switch string(s) {
      case "i":
        val++
      case "d":
        val--
      case "s":
        val = val * val
      case "o":
        output = append(output, val)
    }
  }
  
  return output
}
__________________________________________
package kata

func Parse(data string) (res []int){
  i := 0
  res = make([]int, 0)
  for _, el := range data {
    switch el {
      case 'i': i++;
      case 'd': i--;
      case 's': i*=i;
      case 'o': res = append(res, i);
    }
  }
  return res
}
__________________________________________
package kata

func Parse(data string) []int {
  var curr int
  result:= []int{}
  for _, v := range data {
    switch v {
    case 'i':
      curr++
    case 'd':
      curr--
    case 's':
      curr *= curr
    case 'o':
      result = append(result, curr)
    }
  }
  return result
}
__________________________________________
package kata

func Parse(data string) []int {
  var tmp int
  result := []int{}
  for _, r := range data {
    switch r {
    case rune('i'):
      tmp++
    case rune('o'):
      result = append(result, tmp)
    case rune('d'):
      tmp--
    case rune('s'):
      tmp *= tmp 
    default:
      continue
    }
  }

  return result
}
