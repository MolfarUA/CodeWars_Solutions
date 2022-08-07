58c5577d61aefcf3ff000081


package kata

import "strings"

func Encode(s string,n int) string {
  b := board(len(s), n)
	sr := []rune(s)
	var builder strings.Builder
	for _, v := range b {
		builder.WriteRune(sr[v])
	}
	return builder.String()
}

func Decode(s string,n int) string {
  b := board(len(s), n)
	sr := []rune(s)
	decoded := make([]rune, len(s))
	for i, v := range b {
		decoded[v] = sr[i]
	}
	return string(decoded)
}

func board(w, r int) (p []int) {
	var px, py = 0, 1
	pattern := make([][]int, r)
	for i := 0; i < w; i++ {
		pattern[px] = append(pattern[px], i)
		px += py
		if px == 0 || px == r-1 {
			py *= -1
		}
	}

	for _, row := range pattern {
		for _, b := range row {
			p = append(p, b)
		}
	}
	return p
}
_____________________________
package kata

type index struct {
	up   bool
	rail int
}

func printRails(r [][]rune) (res string) {
	for _, str := range r {
		res += string(str)
	}
	return
}

func splitStr(s string, n int) [][]rune {
	res := make([][]rune, n)
	i := index{true, 0}

	for _, r := range s {

		res[i.rail] = append(res[i.rail], r)

		if i.rail == n-1 {
			i.up = false
		}
		if i.rail == 0 {
			i.up = true
		}

		if i.up {
			i.rail++
		} else {
			i.rail--
		}
	}
	return res
}

func Encode(s string, n int) string {
	return printRails(splitStr(s, n))
}

func Decode(s string, n int) string {
	rails := splitStr(s, n)
	slen := len(s)
	res := []rune{}
	for index, rail := range rails {
		rails[index] = []rune(s[:len(rail)])
		s = s[len(rail):]
	}
	i := index{true, 0}

	for x := 0; x < slen; x++ {
		res = append(res, rails[i.rail][0])
		rails[i.rail] = rails[i.rail][1:]

		if i.rail == n-1 {
			i.up = false
		}
		if i.rail == 0 {
			i.up = true
		}

		if i.up {
			i.rail++
		} else {
			i.rail--
		}

	}
	return string(res)
}
_____________________________
package kata

import "strings"

func Encode(s string,n int) string {
  var es string
  str := strings.Split( s, "" )

  for i := 0; i < n; i++ {
    ls := getLetterSkips( n - 1, i ) // [ letter til next top, letter til next bottom ]
    index := i
    skipIndex := 1

    for index < len( s ) {
      es += str[ index ]

      index += ls[ skipIndex ]
      skipIndex = Abs( skipIndex - 1 )
    }
  }
  
  return es
}

func Decode(s string,n int) string {
  str := strings.Split( s, "" )
  dec := make( []string, len( str ) )
  i := 0

  for j := 0; j < n; j++ {
    ls := getLetterSkips( n - 1, j )
    skipIndex := 1
    index := j

    for index < len( dec ) && i < len( str ) {
      dec[ index ] = str[ i ]

      i++
      index += ls[ skipIndex ]
      skipIndex = Abs( skipIndex - 1 )
    }
  }
  
  return strings.Join( dec, "" )
}

func getLetterSkips ( maxIndex int, rail int ) [2]int {
  if rail == 0 || rail == maxIndex {
    return [2]int{ maxIndex * 2, maxIndex * 2 }
  } else {
    return [2]int{ rail * 2, ( maxIndex - rail ) * 2 }
  }
}

func Abs ( x int ) int {
  if x < 0 { x = -x }
  return x
}
