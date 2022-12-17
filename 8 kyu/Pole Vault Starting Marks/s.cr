5786f8404c4709148f0006bf


def starting_mark(h)
  (3.9354838709677433*h+3.4680645161290293).round(2)
end
____________________________________
def starting_mark(height)
  (height * 3.9354 + 3.4681).round(2)
end
____________________________________
def starting_mark(x)
    s = (10.67 - 9.45) / (1.83 - 1.52)
    y = (x - 1.52) * s + 9.45
    return y.round(2)
end
____________________________________
def starting_mark(height)
  dx = height - 1.52
  dy_dx = (10.67 - 9.45) / (1.83 - 1.52)
  (9.45 + dy_dx * dx).round(2)
end
