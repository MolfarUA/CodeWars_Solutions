5834fec22fb0ba7d080000e8


function sixToast(num) {
  return Math.abs(num-6)
}
________________________
function sixToast(num) {
  if (num < 6){
  return 6 - num
  } else 
  return num -6; 
}
________________________
const sixToast = n => Math.abs(6 - n);
________________________
function sixToast(num) {
  
  return num >= 6 ? num - 6 : num;
}
