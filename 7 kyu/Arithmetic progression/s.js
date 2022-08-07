55caf1fd8063ddfa8e000018


function arithmeticSequenceElements(a,r,n) {
  var ret = [a]
  while (--n) ret.push(a+=r);
  return ret.join(', ')
}
___________________________
function arithmeticSequenceElements(a, r, n) {
  return Array.from({length: n}, (_, i) => a + r * i).join(', ');
}
___________________________
function arithmeticSequenceElements(a,r,n) {
  return new Array(n).fill().map((i,k) => a + k * r).join(", ");
}
___________________________
function arithmeticSequenceElements(a,r,n) {
  var array = [a]
  var newnum = a
  for(i=1;i<n;i++){
    array.push(newnum+=r)
  }
  return array.join(", ")
}
