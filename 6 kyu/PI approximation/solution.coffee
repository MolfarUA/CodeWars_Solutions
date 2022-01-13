iterPi = (epsilon) ->
  [approx, sum, i] = [0, 0, 0]
  while Math.abs(approx - Math.PI) >= epsilon
    sum += (-1) ** i / (2 * i++ + 1)
    approx = 4 * sum
  [i, +approx.toFixed(10)]
________________________________________
iterPi = (epsilon) ->
  myPi = i = 0
  myPi += 4 * Math.pow(-1, i) / (2 * i++ + 1) while Math.abs(myPi - Math.PI) > epsilon
  [i, Math.round(1e10 * myPi) / 1e10]
________________________________________
iterPi = (epsilon) ->
  n = 1.0
  value = 0.0
  counter = 0
  while Math.abs(Math.PI - (4 * value)) > epsilon
    value += 1.0 / n
    n = -n
    if n > 0
      n += 2.0
    if n < 0
      n -= 2.0
    counter += 1
  [
    counter
    parseFloat((value * 4).toFixed(10))
  ]
________________________________________
iterPi = (epsilon) ->
  pi4 = 1
  sign = -1
  iterations = 1
  denom = 3
  while Math.abs(4 * pi4 - (Math.PI)) >= epsilon
    pi4 += sign * 1 / denom
    sign *= -1
    denom += 2
    iterations++
  [
    iterations
    +(pi4 * 4).toFixed(10)
  ]
________________________________________
iterPi = (epsilon) ->
  estimate = 1;
  d = 3;
  sign = -1;
  iterationsCount = 1;
  while (Math.abs(4 * estimate - Math.PI) >= epsilon)
    estimate += sign * (1/d);
    d += 2;
    iterationsCount += 1;
    sign *= -1;
  return [iterationsCount, parseFloat((4 * estimate).toFixed(10))];
