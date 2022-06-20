55466989aeecab5aac00003e


squaresInRect <- function(lng, wd) {
    sq <- function(l, w) {
        if (l == w) c(w)
        else if (l > w) c(w, sq(w, l -w))
        else c(l, sq(l, w - l))
    }
    if (lng == wd) NULL else sq(lng, wd)
}
______________________________
squaresInRect <- function(lng, wd,START=T) {
    if (START &lng==wd) return (NULL)
    if (lng==wd) return (lng)
    else{ 
     m<-min(c(lng, wd))
     return (c(m, squaresInRect(max(c(lng, wd))-m,m,F)))
    }            
}
______________________________
squaresInRect <- function(lng, wd) {
  if (lng == wd) { # return NULL if square is provided
    return(NULL)
  } else {
    rect_area <- lng * wd # get total rectangle area
    all_sqr <- c() # initialize empty vector to store results
    while (sum(all_sqr^2) != rect_area) { # repeat until entire area is occupied by squares
      # Biggest square possible has the same side as wd of the rectangle and can be fitted
      # as many times as lng / wd (wihtout remainder)
      all_sqr <- c(all_sqr, rep(wd, floor(lng / wd)))
      # "New" lng and wd after "cutting" the calculated squares, new lng is equal to the side
      # of the square (so current wd), while new wd is the remainder of the lng / wd division
      new_lng <- wd
      new_wd <- lng %% wd
      lng <- new_lng
      wd <- new_wd
    }
    return(all_sqr)
  }
}
