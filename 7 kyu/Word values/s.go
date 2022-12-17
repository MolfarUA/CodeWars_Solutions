598d91785d4ce3ec4f000018


package kata

func NameValue(my_list []string) []int {
	var result = make([]int, len(my_list))

	for idx, str := range my_list {
		for _, chr := range str {
			if chr >= 'a' && chr <= 'z' {
				result[idx] += int(chr-'a') + 1
			}
		}

		result[idx] = result[idx] * (idx + 1)
	}

	return result
}
_____________________________
package kata

func NameValue(words []string) []int {
	sums := []int{}
  for position, word := range words {
    wordSum := 0
    for _, c := range word {
      if 'a' <= c && c <= 'z' {
        wordSum += int(c) - int('a') + 1
      }
    }
    sums = append(sums, (position + 1) * wordSum)
  }
  return sums
}
_____________________________
package kata
 
func NameValue(my_list []string) []int {
  var vals []int
  for i, s := range my_list {
    v := 0
	  for _, c := range s {
      if c!=' ' {
        v += int(c) - 96
      }
    }
    vals = append(vals, (i+1) * v)
  }

  return vals
}
