5659c6d896bc135c4c00021e


package kata

import (
    "sort"
    "strconv"
    "strings"
)

func NextSmaller(n int) int {
    ns := strconv.Itoa(n)
    digits := strings.Split(ns, "")
    digitsInt := make([]int, 0)
    hasSmaller := false
    for _, v := range digits {
        a, _ := strconv.Atoi(v)
        digitsInt = append(digitsInt, a)
    }
    for i := len(ns) - 1; i > 0; i-- {
        if digitsInt[i-1] > digitsInt[i] {
            j := i
            for ; j < len(ns); j++ {
                if digitsInt[j] >= digitsInt[i-1] {
                    break
                }
            }
            digitsInt[i-1], digitsInt[j-1] = digitsInt[j-1], digitsInt[i-1]
            sort.Slice(digitsInt[i:], func(x, y int) bool {
                return digitsInt[i+x] > digitsInt[i+y]
            })
            hasSmaller = digitsInt[0] != 0
            break
        }
    }
    if hasSmaller {
        result := 0
        for _, v := range digitsInt {
            result *= 10
            result += v
        }
        return result
    }
    return -1
}
_______________________________
package kata

import (
  "math"
  "sort"
)


func NextSmaller(n int) int {
  ds := digits(n)

  i, j := toSwap(ds)
  if i < 0 {
    return -1
  }

  ds[i], ds[j] = ds[j], ds[i]
  sort.Ints(ds[:i])

  res := 0
  for p, v := range ds {
    res += int(math.Pow10(p)) * v
  }

  return res
}

func toSwap(digits []int) (int, int) {
  l := len(digits)
  for i := 1; i < l; i++ {
    jMax := -1
    j := -1
    for k := i - 1; k > -1; k-- {
      if digits[k] < digits[i] && digits[k] > jMax && (i < l-1 || digits[k] != 0) {
        jMax = digits[k]
        j = k
      }
    }
    if j > -1 {
      return i, j
    }
  }
  return -1, -1
}

func digits(n int) []int {
  var ds []int
  for ; n > 0; n /= 10 {
    ds = append(ds, n%10)
  }
  return ds
}
_______________________________
package kata
import (

  "fmt"
)

func NextSmaller(n int) int {
  fmt.Println("n:",n)
  if n <= 10 {
    return -1
  }
  arr := getContent(n)
  nLen := len(arr)
  end:=0
  for i:=0;i< nLen-1;i++{
    if arr[i]<arr[i+1]{
      end=i+1
      break
    }
  }
  if end==0 {
    return -1
  }
  //找到end之后，在剩下的数字里面找到比end处小一点点的
  num:=end-1
  for i:=0;i< end;i++{
      if arr[i]>arr[num] && arr[i]<arr[end]{
        num=i
      }
  }
  tmp1:=arr[num]
  arr[num]=arr[end]
  arr[end]=tmp1
  if arr[nLen-1]==0{
    return -1
  }

  //这里应该不包含
  b:=arr[:end]
  blen:= len(b)
  for i:=0;i< blen;i++{
    for j:=i;j< blen;j++{
      if arr[i]>arr[j]{
        temp:=arr[i]
        arr[i]=arr[j]
        arr[j]=temp
      }
    }
  }
  return getArrSum(arr)
}
//将一个整数分解成数组
func getContent(n int) []int {
  var result = []int{}
  for i := 0; i < 20; i++ {
    result = append(result, n%10)
    n = n / 10
    if n < 10 {
      result = append(result, n)
      return result
    }
  }
  return result
}
//将一个数组还原成整数
func getArrSum(n []int) int {
  if len(n)==0{
    return 0
  }
  if len(n)==1{
    return n[0]
  }
  var result = 0
  for i := 1; i < len(n); i++ {
    temp:=n[i]
    for j:=0;j<i;j++{
      temp*=10
    }
    result+=temp
  }
  result+=n[0]
  return result
}
