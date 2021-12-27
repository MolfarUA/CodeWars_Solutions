function numberOfPairs(gloves) {

  var pairs = 0
  ,  counts = {};
  
  for (var color of gloves) {
  
    if (!counts.hasOwnProperty(color))
      counts[color] = 0;

    if (++counts[color] === 2) {
      counts[color] -= 2;
      pairs++;
    }
  }
    
  return pairs;
}

____________________________
function numberOfPairs(gloves){
  var res = {};
  gloves.map(function(x){
    res[x] = res[x] ? res[x]+1 : 1;
  });
  return Object.keys(res).reduce(function(a,b){
    return a + (res[b] > 1 ? Math.floor(res[b]/2) : 0);
  },0);
}

___________________
function numberOfPairs(gloves)
{
  var arr = Array.from(new Set(gloves));
  return arr.reduce((a,b) => a + Math.floor(gloves.join('').match(new RegExp(b, 'g')).length / 2), 0);
}

___________________
function numberOfPairs(gloves){
  return [...new Set(gloves)].reduce( (acc,el) => acc + ~~(gloves.filter(x => x === el).length / 2), 0);
}

___________________
numberOfPairs=a=>[...new Set(a)].map(b=>a.join``.split(b).length-1).reduce((a,b)=>a+(b>>1),0)

_________________
function numberOfPairs(gloves){
  let cnt=gloves.reduce((o,g)=>(o[g]=o[g]+1||1,o), {})
  return Object.values(cnt).reduce((s,v)=>s+v/2|0,0)
}

________________
function numberOfPairs(gloves) {
  let pairs = 0;
  let count = {}
  for (let color of gloves) {
    if (color in count) {
      count[color]++;
      if (count[color] === 2) {
        pairs++;
        count[color] = 0;
      }   
    } else {
      count[color] = 1;
    }
  }
  return pairs;
}
