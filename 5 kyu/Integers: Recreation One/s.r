55aa075506463dac6600010d


listSquared <- function (m, n) {
  output <- list()
  for (i in m:n) {
    divis <- which((i %% (1:i)) == 0)
    sum_squares <- sum(divis * divis)
    if ((sqrt(sum_squares) %% 1) == 0) { output[[length(output) + 1]] <- c(i, sum_squares) }
  }
  output
}
________________________________
listSquared <- function (m, n) {
  res <- list()
  j <- 1
  for (i in seq.int(from = m, to = n)) {
    divs <- c(seq_len(i %/% 2), i)
    divs <- divs[i %% divs == 0]
    ss <- sum(divs ** 2)
    sqss <- ss ** 0.5
    if (as.integer(sqss) == sqss) {
      res[[j]] <- c(i, ss); j <- j + 1
    }
  }
  res
}
________________________________
listSquared <- function (m, n) {
  all <- list()
  for (i in m:n) {
    divisors <- c()
    for (j in 1:round(sqrt(i))) {
      if (i %% j == 0) {
        divisors <- c(divisors, j, i/j)
      }
    }
    tot <- sum(unique(divisors)^2)
    if (sqrt(tot) %% 1 == 0) {
      all[[length(all)+1]] <- c(i, tot)
    }
  }
  return(all)
}
