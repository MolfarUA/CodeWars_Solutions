539a0e4d85e3425cb0000a88


function add(n){
  var fn = function(x) {
    return add(n + x);
  };
  
  fn.valueOf = function() {
    return n;
  };
  
  return fn;
}
______________________
var add = function(n) {
  const f = x => add(n + x)
  f.valueOf = () => n
  return f;
}
______________________
const add = n => Object.assign(i => add(i + n), { valueOf: () => n })
______________________
function add(n) {
  var next = add.bind(n += this | 0);
  next.valueOf = function() { return n; };
  return next;
}
