5545f109004975ea66000086


func isDivisible(_ n: Int, _ x: Int, _ y: Int) -> Bool {
    return n % x == 0 && n % y == 0
}
_____________________
func isDivisible(_ n: Int, _ x: Int, _ y: Int) -> Bool {
    return n.isMultiple(of: x) && n.isMultiple(of: y)
}
_____________________
func isDivisible(_ n: Int, _ x: Int, _ y: Int) -> Bool {
    return n % x + n % y == 0
}
_____________________
func isDivisible(_ n: Int, _ x: Int, _ y: Int) -> Bool {
    return !((n % x) != 0 || (n % y) != 0)
}
