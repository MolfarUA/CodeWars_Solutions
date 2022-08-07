57cfdf34902f6ba3d300001e


function twoSort(s) {
  return s.sort()[0].split('').join('***');
}
___________________________
twoSort = s => s.sort()[0].split('').join('***')
___________________________
const twoSort = s => [...s.sort()[0]].join('***');
___________________________
function twoSort(s) {
  s.sort();
  return s[0].split('').join('***');
}
