function potatoes(p0, w0, p1) {
   return Math.floor(w0 * (100 - p0) / (100 - p1))
}
_______________________________________________
function potatoes(p0, w0, p1) {
    return ~~(w0 * (100.0 - p0) / (100.0 - p1))
}
_______________________________________________
function potatoes(p0, w0, p1) {
    let w1 =  w0 - (w0 * p0 / 100)
    let w2 = (w1 * 100) / (100 - p1)
    console.log(w1, w2)
   return Math.trunc(w2.toFixed(2))
}
_______________________________________________
function potatoes(p0, w0, p1) {
    let d  = w0 * (100 - p0)/100;
    let ans = d * 100/(100 - p1);
    return Math.floor(ans)
}
_______________________________________________
function potatoes(p0, w0, p1) {
  return Math.floor(w0 * (100 - p0) / (100 - p1))
   
}

// p0 = initial percent of water - 99
// w0 = initial weight - 100 
// p1 = final perecent of water - 98

// potatoes(99, 100, 98) --> 50

// function potatoes should return final weight.. 
