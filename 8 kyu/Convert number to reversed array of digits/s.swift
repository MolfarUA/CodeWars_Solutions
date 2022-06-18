func digitize(_ num:Int) -> [Int] {
  return String(num).characters.flatMap { Int(String($0)) }.reversed()
}
________________________
func digitize(_ num: Int) -> [Int] {
    guard num > 0 else {
        return [0]
    }
    var result: [Int] = []
    var i = num
    while i != 0 {
        result.append(i % 10)
        i /= 10
    }
    return result
}
________________________
func digitize(_ num:Int) -> [Int] {
  let numb = String(num)
  let digits = numb.compactMap{ $0.wholeNumberValue }
  return digits.reversed()
}
________________________
func digitize(_ num:Int) -> [Int] {
  return String(num).map{ $0.wholeNumberValue! }.reversed()
}
________________________
func digitize(_ num:Int) -> [Int] {
    return String(num).characters.map{ Int(String($0))! }.reversed()
}
________________________
func digitize(_ num:Int) -> [Int] {
  return String(num)
    .compactMap { Int($0.description) }
    .reversed()
}
