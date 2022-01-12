extension Array {
  var combinationsWithoutRepetition: [[Element]] {
    guard !isEmpty else { return [[]] }
    return Array(self[1...]).combinationsWithoutRepetition.flatMap { [$0, [self[0]] + $0] }
  }
}

func chooseBestSum(_ t: Int, _ k: Int, _ ls: [Int]) -> Int {
  var result   = -1
  var auxArray = ls.combinationsWithoutRepetition
  for array in auxArray {
    if array.count == k {
      let value = array.reduce(0, +)
      if value <= t, value > result {
        result = value
      }
    }
  }
  return result
}
_______________________________________
func chooseBestSumAux(_ t: Int, _ k: Int, _ ls: [Int], _ from: Int) -> Int {
    if k == 0 {return t >= 0 ? 0 : t}
    else {
        if t < k {return -1}
    }
    var best: Int = -1
    var tmpBest: Int
    for i in from..<ls.count {
        tmpBest = chooseBestSumAux(t - ls[i], k - 1, ls, i + 1)
        if tmpBest >= 0 {
            best = max(best, ls[i] + tmpBest)
        }
    }
    return best
    
}
func chooseBestSum(_ t: Int, _ k: Int, _ ls: [Int]) -> Int {
    return chooseBestSumAux(t, k, ls, 0)
}
_______________________________________
func chooseBestSumAux(_ t: Int, _ k: Int, _ ls: [Int], _ from: Int) -> Int {
    if k == 0 {return t >= 0 ? 0 : t}
    else {
        if t < k {return -1}
    }
    var best: Int = -1
    var tmpBest: Int
    for i in from..<ls.count {
        tmpBest = chooseBestSumAux(t - ls[i], k - 1, ls, i + 1)
        if tmpBest >= 0 {
            best = max(best, ls[i] + tmpBest)
        }
    }
    return best
    
}
func chooseBestSum(_ t: Int, _ k: Int, _ ls: [Int]) -> Int {
    return chooseBestSumAux(t, k, ls, 0)
}
_______________________________________
func chooseBestSum(_ t: Int, _ k: Int, _ ls: [Int]) -> Int {
    func combinations(_ n: [Int], _ k: Int) -> [[Int]] {
        if k == 0 { return [n] }
        guard !n.isEmpty, k != 0 else { return [] }
        guard k != 1 else { return n.map { [$0] } }
        var arrs = [[Int]]()
        let tail = Array(n.suffix(from: 1))
        arrs += combinations(tail, k - 1).map{[n[0]] + $0}
        arrs += combinations(tail, k)
        return arrs
    }
    let values = combinations(ls, k).map { $0.reduce(0,+) }.sorted().reversed()
    return values.first(where: {($0 <= t )} ) ?? -1 // OK
}
