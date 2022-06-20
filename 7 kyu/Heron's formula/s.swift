57aa218e72292d98d500240f


import Foundation

func heron(_ a: Double, _ b: Double, _ c: Double) -> Double {
  let s = (a + b + c) / 2
  return  sqrt(s * (s - a) * (s - b) * (s - c))
}
________________________
func heron(_ a: Double, _ b: Double, _ c: Double) -> Double {
  return (a+b+c)/2
}
________________________
import Foundation

func heron(_ a: Double, _ b: Double, _ c: Double) -> Double {
  let s = (a + b + c) / 2
  let t = s*(s - a)*(s - b)*(s - c)
  return sqrt(t)
}
