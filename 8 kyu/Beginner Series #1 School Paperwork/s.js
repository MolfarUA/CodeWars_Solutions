55f9b48403f6b87a7c0000bd


function paperwork(n, m) {
  return n > 0 && m > 0 ? n * m : 0
}
__________________________
function paperwork(n, m) {
  let copies = 0;
  if( n < 0 || m < 0){
    copies = 0 
  }else{
    copies = n * m
  }
  return copies
}
__________________________
function paperwork(n, m) {
  if(n < 0 || m < 0){
    return 0
  } else if (n < 0){
    return n - m
  } else if (m < 0){
    return m - n
  } else if (n > 0 & m > 0){
    return n * m
  } else {
    return 0
  }
}
__________________________
const paperwork = (n, m) => { 
  let c= n> 0 && m>0
 return c ? n*m: 0 }
__________________________
function paperwork(n, m) {
 let blankPaper = n < 0 || m < 0 ? 0 : n*m;
  
  return blankPaper;
}
__________________________
function paperwork(n, m) {
  if(n > 0 && m > 0){
    return n * m
  }
  else{
    return n * 0
  }
}
