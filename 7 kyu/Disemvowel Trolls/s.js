function disemvowel(str) {
  return str.replace(/[aeiou]/gi, '');
}
______________________________
disemvowel = str => str.replace(/[aeiou]/gi,'');
______________________________
function disemvowel(str) {
  return (str || "").replace(/[aeiou]/gi, "");
}
______________________________
function disemvowel(str) {
  var vowels = ['a', 'e', 'i', 'o', 'u'];
  
  return str.split('').filter(function(el) {
    return vowels.indexOf(el.toLowerCase()) == -1;
  }).join('');
}
______________________________
const vowels = 'aeiou';

function disemvowel(str) {
  return str
    .split('')
    .filter(letter => !vowels.includes(letter.toLowerCase()))
    .join('');
}
