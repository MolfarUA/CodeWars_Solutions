55c04b4cc56a697bb0000048


scramble <- function(s1, s2){
  all(table(factor(unlist(strsplit(s2,"")), levels = letters)) <= table(factor(unlist(strsplit(s1,"")), levels = letters)))
}
______________________________
scramble <- function(s1, s2){
  l1 <- table(unlist(strsplit(s1, "")))
  l2 <- table(unlist(strsplit(s2, "")))
  isTRUE(all(l1[names(l2)] >= l2))
}
______________________________
scramble <- function(s1, s2) {
  if(length(s1 > 1)) s1 <- stringr::str_c(s1, collapse = "")
  if(length(s2 > 1)) s2 <- stringr::str_c(s2, collapse = "")
  all(stringr::str_count(s1, letters) >= stringr::str_count(s2, letters))
}
