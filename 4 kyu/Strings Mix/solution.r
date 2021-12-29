mix <- function(s1, s2) {
    g1 <- table(strsplit(s1, split = '')[[1]][unlist(gregexpr('[a-z]', s1))])
    g2 <- table(strsplit(s2, split = '')[[1]][unlist(gregexpr('[a-z]', s2))])
    x <- sapply(
        unique(c(names(g1[g1 > 1]), names(g2[g2 > 1]))),
        function(x) {
            if (is.na(g2[x]))
                c(sprintf('1:%s', stringr::str_dup(x, g1[x])), g1[x])
            else if (is.na(g1[x]))
                c(sprintf('2:%s', stringr::str_dup(x, g2[x])), g2[x])
            else if (g1[x] > g2[x])
                c(sprintf('1:%s', stringr::str_dup(x, g1[x])), g1[x])
            else if (g2[x] > g1[x])
                c(sprintf('2:%s', stringr::str_dup(x, g2[x])), g2[x])
            else
                c(sprintf('E:%s', stringr::str_dup(x, g1[x])), g1[x])
        }
    )
    if (length(x) == 0) return('')
    y <- data.frame(mix = x[1,], len = x[2,])
    stringr::str_c(dplyr::arrange(y, desc(len), mix)$mix, collapse = '/')
}

_____________________________________________________
mix <- function(s1, s2) {
mix0 <- sapply(letters,function(x){
  freqs <- lengths(gregexpr(x,c(s1,s2)))
  if((max_f <- max(freqs))==1) return('')
  paste0(if(diff(freqs)) which.max(freqs) else "E",":",paste(rep(x,max_f),collapse=""))})
mix0 <- mix0[mix0 !=""]
paste(mix0[order(-nchar(mix0),sapply(mix0,substr,1,1))],collapse="/")
}

_____________________________________________________
mix <- function(s1, s2){
  s11 <- unlist(strsplit(s1, NULL))
  s11 <- s11[which(s11 %in% letters)]
  s11 <- sort(s11)
  
  s22 <- unlist(strsplit(s2, NULL))
  s22 <- s22[which(s22 %in% letters)]
  s22 <- sort(s22)
  
  
  u1 <- unique(s11)
  u2 <- unique(s22)
  u <- append(u1, u2)
  u <- sort(unique(u))
  
  s11 <- factor(s11, levels = u)
  s22 <- factor(s22, levels = u)
  
  st1 <- table(s11)
  st1 <- as.data.frame(st1)
  colnames(st1)[1] <- "level"
  colnames(st1)[2] <- "Freq1"
  
  st2 <- table(s22)
  st2 <- data.frame(st2)
  colnames(st2)[1] <- "level"
  colnames(st2)[2] <- "Freq2"
  
  st <- merge(st1, st2)
  result <- c()
  part1 <- c()
  for(i in 1:nrow(st)){
    if(st[i, 2] == st[i, 3]){
      result[i] <- st[i, 2]
      part1[i] <- "E:"
    }
    if(st[i, 2] < st[i, 3]){
      result[i] <- st[i, 3]
      part1[i] <- "2:"
    }
    if(st[i, 2] > st[i, 3]){
      result[i] <- st[i, 2]
      part1[i] <- "1:"
    }
    
  }
  part1 <- factor(part1, levels = c("1:", "2:", "E:"))
  st <- cbind(st, result, part1)
  
  for(i in 1:nrow(st)){
    if(st[i, 4] <=1){
      st[i, 4] <- NA
    }
  }
  
  final <- c()
  if(all(is.na(st$result)) == TRUE){
    final <- ""
  }
  else{
    st <- na.omit(st)
    st$level <- as.character(st$level)
    st <- st[order(st$part1), ]
    st <- st[order(st$result, decreasing = TRUE), ]
    
    part2 <- c()
    for(i in 1:nrow(st)){
      part2[i] <- paste(rep(st$level[i], times = st$result[i]), collapse = "")
    }
    st <- cbind(st, part2)
    st$part1 <- as.character(st$part1)
    
    outcome <- paste(st$part1, st$part2, sep = "")
    final <- paste(outcome, collapse = "/") 
  }
  
  print(final)
}

