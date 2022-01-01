your_order <- function(s){
  l <- unlist(strsplit(s, " "))
  names(l) <- as.numeric(gsub("[[:alpha:]]", "", l))
  paste(l[order(names(l))], collapse = " ")
}

_____________________________________________
your_order <- function(sentence){
  w <- unlist(strsplit(sentence, " "))
  paste(w[order(gsub("\\D", "", w))], collapse = " ")
}

_____________________________________________
your_order <- function(sentence){
  sentence_to_words <- strsplit(sentence, " ")[[1]]
  numbers_in_words <- as.numeric(gsub("[A-Za-z]", "", sentence_to_words))
  names(numbers_in_words) <- sentence_to_words
  sorted_words <- names(sort(numbers_in_words))
  paste(sorted_words, collapse = " ")
}

_____________________________________________
your_order <- function(sentence){
  if (sentence != ""){
    words.new <- c()
    words.new[as.integer(grep("[0-9]", strsplit(sentence, split = "")[[1]], value=T))] <- strsplit(sentence, split = " ")[[1]]
    paste0(words.new, collapse = " ")
  }else{
    return("")
  }
}

_____________________________________________
library(stringr)

your_order <- function(sentence){
  test = gsub(".*?([1-9]+).*", "\\1", sentence)
  num_id = as.character(c(1:9))
  if( sum(test == num_id) > 0){
  words = unlist(strsplit(sentence," "))
  num = as.numeric(gsub(".*?([1-9]+).*", "\\1", words))
  y <- cbind(num, words)
  z <-as.data.frame(y)
  ordered <- z[order(z$num),]
  ans = str_c(ordered$words, collapse = " ")
  print(ans)
 }else{
    print("")
  }
}
