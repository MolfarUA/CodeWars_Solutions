require(dplyr)
require(tidyr)

earth_movers_distance <- function(x, px, y, py) {
  
  df_x <- tibble(v = x, px = px)
  df_y <- tibble(v = y, py = py)
  
  df <- df_x %>%
    full_join(df_y) %>%
    replace_na(list(px=0, py=0)) %>%
    arrange(v) %>%
    mutate(dif = py - px) %>% 
    mutate(dist = v - lag(v, default = 0)) %>%
    mutate(cumsum = cumsum(dif)) %>%
    mutate(cost = lag(abs(cumsum), default = 0) * dist)
  
  sum(df$cost)
}
_________________________________________________
earth_movers_distance = function(x, px, y, py) {
    w <- sort(union(x, y))
    d <- head(mapply(sum, py[match(w, y)], -px[match(w, x)], na.rm = TRUE), -1)
    sum(diff(w) * abs(cumsum(d)))
}
_________________________________________________
earth_movers_distance = function(x, px, y, py) {
    w <- sort(union(x, y))
    px <- ifelse(is.na(match(w, x)), 0, px[match(w, x)])  
    py <- ifelse(is.na(match(w, y)), 0, py[match(w, y)])
    sum(abs(c(diff(w), 0) * cumsum((py - px))))  
}
_________________________________________________
earth_movers_distance = function(x, px, y, py)
{
 # Let D be the difference of the cdfs.
 z = c(x, y);                          # points at which D is discontinuous
 d = tapply(c(px,-py), z, sum);        # jump sizes at the unique points of z
 d = abs(cumsum(d));                   # values of |D| at the unique points of z
 d = d[-length(d)];                    # discard last value (it will be zero)
 z = sort(unique(z));                  # the points of discontinuity, in order
 return(sum(d * diff(z)));             # integral of |D|
}
