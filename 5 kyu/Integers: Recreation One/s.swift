55aa075506463dac6600010d


func listSquared(_ m: Int, _ n: Int) -> [(Int, Int)] {
  return (m...n).flatMap { (val) -> (Int, Int)? in
    let divisors = (1...(Int(sqrt(Double(val)))))
      .flatMap({val % $0 == 0 ? [$0, val / $0] : []})
    let sum = Array(Set(divisors)).reduce(0, {$0 + ($1 * $1)})
    if sqrt(Double(sum)).truncatingRemainder(dividingBy: 1) == 0 {
      return (val, sum)
    }
    return nil
  }
}
________________________________
func listSquared(_ m: Int, _ n: Int) -> [(Int, Int)] {
    var resultArray = [(Int, Int)]()
    for index in m...n {
        var total = index*index
        if index > 1 {
            for divisor in 1...index/2 {
                if index%divisor == 0 {
                    total += (divisor*divisor)
                }
            }
        }
        if Double(total).squareRoot() == Double(Int(Double(total).squareRoot())) {
            resultArray.append((index, total))
        }
    }
    return resultArray
}
________________________________
func getAllDivisors(number: Int) -> Int {
  guard number > 1 else { return 1} 
  var sum: Int = 0
  let some: Int = number / 2
  for divisor in 1...some {
    if (number % divisor == 0) {
      sum += divisor * divisor
    }
  }
  sum += number * number
  return sum
}

func listSquared(_ m: Int, _ n: Int) -> [(Int, Int)] {
    guard m <= n else { return [] }
    var result: [(Int, Int)] = []
    let sum = getAllDivisors(number: m)
    let sqrtOfSum = Double(sum).squareRoot()
    let fractionalPart = modf(sqrtOfSum)
    if (fractionalPart.1 == 0.0) {
        result.append((m, sum))
    }
    
    return result + listSquared(m + 1, n)
}
