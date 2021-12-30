func digitalRoot(of number: Int) -> Int {
    return (1 + (number - 1) % 9)
}

________________________________
func digitalRoot(of number: Int) -> Int {
    let digit = String(number).characters.flatMap { Int(String($0)) }.reduce(0, +)
    return digit > 9 ? digitalRoot(of: digit) : digit
}

________________________________
func digitalRoot(of number: Int) -> Int {
  let value = String(number).map {Int(String($0))!}.reduce(0, +)
    if value > 10 {
        return digitalRoot(of: value)
    } else {
        return value
    }
}
