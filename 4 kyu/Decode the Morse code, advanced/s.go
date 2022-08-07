54b72c16cd7f5154e9000457


package kata

import (
  "regexp"
  "strings"
  . "math"
)

func DecodeBits(bits string) string {
  bits = compact(strings.Trim(bits, "0"))
  
  bits = replace(bits, `111(0|$)`, "-")
  bits = replace(bits, `1(0|$)`, ".")
  bits = replace(bits, `0`, " ")

  return bits
}

func DecodeMorse(morseCode string) string {
  decoded := ""
  
  for _, word := range strings.Split(morseCode, "   ") {
    decodedWord := ""

    for _, char := range strings.Split(word, " ") {
      decodedWord += MORSE_CODE[char]
    }

    if (decodedWord != "") {
      decoded += " " + decodedWord
    }
  }

  return strings.Trim(decoded, " ")
}

func replace(src, re, newSubStr string) string {
  return regexp.MustCompile(re).ReplaceAllString(src, newSubStr)
}

func compact(bits string) string {
  chunks := regexp.MustCompile(`(0+|1+)`).FindAllString(bits, -1)
  
  // Find minimum chunk length
  min := MaxInt16
  for _, str := range chunks {
    if len(str) < min { min = len(str) }
  }

  // Compact string
  compacted := ""
  for _, str := range chunks {
    compacted += str[0:(len(str) / min)]
  }
  
  return compacted
}
_____________________________
package kata

import "strings"

func getTimeUnit(bits string) int {
  minTimeUnit := len(bits)
  
  oneCount := 0
  zeroCount := 0
  for _, bit := range bits {
    if bit == '1' {
      oneCount += 1
      if zeroCount > 0 && zeroCount < minTimeUnit {
        minTimeUnit = zeroCount
        zeroCount = 0
      }
    } else if bit == '0' {
      zeroCount += 1
      if oneCount > 0 && oneCount < minTimeUnit {
        minTimeUnit = oneCount
        oneCount = 0
      }
    }
  }
  return minTimeUnit
}

func DecodeBits(bits string) string {
  bits = bits[strings.Index(bits, "1"):strings.LastIndex(bits, "1") + 1]
  timeUnit := getTimeUnit(bits)
  
  var result string
  for _, word := range strings.Split(bits, strings.Repeat("0", 7 * timeUnit)) {
    for _, wordChar := range strings.Split(word, strings.Repeat("0", 3 * timeUnit)) {
       for _, char := range strings.Split(wordChar, strings.Repeat("0", timeUnit)) {
         if char == strings.Repeat("1", timeUnit) {
           result += "."
         } else if char == strings.Repeat("1", 3 * timeUnit) {
           result += "-"
         }
       }
       result += " "
    }
    result += "  "
  }
  return result
}

func DecodeMorse(morseCode string) string {
  var result string
  codes := strings.Split(morseCode, " ")
  for i := 0; i < len(codes); i++ {
    if len(codes[i]) != 0 {
      result += MORSE_CODE[codes[i]]
    } else if i + 1 < len(codes) && len(codes[i + 1]) == 0 {
      result += " "
    }
  }
  return strings.TrimSpace(result)
}
_____________________________
package kata

import (
  "regexp"
  "strings"
)

var charMap = map[byte]map[int]string{
  '0': {
    1: "",
    3: " ",
    7: "   ",
  },
  '1': {
    1: ".",
    3: "-",
  },
}


func getTimeUnit(charSlice []string) int {
  min := len(charSlice[0])
  
  for _, char := range charSlice {
    clen := len(char)
    if min > clen {
      min = clen
    }
  }
  return min
}

func DecodeBits(bits string) string {
  var res string
  
  bitsTrim := strings.Trim(bits, "0")
  
  re := regexp.MustCompile(`(0+)|(1+)`)
  charSlice := re.FindAllString(bitsTrim, -1)
  
  timeUnit := getTimeUnit(charSlice)

  for _, char := range charSlice {
    res += charMap[char[0]][len(char) / timeUnit]
  }
  return res
}

func DecodeMorse(morseCode string) string {
  var res []string
  
  morseCode = strings.Trim(morseCode, " ")
  
  for _, word := range strings.Split(morseCode, "   ") {
    var w string

    for _, letter := range strings.Split(word, " ") {
      w += MORSE_CODE[letter]
    }
    res = append(res, w)
  }
  
  return strings.Join(res, " ")
}
_____________________________
package kata
import (
  "strings"
  "regexp"
)

func getUnitLen(t string) int {
  r := regexp.MustCompile(`1+|0+`)
  allSubseq := r.FindAllString(t,-1)
  var minLen int  
  for i,v := range allSubseq {
    if i == 0 || minLen > len(v){ minLen = len(v) }
  } 
  return minLen
}

func DecodeBits(bits string) (res string) {
  b := strings.Trim(bits,"0") 
  if len(b) == 0 {return " "}  
  unit := getUnitLen(b)  
  pause := strings.Repeat("0",unit)
  c := strings.Split(b,pause)
  dot := strings.Repeat("1",unit)
  dash := strings.Repeat(dot,3)  
  var space int
  for _,v := range c {
    if len(v) == 0 { space++ }
    if space == 2 {res+=" ";space=0}
    if v == dot {res+="."}
    if v == dash {res+="-"}
  }
  return res
}

func DecodeMorse(morseCode string) (res string) {
  m := strings.TrimSpace(morseCode)
  if len(m) == 0 {return res}
  c := strings.Split(m, " ")
  var space int
  for _,v := range c {
    if len(v)==0 { space++}
    if space == 2 {res+=" ";space=0}
    res+=MORSE_CODE[v]
  }
  return res
}
