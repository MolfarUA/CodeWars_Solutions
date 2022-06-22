5a2be17aee1aaefe2a000151


function arrayPlusArray(arr1, arr2) {
  return arr1.concat(arr2).reduce((acc, cur) => acc + cur);
}
_________________________
function arrayPlusArray(...arrays) {
  return [].concat(...arrays).reduce((a,b) => a+b,0)
}
_________________________
function arrayPlusArray(arr1, arr2) {
  let arr = [...arr1, ...arr2];
  return arr.reduce((a, b) => a + b);
}
