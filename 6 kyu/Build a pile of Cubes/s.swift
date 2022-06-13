func findNb(_ number: Int) -> Int {

    var sum = 1
    var index = 1
    while number > sum {
        index += 1
        //sum += Int(pow(Double(index),Double(3)))
        sum += index * index * index
    }
    
    return number == sum ? index : -1

}
_________________________________________
import Glibc

// m = 1^3 + 2^3 + ... + (n - 1)^3 + n^3 = (n*(n + 1)/2)^2
func findNb(_ m: Int) -> Int {
  let x = 2*sqrt(Double(m)); // x = n*(n + 1)
  if x != floor(x) { return -1; }
  let n = floor(sqrt(x));
  return n*(n + 1) == x ? Int(n) : -1;
}
_________________________________________
func findNb(_ number: Int) -> Int {
  var m = number
  var n = 0
  while m > 0 {
    n += 1
    m -= n * n * n
  }
  return m == 0 ? n : -1
}
_________________________________________
func findNb(_ number: Int, _ n: Int = 1) -> Int {
  let remainder = number - (n * n * n)
  return remainder > 0 ? findNb(remainder, n + 1) : (remainder == 0 ? n : -1)
}
