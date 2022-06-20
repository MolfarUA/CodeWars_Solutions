57e8f757085f7c7d6300009a


function planeSeat(a){
  const number = parseInt(a);
  const letter = a[a.length - 1];
  if (number > 60 || letter == 'I' || letter == 'J') return 'No Seat!!';
  return `${number > 20 ? number > 40 ? 'Back-' : 'Middle-' : 'Front-'}${letter > 'C' ? letter > 'F' ? 'Right' : 'Middle' : 'Left'}`;
}
_______________________________
function planeSeat(a){
  let [number, letter] = [a.match(/\d+/)[0], a.match(/[a-z]/i)[0]]
  const position = [
    +number <= 20 ? 'Front-' : +number <= 40 ? 'Middle-' : +number <= 60 ? 'Back-' : '', 
    /[A-C]/.test(letter) ? 'Left' : /[D-F]/.test(letter) ? 'Middle' : /[GHK]/.test(letter) ? 'Right' : ''
  ].join('')
  return /^(Front|Middle|Back)-(Left|Middle|Right)$/.test(position) ? position : 'No Seat!!'
}
_______________________________
function planeSeat(a){
  let res = []
  a = a.match(/\d+|\D/g)
  if (+a[0] <= 20) {
    res.push('Front')
  } else if (+a[0] <= 40) {
    res.push('Middle')
  } else if (+a[0] <= 60) {
    res.push('Back')
  } else return 'No Seat!!'
  
  if (/[A-C]/g.test(a[1])) {
    res.push('Left')
  } else if (/[D-F]/g.test(a[1])) {
    res.push('Middle')
  } else if ('GHK'.includes(a[1])) {
    res.push('Right')
  } else return 'No Seat!!'
  return res.join('-')
}
