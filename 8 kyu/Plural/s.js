function plural(n) {
  return n !== 1;
}
__________________
function plural(n) {
  return Number.isNaN(n) ? true : (n == 1 ? false : true);
}
__________________
function plural(n) { // define a function that accepts an argument
  if (n > 1 || n < 1){ // if n is greater than 1 or less than 1 return true
    return true
  }
  return false // else return false
}
__________________
function plural(n) {
  if (String(n).includes(".")) {
    return true
  }
  if (n === 0) {
    return true
  }
  if (n === 1) {
    return false
  }
  
  if (n >= 2) {
    return true
  }
  if (n === Infinity) {
    return true
  }
}
__________________
// Understand:
  // the function can take a number and return true if its a plural number <1 or >1
  // the function can return false if the number is not plural (=1)
  // if its not 1, then it is plural
  // anything smaller than 1 or anything greater than 1
  // it cannot be 1. 1 would give you false.

function plural(n) {
 //if n is less than 1 or greater than 1, then return true;
  if (n < 1 || n > 1) {
    return true;
    // else if n is equal to 1, then return false;
  } else if (n = 1) {
    // if n is equal to 1, then return false;
    return false;
  }
    
}
