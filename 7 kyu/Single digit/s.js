function singleDigit(n) {
  while(n > 9){
    n = n.toString(2).replace(/0/g, "").length
  }
  return n
}
__________________________
function singleDigit(n) { 
  
  return n < 10 ? n : singleDigit([...n.toString(2)].reduce((a, b) => a + +b, 0)) 
}
__________________________
const singleDigit = $ => 
  `${$}`.length < 2 ? $ : 
    singleDigit( [...$.toString(2)].reduce((acc, el) => acc + Number(el), 0) )
__________________________
function singleDigit(n) {
  while (n >= 10) {
    n = (n.toString(2).match(/1/g) || []).length;
  }
  return n;
}
__________________________
function singleDigit(n) {
  return n > 9 ? singleDigit(bitCount(n)) : n;
}

function bitCount (n) {
  return n.toString(2).match(/1/g).length
}
__________________________
function singleDigit(n) {
    while(n>9) n=Array.from(String(n.toString(2)),Number).reduce((v,w) => v+w);
    return n;
}
__________________________
const singleDigit = n => {
  while (n >= 10) {
    let tmp = 0;
    for (let i = 0; i < 32; ++i) {
      tmp += n & 1;
      n >>= 1;
    }
    n = tmp;
  }
  return n;
};
