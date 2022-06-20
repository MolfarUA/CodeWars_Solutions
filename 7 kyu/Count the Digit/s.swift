566fc12495810954b1000030


func nbDig(_ n: Int, _ d: Int) -> Int {
    return (0...n).map{"\($0 * $0)".filter { $0 == Character("\(d)")}}.flatMap { $0 }.count
}
____________________________
func nbDig(_ n: Int, _ d: Int) -> Int {
  var count = 0
  for x in 0...n {
    var cube = x * x
    repeat {
      if cube % 10 == d {
        count += 1 
      }
      cube = cube / 10
    } while cube >= 1
  }
  return count
}
____________________________
func nbDig(_ n: Int, _ d: Int) -> Int {
    let k = (0 ... n)
    let ksq = k.map{ $0 * $0 }
    let kstrA = ksq.map{ "\($0)" }
    let kstr = kstrA.reduce("", +)
    let fkstr = kstr.filter{ "\($0)" == "\(d)" }
    return fkstr.count 
}
