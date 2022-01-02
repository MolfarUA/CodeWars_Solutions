const number = (busStops) => busStops.reduce((rem, [on, off]) => rem + on - off, 0);
_____________________________________
var number = function(busStops){
  var totalPeople = 0;
  for (var i=0; i<busStops.length; i++) {
    totalPeople += busStops[i][0];
    totalPeople -= busStops[i][1];
  }
  return totalPeople;
}
_____________________________________
const number = busStops => busStops.reduce((p,n) => p+n[0]-n[1],0)
_____________________________________
var number = function(busStops){
  return busStops.map(x => x[0] - x[1]).reduce( (x, y) => x + y);
}
