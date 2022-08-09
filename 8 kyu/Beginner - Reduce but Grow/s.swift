57f780909f7e8e3183000078


func grow(_ arr: [Int]) -> Int {
  return arr.reduce(1,*)
}
_______________________
func grow(_ arr: [Int]) -> Int {
    var product = 1
    for num in arr {
        product *= num
    }
    return product
}
_______________________
func grow(_ arr: [Int]) -> Int {
arr.reduce(1,*)
}
