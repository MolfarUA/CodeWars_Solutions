function numIndex(n) {
  if(n<10) return n-1;
  var c = 0;
  for(let i=1;;i++) {
    c += i*9*Math.pow(10,i-1);
    if(n<Math.pow(10,i+1)) return c+(i+1)*(n-Math.pow(10,i));
  }
}

function findPosition(str){
  if(/^0+$/.test(str))return numIndex(+(1+str))+1;
  for(let l=1; l<=str.length; l++) {
    let poss = [];
    for(let i=0; i<l; i++) {
      let sdt = str.slice(0,l-i), end = str.slice(l-i,l);
      for(let c of (+end?[end+sdt,(end-1)+sdt]:[end+sdt])) {
        if(c[0]==='0') continue;
        let ds = c, n = +c;
        while(ds.length<str.length+l) ds += (++n);
        if(ds.indexOf(str)!==-1) poss.push(numIndex(+c)+ds.indexOf(str)); 
      }
    }
    if(poss.length) return Math.min(...poss);
  }
}
___________________________________________________
function findPositionWholeNum(num_str) {
    var len = num_str.length
    var num = parseInt(num_str)
    if (num <= 10) {
        return num - 1
    }
    
    var suffix_str = num_str.substring(1)
    var suffix = parseInt(suffix_str)
    var result = 0
    if (suffix === 0) {
        var less_str = (num - 1).toString()
        result = findPositionWholeNum(less_str) + less_str.length
    }
    else {
        result = findPositionWholeNum((num - suffix).toString()) + suffix * len
    }
    return result
}

function isAll9(num_str) {
    for (var i = 0; i < num_str.length; ++i) {
        if (num_str.charAt(i) !== '9') return false
    }
    return true
}

function isPow10(num_str) {
    if (num_str.charAt(0) != '1') return false
    for (var i = 1; i < num_str.length; ++i) {
        if (num_str.charAt(i) !== '0') return false
    }
    return true
}

function guessNum(num_str, len, end) {
    if (len === end) return parseInt(num_str.substring(0, len))
    
    var known_str = num_str.substring(0, end)
    var next_str = num_str.substr(end, len - end)
    if (isAll9(known_str)) {
        if (isPow10(next_str)) {
            next_str += '0'
        }
        next_str = (parseInt(next_str) - 1).toString()
    }
    
    return parseInt(next_str + known_str)
}

function verifyNum(num_str, len, end, num) {
    var i = - (len - end)
    var j = 0
    var pat_str = num.toString()
    while (i < num_str.length) {
        if (i >= 0 && num_str.charAt(i) !== pat_str.charAt(j)) return false
        i++
        j++
        if (j >= pat_str.length) {
            j = 0
            num++
            pat_str = num.toString()
        }
    }
    
    return true
}

function findPosition(num_str) {
    // enumerate each possible configuration
    // each configuration means the first number that appears in num
    // it can be partial, but will never be longer than num since that would guarantee a higher position than just num whole number
    // 
    // for each configuration, check if it is valid by looking at next number that appears
    // need to guess digits from the next number, if the first one is partial
    // if it is valid, return findPositionWholeNum(first number), plus / minus the partial offset.
    
    var result = -1
    for (var len = 1; len <= num_str.length; ++len) {
        for (var end = 1; end <= len; ++end) {
            var num = guessNum(num_str, len, end)
            if (verifyNum(num_str, len, end, num)) {
                var new_result = findPositionWholeNum(num.toString()) + (len - end)
                if (result === -1 || new_result < result) {
                    result = new_result
                }
            }
        }
        if (result !== -1) return result
    }
    
    if (num_str.charAt(0) === '0') {
        result = findPositionWholeNum('1' + num_str) + 1
    }
    
    return result
}
___________________________________________________
findPosition = d => {
  for(var f=[],c=1;c<=d.length;c++)for(var b=0;b<c;b++)0<=(e=k(d,b,c))&&f.push(e);
  return f.length?Math.min.apply(Math,f):l(+("1"+d))+1
}

k = (d, f, c) => {
    if (f + c <= d.length) var b = +d.substr(f, c);
    else {
        b = d.substr(f);
        var e = d.substr(0, f),
            g = b.length + e.length - c,
            h = [...e.substr(g)]
        h.every(b => "9" == b) ? (b += h.map(_=> "0").join``, b = +b) : (b += e.substr(g), b = +b, b++);
        if (String(b - 1).substr(c - e.length) != e) return -1
    }
    c = [];
    e = 0;
    f && (g = String(b - 1), c.push(g.substr(g.length - f)), e += f);
    for (g = b; e < d.length;) h = String(g), h.length + e > d.length ? (c.push(h.substr(0, d.length - e)), e += d.length - e) : (c.push(h), e += h.length),g++;
    return c.join`` == d ? l(b) - f : -1
}

l = d => {
    for (var f = 0, c = 1, b = 10; d > b;) f += c * (b - b / 10), b *= 10, c++;
    return f + c * (d - b / 10)
}
