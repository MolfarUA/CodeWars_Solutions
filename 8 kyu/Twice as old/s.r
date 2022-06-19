5b853229cfde412a470000d0


twice_as_old <- function(dad_years_old, son_years_old){
    abs(dad_years_old - son_years_old * 2)
  }
______________________________
twice_as_old <- function(a, b) {
   abs(a - 2 * b)
}
______________________________
twice_as_old <- function(dad_years_old, son_years_old){
  diff <- dad_years_old-son_years_old
  ans <- abs(diff-son_years_old)
  ans
}

