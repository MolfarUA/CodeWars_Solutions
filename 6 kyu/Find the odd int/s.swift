func findIt(_ seq: [Int]) -> Int {
  seq.reduce(0, ^)
}
_______________________________
func findIt(_ seq: [Int]) -> Int {
  var n = 0 
  for number in seq {
    for x in seq {
       if number == x {
         n += 1
       }
    }
    if !(n%2 == 0){
      return number
    }
  }
  
  return n
}
_______________________________
func findIt(_ seq: [Int]) -> Int {
    return seq.reduce(0, ^) // <3
}
_______________________________
func findIt(_ seq: [Int]) -> Int {
  return seq.reduce(0, { $1 ^ $0 })
}
_______________________________
func findIt(_ seq: [Int]) -> Int {
  return Dictionary(seq.map { ($0, 1)}, uniquingKeysWith: +).filter { $0.value % 2 == 1}[0].key
}
