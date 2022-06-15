basic_op <- function(operator, value1, value2){
  eval(parse(text = paste(value1, operator, value2)))
}
________________________________
basic_op <- function(operator, value1, value2){
switch(
operator,
"+" = value1 + value2,
"-" = value1 - value2,
"*" = value1 * value2,
"/" = if(value2 != 0) {value1 / value2}
else {"Error!"})
}
________________________________
basic_op <- function(operator, value1, value2){
 do.call(operator, list(value1, value2))
}
________________________________
basic_op <- function(operator, value1, value2) {
  switch(
    operator,
    '+' = `+`(value1, value2),
    '-' = `-`(value1, value2),
    '*' = `*`(value1, value2),
    '/' = `/`(value1, value2),
  ) 
}
________________________________
basic_op <- function(operator, value1, value2){
  ifelse(operator == "+", value1 + value2,
         ifelse(operator == "-", value1 - value2,
                ifelse(operator == "*", value1 * value2,
                       ifelse(operator == "/", value1 / value2, "Null operator"))))
}
