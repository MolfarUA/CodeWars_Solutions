def iter_pi(epsilon)
  p = 0.0
  n = 1
  d = 1.0
  w = 2
  while (4 * p -  Math::PI).abs > epsilon
    p += 1 / d * (-1) ** w
    n += 1
    d += 2
    w += 1
  end
  [n - 1, (4 * p).round(10)]
end
________________________________________
def iter_pi(epsilon)
  pi4 = counter = 0
  while (Math::PI - pi4*4).abs >= epsilon do
    pi4 += (1 - 2*(counter%2)).fdiv(counter*2+1)
    counter += 1
  end
  [counter, (pi4*4).round(10)]
end
________________________________________
def iter_pi(epsilon)

  pi = 4.0
  iterations = 1
  divisor = 3
  add = false

  while (pi - Math::PI).abs > epsilon
    factor = 4.0 / divisor

    if add
      pi += factor
    else
      pi -= factor
    end

    add = !add
    divisor += 2
    iterations += 1
  end
  
  [iterations, pi.round(10)]
end
________________________________________
def iter_pi(epsilon)
  denominator = 3
  plus = false
  pi = 4.0
  i = 1
  while (pi - Math::PI).abs > epsilon
    if plus 
      pi += (4.0 / denominator)
    else
      pi -= (4.0 / denominator)
    end
    plus = !plus
    denominator += 2
    i += 1
  end
  return [i, pi.round(10)]
end
________________________________________
def iter_pi(epsilon, places:10)
  result = 0
  ops = [:+, :-]
  
  1.step(by: 2).with_index(1) do |term, count|
    result = result.send(ops.first, 1.0/(term))
    approx_pi = result * 4
    
    return [count, approx_pi.round(places)] if (approx_pi - Math::PI).abs < epsilon
    
    ops.rotate!
  end
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
  working = Rational 0
  n = 0
  error = (Math::PI - (working * 4)).abs
  until error <= epsilon
    term = (n.odd? ? -1 : 1).fdiv(2 * n + 1)
    working += term
    t = working * 4
    error = (Math::PI - t).abs
    #p [n, 2*n+1, term, working, t.to_f.round(10), error]
    n += 1
  end
  [n, ("%.10f" % (4.0 * working)).to_f]
end
________________________________________
def iter_pi(epsilon)
  sum = 0
  i = 1
  loop do
    sum += 4.fdiv(2*i-1) * (i.odd? ? 1 : -1)
    return [i, sum.round(10)] while (Math::PI-sum).abs < epsilon
    i += 1
  end
end
________________________________________
def iter_pi(epsilon)
  i, p, cnt = 1, 0, 0
  while (p - Math::PI).abs > epsilon
    m = cnt.odd?? -1.0 : 1.0
    p += 4 * m / i
    i += 2
    cnt += 1
  end
  [cnt, p.round(10)]
end
