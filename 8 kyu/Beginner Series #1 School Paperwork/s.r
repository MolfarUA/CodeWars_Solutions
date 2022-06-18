55f9b48403f6b87a7c0000bd


paperwork <- function(n, m){
  ifelse(n > 0 && m > 0, n * m, 0)
}
__________________________
paperwork <- function(n, m){
  return(ifelse(n < 0 | m < 0, 0, n*m))
}
__________________________
paperwork <- function(n, m){
  if (n<0 | m<0){
    return(0)
  }
  n*m
}
__________________________
paperwork <- function(n, m){
  if (n<=0){
  return(0)
  }
  else if (m<=0){
    return(0)
  }
  else {
   return(n*m)
  }
    
}
__________________________
paperwork <- function(n, m){
    if(n<0 | m<0) print(0)
    else print(n*m)
}
__________________________
paperwork <- function(n, m){
  p <- n * m # multiply number of classmates with number of pages
  ifelse(n < 0 | m < 0, 0, p) # reutrn total number of pages (p) only if none of the arguments is negative
}
