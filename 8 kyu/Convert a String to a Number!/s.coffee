544675c6f971f7399a000e79


stringToNumber = (str) -> +str
_______________________
stringToNumber = Number
_______________________
stringToNumber = (str) -> 
  if str? and typeof str is "string"
    tmp = Number(str)
    unless isNaN(tmp)
      return tmp
    return "Not a number"
_______________________
stringToNumber = (str) -> str = + str;
stringToNumber = (str) -> Number(str);
stringToNumber = (str) -> parseFloat(str);
stringToNumber = (str) -> parseInt(str);
stringToNumber = (str) -> Math.floor()(str);  # ... your code here
stringToNumber = (str) -> str = str * 1;
