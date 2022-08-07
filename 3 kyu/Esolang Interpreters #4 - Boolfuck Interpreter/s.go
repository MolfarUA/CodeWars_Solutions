5861487fdb20cff3ab000030


package kata

func Boolfuck(code, input string) string {
  in := 0
  out := 0
  m := make([]byte, 30000)
  mp := len(m) / 2
  var output []byte
  for i := 0; i < len(code); i++ {
    switch code[i] {
    case '+': // Flips the value of the bit under the pointer
      index, bit := mp/8, mp%8
      m[index] ^= 1 << uint(bit)
    case ',': // Reads a bit from the input stream, storing it under the pointer.
      index, bit := in/8, in%8
      in++
      v := (int(input[index]) >> uint(bit)) & 1
      index, bit = mp/8, mp%8
      m[index] &^= 1 << uint(bit)
      m[index] = byte(int(m[index]) | (v << uint(bit)))
    case ';': // Outputs the bit under the pointer to the output stream
      index, bit := mp/8, mp%8
      v := (int(m[index]) >> uint(bit)) & 1
      index, bit = out/8, out%8
      out++
      if len(output) < index+1 {
        output = append(output, 0)
      }
      output[index] &^= 1 << uint(bit)
      output[index] = byte(int(output[index]) | (v << uint(bit)))
    case '<': // Moves the pointer left by 1 bit
      mp--
    case '>': // Moves the pointer right by 1 bit
      mp++
    case '[': // - If the value under the pointer is 0 then skip to the corresponding brace
      index, bit := mp/8, mp%8
      if m[index]&(1<<uint(bit)) == 0 {
        i = findMatch(code, i) - 1
      }
    case ']': // Jumps back to the matching pair, if the value under the pointer is 1
      index, bit := mp/8, mp%8
      if m[index]&(1<<uint(bit)) != 0 {
        i = findMatch(code, i) - 1
      }
    }
  }
  return string(output)
}
func findMatch(s string, i int) int {
  d := 1
  brace := s[i]
  looking4 := m[brace]
  if brace == ']' {
    d = -1
  }
  stack := []byte{}
  for ; i < len(s); i += d {
    switch s[i] {
    case brace:
      stack = append(stack, s[i])
    case looking4:
      if len(stack) == 1 {
        return i
      }
      stack = stack[:len(stack)-1]
    }
  }
  return -1
}

var m = map[byte]byte{'[': ']', ']': '['}
_____________________________
package kata

func Boolfuck(code, input string) string {
  in := []byte(input)
  inputOffset := uint(0)
  tape := make(map[int]byte, 0)
  pointer := 0
  output := make([]byte, 0)
  outpuOffset := uint(0)
  for i := 0; i < len(code); i++ {
    switch code[i] {
    case '+':
      tape[pointer] ^= 1
    case '<':
      pointer--
    case '>':
      pointer++
    case ',':
      read := in[inputOffset/8]
      tape[pointer] = (read >> (inputOffset % 8)) & 1
      inputOffset++
    case ';':
      if outpuOffset/8 == uint(len(output)) {
        output = append(output, 0)
      }
      output[outpuOffset/8] |= (tape[pointer] << (outpuOffset % 8))
      outpuOffset++
    case '[':
      if tape[pointer] == 0 {
        parenthesis := 1
        for i < len(code) && parenthesis != 0 {
          i++
          if code[i] == '[' {
            parenthesis++
          } else if code[i] == ']' {
            parenthesis--
          }
        }
      }
    case ']':
      if tape[pointer] == 1 {
        parenthesis := 1
        for i >= 0 && parenthesis != 0 {
          i--
          if code[i] == '[' {
            parenthesis--
          } else if code[i] == ']' {
            parenthesis++
          }
        }
      }
    }
  }
  return string(output)
}
_____________________________
package kata

import (
        "fmt"
        "strconv"
)

type tape struct {
        i int
        t map[int]byte
}

func newTape() *tape {
        return &tape{
                t: make(map[int]byte),
        }
}

func (t *tape) MoveLeft() {
        t.i--
}

func (t *tape) MoveRight() {
        t.i++
}

func (t *tape) Get() byte {
        b, ok := t.t[t.i]
        if !ok {
                b = '0'
        }
        return b
}

func (t *tape) Set(b byte) {
        t.t[t.i] = b
}

func (t *tape) Flip() {
        b := byte('0')
        if t.Get() == '0' {
                b = '1'
        }

        t.Set(b)
}

type stack struct {
        s []int
}

func newStack() *stack {
        return &stack{
                s: make([]int, 0),
        }
}

func (s *stack) Push(i int) {
        s.s = append(s.s, i)
}

func (s *stack) Pop() (i int) {
        n := len(s.s) - 1
        if n < 0 {
                return -1
        }

        s.s, i = s.s[:n], s.s[n]
        return
}

func strToBits(in string) []byte {
        var out []byte
        for _, c := range []byte(in) {
                big := []byte(fmt.Sprintf("%08b", c))
                little := []byte{
                        big[7], big[6], big[5], big[4], big[3], big[2], big[1], big[0],
                }

                out = append(out, little...)
        }
        return out
}

func bitsToStr(in []byte) string {
        // Padd if necessary
        m := len(in) % 8
        if m > 0 {
                padding := make([]byte, 8-m)
                for i := range padding {
                        padding[i] = '0'
                }
                in = append(in, padding...)
        }


        // Convert
        var out []byte
        for i := 0; i < len(in); i += 8 {
                little := in[i : i+8]
                big := []byte{
                        little[7], little[6], little[5], little[4], little[3], little[2], little[1], little[0],
                }
                by, _ := strconv.ParseUint(string(big), 2, 8)
                out = append(out, byte(by))
        }

        return string(out)
}

func Boolfuck(code, input string) string {
        // Build jumps cache
        jumps := make(map[int]int)
        s := newStack()
        for i, c := range code {
                if c == '[' {
                        s.Push(i)
                } else if c == ']' {
                        j := s.Pop()
                        if j < 0 {
                                continue
                        }

                        jumps[i] = j
                        jumps[j] = i
                }
        }

        // Prepare streams
        var inIndex int
        var out []byte
        in := strToBits(input)

        // Prepare tape
        t := newTape()

        for i := 0; i < len(code); i++ {
                switch code[i] {
                case '<':
                        t.MoveLeft()
                case '>':
                        t.MoveRight()
                case '+':
                        t.Flip()
                case ',':
                        t.Set(in[inIndex])
                        inIndex++
                case ';':
                        out = append(out, t.Get())
                case '[':
                        j, ok := jumps[i]
                        if t.Get() == '0' && ok {
                                i = j
                        }
                case ']':
                        j, ok := jumps[i]
                        if ok {
                                i = j - 1
                        }
                }
        }

        return bitsToStr(out)
}
