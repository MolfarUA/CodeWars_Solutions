559b8e46fa060b2c6a0000bf


func combi(_ n: Int, _ k: Int) -> Int {
    var result = 1
    for i in 0..<k {
        result *= (n - i)
        result /= (i + 1)
    }
    return result
}
func diagonal(_ n: Int, _ p: Int) -> Int {
    return combi(n + 1, p + 1)
}
_____________________________
func diagonal(_ n: Int, _ p: Int) -> Int {
    func factorial(x: Double) -> Double {
        var result: Double = 1
        for i in 1...Int(x) {
            result *= Double(i)
        }
        return result
    }
    
    var sum: Double = 1
    for i in Int(p)+1...Int(n) {
        //print(i)
        if i - Int(p) == 0 || Int(p) == 0 || i == 0 {
            sum += 1
        } else {
            sum += (factorial(x: Double(i))/(factorial(x: Double((p)))*((factorial(x: (Double(i) - Double(p)))))))
        }
    }
    
    
    
    return Int(sum)
}
_____________________________
func diagonal(_ n: Int, _ p: Int) -> Int {
    var sum = 1
    var a = 1
    for i in p+1...n {
        a = a * i / (i - p)
        sum += a
    }
    return sum
}
