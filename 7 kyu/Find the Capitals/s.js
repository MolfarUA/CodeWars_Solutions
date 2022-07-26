53573877d5493b4d6e00050c


function capital(capitals) {
  return capitals.map(function(e) {
    return 'The capital of ' + (e.state || e.country) + ' is ' + e.capital
  })
}
_________________________
function capital(capitals){
  return capitals.map(c => `The capital of ${c.state||c.country} is ${c.capital}`);
}
_________________________
function capital(capitals) {
  return capitals.map(function(v) {return 'The capital of ' + (v.state || v.country) + ' is ' + v.capital;});
}
