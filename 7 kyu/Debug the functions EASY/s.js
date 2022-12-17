5844a422cbd2279a0c000281


function multi(arr) {
  return arr.reduce((a, b) => a * b)
}
function add(arr) {
  return arr.reduce((a, b) => a + b)
}
function reverse(str) {
  return str.split('').reverse().join('')
}
________________________
function multi(arr) {
  return arr.reduce((n, x) => n * x, 1)
}

function add(arr) {
  return arr.reduce((n, x) => n + x, 0)
}

function reverse(str) {
  return [...str].reverse().join("")
}
________________________
function multi(arr) {
  var answer = 1;
  for(var i = 0; i < arr.length; i++){
      answer *= arr[i];  
  }
  return answer;
}
function add(arr) {
  var answer = 0;
  for(var i = 0; i<arr.length; i++){
    answer += arr[i];
  }
  return answer;
}
function reverse(str) {
  return str.split("").reverse().join("");
}
