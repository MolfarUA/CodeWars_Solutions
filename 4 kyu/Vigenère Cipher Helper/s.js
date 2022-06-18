function VigenèreCipher(key, alphabet) {
  function encode(direction, inStr) {
    var inChar, inIdx, outIdx, outChar, keyChar, offset;
    
    var outStr = '';
    
    // Process each character of the input string sequentially
    for (var pos = 0; pos < inStr.length; ++pos) {
      
      // Look up input character in the alphabet
      inChar = inStr.charAt(pos);
      inIdx = alphabet.indexOf(inChar);
      
      // If character isn't in alphabet, just copy it to output
      if (inIdx < 0)
        outChar = inChar;
      else {
        // Get the key character for the current position
        // and determine the shift distance
        keyChar = key.charAt(pos % key.length);
        offset = alphabet.indexOf(keyChar);
        
        // Shift the character forwards or backwards in
        // the alphabet, wrapping around if necessary
        outIdx = inIdx + direction * offset;
        if (outIdx >= alphabet.length)
          outIdx = outIdx - alphabet.length;
        else if (outIdx < 0)
          outIdx = outIdx + alphabet.length;
        
        outChar = alphabet.charAt(outIdx);
      }
      
      outStr += outChar;
    }
    
    return outStr;
  }

  // Encode by shifting characters forward in the alphabet
  this.encode = function(string) {
    return encode(1, string);
  };
  
  // Decode by shifting characters backwards in the alphabet
  this.decode = function(string) {
    return encode(-1, string);
  };
}
_____________________________________________
function VigenèreCipher(key, abc) {
  var self = this;
  var size = abc.length;
    
  this.transform = function (str, getIndex) {
    return str.split('').map(function(ch, index) {
      return abc.indexOf(ch) >= 0 ? abc[getIndex(ch, index)] : ch;
    }).join('');
  }

  this.enocodeIndex = function(ch, index) {
    return (abc.indexOf(ch) + abc.indexOf(key.charAt(index % key.length)) + size) % size
  }

  this.decodeIndex = function(ch, index) {
    return (abc.indexOf(ch) - abc.indexOf(key.charAt(index % key.length)) + size) % size
  }

  this.encode = function (str) {
    return this.transform(str, this.enocodeIndex)
  };
  this.decode = function (str) {
    return this.transform(str, this.decodeIndex)
  };
}
_____________________________________________
function VigenèreCipher(key, abc) {
  this.encode = function(str) {
    return str.split('').map(function(v, i) {
      if(abc.indexOf(v) == -1) {return v;}
      return abc[(abc.indexOf(v) + abc.indexOf(key[i % key.length])) % abc.length];
    }).join('');
  };
  this.decode = function(str) {
    return str.split('').map(function(v, i) {
      if(abc.indexOf(v) == -1) {return v;}
      var ind = abc.indexOf(v) - abc.indexOf(key[i % key.length]);
      return abc[ind < 0 ? ind + abc.length : ind];
    }).join('');
  };
}
