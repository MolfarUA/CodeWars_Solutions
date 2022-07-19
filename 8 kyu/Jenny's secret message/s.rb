55225023e1be1ec8bc000390


def greet(name)
  name == 'Johnny' ? "Hello, my love!" : "Hello, #{name}!"
end
__________________________________
def greet(name)
  return "Hello, my love!" if name == "Johnny"
  "Hello, #{name}!"
end
__________________________________
def greet(name)
  if name == 'Johnny'
    return "Hello, my love!"
  else
    return "Hello, #{name}!"
  end
end
__________________________________
def greet(name)
  "Hello, #{name == 'Johnny' ? 'my love' : name}!"
end
