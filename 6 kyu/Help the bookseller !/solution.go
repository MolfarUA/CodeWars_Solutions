package kata

import "fmt"
import "strings"
import "strconv"

func StockList(listArt []string, listCat []string) string {
  if len(listArt) == 0 || len(listCat) == 0 {
    return ""
  }

  stockCatSlice := []string{}
  for _, cat := range listCat {
    amountTotal := 0
    for _, art := range listArt {
      if cat == string(art[0]) {
        amount, _ := strconv.Atoi(strings.Split(art, " ")[1])
        amountTotal += amount
      }
    }
    stockCatSlice = append(stockCatSlice, fmt.Sprintf("(%s : %d)", cat, amountTotal))
  }
  
  stockCatString := strings.Join(stockCatSlice, " - ")
  
  return stockCatString
}
________________________________________
package kata

import (
  "fmt"
  "strconv"
  "strings"
)

func StockList(listArt []string, listCat []string) string {
  if len(listArt) == 0 || len(listCat) == 0 {
    return ""
  }
  result := ""
  result_map := make(map[string]int)

  for _, listpair := range listCat {
    pair := strings.Split(listpair, " ")
    result_map[pair[0]] = 0
  }

  for _, listpair := range listArt {
    pair := strings.Split(listpair, " ")
    key := string([]rune(pair[0])[0])
    val, _ := strconv.Atoi(pair[1])
    if _, ok := result_map[key]; ok {
      result_map[key] += val
    }
  }
  
  for _, key := range listCat {
    result += fmt.Sprintf("(%s : %d) - ", key, result_map[key])
  }
  return result[:len(result)-3]
}
________________________________________
package kata

import(
  "strings";
  "strconv";
)

func StockList(listArt []string, listCat []string) string {
    // your code
  if len(listArt) == 0 || len(listCat) == 0 {
    return ""
  }
  var result string = ""
  for i := 0; i < len(listCat); i++ {
    var sum int = 0
    for j := 0; j < len(listArt); j++ {
      firstChar := listArt[j][0:1]
      if firstChar == listCat[i] {
        split := strings.Split(listArt[j], " ")
        quantity, _ := strconv.Atoi(split[1])
        sum += quantity
      }
    }
    result += " - (" + listCat[i] + " : " + strconv.Itoa(sum) + ")"
  }
  return result[3:]
}
________________________________________
package kata

import (
  "fmt"
  "strconv"
  "strings"
)

func StockList(listArt []string, listCat []string) string {
  if len(listArt) == 0 || len(listCat) == 0 {
    return ""
  }
  var stock string
  for _, cat := range listCat {
    count := 0
    for _, art := range listArt {
      if strings.HasPrefix(string(art), string(cat)) {
        i, _ := strconv.Atoi(strings.Split(string(art), " ")[1])
        count += i
      }
    }
    stock += fmt.Sprintf("(%s : %d) - ", cat, count)
  }
  return strings.TrimSuffix(stock, " - ")
}
________________________________________
package kata

import "strconv"

func StockList(listArt []string, listCat []string) string {
    // your code
  var count [26]int 
  if len(listArt) == 0 || len(listCat) == 0{
    return ""
  }
  
  var res string
  for _, stock := range listArt{
    cat := stock[0] - 65
    var spaceId int 
    for i := len(stock)-1; i >= 0; i--{
      if stock[i] == ' ' {
        spaceId = i + 1
        break
      }
    }
    num, _ := strconv.Atoi(stock[spaceId:len(stock)])
    count[cat] = count[cat] + num
  }
  
  for _, c := range listCat{
    num := count[c[0]-65]
    res = res + "(" + c + " : " + strconv.Itoa(num) + ") - "
    
  }
  
  return res[0:len(res)-3]
}
________________________________________
package kata

import "fmt"

func StockList(listArt []string, listCat []string) string {
  fmt.Println(listArt, listCat)
  var res []byte
  var num int
  var sum int
  var strSum []byte
  if (len(listArt) == 0) || (len(listCat) == 0) {
    return string(res)
  }
  for _, categ := range listCat {
    sum = 0
    strSum = make([]byte, 0)
    for _, book := range listArt {
      if book[0] == categ[0] {
        num = 0
        for k:=2; k < len(book); k++ {
          if (book[k]-'0' >= 0) && (book[k]-'0' <= 9) {
            num = num*10 + int(book[k]-'0')
          }
        }
        sum+=num
      }
    }
    for s:=sum; s > 0; {
      strSum = append(strSum, byte(s%10+'0'))
      s = s/10
    }
    res = append(res, '(', byte(categ[0]), ' ', ':', ' ')
    if sum == 0 {
      res = append(res, byte(0+'0'))
    } else {
      for s:=len(strSum)-1; s>=0; s-- {
        res = append(res, strSum[s])
      }
    }
    res = append(res, ')', ' ', '-', ' ')
  }  
  return string(res[:len(res) - 3])
}
