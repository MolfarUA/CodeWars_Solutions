def say_hello(name, city, state)
  "Hello, #{name.join(' ')}! Welcome to #{city}, #{state}!"
end
_______________________________________
def say_hello(name, city, state)
  "Hello, %s! Welcome to %s, %s!" % [name.join(" "), city, state]
end
_______________________________________
def say_hello(name, city, state)
  x = name.join(" ")
  return "Hello, #{x}! Welcome to #{city}, #{state}!"
end
_______________________________________
def say_hello(name, city, state)
  if name.empty?
    return "Hello! Welcome to #{city.capitalize}, #{state.capitalize}!"
  else
    return "Hello, #{name.map! {|a| a}.join(' ')}! Welcome to #{city}, #{state}!"
  end
end
_______________________________________
def say_hello(name, city, state)
  new_name = name.join(' ')
  "Hello, #{new_name}! Welcome to #{city}, #{state}!"
end
