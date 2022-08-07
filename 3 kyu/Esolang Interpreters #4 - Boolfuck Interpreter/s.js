5861487fdb20cff3ab000030


function boolfuck(code, input = "") {
  const inputBits = []
  const outputBits = []
  for (let i = 0; i < input.length; ++i) {
    const byte = input.charCodeAt(i)
    for (let n = 0; n < 8; ++n) {
      inputBits.push((byte >> n) & 1)
    }
  }
  const jumpStack = []
  const jumps = {}
  for (let i = 0; i < code.length; ++i) {
    if (code[i] === "[") {
      jumpStack.push(i)
    } else if (code[i] === "]") {
      const j = jumpStack.pop()
      jumps[j] = i
      jumps[i] = j
    }
  }
  const cells = [0]
  let pointer = 0
  let bit = 0
  for (let i = 0; i < code.length; ++i) {
    switch (code[i]) {
      case "+": cells[pointer] ^= 1; break
      case ",": cells[pointer] = bit < inputBits.length ? inputBits[bit++] : 0; break
      case ";": outputBits.push(cells[pointer] || 0); break
      case "<": --pointer; break
      case ">": ++pointer; break
      case "[": cells[pointer] || (i = jumps[i]); break
      case "]": cells[pointer] && (i = jumps[i]); break
    }
  }
  const output = []
  for (let i = 0; i < outputBits.length; i += 8) {
    let byte = 0
    for (let n = 7; n >= 0; --n) {
      byte = (byte << 1) | (outputBits[i + n] || 0)
    }
    output.push(byte)
  }
  return String.fromCharCode(...output)
}
_____________________________
function boolfuck(code, input = "") {
  const n = code.length, M = {0:0}, O = [], J = {};
  const I = input.split('').map(c => (0x100 | c.charCodeAt(0)).toString(2).slice(1)).reverse().join('').split('');
  for (let i = 0, p = 0, S = []; i < n; ++i) // from @smile67's solution
    switch (code[i]) {
      case '[': S.push(i); break;
      case ']': p = S.pop(), J[i] = p, J[p] = i; break;
    }
  for (let i = 0, p = 0; i < n; ++i)
    switch (code[i]) {
      case '>': ++p; break;
      case '<': --p; break;
      case '+': M[p] ^= 1; break;
      case ';': O.push(M[p]|0); break;
      case ',': M[p] = I.pop()|0; break;
      case '[': if (!M[p])  i = J[i]; break;
      case ']': if (!!M[p]) i = J[i]; break;
    }
  while ((O.length & 7) != 0) O.push(0);
  O.reverse();
  const c = [], q = O.length >> 3;
  for (let j = 0; j < q; ++j) c.push(parseInt(O.slice(8*j, 8*(j + 1)).join(''), 2));
  return String.fromCharCode.apply(null, c.reverse());
}
_____________________________
class Memory {
  constructor() {
    this.leftMemory = [];
    this.rightMemory = [];
    this.ptr = 0;
  }
  
  _setMem(indx, value) {
    if(indx >= 0) {
      this.rightMemory[indx] = value;
    } else {
      this.leftMemory[Math.abs(indx) - 1] = value;
    }
  }
  
  _getMem(indx) {
    if(indx >= 0) {
      return this.rightMemory[indx];
    } else {
      return this.leftMemory[Math.abs(indx) - 1];
    }
  }

  
  flipBit() {
    if(this._getMem(this.ptr) === 1) {
      this._setMem(this.ptr, 0);
    } else {
      this._setMem(this.ptr, 1);
    }
  }
  
  setBit(val) {
    if(val !== 0 && val !== 1) {
      throw new Exception(`Tried to set bit to ${val}`);
    }
    this._setMem(this.ptr, val);
  }
  
  readBit() {
    if(this._getMem(this.ptr) === undefined) {
      return 0;
    }
    return this._getMem(this.ptr);
  }
  
  shiftLeft() {
    this.ptr--;
  }
  
  shiftRight() {
    this.ptr++;
  }
}

class Boolfuck {
  constructor(code, input='') {
    this.code = code.split('');
    this.memory = new Memory();
    
    this.inputBits = this.inputToBinary(input);
    this.outputBits = [];
  }
  
  run() {
    const backetMatch = this.getMatchingBrackets();
    
    for(let i = 0; i < this.code.length; i++) {
      switch(this.code[i]) {
        case '+':
          this.memory.flipBit();
          break;
        case '<':
          this.memory.shiftLeft();
          break;
        case '>':
          this.memory.shiftRight();
          break;
        case ',':
          this.acceptInput();
          break;
        case ';':
          this.writeOutput();
          break;
        case '[':
          if(this.memory.readBit() === 0) {
            i = backetMatch[i];
          }
          break;
        case ']':
          i = backetMatch[i] - 1;
          break;
      }
      
    }
  }
  
  acceptInput() {
    this.memory.setBit(this.inputBits.shift());
  }
  
  writeOutput() {
    this.outputBits.push(this.memory.readBit());
  }
  
  getMatchingBrackets() {
    const openingBracketStack = [];
    const backetMatch = {};
    for(let i = 0; i < this.code.length; i++) {
      if(this.code[i] === '[') {
        openingBracketStack.push(i);
      } else if(this.code[i] === ']') {
        const openingIndex = openingBracketStack.pop();
        backetMatch[i] = openingIndex;
        backetMatch[openingIndex] = i;
      }
    }
    return backetMatch;
  }
  
  inputToBinary(input) {
    return input
      .split('')
      .map(this.charToBinary)
      .map(bits => bits.reverse())
      .reduce((inputBits, arr) => inputBits.concat(arr), []);
  }
  
  charToBinary(char) {
    const bitArray = char
      .charCodeAt(0)
      .toString(2)
      .split('')
      .map(Number);
    const paddedZeros = new Array(8 - bitArray.length).fill(0);
    return paddedZeros.concat(bitArray);
  }
  
  outputToStr() {
    let output = '';
    for(let i = 0; i < this.outputBits.length; i += 8) {
      let byte = this.outputBits
        .slice(i, i + 8)
        .reverse()
        .join('');
      byte = '0'.repeat(8 - byte.length) + byte; 
      output += String.fromCharCode(parseInt(byte, 2));
    }
    return output;
  }
}

function boolfuck(code, input='') {
  const boolfucker = new Boolfuck(code, input);
  boolfucker.run();
  return boolfucker.outputToStr();
}
