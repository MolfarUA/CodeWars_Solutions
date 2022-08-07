58c5577d61aefcf3ff000081


function* rails(rn, ln) {
    for (var rc = 0; rc < rn; ++rc) {
        var rv = rc, rd = rc;
        while (rv < ln) {
            yield rv;
            rv += 2 * (rn - 1 - (rn == rd + 1 ? 0 : rd));
            rd = rn - 1 - rd;
        }
    }
}

function encodeRailFenceCipher(s, numberRails) {
    return Array.from(rails(numberRails, s.length)).map(function(i) {
        return s[i];
    }).join("");
}

function decodeRailFenceCipher(s, numberRails) {
    var r = [];
    for (var [i, k] of Array.from(rails(numberRails, s.length)).entries()) {
        r[k] = s[i];
    }
    return r.join("");
}
_____________________________
function encodeRailFenceCipher(string, numberRails) {
  var s = '', count = 2 * numberRails - 3;
  for(var i = 0; i < numberRails; i++) {
    var a = count - i * 2,
        b = i * 2 - 1;
    var iterator = [a < 0 ? 0 : a + 1, b < 0 ? 0 : b + 1]
    for(var j = i, k = -1; j < string.length; j += iterator[k%2] ? iterator[k%2] : iterator[(k+1)%2]) {
      s+= string[j];
      k++;
    }
  }
  return s;
}

function decodeRailFenceCipher(string, numberRails) {
  var s = [], count = 2 * numberRails - 3;
  var globalIndex = 0;
  for(var i = 0; i < numberRails; i++) {
    var a = count - i * 2,
        b = i * 2 - 1;
    var iterator = [a < 0 ? 0 : a + 1, b < 0 ? 0 : b + 1]
    for(var j = i, k = -1; j < string.length; j += iterator[k%2] ? iterator[k%2] : iterator[(k+1)%2]) {
      s[j] = string[globalIndex];
      globalIndex++;
      k++;
    }
  }
  return s.join('');
}
_____________________________
const encodeRailFenceCipher = (source, rail) => coder(source, rail,
    (res, cur, src, ind) => (res[ind++] = src[cur]) && ind
);

const decodeRailFenceCipher = (source, rail) => coder(source, rail,
    (res, cur, src, ind) => (res[cur] = src[ind++]) && ind
);

const coder = function(source, rail, callback) {
    if (!source.length) return source;
    rail = Math.max(rail, 1);
    const res = [...source],
        len = source.length,
        max = (rail - 1) * 2;
    let index = 0;
    for (
        let seed = [max, 0]; seed[0] >= 0 && !seed.every(cur => !cur); seed = [seed[0] - 2, seed[1] + 2]
    ) {
        const clone = [
            seed[0] ? seed[0] : seed[1],
            seed[1] ? seed[1] : seed[0]
        ];
        let cur = (max - seed[0]) / 2;
        clone.index = 0;
        while (cur < len) {
            index = callback(res, cur, source, index);
            cur += clone[clone.index];
            clone.index = clone.index ? 0 : 1;
        }
    }
    return res.join('');
};
_____________________________
function nextRailIndex(currentRailIndex, numberOfRails) {
        if (currentRailIndex === numberOfRails) {
            cursorForward = false; 
        } else if (currentRailIndex === 1) {
            cursorForward = true; 
        }
        cursorForward ? currentRailIndex++ : currentRailIndex-- ;
        return currentRailIndex;
    }

    function fillRailsWithStringChars(string, numberOfRails) {
        let currentRailIndex = 1, rails = {}, cursorForward = true ;
        string.split('').forEach((char) => {
            rails[currentRailIndex] instanceof Array ? rails[currentRailIndex].push(char) :  rails[currentRailIndex] = [char];
            currentRailIndex = nextRailIndex(currentRailIndex, numberOfRails);
        });
        return rails;
    }

    function encodeRailFenceCipher(string, numberOfRails) {
        const rails = fillRailsWithStringChars(string, numberOfRails);
        return Object.keys(rails).map(key => rails[key].join('')).join('');
    }

    function fillRailWithDecodeChars (index, rails, string) {
        let i = 1, substringStartIndex = 0, substringEndIndex = 0;
        while (i <= index) {
            substringStartIndex = substringEndIndex;
            substringEndIndex += rails[i].length;
            i++;
        }
        return string.substring(substringStartIndex, substringEndIndex).split('');
    }

    function getDecodedString (rails, string, numberOfRails) {
        let stringTmp = '';
        let currentRailIndex = 1;
        for (let i=0; i<string.length; i++) {
            stringTmp += rails[currentRailIndex].shift();
            currentRailIndex = nextRailIndex(currentRailIndex, numberOfRails);
        }
        return stringTmp;
    }

    function decodeRailFenceCipher(string, numberOfRails) {
        const dummyRailStructure = fillRailsWithStringChars(string, numberOfRails);
        const railsWithDecodeChars = {};
        Object.keys(dummyRailStructure)
            .map(key => fillRailWithDecodeChars(key, dummyRailStructure, string))
            .forEach((rail, index) => { railsWithDecodeChars[index+1] = rail });
        return getDecodedString(railsWithDecodeChars, string, numberOfRails);
    }
