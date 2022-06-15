func fakeBin(digits: String) -> String {
  
  return String(digits.map { Int(String($0))! >= 5 ?  "1" : "0" })
}
__________________________________
func fakeBin(digits: String) -> String {
  return digits.map({ $0 < "5" ? "0" : "1" }).joined()
}
__________________________________
func fakeBin(digits: String) -> String {
    var bin = ""
    for digit in digits {
        if Int("\(digit)")! < 5 {
            bin += "0"
        } else {
            bin += "1"
        }
    }
    return bin
}
__________________________________
func fakeBin(digits: String) -> String {
  return digits.map({$0 >= "0" && $0 <= "4" ? "0" : "1"}).joined()
}
__________________________________
func fakeBin(digits: String) -> String {
  digits.map { $0 < "5" ? "0" : "1"  }.joined()
}
