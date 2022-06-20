5ab6538b379d20ad880000ab


class Solution {
    static areaOrPerimter(int l, int w) {
        return l == w ? l * w : (l + l) + (w + w);
    }
}
________________________
class Solution {
  static areaOrPerimter(int l, int w) {
      if (l == w){
        def area = l * w
        return area
      }
      else{
        def perimeter = (l + w) * 2
        return perimeter
      }
  }
}
________________________
class Solution {
  static areaOrPerimter(int l, int w) {
      return l == w ? l * l : (l + w) * 2
  }
}
