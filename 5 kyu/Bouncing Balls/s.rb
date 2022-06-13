def bouncingBall(h, bounce, window)
  bounce < 0 || bounce >= 1 || h <= window || window < 0 ? -1 : bouncingBall(h * bounce, bounce, window) + 2
end
_______________________________________________
def bouncingBall(h, bounce, window)
    if h <= 0 || bounce < 0 || bounce >= 1 || window >= h
      -1  
    elsif h * bounce <= window
      1
    else      
      return 2 + bouncingBall(h * bounce, bounce, window)
    end
end
_______________________________________________
def bouncingBall(h, bounce, window)
  return -1 unless h > 0 && (bounce < 1 && bounce > 0) && window < h
  res = 1
  while (h * bounce) > window
    h *= bounce
    res += 2
  end
  res
end
_______________________________________________
def bouncingBall(h, bounce, window)
  return -1 unless h > 0 && window < h && bounce > 0 && bounce < 1
  seen = 1
  
  while h > window
    h *= bounce
    seen += 2 if h > window
  end
  seen
end
_______________________________________________
def bouncingBall(h, bounce, window)
  return -1 if !bounce.between?(0.01, 0.99) || h < 1
  
  counter = -1
  
  while h > window
    h *= bounce
    counter += 2
  end
  
  counter
end
