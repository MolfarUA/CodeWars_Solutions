def validate_pin(pin)
  !pin.match(/\A(\d{4}|\d{6})\z/).nil?
end
____________________________
def validate_pin(pin)
  pin.chars.all?(&.ascii_number?) && (pin.size == 4 || pin.size == 6)
end
____________________________
def validate_pin(pin)
  (pin =~ /^[0-9]{4}([0-9]{2})?(?!\n)$/x) ? true : false
end
____________________________
def validate_pin(pin : String) : Bool
  /\A(\d{4}|\d{6})\z/ === pin
end
____________________________
def validate_pin(pin)
  pin.ends_with?('\n') ? false : /^\d{4}$|^\d{6}$/.matches?(pin)
end
____________________________
def validate_pin(pin)
  (pin.size == 4 || pin.size == 6) && pin.chars.all?{|c| c.ascii_number? }
end
