package kata

func TwoSum(numbers []int, target int) [2]int {
    for i := 0; i < len(numbers)-1; i++ {
        for j := i+1; j < len(numbers); j++ {
            if numbers[i] + numbers[j] == target {
                return [2]int{i, j}
            }
        }
    }
    return [2]int{0, 0}
}
________________________________
package kata

import "fmt"

func TwoSum(numbers []int, target int) [2]int {
  var h = make(map[int]int)
  for i, v := range numbers {
    need := target - v
    if _, ok := h[v]; ok {
      fmt.Println(h[v], i)
      return [2]int{h[v], i}
    }
    h[need] = i
  }
  return [2]int{0, 0}
}
________________________________
package kata

func TwoSum(numbers []int, target int) [2]int {
    for i, num1 := range numbers {
      for j, num2 := range numbers {
        if i != j && num1+num2 == target {
          return [2]int{i, j}
        }
      }
    }
    return [2]int{}
}
________________________________
package kata

func TwoSum(numbers []int, target int) [2]int {
  seenAt := make(map[int]int)
  for i, x := range numbers {
    if j, seen := seenAt[target - x]; seen {
      return [2]int{j, i}
    }
    seenAt[x] = i
  }
  panic("pair not found")
}
________________________________
package kata

func TwoSum(numbers []int, target int) [2]int {
  mem := make(map[int]int)
  
  for i := 0; i < len(numbers); i++ {
    current := numbers[i]
    if val, ok := mem[current]; ok {
        return [2]int{val, i}
    }
    mem[target - current] = i
  }
  
  return [2]int{}
}
