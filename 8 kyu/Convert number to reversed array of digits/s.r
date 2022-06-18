digitize <- function(n) {
  out = strsplit(as.character(n), split = "")[[1]]
  return(as.numeric(rev(out)))
}
________________________
digitize <- function(n){
    a <- as.numeric(strsplit(as.character(n), "")[[1]])
    rev(a)
}
________________________
library(stringr)
digitize <- function(n){
  str_split(n, "") %>% 
  unlist() %>% 
  rev() %>% 
  as.numeric()
}
________________________
digitize <- function(n){
  result <- rev(as.numeric(strsplit(as.character(n), "")[[1]]))
  return (result)
}
________________________
digitize <- function(n){
  n = c(strsplit(as.character(n),'')[[1]])
  n = c(n[length(n):1])
  n = c(as.numeric(n))
}
