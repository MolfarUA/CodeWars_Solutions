515de9ae9dcfc28eb6000001


function solution(s){
   return (s+"_").match(/.{2}/g)||[]
}
________________________________
function solution(str){
  var i = 0;
  var result = new Array();
  if (str.length % 2 !== 0) {
    str = str + '_';
  }
  while (i < str.length) {
      result.push(str[i] + str[i+1]);
      i += 2;
    }
  return result;
}
________________________________
function solution(str){
  arr = [];
  for(var i = 0; i < str.length; i += 2){
    second = str[i+1] || '_';
    arr.push(str[i] + second);
  }
  return arr;
}
________________________________
const solution = str => ((str+"_").match(/../g)||[]);
________________________________
let solution = str => str.length == 0 ? [] : str.length % 2 != 0 ? (str += '_').split('').map((x, i) => i == 0 ? x : i % 2 == 0 ? ' ' + x : x).join('').split(' ') : str.split('').map((x, i) => i == 0 ? x : i % 2 == 0 ? ' ' + x : x).join('').split(' ');
