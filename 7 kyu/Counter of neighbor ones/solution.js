const onesCounter = inp => inp.join('').split('0').map(e=>e.length).filter(e=>e);
_____________________________________________
var onesCounter = ($) => ($.join('').match(/(1+)/g)||[]).map(e=>e.length)
_____________________________________________
function onesCounter(input) {
  const arr = [];
  let counter = 0;
  for(let num of input) {
   if(num === 1) counter ++;
   else if(counter !== 0){
     arr.push(counter);
     counter = 0;
     }
  }
  if(counter) arr.push(counter);
  return arr;
}
_____________________________________________
function onesCounter(input) {
  let result = [];
  let counter = 0;
  let index = 0;
  
  for(let i = 0; i < input.length; i++) {
    if (input[i] === 0) {
      counter = 0;
      index = result.length;
    }
    
    if(input[i] === 1) {
      counter++;
      result[index] = counter;
    }
  }
  
  return result;
}
