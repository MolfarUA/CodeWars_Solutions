function head(a) {return a[0]}

function last(a) {return a[a.length - 1]}

function init(a) {return a.slice(0, -1)}

function tail(a) {return a.slice(1)}
_____________________________
function head(array) {
  return array[0];
}
function tail(array) {
  return array.slice(1);
}
function init(array) {
  return array.slice(0, -1);
}
function last(array) {
  return array[array.length-1];
}
_____________________________
var head = (arr) => arr[0];
var tail = (arr) => arr.slice(1);
var init = (arr) => arr.slice(0, arr.length-1);
var last = (arr) => arr[arr.length-1];
_____________________________
const head = ([head, ...tail]) => head;
const tail = ([head, ...tail]) => tail;
const init = (arr) => arr.slice(0, -1);
const last = (arr) => arr.slice(-1)[0];
