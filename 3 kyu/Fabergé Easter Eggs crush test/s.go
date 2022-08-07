package kata

import (
        "math/big"
)
/*
Summary: Series of combinations of i from i = 0 to i = n
  ∑mCi for integer i ∈ [0,n]
Visually:
  m*m-1*m-2*m-3*m-4*...*m-i * (m-i-1)!        
∑ ------------------------------------      divided by
             (i+1)!         * (m-i-1)!
  
  Equals to,
  m*m-1*m-2*m-3*m-4*...*m-i
∑ -----------------------------     for i from 0 to n
                 (i+1)!
                 
i=     0    ,        1     ,           2        ,             3               , ...

let T0 = 1. Then,

               (m - i)           
Hi= H(i-1) * ----------  ;  Thus,  Si = ∑ Hi
               (i + 1)     

      m        [m]  *(m-1)   [m*(m-1)]* (m-2)        [m*(m-1)*(m-2)] * (m-3)       
S=  ------  +  ----------- +  ---------------   +  -------------------------  + ...
      1!       [1!] * 2           [2!]*  3                  [3!]     *  4          

*/


/*Note1: This way get stack-overflow. Thus need to reduce factorial combutation to simpler ways
func Factorial(num int64) *big.Int {
  return big.NewInt(num).MulRange(1,num)
}
*/

func Height(n, m *big.Int) *big.Int {
  eggs, totalTries := int64(n.Uint64()), int64(m.Uint64())
  
  // s : max height which is sum of heights; h: each height for each iteration of tries
  s, h := big.NewInt(0), big.NewInt(1)  
  
  /*//Note1: This way get stack-overflow, time limit error. 
    //Thus need to reduce factorial combutation to simpler ways
  
  for i:= int64(1); i <= eggs; i++ {
    s.Add(s, big.NewInt(1).Div(Factorial(totalTries), big.NewInt(1).Mul(Factorial(totalTries-i),Factorial(i))))
  }
  
  */
  
  for i:= int64(0); i < eggs; i++ {
    // Calculate Hi
    h.Mul(h, big.NewInt(totalTries-i))
    h.Div(h, big.NewInt(i+1))
    
    // Sum = Hi + { ∑Ht for t ∈ [0,i-1] }
    s.Add(s,h)
  }
  
  return s
}
_________________________
package kata

import (
  "math/big"
)

func Height(n, m *big.Int) *big.Int {
  // There's no need to calculate for more eggs than tries
  if n.Cmp(m) == 1 {
    n = new(big.Int).Set(m)
  }

  one := big.NewInt(1)
  floor := big.NewInt(0) // Start on floor 0

  numerator := new(big.Int).Set(m)
  last_i := big.NewInt(0)

  // Tracks i!
  fac := big.NewInt(1) // 0!

  for i := new(big.Int).Set(one); i.Cmp(n) <= 0; i.Add(i, one) {
    // denominator = m * i!
    denominator := new(big.Int).Mul(m, fac.Mul(fac, i))
    // numerator = (current_numerator) * (m - (i-1))
    numerator.Mul(numerator, new(big.Int).Sub(m, last_i))

    floor.Add(floor, new(big.Int).Div(numerator, denominator))

    // Set last_i so it equals i-1 on the next iteration
    last_i = new(big.Int).Set(i)
  }
  return floor
}
_________________________
package kata

import (
        "math/big"
)


func Height(n, m *big.Int) *big.Int {
  var floor = big.NewInt(0)
  var verifiedFloor = big.NewInt(1)
  for i := int64(1); i <= n.Int64(); i++ {
    verifiedFloor.Quo(verifiedFloor.Mul(verifiedFloor, big.NewInt(0).Add(m, big.NewInt(-i+1))), big.NewInt(i))
    floor.Add(floor, verifiedFloor)
  }
  return floor
}
