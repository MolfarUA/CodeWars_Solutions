52597aa56021e91c93000cb0


package kata

func MoveZeros(arr []int) []int {
 	res:= make([]int,len(arr))
	ind:=0
	for i:=0;i<len(arr);i++{
		if arr[i]!=0{
			res[ind]=arr[i]
			ind++
		}
	}
	return res
}
_____________________________
package kata

func MoveZeros(arr []int) []int {
	var arrnew []int
	var arrzero []int

	for _, x := range arr {
		if x == 0 {
			arrzero = append(arrzero, x)
		} else {
			arrnew = append(arrnew, x)
		}
	}
	arrnew = append(arrnew, arrzero...)
	return arrnew
}
_____________________________
package kata

func MoveZeros(arr []int) []int {
  

  for i := 0; i<len(arr); i++ {
    for j:= 0; j<i; j++ {
      if arr[j] == 0 {
        arr[i], arr[j] = arr[j], arr[i]
      }
    }
  }
  return arr
}
