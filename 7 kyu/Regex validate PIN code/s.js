function validatePIN(pin) {
  return /^(\d{4}|\d{6})$/.test(pin)
}
____________________________
function validatePIN (pin) {
  
  var pinlen = pin.length;
  var isCorrectLength = (pinlen == 4 || pinlen == 6);
  var hasOnlyNumbers = pin.match(/^\d+$/);
    
  if(isCorrectLength && hasOnlyNumbers){
    return true;
  }
  
  return false;

}
____________________________
function validatePIN (pin) {
  pin = pin.split('')
 const findNaN = pin.find(character => !(parseInt(character) >= 0))
  if ((pin.length === 4 || pin.length === 6) && !findNaN) {
    return true
  } else {
    return false
  }

}
____________________________
const validatePIN = pin => /^(\d{4}|\d{6})$/.test(pin);
