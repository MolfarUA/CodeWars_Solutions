55c6126177c9441a570000cc


function orderWeight(strng) {
 const sum = (str)=>str.split('').reduce((sum,el)=>(sum+(+el)),0);
  function comp(a,b){
    let sumA = sum(a);
    let sumB = sum(b);
    return sumA === sumB ? a.localeCompare(b) : sumA - sumB;
   };
 return strng.split(' ').sort(comp).join(' ');
}
_______________________________
function orderWeight(strng) {
  return strng
    .split(" ")
    .map(function(v) {  
      return {
        val: v,
        key: v.split("").reduce(function(prev, curr) {
          return parseInt(prev) + parseInt(curr);
        }, 0)
      };
    })
    .sort(function(a, b) {
      return a.key == b.key 
        ? a.val.localeCompare(b.val)
        : (a.key - b.key);
    })
    .map(function(v) {
      return v.val;
    })
    .join(" ");
}
_______________________________
function digitSum(str) {
  return str.split('').reduce(function(s, e) { 
    return s + parseInt(e); 
  }, 0);
}

function orderWeight(str) {
    return str.split(' ').sort(function(a, b) {
      return digitSum(a) - digitSum(b) || a.localeCompare(b);
    }).join(' ');
}
