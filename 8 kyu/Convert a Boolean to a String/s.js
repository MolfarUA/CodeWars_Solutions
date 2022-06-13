function booleanToString(b){
  return b.toString();
}
_________________________________
function booleanToString(b){
  return b ? 'true' : 'false';
}
_________________________________
function booleanToString(b){
  return String(b);
}
_________________________________
function booleanToString(b){
  if(typeof(b) !== 'boolean') throw 'input must be a boolean'
  
  return b ? 'true' : 'false'
}
_________________________________
const booleanToString = (b) => {
  
  const makeString = String(b);
  
  return makeString;
  
}
