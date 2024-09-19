54d7660d2daf68c619000d95



func gcdi(_ x: Int, _ y: Int) -> Int {
    let m = abs(x), n = abs(y)
    if m == 0 {return n} else {return gcdi(n % m, m)}
}
func lcmu(_ a: Int, _ b: Int) -> Int {
    return abs(a) * abs(b) / gcdi(a, b)
}
func lcmuAll(_ a: [Int]) -> Int {
    return a.reduce(1, lcmu)
}
func simp(_ xy: (Int, Int)) -> (Int, Int) {
    let g = gcdi(xy.0, xy.1)
    return (xy.0 / g, xy.1 / g)
}
func convertFracts(_ l: [(Int, Int)]) -> [(Int, Int)] {
    // fractions simplified
    let v = l.map( { (s: (Int, Int)) -> (Int, Int) in
            return simp(s) } )
    // denominators
    let d = v.map( { (s: (Int, Int)) -> Int in 
            return s.1 } )
    // common denominator
    let lc = lcmuAll(d)
    // new fractions
    let ll = v.map( { (s: (Int, Int)) -> (Int, Int) in
            return (s.0 * lc / s.1, lc) } )
    return ll
}
##########################
func convertFracts(_ l: [(Int, Int)]) -> [(Int, Int)] {
  func greatestCommonDivisor(_ a: Int, _ b: Int) -> Int {
        var a = a, b = b
        while b != 0 { let temp = b; b = a % b; a = temp }
        return a
    }
    let max = l.map { $1 }.reduce(1, *), step = l.map { max * $0 / $1 }
    let denom = step.reduce(max, greatestCommonDivisor)
    return step.map { ($0 / denom, max / denom) }
}
###########################
func simplePare(pare: (Int, Int)) -> (Int, Int) {
    var leftParts = pare.0.parts
    var rightParts = pare.1.parts
    leftParts.remove(1)
    rightParts.remove(1)
    
    var ls: Int = pare.0
    var rs: Int = pare.1
    
    var partsUnion = leftParts.union(rightParts)
    if leftParts.intersection(rightParts).isEmpty {
        return pare
    }
    
    partsUnion.forEach { part in
        if ls % part == 0 && rs % part == 0 {
            ls = ls / part
            rs = rs / part
        }
    }
    return simplePare(pare: (ls, rs))
}

func gcd(_ a: Int, _ b: Int) -> Int {
    var a = a
    var b = b
    while b != 0 {
        let temp = b
        b = a % b
        a = temp
    }
    return a
}

func lcm(_ a: Int, _ b: Int) -> Int {
    return abs(a * b) / gcd(a, b)
}

func lcmOfArray(_ array: [Int]) -> Int {
    
    guard !array.isEmpty else {
        return 0
    }
    
    let result = array.reduce(1) { lcm($0, $1) }
    print("LCM input: \(array)\nLCM output: \(result)")
    return result
}

func convertFracts(_ l: [(Int, Int)]) -> [(Int, Int)] {
    print("---------------------")
    var setOfParts: Set<Int> = []

    
    let simprifiedInput = l.map { simplePare(pare: $0) }
    print("bareInput : \(l)")
    print("simprifiedInput : \(simprifiedInput)")
    
    guard let first = l.first else { return [] }
    var minValue = first.1
    var maxValue = first.1
    
    l.forEach { element in
        minValue = min(minValue, element.1)
        maxValue = max(maxValue, element.1)
    }
    print("minValue: \(minValue) maxValue: \(maxValue)")
    
    simprifiedInput.forEach { element in
        setOfParts.formUnion(element.1.parts)
    }
    print("setOfParts : \(setOfParts)")
    
    let maxElement = lcmOfArray(simprifiedInput.map { $0.1 })
    
    print("maxElement after: \(maxElement)")
    print("setOfParts : \(setOfParts)")
    
    var result: [(Int, Int)] = []
    simprifiedInput.forEach { element in
        let diff = maxElement / element.1
        print("diff: \(diff) maxElement: \(maxElement) / element.1: \(element.1)")
        result.append((element.0 * diff, element.1 * diff))
    }
    print("result : \(result)")
    return result
}

extension Int {
    var parts: Set<Int> {
        var result: Set<Int> = []
        for i in 1...self {
            if self % i == 0 {
                if i > 3 {
                    if i == self {
                        if self.isPrime {
                            result.insert(i)
                        }
                    } else {
                        result.formUnion(i.parts)
                    }
                } else {
                    result.insert(i)
                }
            }
        }
        return result
    }
    
    var isPrime: Bool {
        self > 1 && !(2..<self).contains { self % $0 == 0 }
    }
}
