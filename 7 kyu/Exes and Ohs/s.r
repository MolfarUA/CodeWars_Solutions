xo <- function(s){
  s <- unlist(strsplit(casefold(s), ""))
  sum(s == "o") == sum(s == "x")
}
__________________________________
xo <- function(s) {
  chars <- strsplit(tolower(s), "")[[1]]
  sum(chars == "x") == sum(chars == "o")
}
__________________________________
xo <- function(s) {
  s <- unlist(strsplit(s, ""))
  x <- length(grep("x", s, ignore.case = T))
  o <- length(grep("o", s, ignore.case = T))
  if (identical(x, o)) {
    return(TRUE)
  } else return(FALSE)
}
__________________________________
xo <- function(s){
  string <- s
  x <- ifelse(unlist(strsplit(string, "")) %in% c("x","X"), TRUE, FALSE) %>% sum()
  o <- ifelse(unlist(strsplit(string, "")) %in% c("o","O"), TRUE, FALSE) %>% sum()
  
  if (x == o) {
    return(TRUE)
    }
  return(FALSE)
}
__________________________________
library(stringr)
xo <- function(s) { 
  y = tolower(s) 
  if(str_count(y,'[xo]') != 0) {
    str_count(y,'o') == str_count(y,'x') }
  else{return(TRUE)}
}
