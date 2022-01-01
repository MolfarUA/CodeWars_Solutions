func flip(_ direction: String, _ a: [Int]) -> [Int] {
  return a.sorted(by: direction == "L" ? (>) : (<))
}

____________________________
func flip(_ direction: String, _ a: [Int]) -> [Int] {
    return direction == "R" ? a.sorted() : a.sorted().reversed()
}

____________________________
func flip(_ direction: String, _ a: [Int]) -> [Int] {
  direction == "R" ? a.sorted() : a.sorted(by: >)
}

____________________________
func flip(_ direction: String, _ a: [Int]) -> [Int] {
  var arr = a
  if direction == "R" {
    arr.sort{$0 < $1}
  } else if direction == "L" {
    arr.sort{$0 > $1}
  }
  return arr
}
