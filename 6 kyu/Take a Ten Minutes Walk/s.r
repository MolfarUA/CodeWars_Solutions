isValidWalk <- function(walk){
  length(walk)==10 &(sum(walk=="n") ==sum(walk =="s")) &(sum(walk=="w") ==sum(walk =="e"))
}
__________________________________________
isValidWalk <- function(walk){
  dict <- data.frame(code = c("n", "e", "w", "s"), val = c(1, 100, -100, -1))
  walk <- data.frame(code = walk)
  data <- merge(dict, walk)
  return(nrow(data) == 10 & sum(data$val) == 0)
  }
__________________________________________
isValidWalk <- function(walk){
  sum(walk =='n') == sum(walk == 's') & sum(walk =='e') == sum(walk == 'w') & length(walk) == 10
}
__________________________________________
isValidWalk <- function(walk){
  tab <- table(walk)
  if (length(walk) == 10) {
    if (dim(tab) == 4) {
      tab["e"] == tab["w"] && tab["n"] == tab["s"]
    } else if (dim(tab) == 2) {
      sort(walk)[5] != sort(walk)[6]
    } else {
      FALSE
    }
  } else {
    FALSE
  }
}
__________________________________________
isValidWalk <- function(walk){
    require(tidyverse)
  directions <- data.frame(e = 0, n = 0, s = 0, w = 0)
  walk_tbl <-   as.matrix(t(table(walk)))
  names(walk_tbl) <- names(table(walk))
  frecs <- colSums(bind_rows(as.matrix(walk_tbl), directions))
  frecs <- frecs %>% replace_na(replace = 0)
  if (
    length(walk) == 10 &
    frecs["n"] == frecs["s"] &
    frecs["e"] == frecs["w"]) {
    print(TRUE)
  } else {
      FALSE
    }
}
