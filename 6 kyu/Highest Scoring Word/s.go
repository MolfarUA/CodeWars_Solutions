57eb8fcdf670e99d9b000272


package kata

import "strings"

func wordScore(s string) (scor byte) {
  for i := range s {
    scor += s[i] - 96
  }
  return
}

func High(s string) string {
  var scor, scorNew byte
  var word string
  for _, wd := range strings.Split(s, " ") {
    scorNew = wordScore(wd)
    if scorNew > scor {
      scor = scorNew
      word = wd
    }
  }
  return word
}
_____________________________________________
package kata

import "strings"

func High(s string) string {
  best := ""
  bestScore := -1
  
  for _, word := range strings.Split(s, " ") {
    score := 0
    for _, c := range word {
      score += int(c - 'a') + 1
    }
    
    if score > bestScore {
      best = word
      bestScore = score
    }
  }
  
  return best
}
_____________________________________________
package kata

import "strings"

func High(s string) string {
  leadWord, leadScore := "", 0
  
  for _, word := range strings.Split(s, " ") {
    currentScore := 0
    for _, letter := range word {
      currentScore += int(letter) - 'a' + 1
    }
    if currentScore > leadScore {
      leadScore = currentScore
      leadWord = word
    }
  }
  
  return leadWord
}
_____________________________________________
package kata

func High(s string) string {
  m, pre, at := 0, -1, 0
  mx := ""
  for i := 0; i < len(s); i++ {
    if s[i] == ' ' {
      if m < at {
        m = at
        mx = s[pre+1 : i]
      }
      pre = i
      at = 0
    } else {
      at += int(s[i]-'a'+1)
    }
  }
  if m < at {
    mx = s[pre+1 : ]
  }
  return mx
}
_____________________________________________
package kata

import (
  "strings"
)

func High(s string) (maxWord string) {
  var maxInt int32
  for _, word := range strings.Split(s, " ") {
    var wordSum int32
    for _, code := range word {
      wordSum += code - 96
    }
    if wordSum > maxInt {
      maxInt = wordSum
      maxWord = word
    }
  }
  return
}
