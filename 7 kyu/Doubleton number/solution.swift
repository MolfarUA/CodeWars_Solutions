func doubleton(_ num: Int) -> Int {
  return Set(Array(String(num + 1))).count == 2 ? num + 1 : doubleton(num + 1)
}

#############
func doubleton(_ num: Int) -> Int {
  return Set(String(num + 1).compactMap{ $0.wholeNumberValue }).count == 2 ? num + 1 : doubleton(num + 1)
}

############
func doubleton(_ num: Int) -> Int {
    var numStr = ""
    for i in num + 1...1000000 {
        numStr = ""
        for j in "\(i)" {
            if !numStr.contains(j) {
                numStr.append(j)
            }
        }
        if numStr.count == 2 {
            return i
        }
    }
    return 0
}

##############
func doubleton(_ num: Int) -> Int {

    var inpoutNum = num
    var result = Set<Int>()
    var numToSingleDigit = String(inpoutNum).compactMap{ $0.wholeNumberValue }

    if numToSingleDigit.count == 1 {
        return 10
    } else if numToSingleDigit.count >= 2 {
        repeat {
            inpoutNum += 1
            numToSingleDigit = String(inpoutNum).compactMap{ $0.wholeNumberValue }
            result = Set(numToSingleDigit)
            if result.count == 2 { 
                return inpoutNum
            }
        } while result.count != 2
    }

    return 0
}

#############
func doubleton(_ num: Int) -> Int {
    var numCopy = num
    var helpArr = 0
    while helpArr != 2 {
        numCopy += 1
        helpArr = Set(String(numCopy)).count
    }
    return numCopy
}

#####################
func doubleton(_ num: Int) -> Int {
    var numCopy = num
    var helpArr = [0]
    while helpArr.count != 2 { //it hurts to look at it
        numCopy += 1
        helpArr = Array(Set(String(numCopy).map{Int(String($0))!}))
    }
    return numCopy
}

##########################
func doubleton(_ num: Int) -> Int {
  var n = num
  while true {
    n += 1
    if Set(String(n)).count == 2 {
     return n
    }
  }
}

#######################
func doubleton(_ num: Int) -> Int {
  var set = Set<String>()
  var next = num + 1
  var a = true
  while a {
      Array(String(next)).map{"\($0)"}.map{set.insert($0)}
      if set.count == 2 {return next}
      next += 1
      set.removeAll()
  }
        
}
