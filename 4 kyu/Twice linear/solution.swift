func dblLinear(_ n: Int) -> Int {
    var array = [1]
    
    var x = 0
    var y = 0
    while array.count <= n {
        let xx = 2 * array[x] + 1
        let yy = 3 * array[y] + 1
        
        if xx < yy {
            array.append(xx)
            x += 1
        } else if xx > yy {
            array.append(yy)
            y += 1
        } else {
            array.append(yy)
            x += 1
            y += 1
        }
    }
    
    return array[n]
}

__________________________________________________
func dblLinear(_ n: Int) -> Int {
    var u = [1], x = 0, y = 0
    (0..<n).forEach { _ in
        let nextX = 2 * u[x] + 1, nextY = 3 * u[y] + 1
        if nextX <= nextY {
            u.append(nextX); x += 1
            if nextY == nextX {y += 1}
        } else {
            u.append(nextY); y += 1
        }
    }
    return u[n]
}

__________________________________________________
func dblLinear(_ n: Int) -> Int {
  var u = Array(repeating: 0, count: n + 1)
  u[0] = 1
  var x = 0
  var y = 0
  var i = 1
  while (i <= n) {
      u[i] = min(2 * u[x] + 1, 3 * u[y] + 1)
      if (u[i] == 2 * u[x] + 1) {
          x += 1
      }
      if (u[i] == 3 * u[y] + 1) {
          y += 1
      }
      i += 1
  }
  return u[n]
}
