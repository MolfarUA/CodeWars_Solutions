function makePassword(phrase) {
  return phrase
    .split(' ')
    .map(s => s[0])
    .join('')
    .replace(/i/ig, '1')
    .replace(/o/ig, '0')
    .replace(/s/ig, '5');
}
__________________________________
const makePassword = (phrase) => phrase
    .split(" ")
    .map((el) => el[0])
    .join("")
    .replace(/[iso]/gi, (x) => ({ i: 1, s: 5, o: 0 }[x.toLowerCase()]));
__________________________________
const makePassword = $ => $.match(/\b\w/g).join('').replace(/i/ig,'1').replace(/o/ig,'0').replace(/s/ig,'5')
__________________________________
const makePassword = (phrase, d={'i':'1','o':'0','s':'5'}) => phrase.replace(/\b(\w)\w+(\W|$)/gi,(a,b,c)=> d[b.toLowerCase()]||b );
__________________________________
const makePassword = (phrase) => phrase
  .match(/\b\w/g, '$1')
  .join('')
  .replace(/o/gi, '0')
  .replace(/i/gi, '1')
  .replace(/s/gi, '5');
