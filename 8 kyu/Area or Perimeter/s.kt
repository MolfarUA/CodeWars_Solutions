5ab6538b379d20ad880000ab


object Solution {
  fun areaOrPerimeter(l: Int, w: Int) = if (l == w) l * w else 2 * (l + w)
}
________________________
object Solution {
  fun areaOrPerimeter(l:Int, w:Int):Int {
    var j = 0
      if(l==w) j=l*w else j=(2*l+2*w)
      return j
}
  }
________________________
object Solution {
  fun areaOrPerimeter(l:Int, w:Int) = if (l.equals(w)) l*w else 2*(l+w)
}
________________________
object Solution {
  fun areaOrPerimeter(l:Int, w:Int) = if (w == l) w * l else w + w + l + l 
}
