54acd76f7207c6a2880012bb


package kata

import (
  "math"
  "regexp"
  "strings"
  "sort"
)

func getBestLen(dataLen int, sampleLen float64) (times int, residual float64) {

  residual = math.MaxFloat64
  values := []int{1, 3, 7}
  for _, v := range values {
    r := math.Pow(float64(dataLen)-float64(v)*sampleLen, 2.0)
    if r < residual {
      times, residual = v, r
    }
  }
  return
}

func getResidual(samples []string, sampleLen float64) float64 {
  var res float64
  for _, s := range samples {
    _, r := getBestLen(len(s), sampleLen)
    res += r
  }
  return res / float64(len(samples))
}

type residualToLen struct {
  residual float64
  len      float64
}

func getResiduals(samples []string) []residualToLen {

  var maxSampleLen int
  for _, s := range samples {
    if len(s) > maxSampleLen {
      maxSampleLen = len(s)
    }
  }

  res := make([]residualToLen, 0)
  for i := 0.5; i <= float64(maxSampleLen); i += 0.125 {
    r := getResidual(samples, i)
    res = append(res, residualToLen{r, i})
  }
  return res
}

func tryDecodeMorse(morseCode string) (string, bool) {

  morseWords := strings.Split(strings.TrimSpace(morseCode), "   ")
  words := make([]string, len(morseWords))
  for i, w := range morseWords {
    morseLetters := strings.Split(w, " ")
    for _, l := range morseLetters {
      c, ok := MORSE_CODE[l]
      if !ok {
        return "", false
      }
      words[i] += c
    }
  }
  return strings.Join(words, " "), true
}

func DecodeBitsAdvanced(bits string) string {

  bits = strings.Trim(bits, "0")
  re := regexp.MustCompile(`0+|1+`)
  samples := re.FindAllString(bits, -1)

  if len(samples) == 1 {
    return "."
  }

  residuals := getResiduals(samples)

  sort.Slice(residuals, func(i, j int) bool {
    return residuals[i].residual < residuals[j].residual
  })

  transcodeTable := map[string]map[int]string{
    "1": {
      1: ".",
      3: "-",
    },
    "0": {
      3: " ",
      7: "   ",
    },
  }

  for _, r := range residuals {
    var res string
    for _, s := range samples {
      bestLen, _ := getBestLen(len(s), r.len)
      res += transcodeTable[s[0:1]][bestLen]
    }
    _, ok := tryDecodeMorse(res)
    if ok {
      return res
    }
  }
  return ""
}

func DecodeMorse(morseCode string) string {

  res, _ := tryDecodeMorse(morseCode)
  return res
}
___________________________________________________
package kata

import (
  "strings"
  "regexp"
  "math"
)

func init() {
  // add special character for space between words
  if _,ok := MORSE_CODE["/"]; !ok {
    MORSE_CODE["/"] = " "
  }
}

func DecodeBitsAdvanced(bits string) string {
  // clean up input
  s0 := strings.Trim(bits, "0")
  if len(s0) == 0 {
    return ""
  }
  // split bits into zeroes or ones frames
  re := regexp.MustCompile("0+|1+")
  frames := re.FindAllString(s0, -1)
  
  // calculate expected frame lenghts
  minFrameLen := getMinimumFrameLength(frames)
  onesMaxFrameLen := getOnesMaxFrameLength(frames)
  dashFrameLen := 0
  if minFrameLen != onesMaxFrameLen {
    dashFrameLen = onesMaxFrameLen 
  } else { 
    dashFrameLen = minFrameLen*3 // fallback for when no dash is present
  }
  // use minimum frame length and dash frame length to estimate maximum exclusive length of one unit time
  oneTimeUnitMaxFrameLen := int(math.Ceil(float64(minFrameLen+dashFrameLen)/2))
  threeTimeUnitMaxFrameLen := dashFrameLen + 3
  
  d := ""
  for _,f := range frames {
    fOfZeros, fOfOnes := strings.ContainsRune(f, '0'), strings.ContainsRune(f, '1')
    switch {
      case fOfZeros && len(f) < oneTimeUnitMaxFrameLen:
       // character pause, nothing to generate
      case fOfZeros && len(f) < threeTimeUnitMaxFrameLen:
       d += " "
      case fOfZeros:
       d += " / "
      case fOfOnes && len(f) < oneTimeUnitMaxFrameLen:
       d += "."
      case fOfOnes:
       d += "-"
    }
  }
  return d
}

func DecodeMorse(morseCode string) string {
  s0 := strings.TrimSpace(morseCode)
  s1 := strings.Split(s0, " ")
  r := ""
  for _,v := range s1 {
    r += MORSE_CODE[v]
  }
  return r
}

func getMinimumFrameLength(frames []string) int {
  min := math.MaxInt32;
  for _,f := range frames {
    if len(f) < min {
      min = len(f)
    }
  }
  return min
}

func getOnesMaxFrameLength(frames []string) int {
  max := 0;
  for _,f := range frames {
    if strings.ContainsRune(f, '1') && len(f) > max {
      max = len(f)
    }
  }
  return max
}
