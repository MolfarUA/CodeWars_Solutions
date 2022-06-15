function fakeBin(x) {
    return x.split('').map(n => n < 5 ? 0 : 1).join('');
}
__________________________________
function fakeBin(x) {
  return x.replace(/\d/g, d => d < 5 ? 0 : 1);
}
__________________________________
function fakeBin(x) {
  let arr = x
    .split("")
    .map((a) => (a >= 5 ? 1 : 0))
    .join("");
    return arr
}
__________________________________
function fakeBin(str) {
  return str.split('').map(value => value >= 5 ? 1 : 0).join('');
}
__________________________________
function fakeBin(x){
  let z = x.replace(/[0-4]/g, 0);
 return z.replace(/[5-9]/g, 1);
}
