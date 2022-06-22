5842df8ccbd22792a4000245


func expandedForm(_ num: Int) -> String {
    let digits = String(num).characters
    let maxZeros = digits.count - 1
    
    let parts = digits
        .enumerated()
        .filter { $0.element != "0" }
        .map { String($0.element) + String(repeating: "0", count: maxZeros - $0.offset) }
    
    return parts.joined(separator: " + ")
}
_________________________
func expandedForm(_ num: Int) -> String {
    let digits = String(num).characters
    return digits.enumerated().flatMap { $1 == "0" ? nil : "\($1)" + String(repeating: "0", count: digits.count - $0 - 1) }.joined(separator: " + ")
}
_________________________
func expandedForm(_ num: Int) -> String {
    let array = String(num).characters.flatMap{ Int(String($0)) }
    var count = array.count
    let result = array.map({ (number) -> String in
        count -= 1
        return String(number * Int(pow(10.0,Double(count))))
    }).filter({ $0 != "0" }).joined(separator: " + ")
    return result
}
