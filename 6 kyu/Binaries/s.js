function code(strng) {
    return strng.split('').map(function (n) { 
      var str = '1' + Number(n).toString(2);
      while (n>>=1 != 0) str = '0' + str;
      return str;
    }).join('');
    
}
function decode(str) {
    var regex, matches, strng;
    regex = /0*1/g;
    strng = '';
    while (matches = regex.exec(str)) {
      strng += parseInt(str.substr(regex.lastIndex, matches[0].length), 2);
      regex.lastIndex += matches[0].length;
    }
    return strng;
}
__________________________
const ENC = ['10','11','0110','0111','001100','001101','001110','001111','00011000','00011001']

function code(strng) {
  return [...strng].map(c => ENC[c]).join('')
}
function decode(str) {
    pattern = new RegExp(ENC.join('|'), 'g')
    return str.replace(pattern, m => ENC.indexOf(m))
}
__________________________
const code = str =>
  [ ...str ].map(Number).reduce((a, b) => 
    a + '0'.repeat(Math.log2(b || 1) | 0) + '1' + b.toString(2)
  , '');

const decode = str => {

  if (!str) return '';
  
  const [_, a, b] = str.match(/^(0*1)(.*)$/);
  
  return parseInt(b.slice(0, a.length), 2) 
       + decode(b.slice(a.length));
  
};
__________________________
const [code, decode] = (() => {
  const CODES = ['10', '11', '0110', '0111', '001100', '001101', '001110', '001111', '00011000', '00011001'];
  const codelength = str => (str || '').match(/^0*/)[0].length * 2 + 2;
  return [
    str => [...str].map(d => CODES[d]).join(''),
    str => {
      let result = '';
      while (str.length) {
        let code = str.slice(0, codelength(str));
        result += CODES.indexOf(code);
        str = str.slice(codelength(str));
      }
      return result;
    }
  ];
})();
