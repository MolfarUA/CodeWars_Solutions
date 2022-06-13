function isCoprime(x, y) {
  const min = Math.min(x, y);
  
  for (let i = 2; i <= min; i++) {
    if (x % i === 0 && y % i === 0) {
      return false;
    }
  }
  
  
  return true;
}
___________________________
function isCoprime(x, y){
    var factorsX = [];
    var factorsY = [];
    var gcf = 1;
    for (var i = 2; i <= x; i++) {
        if (x % i === 0) {
        factorsX.push(i);
        }
    }
    for (var i = 2; i <= y; i++) {
        if (y % i === 0) {
        factorsY.push(i);
        }
    }
    for (var i = 0; i < factorsX.length; i++) {
        for (var j = 0; j < factorsY.length; j++) {
        if (factorsX[i] === factorsY[j]) {
            gcf = factorsX[i];
        }
        }
    }
    if (gcf === 1) {
        return true;
    } else {
        return false;
    }
}
___________________________
const isCoprime = (x, y) => y ? isCoprime(y, x % y) : x === 1;
___________________________
function isCoprime(x, y) {
  let arrX = Array.from({length:x}, (_,i)=> x % (i+1) === 0 ? i+1 : 0).filter(e => e)
  let arrY = Array.from({length:y}, (_,i)=> y % (i+1) === 0 ? i+1 : 0).filter(e => e)
  let arr = arrX.filter(e => arrY.includes(e))
  return arr.length === 1
}
