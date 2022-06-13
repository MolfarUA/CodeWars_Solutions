function bouncingBall(h,  bounce,  window) {
  var rebounds = -1;
  if (bounce > 0 && bounce < 1) while (h > window) rebounds+=2, h *= bounce;
  return rebounds;
}
_______________________________________________
function bouncingBall(h,  bounce,  window) {
  if( h <= 0 || bounce >= 1 || bounce <= 0 || window >= h) return -1
  let seen = 0;
  
  while(h > window){
    seen += 1
    h *= bounce
    if(h > window) seen += 1
  }
  
  return seen;
}
_______________________________________________
function bouncingBall(h,  bounce,  window) {
  let count = 0
  let currentHeight = h
  if (h > 0 && bounce > 0 && bounce < 1 && window < h) {
    while (currentHeight >= window) {
      if (currentHeight > window)
        count++
      currentHeight *= bounce
      if (currentHeight > window)
        count++
    }
    return count
  }
  else
    return -1
}
_______________________________________________
function bouncingBall(h, bounce, window) {
    let result = 1
    if (bounce >= 1 || bounce <= 0 || h <= 0 || window >= h) return -1
    while (h >= window) {
        // debugger
        h *= bounce
        if(h>window) result += 2
    }
    return result
}
