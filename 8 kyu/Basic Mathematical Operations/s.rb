def basic_op(operator, value1, value2)
  value1.send(operator, value2)
end
________________________________
def basic_op(operator, value1, value2)
  eval("#{value1}#{operator}#{value2}")
end
________________________________
def basic_op(operator, value1, value2)
  case operator
  when "+"
    value1 + value2
  when "-"
    value1 - value2
  when "*"
    value1 * value2
  when "/"
    value1 / value2
  end
end
________________________________
def basic_op(operator, *values)
  values.reduce(operator)
end
________________________________
def basic_op(operator, value1, value2)
  value1.public_send operator, value2
end
________________________________
def basic_op(o,a,b)
  eval [a,o,b].join
end
