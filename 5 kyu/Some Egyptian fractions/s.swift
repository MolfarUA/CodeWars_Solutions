54f8693ea58bce689100065f

func GCD(x: Int, y: Int) -> Int {
    var x = x, y = y
    while y != 0 {
        (x, y) = (y, x % y)
    }
    return x
}

func decompose(_ nrStr: String, _ drStr: String) -> String {
    var nr = Int(nrStr) ?? 0, dr = Int(drStr) ?? 0, res = [Int](), n = nr / dr
    nr = nr % dr
    while nr > 0 {
        let v = dr / nr + (dr % nr != 0 ? 1 : 0), g = GCD(x: dr, y: v)
        res.append(v)
        (nr, dr) = ((nr * v - dr) / g, dr * v / g)
    }
    return ((n == 0 ? [] : ["\(n)"]) + res.map { i -> String in "1/\(i)" }).joined(separator: ",")
}
_________________________________
func decompose(_ nrStr: String, _ drStr: String) -> String {
  let nrInt = Int(nrStr) ?? 0
  let drInt = Int(drStr) ?? 0
  
  guard nrInt > 0 && drInt > 0 else { return "" }
  
  if drInt == nrInt {
    return "1"
  }
  
  if drInt % nrInt == 0 {
    return "1/\(drInt / nrInt)"
  }
  
  if nrInt % drInt == 0 {
    return "\(nrInt / drInt)"
  }
  
  if  nrInt > drInt {
    return "\(nrInt / drInt)," + decompose(String(nrInt % drInt), String(drInt))
  }
  
  let n = drInt/nrInt + 1
  
  return "1/\(n)," + decompose(String(nrInt * n - drInt), String(drInt * n))
}
