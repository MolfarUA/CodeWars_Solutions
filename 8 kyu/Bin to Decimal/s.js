57a5c31ce298a7e6b7000334


function binToDec(bin){
  return parseInt(bin,2);
}
_________________________
const binToDec = bin => parseInt(bin,2);
_________________________
binToDec=n=>parseInt(n,2)
_________________________
const binToDec = bin => [...bin].reverse().reduce((acc, elt, idx) => acc + elt * 2 ** idx, 0)
