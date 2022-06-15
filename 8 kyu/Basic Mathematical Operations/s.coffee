ops =
  '+': (x, y) => x + y
  '-': (x, y) => x - y
  '*': (x, y) => x * y
  '/': (x, y) => x / y
basicOp= (operation, value1, value2) -> ops[operation] value1, value2
________________________________
basicOp = (op, a, b)->
    switch op
        when "+" then a + b
        when "-" then a - b
        when "*" then a * b
        when "/" then a / b
        else throw Error "Wrong op"
________________________________
basicOp=(operation, value1, value2)->
  eval(value1+operation+value2)
________________________________
basicOp=(operation, value1, value2)->
  if operation == "+"
    return value1+value2;
  else if operation == "-"
    return value1-value2;
  else if operation == "*"
    return value1*value2;
  else if operation == "/"
    return value1/value2;
  else
    return 0;
________________________________
basicOp = (operation, value1, value2) ->
  operators = {"+": ((a, b) -> a + b), "-": ((a, b) -> a - b), "*": ((a, b) -> a * b), "/": ((a, b) -> a / b)}
  operators[operation](value1, value2)
