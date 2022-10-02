5547cc7dcad755e480000004


func removNb(_ n: Int) -> [(Int,Int)] {
    let sum: Int = (n*n+n)/2
    var results: [(Int, Int)] = []
    
    // The least multiplicand must be greater than sum/n since n
    // is the greatest possible multiplicand.  I used that to reduce
    // the values that need to be checked
    for a in sum/n...n{
      // The largest test sum would then be sum-a-n, dividing by a gives
      // a lower bound for the other multiplicand
      for b in (sum-a-n)/(a)...sum/a{
        if (sum-a-b) == (a*b){
          results.append((a,b))
          break
        }
      }
    }
    return results
}
______________________________
func removNb(_ n: Int) -> [(Int,Int)] {
  var sum = (n+1)*n/2
  var answ = [(Int,Int)]()
  for i in 1..<n {
    var a = (sum - i)/(i+1)
      if (a*i == sum - a - i && a <= n ){
        answ.append((i, a))
        }   
  }
  return answ
}
______________________________
func removNb(_ n: Int) -> [(Int,Int)] {
  var s = n * (n + 1) / 2
  var res = [(Int,Int)]()
  for i in 1..<n {
    var nb = (s - i) / (i + 1)
      if (nb * i == s - nb - i && nb <= n ){
        res.append((i, nb))
        }    
  }
  return res
}
