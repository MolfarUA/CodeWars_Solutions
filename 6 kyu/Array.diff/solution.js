function arrayDiff(a, b) {
  return a.filter(i => !b.includes(i))
}
###########
function array_diff(a, b) {
  return a.filter(function(x) { return b.indexOf(x) == -1; });
}
###########
function array_diff(a, b) {
  return a.filter(function (v) { return b.indexOf(v) === -1 });
}
#######
function array_diff(a, b) {

    var arr = new Array();
    
    for(var i = 0;i<a.length;i++){
        if(b.indexOf(a[i])<0){
            arr.push(a[i]);
        }
    }
  
    return arr;
}
###############
function arrayDiff(a, b) {
  const output = []
  
  for (let i = 0; i < a.length; i++) {
    if (!b.includes(a[i])) {
      output.push(a[i])
    }
  }
  return output
}
#############
function arrayDiff(a, b) {
result = [];
  for(n of a) {
if (!b.includes(n)){
result.push(n)
}
  }
  return result;
}
#################
function arrayDiff(a, b) {
  if(a.length == 0)return a;
  return a.filter(num=>!b.includes(num));
}
