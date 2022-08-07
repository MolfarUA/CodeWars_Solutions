54cf7f926b85dcc4e2000d9d



function frequencies(s) {
  const occ = s.split('').reduce((a, c) => { a[c] = ~~a[c] + 1; return a; }, {});
  return Object.keys(occ).map(k => [k, occ[k]]);
}

class Node {
  constructor(value, frequency, left, right) {
    this.value = value;
    this.frequency = frequency;
    this.left = left;
    this.right = right;
  }
}

function buildTree(freqs) {
  var nodes = freqs.map(f => new Node(f[0], f[1])).sort((a, b) => b.frequency - a.frequency);
  
  while(nodes.length !== 1) {
    let right = nodes.pop();
    let left = nodes.pop();
    
    if(left.value && right.value && left.value > right.value) {
      const l = left;
      left = right;
      right = l;
    }
    
    const node = new Node(null, left.frequency + right.frequency, left, right);
    
    const index = nodes.findIndex(n => n.frequency < node.frequency);
    if(index === -1){
      nodes.push(node);
    } else {
      nodes.splice(index, 0, node);
    }
  }
  
  return nodes[0];
}

function buildEncodingTable(tree) {
  const table = {};
  const stack = [];
  stack.push({ node: tree, path: '' });

  while(stack.length) {
    const current = stack.pop();
    
    if(current.node.value) {
      table[current.node.value] = current.path;
    } else {
      stack.push({ node: current.node.left, path: current.path + '0' });
      stack.push({ node: current.node.right, path: current.path + '1' });
    }
  }
  
  return table;
}

function decodeChar(tree, bits, index) {
  let current = tree;
  
  while(!current.value) {
    current = bits[index++] === '0' ? current.left : current.right;
  }
  
  return [current.value, index];
}

function encode(freqs,s) {
  if(freqs.length <= 1) {
    return null;
  }
  
  const tree = buildTree(freqs);
  const table = buildEncodingTable(tree);
  
  return s.split('').map(c => table[c]).join('');
}

function decode(freqs,bits) {
  if(freqs.length <= 1) {
    return null;
  }
  
  const tree = buildTree(freqs);
  
  let index = 0;
  let output = '';
  while(index < bits.length) {
    const [char, nextIndex] = decodeChar(tree, bits, index);
    output += char;
    index = nextIndex;
  }
  
  return output;
}

___________________________________________________
const frequencies = s => {
  if (s.length < 2) return null;
  const freqTable = s.split``.reduce((acc, e) => {
    acc[e] = !acc[e] ? 1 : acc[e] + 1;
    return acc;
  }, {});

  return s.split``.reduce((acc, l) => {
    if (freqTable[l]) {
      acc.push([l, freqTable[l]]);
      delete freqTable[l];
    }
    return acc;
  }, []);
}

const buildTree = freqs => {
  if (!freqs || freqs.length <= 1) return null;
  let queue = JSON.parse(JSON.stringify(freqs)).sort((a, b) => b[1] - a[1]);
  while (queue.length > 1) {
    const [right, left] = queue.splice(-2);
    const internalNode = [ `${left[0]}${right[0]}`, left[1] + right[1], left, right];
    queue.push(internalNode);
    queue = queue.sort((a, b) => b[1] - a[1]);
  }
  return queue[0];
}

const encode = (freqs, s) => {
  const findBit = (bitTree, symbol) => {
    const [treeSymbol,, bit, left = null, right = null] = [...bitTree];
    if (!left && !right) 
      return (treeSymbol === symbol) ? bit : null;
    const leftBitString = findBit(left, symbol);
    const rightBitString = findBit(right, symbol);
    return leftBitString ? leftBitString : rightBitString;
  }

  const encodeTree = (tree, bit = '') => {
    const [rootSymbol, freq, left = null, right = null] = [...tree];
    return !left && !right ? [rootSymbol, freq, bit] :
      [rootSymbol, freq, bit, encodeTree(left, `${bit}0`), encodeTree(right, `${bit}1`)];
  }

  if (!freqs || freqs.length <= 1) return null;
  const bitTree = encodeTree(buildTree(freqs));
  return s.split``
    .reduce((acc, symbol) => acc + findBit(bitTree, symbol), '');
}

const decode = (freqs,bits) => {
  if (!freqs || freqs.length < 2) return null;
  const tree = buildTree(freqs);
  let i = 0;
  let result = '';
  let tempRoot = tree;
  while (i <= bits.length) {
    const [symbol,, left = null, right = null] = tempRoot;
    if (!left && !right) {
      result += symbol;
      tempRoot = tree;
    } else {
      if (bits[i] == 0) tempRoot = left;
      else tempRoot = right;
      i++;
    }
  }
  return result;
}

