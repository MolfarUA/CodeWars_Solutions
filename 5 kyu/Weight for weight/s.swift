55c6126177c9441a570000cc


func orderWeight(_ s: String) -> String {
  return s.components(separatedBy: " ").sorted {
    let lhs = $0.compactMap{ Int(String($0)) }.reduce(0, +)
    let rhs = $1.compactMap{ Int(String($0)) }.reduce(0, +)
    return lhs == rhs ? $0 < $1 : lhs < rhs
  }.joined(separator: " ")
}
______________________________
func orderWeight(_ s: String) -> String {
    let result = s.components(separatedBy: " ").sorted {
        let lhs = $0.compactMap{Int("\($0)")}.reduce(0, +)
        let rhs = $1.compactMap{Int("\($0)")}.reduce(0, +)
        return lhs == rhs ? $0 < $1 : lhs < rhs
      }.joined(separator: " ")
    return result
}
______________________________
struct Numbers{
    var number:String
    var weight:Int
    init(_ num:String) {
        number = num
        weight = num.replacingOccurrences(of: " ", with: "").compactMap{$0.wholeNumberValue}.reduce(0, +)
    }
}

func orderWeight(_ s: String) -> String {
    let data = s.split(separator: " ").map{Numbers(String($0))}
    return data.sorted {$0.weight == $1.weight ? $0.number < $1.number : $0.weight < $1.weight}.map{$0.number}.joined(separator: " ")
}
