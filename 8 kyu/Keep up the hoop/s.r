55cb632c1a5d7b3ad0000145


hoop_count <- function(n){
  ifelse(n >= 10, "Great, now move on to tricks", "Keep at it until you get it")
}
_____________________________
hoop_count <- function(n){
  ifelse(n<10,"Keep at it until you get it","Great, now move on to tricks")
}
_____________________________
hoop_count <- function(n){
  if (n<10){
    print("Keep at it until you get it")
  } else{
    print("Great, now move on to tricks")
  } 
}
