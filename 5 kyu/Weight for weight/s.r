55c6126177c9441a570000cc


orderWeight <- function(st) {
  s <- as.character(sort(unlist(strsplit(st, ' '))))
  w <- sapply(s, function(x) sum(sapply(unlist(strsplit(x, '')), as.double)))
  paste0(s[order(w, s)], collapse = ' ')
}
______________________________
orderWeight <- function(st) {
  digitSum <- function(n) {
    sum((function(x) (floor(x / 10^(0:(nchar(x) - 1))) %% 10))(n))
  }
  if (nchar(st) == 0) return("")
  fs <- strsplit(st, " ")[[1]]
  f <- as.numeric(fs)
  res <- mapply(digitSum, f)
  c <- data.frame(we = res, value = fs)
  u <- c[with(c, order(we, value)), ]
  paste(u$value, collapse=" ")
}
______________________________
orderWeight <- function(st) {
  
  if(st == "") {return(st)} #check for null string
  
  s <- strsplit(st, " ")
  s1 <- strsplit(s[[1]], "") #get all digits separated
  s2 <- lapply(s1, as.numeric) #turn digits into numeric
  s3 <- unlist(lapply(s2, sum)) #add all the digits and return as a vector
  
  df <- data.frame(unlist(s), s3)
  newDf <- df[order(df$unlist.s.), ] #put 'alphabetically' in case duplicate weights
  newNewDf <- newDf[order(newDf$s3), ] #sort by weights
  newOrder <- newNewDf$unlist.s. #put the sorted original numbers in a vector
  
  ans <- paste(newOrder, collapse = " ") #collapse to one string
  return(ans)
  
}
