55466989aeecab5aac00003e


func sqInRect(_ x: Int, _ y: Int) -> [Int]? {
    guard x != y else { return nil }
    let minSide = min(x, y)
    let maxSide = max(x, y)
    return minSide > 0 ? Array([[minSide], sqInRect(maxSide - minSide, minSide) ?? [minSide]].joined()) : []
}
______________________________
func sqInRect(_ l: Int, _ w: Int) -> [Int]? {
  guard l != w else { return nil }
  guard l < w else { return sqInRect(w, l) }
  
  return [l] + (sqInRect(w - l, l) ?? [l])
}
______________________________
func sqInRect(_ length: Int, _ width: Int) -> [Int]? {
  guard length != width else {
    return nil
  }
  var squareSizes = [Int]()
  
  var newLength = length
  var newWidth = width
  
  while newLength * newWidth > 0 {
    let maxSquareSize = min(newLength, newWidth)
    squareSizes.append(maxSquareSize)
    
    if maxSquareSize == newLength {
      newWidth -= maxSquareSize
    } else {
      newLength -= maxSquareSize
    }
  }
  
  return squareSizes
}
______________________________
func sqInRect(_ lng: Int, _ wdth: Int) -> [Int]? {
    if lng == wdth {return nil}
    var l = lng, w = wdth, tmp = 0
    if lng < wdth {w = lng; l = wdth;}
    var res = [Int]()
    while l != w {
        res.append(w)
        l = l - w
        if l < w {tmp = w; w = l; l = tmp;}
    }
    res.append(w)
    return res
}
