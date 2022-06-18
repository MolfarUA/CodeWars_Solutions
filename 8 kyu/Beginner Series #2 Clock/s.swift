55f9bca8ecaa9eac7100004a


func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
  return s * 1000 + m * 60000 + h * 3600000
}
__________________________
func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
    let hour = h * 3600000
    let minutes = m * 60000
    let seconds = s * 1000
    return hour + minutes + seconds
}
__________________________
func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
    return 1000 * (s + (60 * (m + (60 * h))))
}
__________________________
func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
    return (s + m * 60 + h * 3600) * 1000 // OK
}
__________________________
func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
  let hMs = h * 60 * 60 * 1000
  let mMs = m * 60 * 1000
  let sMs = s * 1000
  
  let timeMS = hMs + mMs + sMs
  
  return
    timeMS
}
__________________________
func past(_ h: Int, _ m: Int, _ s: Int) -> Int {
    var milliseconds = 0

    if h >= 0 && h <= 59 {
        milliseconds += h * 3_600_000
    }
    
    if m >= 0 && m <= 59 {
        milliseconds += m * 60_000
    }
    
    if s >= 0 && s <= 59 {
        milliseconds += s * 1_000
    }
    
    return milliseconds
}
