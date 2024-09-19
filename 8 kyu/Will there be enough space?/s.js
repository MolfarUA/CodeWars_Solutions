5875b200d520904a04000003

function enough(cap, on, wait) {
  return cap >= on + wait ? 0 : wait - (cap - on);
  // return Math.max(wait + on - cap, 0);
}
#########################
function enough(cap, on, wait) {
    if (on+wait > cap) {
       var x = on + wait - cap ;
        return x;
        
    }
    else{
        return 0;
    }
  }
###########################
function enough(cap, on, wait) {
  const capacity = cap - (on + wait)
 return capacity >= 0 ? 0 : (on + wait) - cap
}
#########################
function enough(c,o,w){
  return ((c - o) - w) < 0 ? (((c - o) - w) * (-1)) : 0;
}
