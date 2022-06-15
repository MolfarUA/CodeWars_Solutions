function isValidWalk(walk) {
  var dx = 0
  var dy = 0
  var dt = walk.length
  
  for (var i = 0; i < walk.length; i++) {
    switch (walk[i]) {
      case 'n': dy--; break
      case 's': dy++; break
      case 'w': dx--; break
      case 'e': dx++; break
    }
  }
  
  return dt === 10 && dx === 0 && dy === 0
}
__________________________________________
function isValidWalk(walk) {
  if(walk.length != 10) return false;
  
  var directions = walk.reduce((acc, e) => acc.set(e, (acc.get(e) || 0) + 1), new Map());
  if(directions.get("w") == directions.get("e") && directions.get("n") == directions.get("s")) {
    return true;
  }
}
__________________________________________
function isValidWalk(walk) {
  if(walk.length === 10){
    let vert = 0
    let hori = 0
    for(i = 0; i < walk.length; i++){
      if(walk[i] === 'n'){
        vert += 1
      }else if(walk[i] === 's'){
        vert -= 1
      }else if(walk[i] === 'e'){
        hori += 1
      }else if(walk[i] === 'w'){
        hori -= 1
      }
    }
    if(vert === 0 && hori === 0){
      return true
    }else{
      return false
    }
  }else{
    return false
  }
}
__________________________________________
function isValidWalk(walk) {
    let res = false;
    var x = 0, y = 0;
    for (var i = 0; i < walk.length; i++) {
        y += (walk[i] == 's') ? -1 : ((walk[i] == 'n') ? 1 : 0);
        x += (walk[i] == 'w') ? -1 : ((walk[i] == 'e') ? 1 : 0);
    }
    res = ((x == 0 && y == 0) && walk.length == 10);
    return res;
}
