def iter_pi(epsilon)
  my_pi = 0.0
  nb_loop = 0
  while(((my_pi*4)-Math::PI).abs >= epsilon)
    my_pi += ((nb_loop%2).zero? ? 1 : -1)/((nb_loop)*2+1)
    nb_loop+=1
  end
  return  [nb_loop, (my_pi*4).round(10)]
end
________________________________________
def iter_pi(epsilon)
  pi4 = 1.0
  sign = -1.0
  iterations = 1
  denom = 3.0
  while (4 * pi4 - Math::PI).abs >= epsilon
    pi4 += sign * (1.0 / denom)
    sign *= -1
    denom += 2
    iterations += 1
  end
  [iterations, (4 * pi4).round(10)]
end
________________________________________
def iter_pi(epsilon)
  i, t = 0, 1
  pi = t
  while (Math::PI - pi * 4).abs > epsilon
    i += 1
    t += 2
    pi += (i.even? ? 1.0 : -1.0) / t
  end
  [i+1, (pi * 4).round(10)]
end
________________________________________
require "math"

# Int32 overflow with built-in crystal .round
def string_round(val, dg = 1)
  sint, sdec = val.to_s.split(".")
  sround = (sdec[dg - 1..dg].to_i / 10.0).round.to_i
  "#{sint}.#{sdec[0..dg-2]}#{sround}".to_f64
end

def iter_pi(epsilon)
  val, n = 1.0, 1
  
  (3..Int32::MAX).step(2) do |i|
    val += (1.0 / i) * ((i / 2 % 2).zero? ? 1 : -1)
    n += 1
    break if (Math::PI - val * 4.0).abs < epsilon
  end
  [n, string_round(val * 4.0, 10)]
end
________________________________________
def iter_pi(epsilon)
  my_pi = i = 0
  while (my_pi - Math::PI).abs > epsilon
    my_pi += (i % 2 == 0 ? 4.0 : -4.0) / (2 * i + 1)
    i += 1
  end
  [i, (1e10 * my_pi).round / 1e10]
end
________________________________________
def iter_pi(epsilon)
  divisor = 1.0; sign = 1.0; count = 0; sum = 0.0
  while (sum - Math::PI).abs > epsilon
    sum += sign * 4.0 / divisor
    divisor += 2.0; sign *= -1.0; count += 1
  end
  r = (sum * 1e10).round / 1e10
  [ count, r ]
end
