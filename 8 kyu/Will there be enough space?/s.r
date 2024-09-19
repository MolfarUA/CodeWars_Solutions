5875b200d520904a04000003

enough <- function(cap, on, wait){
  space <- cap - on
  ifelse(space >= wait, 0, (wait - space))
}
_______________________________
enough 

<- function(cap, on, wait) max(on + wait - cap, 0)
_______________________________
enough <- function(cap, on, wait){
  if (cap >= on + wait) {0}
  else if (cap < on + wait) {
    x <- (on + wait) - cap
    x
  }
}
_______________________________
enough <- function(cap, on, wait) {
  ifelse(wait <= (cap-on), 0, wait - (cap-on))
}
