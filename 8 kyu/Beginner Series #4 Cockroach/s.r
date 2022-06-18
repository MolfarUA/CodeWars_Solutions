55fab1ffda3e2e44f00000c6


cockroach_speed <- function(s){
  s %/% 0.036
}
__________________________
cockroach_speed <- function(s){
 x <- s * 27.77777777777778
 floor(x)
}
__________________________
cockroach_speed <- function(s){
 floor(s * 100000/60**2)
}
__________________________
cockroach_speed <- function(s){
  b = s*1000*100/3600
  return(floor(b))
}
__________________________
cockroach_speed <- function(s){
 x <- s * 27.7778
  floor(x)
}
