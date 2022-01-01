function filter_list(l) {
  return l.filter(function(v) {return typeof v == 'number'})
}

_____________________________________________
function filter_list(l) {
 return l.filter(v => typeof v == "number")
}

_____________________________________________
function filter_list(l) {
  return l.filter(e => Number.isInteger(e));
}

_____________________________________________
function filter_list(l) {
  return l.reduce((result, x) => typeof x !== "string" ? result.concat(x) : result, [])
}

_____________________________________________
function filter_list(l) {
const result = l.filter(l => typeof l != 'string');
  return result;
}
