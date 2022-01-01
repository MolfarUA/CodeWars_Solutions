const flip = (d, a) => a.sort((x, y) => d === 'R' ? x - y : y - x);

_____________________________________________
const flip=(d, a)=>{
  if(d === 'R') return a.sort((a,b)=>a-b);
  if(d === 'L') return a.sort((a,b)=>b-a);
}

_____________________________________________
const flip = (d, a) => d === 'R' ? a.sort((a, b) => a - b) : a.sort((a, b) => b - a)

_____________________________________________
const flip = (d, a) => {
  return d === 'R' ? sortArray(a)
    : 'L' ? sortArray(a).reverse()
      : false;
}

const sortArray = arr => arr.sort((a, b) => (a - b));

_____________________________________________
const flip=(d, a)=>{
  console.log(d)
  console.log(a)
  let result = a
  if(d == 'L')  {
    return result.sort(function(a,b) {return a - b}).reverse()
  } else {
    return result.sort(function(a,b) {
      return a - b
    })
  }
  return 
}