_____________________________________________________
library(stringr)
library(dplyr)

mix <- function(s1, s2) {
  re <- regex('[a-z]')
  s1 <- strsplit(s1, '')[[1]] %>% str_extract(re)
  s2 <- strsplit(s2, '')[[1]] %>% str_extract(re)
  
  tally_1 <- table(s1) %>% Filter(function(x) x > 1, .)
  tally_2 <- table(s2) %>% Filter(function(x) x > 1, .)
  
  tally_1 <- tally_1[order(-tally_1, names(tally_1))]
  tally_2 <- tally_2[order(-tally_2, names(tally_2))]
  
  all_letters <- c(names(tally_1), names(tally_2)) %>% unique()
  
  if (length(all_letters) == 0) return('')
  
  df <- data.frame(
    letter   = all_letters,
    s1_count = as.numeric(tally_1[all_letters]),
    s2_count = as.numeric(tally_2[all_letters])
  ) %>% 
    replace(is.na(.), 0)
  
  df$shorthand <- apply(df, 1, function(r) {
    s1_count <- r['s1_count'][[1]]
    s2_count <- r['s2_count'][[1]]
    if (s2_count > s1_count) {
      return( paste(c('2:', rep(r['letter'], s2_count)), collapse='') )
    } else if (s1_count > s2_count) {
      return( paste(c('1:', rep(r['letter'], s1_count)), collapse='') )
    } else {
      return( paste(c('E:', rep(r['letter'], s1_count)), collapse='') )
    }
  })
  
  df <- arrange(df, -apply(df[c('s1_count', 's2_count')], 1, max), shorthand)
  
  return(paste(df$shorthand, collapse = '/'))
}

_____________________________________________________
mix <- function(s1, s2) {
    # make list of strings, get only lowercase letters, make a table to count and subset values > 1
    s1_list <- unlist(strsplit(s1, ""));         s2_list <- unlist(strsplit(s2, "")) 
    s1_list <- s1_list[s1_list %in% letters];    s2_list <- s2_list[s2_list %in% letters]
    s1_tabl <- table(s1_list)[table(s1_list)>1]; s2_tabl <- table(s2_list)[table(s2_list)>1] 
    # if not any values > 1, return "", if only not values in s1 data <- data.frame(s2_table) else data.frame(s1_table)
    if ((length(s1_tabl) == 0) | (length(s2_tabl) == 0)) {
        if (length(s1_tabl) == length(s2_tabl)) return("")
        if (length(s1_tabl) == 0) data <- data.frame(val = names(s2_tabl), freq = as.numeric(s2_tabl), string = 2)
        else data <- data.frame(val = names(s1_tabl), freq = as.numeric(s1_tabl), string = 1)
    } else { # else data <- data.frame(join both data.frames of strings_tables)
    data_s1 <- data.frame(val = names(s1_tabl), freq = as.numeric(s1_tabl), string = 1)
    data_s2 <- data.frame(val = names(s2_tabl), freq = as.numeric(s2_tabl), string = 2)
    data    <- rbind(data_s1, data_s2)
    }
    # order data, format equal values, quit repeated values
    ans <- c()
    data <- data[order(-data$freq, data$val),]
    if (length(data[,1]) > 1) for (i in 2:length(data[,1]) - 1) if (data$val[i] == data$val[i+1] & data$freq[i] == data$freq[i+1]) data$string[i] <- "E" 
    data <- data[!duplicated(data$val), ]
    data <- data[order(-data$freq, data$string, data$val),]
    # format data in the require format
    for (i in 1:length(data[,1])) ans <- c(ans, paste0(data$string[i], ":", paste(rep(data$val[i], data$freq[i]), collapse = ""), "/"))
    ans <- paste(ans, collapse = "")
    ans <- substr(ans, 1, nchar(ans)-1)
}
