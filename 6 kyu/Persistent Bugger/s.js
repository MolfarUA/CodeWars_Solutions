function persistence(num) {
   var times = 0;
   
   num = num.toString();
   
   while (num.length > 1) {
     times++;
     num = num.split('').map(Number).reduce((a, b) => a * b).toString();
   }
   
   return times;
}
________________________________________
const persistence = num => {
  return `${num}`.length > 1 
    ? 1 + persistence(`${num}`.split('').reduce((a, b) => a * +b)) 
    : 0;
}
________________________________________
function persistence(num) {
   for (var i = 0; num > 9; i++) {
     num = num.toString().split('').reduce((t, c) => c * t);
   }
   return i;
}
________________________________________
/**
 * This function will calculate the multiplication of the digit of the number 
 * given as parameter
 */
function multiplyDigits( num ) {
  // If have just 1 digit number, we just return it
  if( num < 10 ) {
    return num;
  // If more than one digit, will be first digit * recursive call to this function
  }else {
    let firstDigit = Math.floor( num / 10 );
    return ( num - firstDigit * 10 ) * 
      multiplyDigits(firstDigit);
  }
}

/**
 * This function will count on the number of times we have to call multiply
 * till we don't have any more times to call ( we just have one digit ) 
 */
function count( num, times = 0 ) {
  if( num < 10 ) {
    return times;
  }else {
    // 999 = 9 * 9 * 9 = 729, ...
    return count( multiplyDigits( num ), ++times );
  }
}
/**
 * Just the public function we call in order to count the number of times
 * we have to multiply the digits of the param number till we have just 
 * one digit as result 
 */
function persistence( num ) {
  return count( num );
}
