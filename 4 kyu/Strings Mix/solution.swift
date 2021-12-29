func mix(_ s1: String, _ s2: String) -> String {
    let alphabet = "abcdefghijklmnopqrstuvwxyz"
    var result : [(String,String)] = [(String,String)]()
    for ch in alphabet.characters {
        let s1Count = s1.components(separatedBy:String(ch)).count-1
        let s2Count = s2.components(separatedBy:String(ch)).count-1
        if max(s1Count,s2Count) > 1 {
            if s1Count > s2Count {
                result.append(("1",String(repeating: String(ch), count:s1Count)))
            } else if s1Count == s2Count {
                result.append(("E",String(repeating: String(ch), count:s1Count)))
            } else {
                result.append(("2",String(repeating: String(ch), count:s2Count)))
            }
        }
    }
    return result.sorted(by:{ $0.1.characters.count > $1.1.characters.count || ($0.1.characters.count == $1.1.characters.count && $0.0 < $1.0 || ($0.0 == $1.0 && $0.1 < $1.1)) }).map({$0+":"+$1}).joined(separator: "/")
}

_____________________________________________________
func mix(_ s1: String, _ s2: String) -> String {
  
  //count lowercased letters with occurrence > 1 into dictionary
  let s1Prepared = prepareString(s1)
  let s2Prepared = prepareString(s2)
  
  //filter equals and keep on s1Filtered and s2Filtered only if it is max.
  let equalsFiltered = s1Prepared.filter {$0.value == s2Prepared[$0.key] ?? -1}
  let s1Filtered = s1Prepared.filter { $0.value > s2Prepared[$0.key] ?? 0 }
  let s2Filtered = s2Prepared.filter { $0.value > s1Prepared[$0.key] ?? 0 }
  
  //map results in a way easy to sort and format
  var results = [(String, String, Int)]()
  results = equalsFiltered.map{("E:", String(repeating: $0.key, count: $0.value), $0.value)}
  results.append(contentsOf: s1Filtered.map{("1:", String(repeating: $0.key, count: $0.value), $0.value)})
  results.append(contentsOf: s2Filtered.map{("2:", String(repeating: $0.key, count: $0.value), $0.value)})
  
  results.sort {
    if $0.2 != $1.2 { return $0.2 > $1.2 } // first sort decreasing occurrences
    else if $0.0 != $1.0 { return $0.0 < $1.0 } // second sort increasing groups
    else { return $0.1 < $1.1 } // third sort increasing letters
  }
  
  let formattedResults = results.map{ $0.0 + $0.1 }.joined(separator: "/")
  return formattedResults
}

// Count lowercased letters into dictionary and remove lonely ones.
func prepareString(_ string: String) -> [String: Int] {
  return Array(string)
  .filter{$0.isLetter && $0.isLowercase}
  .reduce(into: [:]) { counts, letter in
    counts[String(letter), default: 0] += 1
  }.filter{ $0.value > 1 }
}

_____________________________________________________
func mix(_ s1: String, _ s2: String) -> String {
 func handelString(str:String)-> Array<String> {
        let str1 = str.replacingOccurrences(of: " ", with: "")
        var str1Arr = [String]()
        for index in str1{
             if index.isLowercase {
              str1Arr.append(String(index))
            }
        }
        str1Arr.sort { (s1, s2) -> Bool in
            return s1 < s2
        }
        
        var needStr1Arr = [String]()
        needStr1Arr.append(str1Arr.first!)
        for index in 0..<str1Arr.count - 1 {
            let stra = str1Arr[index]
            let strb = str1Arr[index + 1]
            if strb == stra {
                needStr1Arr[needStr1Arr.count - 1] = needStr1Arr.last! + strb
            } else {
                needStr1Arr.append(strb)
            }
        }
       
        needStr1Arr.sort { (s1, s2) -> Bool in
            return s1.count > s2.count
        }
        needStr1Arr = needStr1Arr.filter({$0.count > 1})
        return needStr1Arr
    }
        let str1Arr = handelString(str: s1)
//        print(str1Arr)
        let str2Arr = handelString(str: s2)
//       print(str2Arr)
        var resultArr = [String]()
        resultArr.append(contentsOf:str1Arr)
        resultArr.append(contentsOf:str2Arr)
        resultArr.sort { (s1, s2) -> Bool in
            if s1.count == s2.count {
               return s1 < s2
            }
            return s1.count > s2.count
        }
//        print(resultArr)
        
        for i in 0 ..< resultArr.count {
            for j in 0 ..< resultArr.count {
                if i != j {
                    if resultArr[i].first == resultArr[j].first {
                        if resultArr[i].count > resultArr[j].count {
                            resultArr[j] = ""
                        } else if resultArr[i].count <= resultArr[j].count {
                            resultArr[i] = ""
                        }
                    }
                }
            }
        }
        resultArr = resultArr.filter({$0.count > 1})
        
        
        for index in 0 ..< resultArr.count {
            let  item = resultArr[index]
            if str1Arr.contains(item) && !str2Arr.contains(item) {
               resultArr[index] = "1:\(item)"
            } else if !str1Arr.contains(item) && str2Arr.contains(item) {
               resultArr[index] = "2:\(item)"
            } else if  str1Arr.contains(item) && str2Arr.contains(item) {
               resultArr[index] = "E:\(item)"
            }
        }
        
//        print(resultArr)
        
        resultArr.sort { (s1, s2) -> Bool in
            if s1.count == s2.count {
                return s1 < s2
            }
            return s1.count > s2.count
        }
        let resultArrStr = resultArr.joined(separator: "/")
        return resultArrStr
}
