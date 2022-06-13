bouncingBall <- function(h, bounce, window) {
    if ((h <= 0.0) || (window >= h) || (bounce <= 0.0) || (bounce >= 1.0)) -1
    else 2 + bouncingBall(h * bounce, bounce, window)
}
_______________________________________________
bouncingBall <- function(h, bounce, window) {
    
    if (h<=0 ||bounce <= 0 || 1 <= bounce || h <= window) return(-1)
    
    fall = h*bounce
    glympse = 1;
    
    while(fall > window) {
      fall = fall * bounce
      glympse = glympse + 2
    }
    
    return(glympse)
}
_______________________________________________
bouncingBall <- function(h, bounce, window) {
  if (h <= 0 | window <= 0 | window >= h | bounce <= 0 | bounce >= 1) return(-1)
  lg <- log(window/h, bounce)
  1 + 2*(floor(lg) - (lg %% 1 == 0))
}
_______________________________________________
bouncingBall <- function(h, bounce, window) {
    # your code
  if ((h < 0) | (bounce <= 0) | (bounce >= 1) | (window > h)) {
    return(-1)
  }
  passes = -1
# Solve equation for f(x) = window, using logarithms
  bounces = log(window / h, bounce)
    # Get actual number of bounces that still puts 
    # the ball above window height
  exactBounces = floor(bounces)
    # If last bounce is not strictly higher than window 
    # height, it can't be seen
  if (bounces == exactBounces){
    
        exactBounces = exactBounces-1
  } 
    # The ball will pass the window two times for each bounce, 
    # plus one for the initial drop past window
  passes = exactBounces * 2 + 1
  return(passes)
}
