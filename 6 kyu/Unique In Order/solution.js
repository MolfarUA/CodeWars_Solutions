function uniqueInOrder(it) {
  var result = []
  var last
  
  for (var i = 0; i < it.length; i++) {
    if (it[i] !== last) {
      result.push(last = it[i])
    }
  }
  
  return result
}
_____________________________________________
var uniqueInOrder=function(iterable){
    return [...iterable].filter((a, i) => a !== iterable[i-1])
}
_____________________________________________
var uniqueInOrder = function (iterable)
{
  return [].filter.call(iterable, (function (a, i) { return iterable[i - 1] !== a }));
}
_____________________________________________
var uniqueInOrder=function(iterable){
  var res = [];
  for (var i = 0; i < iterable.length; i++) {
    if (iterable[i] != iterable[i+1]) res.push(iterable[i]);
  }
  return res;
}
_____________________________________________
var uniqueInOrder=function(iterable){
  var result = [];
  for (var i = 0; i < iterable.length; i++) {
    if (iterable[i-1] === undefined || iterable[i-1] !== iterable[i]) {
      result.push(iterable[i]);
    }
  }
  return result;
}
