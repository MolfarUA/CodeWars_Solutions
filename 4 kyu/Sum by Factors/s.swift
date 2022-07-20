54d496788776e49e6b00052f


func sumOfDivided(_ l: [Int]) -> [(Int, Int)] {
    guard let max = l.max() else { return [(Int, Int)]() }
    guard let min = l.min() else { return [(Int, Int)]() }
    let maxValue = max < 0 ? min : max
    let primes = stride(from: 0, through: abs(maxValue), by: 1).filter { prime in prime.isPrime() }
    let validPrimes = primes.filter { prime in l.map { number in number.isMultiple(of: prime) }.contains(true) }

    return validPrimes.map { prime in
        (prime, l.filter { $0.isMultiple(of: prime) }.reduce(0, +))
    }
}

extension Int {
    func isPrime() -> Bool {
        guard self >= 2 else { return false }
        guard self != 2 else { return true }

        let max = Int(ceil(sqrt(Double(self))))

        for number in 2 ... max {
            if self % number == 0 {
                return false
            }
        }
        return true
    }
}
________________________________________________
func primesUntil(_ x: Int) -> [Int] {
    // Sieve of Eratosthenes
    var primes: [Bool] = [Bool](repeating: true, count: x+1)

    for i in 2..<x {
        if primes[i] {
            for j in stride(from: i*i, to: x+1, by: i) {
                primes[j] = false
            }
        }
    }

    primes[0] = false
    primes[1] = false
    return primes.enumerated().filter { $0.element }.map { $0.offset }
}

func sumOfDivided(_ l: [Int]) -> [(Int, Int)] {
    if l.isEmpty {
        return []
    }
    
    let xs = l.sorted()
    let largest = xs.map { abs($0) }.max()!
    let primes = primesUntil(largest)
    print(primes)
    var results = [(Int, Int)]()
    for p in primes {
        let hasFactor = xs.filter { $0 % p == 0 }
        if hasFactor.count > 0 {
            results.append((p, hasFactor.reduce(0, +)))
        }
    }

    print(results)
    return results
}
________________________________________________
func sumOfDivided(_ l: [Int]) -> [(Int, Int)] {
    guard l.count > 0 else { return [] }
    var checked : Set = [1], result = [(Int, Int)](), maxx = max(abs(l.min()!), abs(l.max()!))
    
    for i in 2...maxx {
        if checked.contains(i) {continue}
        let filtered = l.filter { $0.isMultiple(of: i)}
        if filtered.count > 0 {
            result.append((i, filtered.reduce(0, +)))
            var toCheck = i;
            while toCheck <= maxx { checked.insert(toCheck); toCheck += i }
        }
    }
    return result
}
