def validate_pin(pin)
  pin.match? /\A\d{4}(\d{2})?\z/
end
____________________________
def validate_pin(pin)
  (pin.length == 4 || pin.length == 6) && pin.count("0-9") == pin.length
end
____________________________
def validate_pin(pin)
  /\A(\d{4}|\d{6})\z/ === pin
end
____________________________
def validate_pin(pin)
  pin.match?(/\A\d+\z/) ? pin.length == 4 || pin.length == 6 : false
end
