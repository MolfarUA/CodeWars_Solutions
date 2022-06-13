function convert(input, source, target) {
  var inBase = source.length, len = input.length;
  var value = input.split('')
    .reduce(function(p,v,i){return p+source.indexOf(v)*Math.pow(inBase,len-i-1)},0);
  return toBase(value,target);
}

function toBase(value, target){
  var base = target.length;
  if(value<base) return ''+target.charAt(value);
  return toBase(Math.floor(value/base),target) + target.charAt(value%base);
}
__________________________________________
function convert(input, source, target) {
  let s=0;  let str='';
  for (let i=0; i<input.length; i++) {
    s=s*source.length+source.indexOf(input[i]);
  }
  while (s>0) {
    str=target[s%target.length]+str;
    s=Math.floor(s/target.length);
  }  
  return str ? str : target[0];
}
__________________________________________
function convert(input, source, target) {
  /* both bases the same, no converting needed */
  if (source === target) {
    return input;  // exit 1/3
  }
  
  var srcLen = source.length;
  var tgtLen = target.length;
  
  /* bases of the same length, only simple substitution needed */
  if (srcLen === tgtLen) {
    var output = [];
    for (var i in input) {
      var char = input.charAt(i);
      var srcIndex = source.indexOf(char);
      output.push(target.charAt(srcIndex));
    }
    return output.join("");  // exit 2/3
  }
  
  /* else convert to base of different length */
  var value = 0;
  for (var i = 0, len = input.length; i < len; i++) {
    var char = input.charAt(len - i - 1);
    var srcIndex = source.indexOf(char);
    value += Math.pow(srcLen, i) * srcIndex;
  }
  
  var tgtValues = [];
  do {
    var tgtIndex = value % tgtLen;
    value = Math.floor(value / tgtLen);
    tgtValues.push(target.charAt(tgtIndex));
  } while (value > 0);
  
  return tgtValues.reverse().join("");  // exit 3/3
  
}
__________________________________________
function convert(input, source, target) {
  var t = '', n = input.split('').reduce((n,v)=>n * source.length + source.indexOf(v), 0);
  do { t = target[n % target.length] + t;
       n = Math.floor(n / target.length); 
     } while (n > 0)
  return t;
}
__________________________________________
function convert(input, source, target) {
    // convert source to number (decmal)
    if (input === source[0]) {
        return target[0];
    }
    let mul = 1;
    let number = 0;
    for (let i = input.length - 1; i >= 0; i--) {
        let ch = input[i];
        let ndx = source.indexOf(ch);
        number += ndx * mul;
        mul *= source.length;
    }

    let result = "";
    let ndigits = target.length;
    while (number > 0) {
        let rest = number % ndigits;
        result = target[rest] + result;
        number = Math.floor(number / ndigits);
    }

    return result;
}
__________________________________________
function convert(input, source, target) {
  const convertFrom = (inp, s) =>
    [...inp].reduce((acc, val) => s.indexOf(val) + acc * s.length, 0);
  const convertTo = (inp, t) => {
    const res = [];
    if (inp == 0) return t[0];
    while (inp > 0) {
      res.unshift(t[inp % t.length]);
      inp = Math.floor(inp / t.length);
    }
    return res.join('');
  };
  
  return convertTo(convertFrom(input, source), target);
}
