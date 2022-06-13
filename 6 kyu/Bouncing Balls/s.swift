func bouncingBall(_ h: Double, _ bounce: Double, _ window: Double) -> Int {
    guard h > 0 && bounce > 0 && bounce < 1 && window < h else {return -1}
    var views = 1
    var height = h * bounce
    while height > window {
      views += 2
      height *= bounce
    }
    return views
}
_______________________________________________
func bouncingBall(_ h: Double, _ bounce: Double, _ window: Double) -> Int {
    if !(h > 0 && 0 < bounce && bounce < 1 && window < h) {
        return -1
    }
    return Int(ceil(log(window / h) / log(bounce))) * 2 - 1
}
_______________________________________________
func bouncingBall(_ h: Double, _ bounce: Double, _ window: Double) -> Int {
  guard h > 0.0 && bounce > 0.0 && bounce < 1.0 && window < h else { return -1 }
  var jumpH = h, jumpC = 0
  while jumpH > window {
      jumpH *= bounce
      jumpC += 2
  }
  return jumpC - 1
}
_______________________________________________
func bouncingBall(_ h: Double, _ bounce: Double, _ window: Double) -> Int {
    guard h > window, 0 < bounce && bounce < 1 else { return -1 }
    var i = 0, h = h
    while h * bounce > window {
        h *= bounce
        i += 1
    }
    return i * 2 + 1
}