___________________________________________________
function frequencies(input) {
    var frequesncies = input.split('').reduce((memo, s) => { memo[s] = (memo[s] || 0) + 1; return memo; }, {});        
    return Object.keys(frequesncies).map(key => [key, frequesncies[key]]);
}

function createTree(freqs) {
    freqs = freqs.map(item => { return {type: 'leaf', value: item[1], letter: item[0]}; });

    while (freqs.length > 1) {
        freqs.sort((a, b) => { if (a.value < b.value) return 1; if (b.value < a.value) return -1; return 0; });
        
        var left = freqs[freqs.length - 1],
            right = freqs[freqs.length - 2];
            
        freqs = freqs.slice(0, freqs.length - 2);
        
        var node = {
            type: 'node',
            value: left.value + right.value,
            
            left: left,
            right: right            
        }
        
        freqs.unshift(node);
    }        
    
    return freqs[0];
}

function getLettersData(node, acc, prefix) {
    if (node.type == 'node') {
        getLettersData(node.left, acc, prefix + '0');
        getLettersData(node.right, acc, prefix + '1');
    }
    
    if (node.type == 'leaf') {
        acc[node.letter] = prefix;
    }
    
    return acc;
}

function encode(freqs, s) {
    if (freqs.length < 2) return null;
    
    var rootNode = createTree(freqs);
    var lettersData = getLettersData(rootNode, {}, '');
    
    var result = s.split('').map(letter => lettersData[letter]).join('');
    
    return result;
}

function decode(freqs, bits) {
    if (freqs.length < 2) return null;
    
    var rootNode = createTree(freqs);
    var lettersData = getLettersData(rootNode, {}, '');
    
    var lettersByCodes = Object.keys(lettersData).reduce((memo, letter) => { memo[lettersData[letter]] = letter; return memo; }, {});

    var output = '';
    
    while (bits.length) {
        var code = Object
            .keys(lettersByCodes)
            .filter(code => new RegExp('^' + code).test(bits))
            .reduce((longestCode, code) => code.length > longestCode ? code : longestCode, '');
            
        output += lettersByCodes[code];
        
        bits = bits.replace(new RegExp('^' + code), '');
    }
    
    return output;
}

___________________________________________________
function frequencies(s) {
  const map = new Map();
  for(let ch of s) {
    let count = map.get(ch) || 0;
    map.set(ch, ++count);
  };
  return [...map];
}

// takes: [ [String,Int] ], String; returns: String (with "0" and "1")
function encode(freqs,s) {
  if(freqs.length < 2) return null;
  const map = new Tree(freqs).toMap();
  return s.split('').map(symbol => map.get(symbol)).join('');
}

// takes [ [String, Int] ], String (with "0" and "1"); returns: String
function decode(freqs,bits) {
  if(freqs.length < 2) return null;
  const root = new Tree(freqs);
  let result = '';
  let activeNode = root;
  for(let bit of bits) {
    if(bit == '0') {
      result += activeNode.left;
      activeNode = root;
    } else {
      activeNode = activeNode.right;
      if(!activeNode.right.left) {
        result += activeNode.left;
        activeNode = root;
      }
    }
  };
  return result;
}

class Node {
  constructor() {
  }
  extend(value) {
    this.left = value;
    this.right = new Node();
    return this.right;
  }
}

class Tree extends Node {
  constructor (freqs) {
    super()
    freqs = freqs.sort(([s1, c1], [s2, c2]) => c2 - c1);
    let currentNode = this;
    freqs.forEach(([symbol, count]) => {
      currentNode = currentNode.extend(symbol)
    })
  }
  toMap() {
    const map = new Map();
    for(let node = this, code = ''; node.right; node = node.right) {
      map.set(node.left, node.right.left ? code + '0' : code);
      code += '1';
    }
    return map;
  }
}

___________________________________________________
const frequencies=s=>s.split``.reduce((f,c)=>((i=f.findIndex(p=>p[0]==c))>-1?f[i][1]++:f.push([c,1]),f),[])

function encode(freqs,s) {
  if (freqs.length<2) return null
  let codes = {}
  freqs.sort((a,b)=>b[1]-a[1]).forEach((f,i,a)=>codes[f[0]]='1'.repeat(i)+(i<a.length-1?'0':''))
  return s.split``.map(c=>codes[c]).join``
}

function decode(freqs,bits) {
  if (freqs.sort((a,b)=>b[1]-a[1]).length<2) return null
  return bits==''?'':bits.match(RegExp(`(1{0,${freqs.length-2}}0)|(1{${freqs.length-1}})`,'g')).map(b=>freqs[eval(b.split``.join`+`)][0]).join``
}
