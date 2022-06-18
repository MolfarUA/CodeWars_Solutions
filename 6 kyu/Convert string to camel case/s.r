to_camel_case <- function(text){
  gsub('[-_](.)','\\U\\1',text,perl=T)
}
________________________
to_camel_case <- function(text){
  regex = "[-_]([[:alpha:]])"
  return(gsub(regex, "\\U\\1", text, perl = TRUE))
}
________________________
to_camel_case <- function(text){
  return(gsub("\\_(\\w?)", "\\U\\1", gsub("-", "_", text), perl = TRUE))
}
________________________
capitalize <- function(word){
  return(paste(toupper(substr(word,1,1)), substr(word,2,nchar(word)), sep = ""))
}
to_camel_case <- function(text){
  s <- strsplit(text,"[-_]")
  cap_text <- paste(unlist(lapply(s, capitalize)),collapse = "")
  #check if fist one is capital
  if(grepl("[A-Z]",substring(text,1,1))){
    return(cap_text)
  }else{
    return(paste(tolower(substr(cap_text,1,1)), substr(cap_text,2,nchar(cap_text)), sep = ""))
  }
}
________________________
to_camel_case <- function(text){
  # Your code here
  library(stringr)
#   x = unlist(strsplit(gsub("[^A-Za-z0-9]", "_", text), " "))
  x = unlist(strsplit(gsub("-", "_", text), "[_]+"))
  if(length(x) < 1)
    return("")
  else{
    if(length(x) > 1){
      for(i in 2:length(x)){
        x[i] = str_to_title(x[i])  
      }
      x = paste0(x, collapse = "")
     }
    return(x)
  }
  
}
