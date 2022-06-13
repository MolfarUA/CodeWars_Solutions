def boolean_to_string(b)
  b ? "true" : "false"
end
_________________________________
def boolean_to_string(b)
  b.to_s
end
_________________________________
def boolean_to_string(b)
  b.inspect
end
_________________________________
def boolean_to_string(b)
  string = "false"
  if b
      string = "true" end
  return string
end
_________________________________
def boolean_to_string(b)
  if b == true then return "true"
  end
  "false"
end
_________________________________
def boolean_to_string(b)
  if b
    return "true"
  else
    "false"
  end
end
