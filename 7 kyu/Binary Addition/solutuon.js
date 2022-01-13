function addBinary(a,b) {
  const decimalSum = a + b;
  const binarySum = decimalSum.toString(2);
  return binarySum.toString()
}
__________________________________
function addBinary(a,b) {
  return ((a+b)).toString(2);
}

console.log(addBinary(3,1));
__________________________________
function addBinary(a,b) {
let vs = a + b;
  return vs.toString(2);
}
__________________________________
function addBinary(a,b) {
 let sum = a + b;
  let remainder = "";
  while (sum > 0) {
    remainder += sum % 2;
    sum = Math.trunc(sum / 2);
  }
  return remainder.split("").reverse().join("");
}
__________________________________
function addBinary(a,b) {
 let sum = a + b;
 let digitArray = []; 
  while (sum >= 1){
    digitArray.push(sum % 2);
    sum = Math.trunc(sum / 2);
  }
  return digitArray.reverse().join('')
}
__________________________________
function addBinary(a,b) {
  let sum = +a + +b;
  let binary = "";
  while (sum >= 1) {
    binary += Math.trunc(sum % 2)
    sum =  sum / 2;
  }
  return binary.split("").reverse().join("")
}
