validatePIN = (pin) ->
  /^(\d{4}|\d{6})$/.test(pin)
____________________________
validatePIN = (p) -> /^\d\d\d\d(\d\d)?$/.test p
____________________________
validatePIN = (pin) ->
  if pin.match /^(\d{4}|\d{6})$/ then true else false
____________________________
validatePIN = (pin) ->
  len = pin.toString().length 
  return false if len isnt 4 and len isnt 6
  return false if isNaN pin
  return false if /\./.test pin
  return false if /\D/.test pin
  return false if pin<0
  return false if pin%1
  return true
  # return true or false
