package kata

import "math/big"

var MOD int64 = 998244353
var eggsArray = CreateEggs()

func CreateEggs() []int64 {
  eggs := []int64{0, 1}
  for i := int64(2); i <= 80000; i++ {
    eggs = append(eggs, ((MOD - MOD/i) * eggs[MOD%i] % MOD))
  }
  return eggs
}

func Height(n, m *big.Int) int64 {

  floor, verifiedFloor := int64(0), big.NewInt(1)
  m.Mod(m, big.NewInt(MOD))

  for i := int64(1); i <= n.Int64(); i++ {
    verifiedFloor.Mul(verifiedFloor, big.NewInt(0).Add(m, big.NewInt(-i+1)))
    verifiedFloor.Mul(verifiedFloor, big.NewInt(eggsArray[i]))
    floor = (floor + verifiedFloor.Mod(verifiedFloor, big.NewInt(MOD)).Int64())
  }
  return floor % MOD
}
__________________________________________________
package kata

import "math/big"

var MOD int64 = 998244353
var mod = big.NewInt(MOD)
var bc []*big.Int

func modInverse(n *big.Int) *big.Int {
  res, x := big.NewInt(1), new(big.Int).Set(n)
  x.Mod(x, mod)
  
  i := MOD-2
  for i > 0 {
    if i&1 > 0 {
      res.Mul(res, x).Mod(res, mod)
    }
    
    i = i >> 1
    x.Mul(x, x).Mod(x, mod)
  }
  
  return res
}

func Height(n, m *big.Int) int64 {
  ni, mi := int64(n.Mod(n, mod).Uint64()), int64(m.Mod(m, mod).Uint64())
  if ni > mi {
    ni = mi
  }
  
  sum, mul, div := big.NewInt(0), big.NewInt(1), big.NewInt(1)
  
  var i int64
  for i = 0; i < ni; i++ {
    mul.Mul(mul, big.NewInt(mi-i)).Mod(mul, mod)
    div.Mul(div, big.NewInt(i+1)).Mod(div, mod)
    
    if len(bc) < int(i)+1 {
      bc = append(bc, modInverse(div))
    }
    sum.Add(sum, new(big.Int).Mul(mul, bc[i]))
  }
  
  return sum.Mod(sum, mod).Int64()
}
__________________________________________________
package kata

import "math/big"

var MOD int64 = 998244353

func madd(a, b int64) int64 {
  return (a + b) % MOD
}
func mmul(a, b int64) int64 {
  return (a * b) % MOD
}
func mpow(a, b int64) int64 {
  if b == 0 {
    return 1
  } else if b % 2 == 0 {
    return mpow(mmul(a, a), b / 2)
  } else {
    return mmul(mpow(mmul(a, a), b / 2), a)
  }
}

func extEu(a, b int64) (int64, int64) {
  if b == 0 {
    return 1,0
  } else {
    q := a / b
    r := a % b
    s, t := extEu(b, r)
    return t, s-q*t
  }
}

func inv(x int64) int64 {
  s, _ := extEu(x, MOD)
  return (s + MOD) % MOD
}

func sc(n, m int64) int64 {
  if m * 2 > n {
    return madd(mpow(2, n), MOD - sc(n, n-m+1))
  } else {
    sum := int64(0)
    r := n
    for i := int64(0); i < m; i++ {
      if i == 0 {
        sum += 1
      } else {
        sum = madd(sum, r)
        r = mmul(mmul(r, (n-i)), inv(i+1))
      }
    }
    return sum
  }
}

func Height(e, t *big.Int) int64 {
  if e.Cmp(t) > 0 {
    return Height(t, t)
  } else {
    return sc(big.NewInt(0).Rem(t, big.NewInt(MOD)).Int64(), e.Int64() + 1) - 1
  }
}
__________________________________________________
package kata

import "math/big"

var MOD int64 = 998244353
var M = big.NewInt(MOD)

var invs []*big.Int = setup(80000)

func Height(n, m *big.Int) int64 {
  h, t := big.NewInt(0), big.NewInt(1)
  m.Mod(m, M)

  for i := int64(1); i <= n.Int64(); i++ {
    b := big.NewInt(1 - i)
    b.Add(b, m)
    t.Mul(t, b).Mul(t, invs[i]).Mod(t, M)
    h.Add(h, t).Mod(h, M)
  }
  return h.Int64()
}

func setup(n int64) []*big.Int {
  invs := []*big.Int{big.NewInt(0), big.NewInt(1)}
  for i := int64(2); i <= n; i++ {
    x := big.NewInt(MOD - MOD/i)
    x.Mul(x, invs[MOD%i])
    x.Mod(x, M)
    invs = append(invs, x)
  }
  return invs
}
