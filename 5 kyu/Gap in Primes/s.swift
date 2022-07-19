561e9c843a2ef5a40c0000a4


func gap(_ g: Int, _ m: Int, _ n: Int) -> (Int, Int)? {

  var lastPrime:Int?
  
  for number in (m...n)  {
    if !number.isPrime { continue }
    if lastPrime != nil, number - lastPrime! == g {
      return (lastPrime!, number)
    }
    lastPrime = number
  }
  return nil
}

extension Int {
    var isPrime: Bool {
        guard self >= 2     else { return false }
        guard self != 2     else { return true  }
        guard self % 2 != 0 else { return false }
        return !Swift.stride(from: 3, through: Int(sqrt(Double(self))), by: 2).contains { self % $0 == 0 }
    }
}
__________________________________
func gap(_ g: Int, _ m: Int, _ n: Int) -> (Int, Int)? {
  guard g % 2 == 0 else { return nil }
  let primes = (m...n).lazy.filter(isPrime)
  return zip(primes, primes.dropFirst()).first(where: { $0.1 - $0.0 == g })
}

func isPrime(_ n: Int) -> Bool {
  return (2...Int(Double(n).squareRoot())).lazy.filter({ n % $0 == 0 }).first == nil
}
__________________________________
func gap(_ g: Int, _ m: Int, _ n: Int) -> (Int, Int)? {
    var prev: Int?
    for num in m...n {
        if num == 2 && g == 1 { return (2, 3) }
        if num == 3 { prev = num; continue }
        guard !(2...Int(sqrt(Double(num)))).contains(where: { num % $0 == 0 }) else { continue }
        if let prev = prev, num - prev == g { return (prev, num) }
        prev = num
    } // OK
    return nil
}
