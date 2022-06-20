559b8e46fa060b2c6a0000bf


def choose(n : UInt64, p : UInt64) : UInt64
    if (p > n) 
      return 0_u64 
    end
    if (p > n - p) 
      p = n - p 
    end
    nu_u64 = (n - p + 1_u64 .. n).reduce(1_u64){|m_u64, e| m_u64 * e}
    de_u64 = (2_u64 .. p).reduce(1_u64){|m_u64, e| m_u64 * e}
    nu_u64 / de_u64
end

def diagonal(n : UInt64, p : UInt64) : UInt64
    choose(n+1, p+1)
end
_____________________________
require "big"

def choose(n : BigInt, k : BigInt) : BigInt
  res = 1.to_big_i
  (1..k).each {|i|
    res = res * (n - i + 1) / i
  }
  res
end

def diagonal(n : UInt64, p : UInt64) : UInt64
  choose((n + 1).to_big_i, (p + 1).to_big_i).to_u64;
end
