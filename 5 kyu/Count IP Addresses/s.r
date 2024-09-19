ips_between <- function(start, end) {
  sum(Reduce(function(a, b) as.integer(a) - as.integer(b),
             strsplit(c(end, start), "\\.")) * 256^(3:0))
}
____________
ips_between <- function(start, end) {
  s <- as.integer(unlist(strsplit(start, ".", fixed = TRUE)))
  e <- as.integer(unlist(strsplit(end, ".", fixed = TRUE)))
  difference <- rev(e-s)
  sum(sapply(seq_along(difference), function(i){
    difference[i]*256^(i-1)
  }))
  
}
__________________
ips_between <- function(start, end) {
  toBase256 <- function(ip) {
    ip <- as.numeric(strsplit(ip,"\\.")[[1]])
    sum(mapply(`*`, ip, 256^(3:0)))
  }
  
  toBase256(end) - toBase256(start)
}
