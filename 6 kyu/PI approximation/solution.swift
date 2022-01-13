// use String(format: "%.10f", ...) for the rounding

func iterPi(_ epsilon: Double) -> (Int, String) {
    var steps = 1
    var approx = 1.0 * 4.0
    while abs(approx - Double.pi) > epsilon {
      steps += 1
      let d = 4 * 1 / (Double(steps) * 2 - 1)
      if steps % 2 == 0 {
        approx -= d
      } else {
          approx += d
      }
    }
   return (steps, String(format: "%.10f", approx))
}
________________________________________
func iterPi(_ epsilon: Double) -> (Int, String) {
    var error = epsilon + 1
    var n = 1
    var pi4 = 1.0
    var sign = -1.0
  
    while(error > epsilon) {
      pi4 += sign / (2*Double(n)+1)
      error = abs(pi4*4 - Double.pi)
      
      n += 1
      sign *= -1
    }
  
    return (n, String(format:"%.10f", pi4*4))
}
________________________________________
func iterPi(_ epsilon: Double) -> (Int, String) {
    var pa: Double = 1
    var i:Double = 1
    var a = -1
    var f: Double = 0
    while(abs(3.1415926535897932384 - 4*pa)>epsilon){
        f = 1/(2*i+1)
        if(a == -1){pa = pa - f; a = 1}
        else{pa = pa + f;a = -1}
        i = i + 1
      
    }
  pa = 4*pa
    return (Int(i),String(format: "%.10f", pa))
}
________________________________________
func iterPi(_ epsilon: Double) -> (Int, String) {
  var pi4 = 1.0
  var sign = -1.0
  var iterations = 1
  var denom = 3.0
  while abs(4.0 * pi4 - 3.14159265358979323846) >= epsilon {
    pi4 += sign * (1.0 / denom)
    sign *= -1.0
    denom += 2.0
    iterations += 1
  }
  return (iterations, String(format: "%.10f", 4.0 * pi4))
}
