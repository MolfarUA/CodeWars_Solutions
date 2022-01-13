iterPi <- function(epsilon) {
  value <- 0; cnt <- 0; factor <- 1; divider <- 1
  while (abs(pi - (value * 4)) >= epsilon) {
    value <- value + factor / divider
    factor <- -factor
    divider <- divider + 2
    cnt <- cnt + 1
  }
  c(cnt, round(value * 4, 10))
}
________________________________________
#' Calculates decimals of PI using Leibniz formula.
#'
#' @param epsilon double
#' Precision value for calculation.
#'
#' @return double; vector
#' Result in form: iterations, PI approximation.
#' @export
#'
#' @examples
iterPi <- function(epsilon) {
  n = 1
  estim = 4
  while (abs(estim - pi) > epsilon) {
    n = n + 1
    estim = estim + c(-4, 4)[(n %% 2) + 1] / (2 * n - 1)
  }

  res = c(n, estim)

  return(res)
}
________________________________________
iterPi <- function(eps) {
  s <- 4
  i <- 1
  my_pi <- 4
  while (abs(my_pi - pi) > eps) {
    my_pi <- my_pi - s / (2 * i + 1)
    i <- i + 1
    s <- -s
  }
  c(i, my_pi)
}
________________________________________
##' Calculate the amount of turns to reach pi with a given epsilon according 
##' to Leibniz formula (PI/4 = 1-1/3+1/5-1/7+...)
##' @title iterPi
##' @param epsilon the epsilon value (desired precision)
##' @return a vector with the number of iterations and the result of pi
##' @author Krisselack
iterPi <- function(epsilon) {

pimin <- pi - epsilon
pimax <- pi + epsilon
res <- 0
iter <- 1
counter <- 0
pi4 <- 1

  while(res < pimin | res > pimax){
    iter <- abs(iter)+2
    if(counter %% 2 == 0){
      iter = iter*(-1)
    }
    pi4 <- pi4+(1/iter)
    res <- pi4*4
    counter = counter +1
  }
  return((c(counter+1, res)))
}
________________________________________
iterPi <- function(epsilon) {
  p = 0
  n = 1
  count = 0
  while (abs(4*p - pi) > epsilon){
    p = p + (1/n)*(-1)**count
    n = n + 2
    count = count + 1
  }
  c(count, 4*p)
}
