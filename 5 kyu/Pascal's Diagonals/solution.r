generate_diagonal <- function(n, l){
  if (l == 0 || n == 0) {
    return(rep(1,l))
  }else{
    return(cumsum(generate_diagonal(n - 1,l)))
  }
}
_______________________________
generate_diagonal <- function(n, l) {
  if (l <= 0) {
    return(sequence(0))
  } else {
    c <- 1
    res <- c(1)
    i <- 1
    while (i < l) {
      c <- c * (n + i) / i
      res[i] <- c
      i <- i + 1
    }
    return(rev(append(rev(res),1)))
  }
}
_______________________________
generate_diagonal <- function(diagonal, len){
  if (len == 0) return(numeric(0))
  if (diagonal == 0) return(rep(1, len))
  return(cumsum(generate_diagonal(diagonal - 1, len)))
}
_______________________________
generate_diagonal <- function(n, l){
  
  pascalTriangle <- function(h) {
    lapply(0:h, function(i) choose(i, 0:i))
  }
  
  outcome <- pascalTriangle(500)
  for(i in 1:length(outcome)){
    outcome[[i]] <- outcome[[i]][-1]
  }
  
  outcome <- outcome[-1]
  len <- length(outcome)
  
  for(i in 1:length(outcome)){
    if(length(outcome[[i]] < len)){
      outcome[[i]] <- c(outcome[[i]], rep(0, (len - length(outcome[[i]]))))
      i <- i + 1
    }
  }
  
  mat <- matrix(unlist(outcome), byrow = TRUE, nrow = len)
  
  final <- c()
  if(n == 0){
    final <- rep(1, times = l)
  }
  if(l == 0){
    final <- numeric(0)
  }
  if(n != 0 & l != 0){
    final <- mat[(n:(n+l-1)),n]
  }
  print(final)
}
