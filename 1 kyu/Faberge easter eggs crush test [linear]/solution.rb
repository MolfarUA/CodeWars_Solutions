5976c5a5cd933a7bbd000029


$invs = [0,1]
for i in 2..80000 do
  $invs << (MOD - MOD / i) * $invs[MOD % i] % MOD
end

def height(n,m)
  m %= MOD
  
  h, t = 0, 1
  for i in 1..n do
    t = t * (m-i+1) * $invs[i] % MOD
    h = (h+t) % MOD
  end
  
  return h
end
__________________________________________________
MOD = 998244353
ARR = [0, 1]

(2..80000).each do |haha_i|
  ARR.append( (MOD - MOD / haha_i) * ARR[MOD % haha_i] % MOD )
end
        
def height(n, m)
    h, t = 0, 1
    m %= MOD
    (1..n).each do |i|
            t = t * (m - i + 1) * ARR[i] % MOD
            h = (h + t) % MOD
     end       
    return h % MOD
end
__________________________________________________
def mod_pow(a,x,p)
  r = 1
  while x>0
    r = (r*a)%p if x.odd?
    a = (a*a)%p; x = x/2
  end
  r
end

def sum_mod_bin(n,k,p)
  s=0; nm=1; dm=1
  (0..k-1).each do |i|
    nn = (nm*(n-i))%p; nd = (dm*(i+1))%p
    s = (s+nn*mod_pow(nd, MOD-2, MOD))%p; nm=nn; dm=nd
  end
  s
end

def height(n,m)
  return mod_pow(2, m, MOD) - 1 if n>m
  return ((MOD-2) + mod_pow(2, m, MOD) - height(m-n-1,m)) % MOD if n > m/2
  sum_mod_bin(m%MOD, n, MOD)
end
__________________________________________________
$r = [nil, 1]
(2..80000).each{|i| $r[i] = - (MOD / i * $r[MOD % i]) % MOD}

def height(n,m)
  return 0 if n.zero? || m.zero?
  return (2 ** m - 1) % MOD if n >= m
  n2 = 2*n
  return (2 ** (m - 1) - 1) % MOD if n2 == m - 1
  return (2 ** m - height(m-n-1, m) - 2) % MOD if n2 > m
  ((1..n).reduce([1]){|num, i| num << (num[-1] * (m-i+1) * $r[i] % MOD)}.sum - 1) % MOD
end
__________________________________________________
$ARR = [0, 1]
i = 2
while i <= 80000
  $ARR  << (MOD - MOD / i) * $ARR[MOD % i] % MOD
  i += 1
end

def height(n,m)
  a, b = 0, 1
  (1..n).each do |i|
    b = b * (m - i + 1) * $ARR[i] % MOD
    a = (a + b) % MOD
  end
  a
end
__________________________________________________
def height(n, m)
  mo = 998244353
  a_inv = [0, 1]
  (2..80000).each do |i|
        a_inv << ( (mo - mo.div(i)) * a_inv[mo % i] % mo )
  end
    h, t= 0, 1
    (1..n).each do |i|
        t = ((t * (m - i + 1)) * a_inv[i]) % mo
        h = (h + t) % mo
        i += 1
    end
    return h
end
__________________________________________________
MAX_N = 100_005
$h_inv_mod = {}


def pow_mod(x, y, m = MOD)
  return 1 if x == 1
  return x % m if y == 1
  return x * pow_mod(x, y - 1, m) % m if y.odd?
  x = pow_mod(x, y >> 1, m)
  x ** 2 % m
end

def inv_mod(x, m = MOD)
  return $h_inv_mod[x] if $h_inv_mod[x]
  $h_inv_mod[x] = pow_mod(x, m - 2, m)
end

def sum_c(n, k, m)
  s = x = n % m
  t = (n + 1) % m
  (2..k).each do |i|
    x = x * (t - i) % m * inv_mod(i, m) % m
    s = (s + x) % m
  end
  s
end

$fact = Array.new(MAX_N, 1)
(2..MAX_N-1).each {|i| $fact[i] = $fact[i-1] * i % MOD}
$inv_fact = $fact.map {|i| inv_mod(i, MOD)}

def sum_c_case_2(n, k, m)
  s = 0
  (1..k).each do |i|
    s = (s + ($inv_fact[i] * $inv_fact[n-i] % MOD)) % MOD
  end
  $fact[n] * s % MOD
end

def height(n,m)
  n > m ? (pow_mod(2,m) - 1) % MOD : m <= 100_000 ? sum_c_case_2(m,n,MOD) : sum_c(m,n, MOD)
end
__________________________________________________
def f(n)
  n%MOD
end

$arr=Array.new(80000, nil)
$arr[0]=1
for n in 1..79999
  $arr[n]=f(MOD-MOD/(n+1)*$arr[MOD % (n+1) - 1])

def height(n,m)
  a=b=m=f(m)
  for i in 1..n-1
    b=f(b*(m-i)*$arr[i])
    a=f(a+b)
    end
  return f(a)
  end
end
