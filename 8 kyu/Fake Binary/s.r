fake_bin <- function(x){
  x <-gsub('[0-4]',0,x)
  x <- gsub('[5-9]',1,x)
  print(x) 
}
__________________________________
library("tidyverse")
fake_bin <- function(x){
 n <- str_split(x, pattern = "") %>% 
  unlist() 
n <- ifelse (n < 5, 0, 1)
paste(n, collapse = "")
}
__________________________________
fake_bin <- function(x){
  numbers <- strsplit(x, "")[[1]]
  ans <- ''
  for (i in numbers){
    if (as.integer(i) < 5){
      ans <- paste(ans, 0, sep="")
    }
    if (as.integer(i) >= 5){
      ans <- paste(ans, 1, sep="")
    }
 }
  return(ans)
}
__________________________________
fake_bin <- function(x){
  xsplit <- as.integer(strsplit(x, "")[[1]])
  fake_binary <- c()
  for (i in xsplit) {
    fake_binary <- c(fake_binary, ifelse(i<5, 0, 1))
  }
  paste(as.character(fake_binary), collapse="")
 
}
