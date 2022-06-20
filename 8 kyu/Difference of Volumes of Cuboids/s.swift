58cb43f4256836ed95000f97


func findDifference(_ a: [Int], _ b: [Int]) -> Int {
  abs(a.reduce(1,*) - b.reduce(1,*))
}
________________________
func findDifference(_ a: [Int], _ b: [Int]) -> Int {
    var sum1 = 1
    var sum2 = 1
    
    for i in a {
        sum1 *= i
    }
    for i in b {
        sum2 *= i
    }
    
    if sum1 >= sum2{
        return sum1 - sum2
    } else {
        return sum2 - sum1
    }
}
________________________
func findDifference(_ a: [Int], _ b: [Int]) -> Int {
  return abs(a[1]*a[2]*a[0] - b[1]*b[2]*b[0] )
}
