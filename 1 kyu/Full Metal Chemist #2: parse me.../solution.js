5a529cced8e145207e000010


// Number:        1      2      3...
const RADICALS    = ['meth', 'eth', 'prop', 'but',   'pent',  'hex',  'hept',  'oct',  'non',  'dec',  'undec',  'dodec',  'tridec',  'tetradec',  'pentadec',  'hexadec',  'heptadec',  'octadec',  'nonadec']
const MULTIPLIERS = [        'di',  'tri',  'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca', 'octadeca', 'nonadeca']

const SUFFIXES    = [         'ol',      'al', 'one', 'oic acid', 'carboxylic acid',                'oate',               'ether', 'amide', 'amine', 'imine', 'benzene', 'thiol',    'phosphine', 'arsine']
const PREFIXES    = ['cyclo', 'hydroxy',       'oxo',             'carboxy',         'oxycarbonyl', 'oyloxy', 'formyl', 'oxy',   'amido', 'amino', 'imino', 'phenyl',  'mercapto', 'phosphino', 'arsino', 'fluoro', 'chloro', 'bromo', 'iodo']
const RADICAL_NUMBERS = RADICALS.reduce((acc, value, index) => {
    acc[value] = index + 1;
    return acc;
  }, {});
const MULTIPLIERS_NUMBERS = MULTIPLIERS.reduce((acc, value, index) => {
  acc[value] = index + 2;
  return acc;
  }, {});

const subBranchesSuffixes = ['yl', 'en', 'yn', 'an', 'hydroxy', 'mercapto', 'imino', 'fluoro', 'chloro', 'bromo', 'iodo', 'oxo', 
              'formyl', 'carboxy', 'amido', 'amino', 'phosphino', 'arsino', 'oxy', 'oxycarbonyl', 
              'oyloxy', 'phenyl']
const directBranches = ['fluoro', 'chloro', 'bromo', 'iodo', 'hydroxy', 'mercapto', 'imino',  'oxo', 
              'formyl', 'carboxy', 'amido']
const alksBranches = ['yl', 'oxy', 'oxycarbonyl', 'oyloxy']
// Note that alkanes, alkenes alkynes, and akyles aren't present in these lists

function parse(name) {
  const radicalsTrie = buildReverseTrie(RADICALS);
  const suffixesTrie = buildReverseTrie([...SUFFIXES, 'ane', 'ene', 'yne', 'yl', 'en', 'an', 'yn']);
  const prefixesTrie = buildReverseTrie(PREFIXES);
  const multipliersTrie = buildReverseTrie(MULTIPLIERS);
  const symbols = {fluoro: ['F'], chloro: ['Cl'], bromo: ['Br'], iodo: ['I'], hydroxy: ['O', 'H'], mercapto: ['S', 'H'], 
          imino: ['N', 'H'], oxo: ['O'], formyl: ['O', 'C', 'H'], carboxy: ['O', 'O', 'C', 'H'], amido: ['O', 'N', 'H', 'H'],
          amine: ['N'], amino: ['N', 'H', 'H'], phosphine: ['P'], phosphino: ['P', 'H', 'H'], arsine: ['As'], arsino: ['As', 'H', 'H'],
          oxy: ['O'], oxycarbonyl: ['C', 'O', 'O'], oyloxy: ['O', 'O'], ether: ['O'], phenyl: ['C','C','C','C','C','C','H','H','H','H','H'] }
  const bondsConsumed = { fluoro: 1, chloro: 1, bromo: 1, iodo: 1, hydroxy: 1, mercapto: 1, imino: 2, oxo: 2, 
              formyl: 1, carboxy: 1, amido: 3, amino: 1, phosphino: 1, arsino: 1, oxy: 1, oxycarbonyl: 1,
              oyloxy: 1, phenyl: 1}
  const alksSubBranchBondsConsumed = {yl: 1, oxy: 1, oyloxy: 3, oxycarbonyl: 1}

  let parts = breakInParts(name);
  
  let base = getBase(parts);
  // console.log('BASE:', base)

  processBranches(parts, base, 0);

  return base;

  function processBranches(parts, base, index){
    while(parts.length > 0){
      if(!subBranchesSuffixes.includes(parts[0].part)){
        console.log("ERROR not identified:", parts[0])
        break;
      }
      if(directBranches.includes[parts[0].part]){
        processDirectBranch(parts, base);
        continue;
      }
      processBranch(parts, base, index);
    }
  }

  function processBranch(parts, base, index){
    let baseBranch = {};
    let mainPrefix =  parts.shift().part
    if(alksBranches.includes(mainPrefix)){
      baseBranch = processAlk(parts);
      baseBranch.H -= alksSubBranchBondsConsumed[mainPrefix];
    }
    
    if(symbols[mainPrefix]) {
      symbols[mainPrefix].map(symbol => {
        if(!baseBranch[symbol]){
          baseBranch[symbol] = 0;
        }
        baseBranch[symbol]++;
      })
    }
    if(parts.length > 0 && parts[0].type === 6){
      parts.shift();
      let subBranchParts = extractBrackets(parts)
      processBranches(subBranchParts, baseBranch, index + 1);
    }
    let multiplier = 1;
    if(parts.length > 0){
      if(parts[0].type === 2){
        next = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[next.part];
      }
      if(parts.length > 0 && parts[0].type === 5){
        parts.shift();
      }
    }
    Object.keys(baseBranch).map(key => {
      if(!base[key]) {
        base[key] = 0;
      }
      base[key] += baseBranch[key] * multiplier;
    })

    let branchBondsConsumed = 1;
    if(bondsConsumed[mainPrefix]){
      branchBondsConsumed = bondsConsumed[mainPrefix];
    }

    base.H -= multiplier * branchBondsConsumed;

    return multiplier;
  }

  function processDirectBranch(parts, base) {
    let prefix = parts.shift().part;
    let multiplier = 1;
    if(parts.length > 0){
      if(parts[0].type === 2){
        next = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[next.part];
      }
      if(parts[0].type === 5){
        parts.shift();
      }
    }
    symbols[prefix].map(symbol => {
      if(!base[symbol]){
        base[symbol] = 0;
      }
      base[symbol] += multiplier;
    })
    base.H -= multiplier * bondsConsumed[prefix];
  }

  function processAlk(parts){
    next = parts[0];
    let type = 'ane';

    while(parts[0].type === 4){
      next = parts.shift()
      type = next.part + 'e';
    }
    parts.unshift({type: 4, part: type});

    return getBase(parts);
  }

  function extractBrackets(parts) {
  let subBranchParts = [];
  let open = 0;
  while(parts.length > 0){
    let next = parts.shift();
    if(next.type === 7 && open === 0){
      break;
    }
    subBranchParts.push(next);
    if(next.type === 7){
      open--;
    }
    if(next.type === 6){
      open++;
    }
  }
  return subBranchParts;
  }

  function getBase(parts){
  let base = {C:0, H:0};
  let mainSuffix = parts.shift();
  if(mainSuffix.type !== 4){
    throw new Error("NOT VALID! ------- " + name + " ---------");
  }
  let multis = 1;
  let subBase = {};
  switch(mainSuffix.part){
    case 'ane':
    case 'an':
      radical = parts.shift();
      num = RADICAL_NUMBERS[radical.part];
      base.C = num;
      base.H = num * 2 + 2;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
        parts.shift();
        base.H -= 2;
      }
      break;
    case 'ene':
    case 'en':
      next = parts.shift();
      if(next.type === 2){
        multis = MULTIPLIERS_NUMBERS[next.part];
        next = parts.shift();
      }
      if(next.type === 5){
        next = parts.shift();
      }
      num = RADICAL_NUMBERS[next.part];
      base.C = num;
      base.H = num * 2 + 2 - multis * 2;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
      parts.shift();
      base.H -= 2;
      }
      break;
    case 'yne':
    case 'yn':
      next = parts.shift();
      if(next.type === 2){
        multis = MULTIPLIERS_NUMBERS[next.part];
        next = parts.shift();
      }
      if(next.type === 5){
        next = parts.shift();
      }
      if(next.type === 4){
        next = parts.shift();
        let doubles = 1;
        if(next.type === 2){
          doubles = MULTIPLIERS_NUMBERS[next.part];
          next = parts.shift();
        }
        if(next.type === 5){
          next = parts.shift();
        }
        base.H -= doubles * 2;
      }
      num = RADICAL_NUMBERS[next.part];
      base.C = num;
      base.H += num * 2 + 2 - multis * 4;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
      parts.shift();
      base.H -= 2;
      }
      break;
    case 'ol':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      break;
    case 'thiol':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.S = subBase.multis;
      break;
    case 'imine':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.N = subBase.multis;
      base.H -= subBase.multis;
      break;
    case 'one':
    case 'al':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      base.H -= subBase.multis * 2;
      break;
    case 'oic acid':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = 2 * subBase.multis;
      base.H -= 2 * subBase.multis;
      break;
    case 'carboxylic acid':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = 2 * subBase.multis;
      base.C += subBase.multis;
      break;
    case 'amide':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      base.N = subBase.multis;
      base.H -= subBase.multis;
      break;
    case 'oate':
      let multiPart;
      let multiplier = 1;
      if(parts[0].type === 2){
        multiPart = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[multiPart.part];
        parts.push(multiPart);
      }
      if(parts[0].type === 5){
        parts.shift();
      }
      base = {O: 2 * multiplier}
      let aux = getBase(parts);
      aux.H -= 2 * multiplier;
      Object.keys(aux).map(key =>{
        if(!base[key]){
          base[key] = 0;
        }
        base[key] += aux[key];
      })
      break;
    case 'benzene':
      base = {C: 6, H: 6}
      break;
    case 'amine':
    case 'phosphine':
    case 'arsine':
    case 'ether':
      if(parts.length === 0 || parts[0].part === 'yl' ||  parts[0].part === 'phenyl'){
        base = {H:3}
        if(mainSuffix.part === 'ether'){
          base.H--;
        }
        symbols[mainSuffix.part].map(symbol => {
          if(!base[symbol]){
            base[symbol] = 0;
          }
          base[symbol] += 1;
        })
      }
      else {
        let subBranch = [];
        let suffixPart = {C: 0, H: 2};
        suffixPart[symbols[mainSuffix.part]] = 1
        if(parts.length > 0 && parts[0].type === 6) {
          parts.shift();
          subBranch = extractBrackets(parts);
          while(subBranch.length > 0 && subBranchesSuffixes.includes(subBranch[0].part)){
            processBranch(subBranch, suffixPart, 0);
          }
        }
        let next = parts[0];
        let multiplier = 1;
        if(next.type === 2){
          multiplier = MULTIPLIERS_NUMBERS[next.part];
          next = parts.shift();
          next = parts[0];
        }
        if(next.type === 5){
          next = parts.shift();
        }
        
        base = getSubBase(parts).base

        Object.keys(suffixPart).map(key =>{
          if(!base[key]){
            base[key] = 0;
          }
          base[key] += suffixPart[key] * multiplier;
        })
        base.H -= multiplier;
      }
      break;
  }
  return base;
  }

  function getSubBase(parts) {
  let next = parts[0];
  let multis = 1;
  if(next.type === 2){
    multis = MULTIPLIERS_NUMBERS[next.part];
    next = parts.shift();
    next = parts[0];
  }
  if(next.type === 5){
    next = parts.shift();
  }
  if(next.type === 1){
    parts.unshift({type: 4, part: 'an'});
  }
  let base = getBase(parts);
  return {base: base, multis:multis}
  }

  function breakInParts(name) {
  let parts = [];
  while(name !== ''){
    // console.log(name)
    if(name[name.length - 1] === '-'){
      name = name.substring(0, name.length - 1);
      let index = name.lastIndexOf('-');
      let whiteSpace = name.lastIndexOf(' ');
      if(whiteSpace > index){
        index = whiteSpace;
      }
      let positions = name.substring(index + 1);
      let num = positions.split(',').length - 2;
      if(num > 0){
        let prev = parts[parts.length - 1];
        if(prev.type !== 2){
          let multi = MULTIPLIERS[num];
          prev.part = prev.part.split(multi)[1];
          parts.push({type: 2, part: multi})
        }
      }
      parts.push({type: 5, part: positions});
      name = name.substring(0, index);
      continue;
    }
    if(name[name.length - 1] === ']'){
      name = name.substring(0, name.length - 1);
      let index = getParentBracket(name);
      parts.push({type: 6, part: ']'})
      parts.push(...breakInParts(name.substring(index + 1)));
      parts.push({type: 7, part: '['})
      name = name.substring(0, index);
      continue;
    }
    let radical = getFromReverseTrie(name, radicalsTrie);
    if(radical !== ''){
      parts.push({type: 1, part: radical});
      name = name.substring(0, name.length - radical.length);
      continue;
    }
    let multi = getFromReverseTrie(name, multipliersTrie);
    if(multi !== ''){
      parts.push({type: 2, part: multi});
      name = name.substring(0, name.length - multi.length);
      continue;
    }
    let prefix = getFromReverseTrie(name, prefixesTrie);
    if(prefix !== ''){
      parts.push({type: 3, part: prefix});
      name = name.substring(0, name.length - prefix.length);
      continue;
    }
    let suffix = getFromReverseTrie(name, suffixesTrie);
    if(suffix !== ''){
      parts.push({type: 4, part: suffix});
      name = name.substring(0, name.length - suffix.length);
      continue;
    }
    if(name[name.length - 1] === ' '){
      name = name.substring(0, name.length - 1);
      continue;
    }
    if(name.length >= 2 && name[name.length - 2] === 'i' && name[name.length - 1] === 'o'){
      name = name.substring(0, name.length - 2);
      parts[parts.length - 1].part = parts[parts.length - 1].part.substring(2);
      
      parts.push({type: 3, part: 'iodo'})
      continue;
    }
    if(name.length >= 3 && name[name.length - 3] === 'a' && name[name.length - 2] === 'm' && name[name.length - 1] === 'i'){
      name = name.substring(0, name.length - 3);
      parts[parts.length - 1].part = parts[parts.length - 1].part.substring(2);
      parts.push({type: 3, part: 'amido'})
      continue;
    }
    console.log(name, "!")
    break;
    }
  return parts;
  }

  function getParentBracket(name){
    let open = 0;
    for(let i = name.length - 1; i >= 0; i--){
      if(name[i] === '[' && open === 0){
        return i;
      }
      if(name[i] === '[') open--;
      if(name[i] === ']') open++;
    }
  }
}  

function getFromReverseTrie(name, trie){
  let i = name.length -1;
  let lastFound = '';
  for(; i >= 0; i--){
    let letter = name[i];
    if (trie[letter]){
      trie = trie[letter];
      if(trie['-']){
        lastFound = name.substring(i);
      }
    }
    else{
      break;
    }
   }
  return lastFound;
}

function buildReverseTrie(dict){
  let trie = {};
  dict.map(word => {
    let aux = trie;
    for(let i = word.length -1; i > 0; i--){
      let letter = word[i];
      if(!aux[letter]){
        aux[letter] = {};
      }
      aux = aux[letter]
    }
    if(!aux[word[0]]){
      aux[word[0]] = {}
    }
    aux[word[0]]['-'] = true;
  })
  
  return trie;
}
________________________________________________________
// Number:        1      2      3...
const RADICALS    = ['meth', 'eth', 'prop', 'but',   'pent',  'hex',  'hept',  'oct',  'non',  'dec',  'undec',  'dodec',  'tridec',  'tetradec',  'pentadec',  'hexadec',  'heptadec',  'octadec',  'nonadec']
const MULTIPLIERS = [        'di',  'tri',  'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca', 'octadeca', 'nonadeca']

const SUFFIXES    = [         'ol',      'al', 'one', 'oic acid', 'carboxylic acid',                'oate',               'ether', 'amide', 'amine', 'imine', 'benzene', 'thiol',    'phosphine', 'arsine']
const PREFIXES    = ['cyclo', 'hydroxy',       'oxo',             'carboxy',         'oxycarbonyl', 'oyloxy', 'formyl', 'oxy',   'amido', 'amino', 'imino', 'phenyl',  'mercapto', 'phosphino', 'arsino', 'fluoro', 'chloro', 'bromo', 'iodo']
const RADICAL_NUMBERS = RADICALS.reduce((acc, value, index) => {
    acc[value] = index + 1;
    return acc;
  }, {});
const MULTIPLIERS_NUMBERS = MULTIPLIERS.reduce((acc, value, index) => {
  acc[value] = index + 2;
  return acc;
  }, {});

const subBranchesSuffixes = ['yl', 'en', 'yn', 'an', 'hydroxy', 'mercapto', 'imino', 'fluoro', 'chloro', 'bromo', 'iodo', 'oxo', 
              'formyl', 'carboxy', 'amido', 'amino', 'phosphino', 'arsino', 'oxy', 'oxycarbonyl', 
              'oyloxy', 'phenyl']
const directBranches = ['fluoro', 'chloro', 'bromo', 'iodo', 'hydroxy', 'mercapto', 'imino',  'oxo', 
              'formyl', 'carboxy', 'amido']
const alksBranches = ['yl', 'oxy', 'oxycarbonyl', 'oyloxy']
// Note that alkanes, alkenes alkynes, and akyles aren't present in these lists

function parse(name) {
  const radicalsTrie = buildReverseTrie(RADICALS);
  const suffixesTrie = buildReverseTrie([...SUFFIXES, 'ane', 'ene', 'yne', 'yl', 'en', 'an', 'yn']);
  const prefixesTrie = buildReverseTrie(PREFIXES);
  const multipliersTrie = buildReverseTrie(MULTIPLIERS);
  const symbols = {fluoro: ['F'], chloro: ['Cl'], bromo: ['Br'], iodo: ['I'], hydroxy: ['O', 'H'], mercapto: ['S', 'H'], 
          imino: ['N', 'H'], oxo: ['O'], formyl: ['O', 'C', 'H'], carboxy: ['O', 'O', 'C', 'H'], amido: ['O', 'N', 'H', 'H'],
          amine: ['N'], amino: ['N', 'H', 'H'], phosphine: ['P'], phosphino: ['P', 'H', 'H'], arsine: ['As'], arsino: ['As', 'H', 'H'],
          oxy: ['O'], oxycarbonyl: ['C', 'O', 'O'], oyloxy: ['O', 'O'], ether: ['O'], phenyl: ['C','C','C','C','C','C','H','H','H','H','H'] }
  const bondsConsumed = { fluoro: 1, chloro: 1, bromo: 1, iodo: 1, hydroxy: 1, mercapto: 1, imino: 2, oxo: 2, 
              formyl: 1, carboxy: 1, amido: 3, amino: 1, phosphino: 1, arsino: 1, oxy: 1, oxycarbonyl: 1,
              oyloxy: 1, phenyl: 1}
  const alksSubBranchBondsConsumed = {yl: 1, oxy: 1, oyloxy: 3, oxycarbonyl: 1}

  let parts = breakInParts(name);
  
  let base = getBase(parts);
  // console.log('BASE:', base)

  processBranches(parts, base, 0);

  return base;

  function processBranches(parts, base, index){
    while(parts.length > 0){
      if(!subBranchesSuffixes.includes(parts[0].part)){
        console.log("ERROR not identified:", parts[0])
        break;
      }
      if(directBranches.includes[parts[0].part]){
        processDirectBranch(parts, base);
        continue;
      }
      processBranch(parts, base, index);
    }
  }

  function processBranch(parts, base, index){
    let baseBranch = {};
    let mainPrefix =  parts.shift().part
    if(alksBranches.includes(mainPrefix)){
      baseBranch = processAlk(parts);
      baseBranch.H -= alksSubBranchBondsConsumed[mainPrefix];
    }
    
    if(symbols[mainPrefix]) {
      symbols[mainPrefix].map(symbol => {
        if(!baseBranch[symbol]){
          baseBranch[symbol] = 0;
        }
        baseBranch[symbol]++;
      })
    }
    if(parts.length > 0 && parts[0].type === 6){
      parts.shift();
      let subBranchParts = extractBrackets(parts)
      processBranches(subBranchParts, baseBranch, index + 1);
    }
    let multiplier = 1;
    if(parts.length > 0){
      if(parts[0].type === 2){
        next = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[next.part];
      }
      if(parts.length > 0 && parts[0].type === 5){
        parts.shift();
      }
    }
    Object.keys(baseBranch).map(key => {
      if(!base[key]) {
        base[key] = 0;
      }
      base[key] += baseBranch[key] * multiplier;
    })

    let branchBondsConsumed = 1;
    if(bondsConsumed[mainPrefix]){
      branchBondsConsumed = bondsConsumed[mainPrefix];
    }

    base.H -= multiplier * branchBondsConsumed;

    return multiplier;
  }

  function processDirectBranch(parts, base) {
    let prefix = parts.shift().part;
    let multiplier = 1;
    if(parts.length > 0){
      if(parts[0].type === 2){
        next = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[next.part];
      }
      if(parts[0].type === 5){
        parts.shift();
      }
    }
    symbols[prefix].map(symbol => {
      if(!base[symbol]){
        base[symbol] = 0;
      }
      base[symbol] += multiplier;
    })
    base.H -= multiplier * bondsConsumed[prefix];
  }

  function processAlk(parts){
    next = parts[0];
    let type = 'ane';

    while(parts[0].type === 4){
      next = parts.shift()
      type = next.part + 'e';
    }
    parts.unshift({type: 4, part: type});

    return getBase(parts);
  }

  function extractBrackets(parts) {
  let subBranchParts = [];
  let open = 0;
  while(parts.length > 0){
    let next = parts.shift();
    if(next.type === 7 && open === 0){
      break;
    }
    subBranchParts.push(next);
    if(next.type === 7){
      open--;
    }
    if(next.type === 6){
      open++;
    }
  }
  return subBranchParts;
  }

  function getBase(parts){
  let base = {C:0, H:0};
  let mainSuffix = parts.shift();
  if(mainSuffix.type !== 4){
    throw new Error("NOT VALID! ------- " + name + " ---------");
  }
  let multis = 1;
  let subBase = {};
  switch(mainSuffix.part){
    case 'ane':
    case 'an':
      radical = parts.shift();
      num = RADICAL_NUMBERS[radical.part];
      base.C = num;
      base.H = num * 2 + 2;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
        parts.shift();
        base.H -= 2;
      }
      break;
    case 'ene':
    case 'en':
      next = parts.shift();
      if(next.type === 2){
        multis = MULTIPLIERS_NUMBERS[next.part];
        next = parts.shift();
      }
      if(next.type === 5){
        next = parts.shift();
      }
      num = RADICAL_NUMBERS[next.part];
      base.C = num;
      base.H = num * 2 + 2 - multis * 2;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
      parts.shift();
      base.H -= 2;
      }
      break;
    case 'yne':
    case 'yn':
      next = parts.shift();
      if(next.type === 2){
        multis = MULTIPLIERS_NUMBERS[next.part];
        next = parts.shift();
      }
      if(next.type === 5){
        next = parts.shift();
      }
      if(next.type === 4){
        next = parts.shift();
        let doubles = 1;
        if(next.type === 2){
          doubles = MULTIPLIERS_NUMBERS[next.part];
          next = parts.shift();
        }
        if(next.type === 5){
          next = parts.shift();
        }
        base.H -= doubles * 2;
      }
      num = RADICAL_NUMBERS[next.part];
      base.C = num;
      base.H += num * 2 + 2 - multis * 4;
      if(parts.length > 0 && parts[0].type === 3 && parts[0].part === 'cyclo'){
      parts.shift();
      base.H -= 2;
      }
      break;
    case 'ol':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      break;
    case 'thiol':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.S = subBase.multis;
      break;
    case 'imine':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.N = subBase.multis;
      base.H -= subBase.multis;
      break;
    case 'one':
    case 'al':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      base.H -= subBase.multis * 2;
      break;
    case 'oic acid':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = 2 * subBase.multis;
      base.H -= 2 * subBase.multis;
      break;
    case 'carboxylic acid':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = 2 * subBase.multis;
      base.C += subBase.multis;
      break;
    case 'amide':
      subBase = getSubBase(parts)
      base = subBase.base;
      base.O = subBase.multis;
      base.N = subBase.multis;
      base.H -= subBase.multis;
      break;
    case 'oate':
      let multiPart;
      let multiplier = 1;
      if(parts[0].type === 2){
        multiPart = parts.shift();
        multiplier = MULTIPLIERS_NUMBERS[multiPart.part];
        parts.push(multiPart);
      }
      if(parts[0].type === 5){
        parts.shift();
      }
      base = {O: 2 * multiplier}
      let aux = getBase(parts);
      aux.H -= 2 * multiplier;
      Object.keys(aux).map(key =>{
        if(!base[key]){
          base[key] = 0;
        }
        base[key] += aux[key];
      })
      break;
    case 'benzene':
      base = {C: 6, H: 6}
      break;
    case 'amine':
    case 'phosphine':
    case 'arsine':
    case 'ether':
      if(parts.length === 0 || parts[0].part === 'yl' ||  parts[0].part === 'phenyl'){
        base = {H:3}
        if(mainSuffix.part === 'ether'){
          base.H--;
        }
        symbols[mainSuffix.part].map(symbol => {
          if(!base[symbol]){
            base[symbol] = 0;
          }
          base[symbol] += 1;
        })
      }
      else {
        let subBranch = [];
        let suffixPart = {C: 0, H: 2};
        suffixPart[symbols[mainSuffix.part]] = 1
        if(parts.length > 0 && parts[0].type === 6) {
          parts.shift();
          subBranch = extractBrackets(parts);
          while(subBranch.length > 0 && subBranchesSuffixes.includes(subBranch[0].part)){
            processBranch(subBranch, suffixPart, 0);
          }
        }
        let next = parts[0];
        let multiplier = 1;
        if(next.type === 2){
          multiplier = MULTIPLIERS_NUMBERS[next.part];
          next = parts.shift();
          next = parts[0];
        }
        if(next.type === 5){
          next = parts.shift();
        }
        
        base = getSubBase(parts).base

        Object.keys(suffixPart).map(key =>{
          if(!base[key]){
            base[key] = 0;
          }
          base[key] += suffixPart[key] * multiplier;
        })
        base.H -= multiplier;
      }
      break;
  }
  return base;
  }

  function getSubBase(parts) {
  let next = parts[0];
  let multis = 1;
  if(next.type === 2){
    multis = MULTIPLIERS_NUMBERS[next.part];
    next = parts.shift();
    next = parts[0];
  }
  if(next.type === 5){
    next = parts.shift();
  }
  if(next.type === 1){
    parts.unshift({type: 4, part: 'an'});
  }
  let base = getBase(parts);
  return {base: base, multis:multis}
  }

  function breakInParts(name) {
  let parts = [];
  while(name !== ''){
    // console.log(name)
    if(name[name.length - 1] === '-'){
      name = name.substring(0, name.length - 1);
      let index = name.lastIndexOf('-');
      let whiteSpace = name.lastIndexOf(' ');
      if(whiteSpace > index){
        index = whiteSpace;
      }
      let positions = name.substring(index + 1);
      let num = positions.split(',').length - 2;
      if(num > 0){
        let prev = parts[parts.length - 1];
        if(prev.type !== 2){
          let multi = MULTIPLIERS[num];
          prev.part = prev.part.split(multi)[1];
          parts.push({type: 2, part: multi})
        }
      }
      parts.push({type: 5, part: positions});
      name = name.substring(0, index);
      continue;
    }
    if(name[name.length - 1] === ']'){
      name = name.substring(0, name.length - 1);
      let index = getParentBracket(name);
      parts.push({type: 6, part: ']'})
      parts.push(...breakInParts(name.substring(index + 1)));
      parts.push({type: 7, part: '['})
      name = name.substring(0, index);
      continue;
    }
    let radical = getFromReverseTrie(name, radicalsTrie);
    if(radical !== ''){
      parts.push({type: 1, part: radical});
      name = name.substring(0, name.length - radical.length);
      continue;
    }
    let multi = getFromReverseTrie(name, multipliersTrie);
    if(multi !== ''){
      parts.push({type: 2, part: multi});
      name = name.substring(0, name.length - multi.length);
      continue;
    }
    let prefix = getFromReverseTrie(name, prefixesTrie);
    if(prefix !== ''){
      parts.push({type: 3, part: prefix});
      name = name.substring(0, name.length - prefix.length);
      continue;
    }
    let suffix = getFromReverseTrie(name, suffixesTrie);
    if(suffix !== ''){
      parts.push({type: 4, part: suffix});
      name = name.substring(0, name.length - suffix.length);
      continue;
    }
    if(name[name.length - 1] === ' '){
      name = name.substring(0, name.length - 1);
      continue;
    }
    if(name.length >= 2 && name[name.length - 2] === 'i' && name[name.length - 1] === 'o'){
      name = name.substring(0, name.length - 2);
      parts[parts.length - 1].part = parts[parts.length - 1].part.substring(2);
      
      parts.push({type: 3, part: 'iodo'})
      continue;
    }
    if(name.length >= 3 && name[name.length - 3] === 'a' && name[name.length - 2] === 'm' && name[name.length - 1] === 'i'){
      name = name.substring(0, name.length - 3);
      parts[parts.length - 1].part = parts[parts.length - 1].part.substring(2);
      parts.push({type: 3, part: 'amido'})
      continue;
    }
    console.log(name, "!")
    break;
    }
  return parts;
  }

  function getParentBracket(name){
    let open = 0;
    for(let i = name.length - 1; i >= 0; i--){
      if(name[i] === '[' && open === 0){
        return i;
      }
      if(name[i] === '[') open--;
      if(name[i] === ']') open++;
    }
  }
}  

function getFromReverseTrie(name, trie){
  let i = name.length -1;
  let lastFound = '';
  for(; i >= 0; i--){
    let letter = name[i];
    if (trie[letter]){
      trie = trie[letter];
      if(trie['-']){
        lastFound = name.substring(i);
      }
    }
    else{
      break;
    }
   }
  return lastFound;
}

function buildReverseTrie(dict){
  let trie = {};
  dict.map(word => {
    let aux = trie;
    for(let i = word.length -1; i > 0; i--){
      let letter = word[i];
      if(!aux[letter]){
        aux[letter] = {};
      }
      aux = aux[letter]
    }
    if(!aux[word[0]]){
      aux[word[0]] = {}
    }
    aux[word[0]]['-'] = true;
  })
  
  return trie;
}
_________________________________________________________________________
var Ctx, MULTIPLIERS, RADICALS, ether_case, fn_postfix, fn_prefix, mult_get, multi_number_prefix_skip, oate_case, parse, probe_parse, radical, radical_c_get, radical_suffix_terminated, ram, ram_opt_radical_terminated, regex, subram, x_ine_case;

RADICALS = ['meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec', 'undec', 'dodec', 'tridec', 'tetradec', 'pentadec', 'hexadec', 'heptadec', 'octadec', 'nonadec'];

MULTIPLIERS = ['di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca', 'octadeca', 'nonadeca'];

regex = function(ctx, regex) {
  var reg_ret;
  if (reg_ret = regex.exec(ctx.name)) {
    ctx.name = ctx.name.substr(reg_ret[0].length);
    return true;
  }
};

multi_number_prefix_skip = function(ctx) {
  var reg_ret;
  if (reg_ret = /^-?\d+(?:,\d+)*-/.exec(ctx.name)) {
    ctx.name = ctx.name.substr(reg_ret[0].length);
    return reg_ret[0].split(",").length;
  }
  return 0;
};

mult_get = function(ctx, expected_count = 0) {
  var found, found_idx, i, idx, len, v;
  if (expected_count) {
    found = MULTIPLIERS[expected_count - 2];
    if (!ctx.name.startsWith(found)) {
      return 1;
    }
    ctx.name = ctx.name.substr(found.length);
    return expected_count;
  }
  found = "";
  found_idx = -1;
  for (idx = i = 0, len = MULTIPLIERS.length; i < len; idx = ++i) {
    v = MULTIPLIERS[idx];
    if (ctx.name.startsWith(v)) {
      if (found.length < v.length) {
        found = v;
        found_idx = idx;
      }
    }
  }
  if (found) {
    ctx.name = ctx.name.substr(found.length);
    return found_idx + 2;
  }
  return 1;
};

radical_c_get = function(ctx) {
  var found, found_idx, i, idx, len, v;
  found = "";
  found_idx = -1;
  for (idx = i = 0, len = RADICALS.length; i < len; idx = ++i) {
    v = RADICALS[idx];
    if (ctx.name.startsWith(v)) {
      if (found.length < v.length) {
        found = v;
        found_idx = idx;
      }
    }
  }
  if (found) {
    ctx.name = ctx.name.substr(found.length);
    return found_idx + 1;
  }
  return 0;
};

radical = function(ctx_orig, arg_mult = 1) {
  var ctx, idx;
  ctx = ctx_orig.clone();
  // OPT cyclo
  if (regex(ctx, /^cyclo/)) {
    ctx.add("H", -2 * arg_mult);
  }
  if (idx = radical_c_get(ctx)) {
    ctx.add("C", arg_mult * idx);
    ctx.add("H", arg_mult * (2 * idx + 2)); // alkane
    ctx_orig.set(ctx);
    return true;
  }
  if (regex(ctx, /^benz/)) { // ene will be parsed later
    ctx.add("C", arg_mult * 6);
    ctx.add("H", arg_mult * 8);
    ctx_orig.set(ctx);
    return true;
  }
  if (regex(ctx, /^phen/)) { // ene will be parsed later
    ctx.add("C", arg_mult * 6);
    ctx.add("H", arg_mult * 6);
    ctx_orig.set(ctx);
    return true;
  }
  return false;
};

radical_suffix_terminated = function(ctx_orig, arg_mult = 1) {
  var count, ctx, ctx_backup, expected_count, mult;
  ctx = ctx_orig.clone();
  if (radical(ctx, arg_mult)) {
    if (regex(ctx, /^an/)) {
      ctx_orig.set(ctx);
      return true;
    }
    if (regex(ctx, /^dial/)) {
      // HACK
      ctx.name += "e";
      ctx.add("H", -4 * arg_mult);
      ctx.add("O", 2 * arg_mult);
      ctx_orig.set(ctx);
      return true;
    }
    count = -1;
    while (true) {
      count++;
      // alkene, alkyne
      ctx_backup = ctx.clone();
      if (expected_count = multi_number_prefix_skip(ctx)) {
        mult = mult_get(ctx, expected_count);
        mult *= arg_mult;
        if (regex(ctx, /^en/)) {
          ctx.add("H", -2 * mult);
          continue;
        }
        if (regex(ctx, /^yn/)) {
          ctx.add("H", -4 * mult);
          continue;
        }
        ctx.set(ctx_backup);
      } else {
        // try elision
        mult = arg_mult;
        if (regex(ctx, /^en/)) {
          ctx.add("H", -2 * mult);
          continue;
        }
        if (regex(ctx, /^yn/)) {
          ctx.add("H", -4 * mult);
          continue;
        }
      }
      break;
    }
    if (count) {
      ctx_orig.set(ctx);
      return true;
    }
  }
  return false;
};

fn_prefix = function(ctx_orig, arg_mult = 1) {
  var ctx, ctx_backup, easy, expected_count, mult, mult2, mult_backup, mult_yn;
  ctx = ctx_orig.clone();
  mult = arg_mult;
  easy = function(element_list, reg_exp, h_mult = 1) {
    var el, i, len;
    if (regex(ctx, reg_exp)) {
      for (i = 0, len = element_list.length; i < len; i++) {
        el = element_list[i];
        ctx.add(el, mult);
      }
      // replace
      ctx.add("H", -mult * h_mult);
      ctx_orig.set(ctx);
      return true;
    }
    return false;
  };
  ctx_backup = ctx.clone();
  mult_backup = mult;
  if (expected_count = multi_number_prefix_skip(ctx)) {
    mult = mult_get(ctx, expected_count);
    mult *= arg_mult;
    if (subram(ctx, mult)) {
      ctx_backup = ctx.clone();
      mult_backup = mult;
    }
    if (easy("F", /^fluoro/)) {
      return true;
    }
    if (easy(["Cl"], /^chloro/)) {
      return true;
    }
    if (easy(["Br"], /^bromo/)) {
      return true;
    }
    if (easy("I", /^iodo/)) {
      return true;
    }
    if (easy("OH", /^hydroxy/)) {
      return true;
    }
    if (easy("SH", /^mercapto/)) {
      return true;
    }
    if (easy("N", /^imino/)) { // -2+1
      return true;
    }
    if (easy("O", /^oxo/, 2)) { // -H2
      return true;
    }
    if (easy("COH", /^formyl/)) {
      return true;
    }
    if (easy("COOH", /^carboxy/)) {
      return true;
    }
    if (easy("NO", /^amido/)) {
      return true;
    }
    if (easy("NHH", /^amino/)) {
      return true;
    }
    if (easy("PHH", /^phosphino/)) {
      return true;
    }
    if (easy(["As", "H", "H"], /^arsino/)) {
      return true;
    }
  } else {
    mult2 = mult_get(ctx, 0);
    mult *= mult2;
    if (subram(ctx, mult)) {
      ctx_backup = ctx.clone();
      mult_backup = mult;
    }
    if (easy("F", /^fluoro/)) {
      return true;
    }
    if (easy(["Cl"], /^chloro/)) {
      return true;
    }
    if (easy(["Br"], /^bromo/)) {
      return true;
    }
    if (easy("I", /^iodo/)) {
      return true;
    }
    if (easy("OH", /^hydroxy/)) {
      return true;
    }
    if (easy("SH", /^mercapto/)) {
      return true;
    }
    if (easy("N", /^imino/)) { // -2+1
      return true;
    }
    if (easy("O", /^oxo/, 2)) { // -H2
      return true;
    }
    if (easy("COH", /^formyl/)) {
      return true;
    }
    if (easy("NO", /^amido/)) {
      
      // MISS carboxy
      return true;
    }
    if (easy("NHH", /^amino/)) {
      return true;
    }
    if (easy("PHH", /^phosphino/)) {
      return true;
    }
    if (easy(["As", "H", "H"], /^arsino/)) {
      return true;
    }
  }
  ctx.set(ctx_backup);
  mult = mult_backup;
  if (!radical(ctx, mult)) {
    expected_count = multi_number_prefix_skip(ctx);
    mult = mult_get(ctx, expected_count);
    mult *= arg_mult;
    subram(ctx, mult);
    if (!radical(ctx, mult)) {
      return false;
    }
  }
  while (true) {
    expected_count = multi_number_prefix_skip(ctx);
    mult_yn = mult_get(ctx, expected_count);
    mult_yn *= mult;
    if (regex(ctx, /^an/)) {
      break;
    }
    if (regex(ctx, /^en/)) {
      ctx.add("H", -2 * mult_yn);
      continue;
    }
    if (regex(ctx, /^yn/)) {
      ctx.add("H", -4 * mult_yn);
      continue;
    }
    break;
  }
  if (regex(ctx, /^oyloxy/)) {
    ctx.add("H", -4 * mult_yn); // -3 for bind C -1 for next
    ctx.add("O", 2 * mult);
  } else {
    return false;
  }
  ctx_orig.set(ctx);
  return true;
};

fn_postfix = function(ctx_orig, arg_mult = 1) {
  var ctx, easy, expected_count, mult;
  ctx = ctx_orig.clone();
  mult = arg_mult;
  easy = function(element_list, reg_exp, h_mult = 1) {
    var el, i, len;
    if (regex(ctx, reg_exp)) {
      for (i = 0, len = element_list.length; i < len; i++) {
        el = element_list[i];
        ctx.add(el, mult);
      }
      // replace
      ctx.add("H", -mult * h_mult);
      ctx_orig.set(ctx);
      return true;
    }
    return false;
  };
  if (expected_count = multi_number_prefix_skip(ctx)) {
    mult = mult_get(ctx, expected_count);
    mult *= arg_mult;
    if (easy("OH", /^ol/)) {
      return true;
    }
    if (easy("SH", /^thiol/)) {
      return true;
    }
    if (easy("N", /^imine/)) { // -2+1
      return true;
    }
    if (easy("O", /^one/, 2)) { // -H2
      return true;
    }
    if (easy("OO", /^oic acid/, 2)) {
      return true;
    }
    if (easy("NO", /^amide/)) {
      return true;
    }
    if (easy("COOH", /^carboxylic acid/)) {
      return true;
    }
    if (easy("O", /^al/, 2)) { // -H2
      return true;
    }
    subram(ctx, mult); // LOL WHAT
    if (easy("NHH", /^amine/)) {
      return true;
    }
    if (easy("PHH", /^phosphine/)) {
      return true;
    }
    if (easy(["As", "H", "H"], /^arsine/)) {
      return true;
    }
  } else {
    mult = mult_get(ctx, 0);
    if (easy("OH", /^ol/)) {
      // accepted elisions
      return true;
    }
    if (easy("SH", /^thiol/)) {
      return true;
    }
    if (easy("N", /^imine/)) { // -2+1
      return true;
    }
    if (easy("O", /^one/, 2)) { // -H2
      return true;
    }
    if (easy("OO", /^oic acid/, 2)) {
      return true;
    }
    if (easy("NO", /^amide/)) {
      return true;
    }
    if (easy("COOH", /^carboxylic acid/)) {
      return true;
    }
    if (easy("O", /^al/, 2)) { // -H2
      return true;
    }
    if (mult !== 1) {
      subram(ctx, mult); // LOL WHAT
      if (easy("NHH", /^amine/)) {
        return true;
      }
      if (easy("PHH", /^phosphine/)) {
        return true;
      }
      if (easy(["As", "H", "H"], /^arsine/)) {
        return true;
      }
    }
  }
  
  // NO amine, phosphine, arsine, because multiple yl use. SEPARATE CASE
  return false;
};

subram = function(ctx_orig, arg_mult = 1) {
  var ctx;
  ctx = ctx_orig.clone();
  if (!regex(ctx, /^\[/)) {
    return false;
  }
  while (true) {
    if (ram(ctx, arg_mult)) {
      // * instead of +
      continue;
    }
    if (fn_prefix(ctx, arg_mult)) {
      continue;
    }
    break;
  }
  if (!regex(ctx, /^\]/)) {
    return false;
  }
  ctx_orig.set(ctx);
  return true;
};

ram = function(ctx_orig, arg_mult = 1) {
  var ctx, expected_count, mult, mult2;
  ctx = ctx_orig.clone();
  mult = arg_mult;
  if (!radical(ctx, mult)) {
    expected_count = multi_number_prefix_skip(ctx);
    mult = mult_get(ctx, expected_count);
    mult *= arg_mult;
    subram(ctx, mult);
    if (!radical(ctx, mult)) {
      return false;
    }
  }
  while (true) {
    if (regex(ctx, /^yl/)) {
      ctx.add("H", -2 * mult);
      break;
    }
    if (regex(ctx, /^oxycarbonyl/)) {
      ctx.add("H", -2 * mult); // 2 for -COO-
      ctx.add("C", mult);
      ctx.add("O", 2 * mult);
      break;
    }
    if (regex(ctx, /^oxy/)) {
      ctx.add("H", -2 * mult); // 2 for -O-
      ctx.add("O", mult);
      break;
    }
    expected_count = multi_number_prefix_skip(ctx);
    mult2 = mult_get(ctx, expected_count);
    mult2 *= mult;
    
    // DUPLICATE CHECK, but it's needed
    // because it's not terminator
    if (regex(ctx, /^en/)) {
      ctx.add("H", -2 * mult2);
      continue;
    }
    if (regex(ctx, /^yn/)) {
      ctx.add("H", -4 * mult2);
      continue;
    }
    return false;
  }
  ctx_orig.set(ctx);
  return true;
};

ram_opt_radical_terminated = function(ctx_orig, arg_mult = 1) {
  var ctx;
  ctx = ctx_orig.clone();
  while (true) {
    if (ram(ctx, arg_mult)) {
      continue;
    }
    if (fn_prefix(ctx, arg_mult)) {
      continue;
    }
    break;
  }
  if (!radical_suffix_terminated(ctx, arg_mult)) {
    return false;
  }
  while (true) {
    if (fn_postfix(ctx, arg_mult)) {
      break;
    }
    if (regex(ctx, /^e/)) {
      break;
    }
    return false;
  }
  ctx_orig.set(ctx);
  return true;
};

oate_case = function(ctx_orig, arg_mult = 1) {
  var ctx, ctx_add, k, ref, ref1, v;
  ctx = ctx_orig.clone();
  subram(ctx, arg_mult);
  if (!ram(ctx, arg_mult)) {
    return false;
  }
  if (!regex(ctx, /^ /)) {
    return false;
  }
  ctx_add = ctx.clone();
  ctx.r = {};
  while (true) {
    if (ram(ctx, arg_mult)) {
      continue;
    }
    if (fn_prefix(ctx, arg_mult)) {
      continue;
    }
    break;
  }
  if (!radical_suffix_terminated(ctx, arg_mult)) {
    return false;
  }
  while (true) {
    multi_number_prefix_skip(ctx);
    if (regex(ctx, /^oate/)) {
      ref = ctx_add.r;
      for (k in ref) {
        v = ref[k];
        ctx.add(k, v);
      }
      break;
    }
    if (regex(ctx, /^dioate/)) {
      ctx.add("O", 4 * arg_mult);
      ctx.add("H", -4 * arg_mult);
      ref1 = ctx_add.r;
      for (k in ref1) {
        v = ref1[k];
        ctx.add(k, 2 * v);
      }
      ctx_orig.set(ctx);
      return true;
    }
    return false;
  }
  ctx.add("O", 2);
  ctx.add("H", -2);
  ctx_orig.set(ctx);
  return true;
};

x_ine_case = function(ctx_orig, arg_mult = 1) {
  var ctx, easy;
  ctx = ctx_orig.clone();
  while (true) {
    while (true) {
      if (ram(ctx, arg_mult)) {
        continue;
      }
      if (fn_prefix(ctx, arg_mult)) {
        continue;
      }
      break;
    }
    if (radical_suffix_terminated(ctx, arg_mult)) {
      ctx.add("H", -2 * arg_mult);
      continue;
    }
    if (subram(ctx, arg_mult)) {
      continue;
    }
    break;
  }
  
  // PATCHED
  easy = function(element_list, reg_exp) {
    var el, i, len;
    if (regex(ctx, reg_exp)) {
      for (i = 0, len = element_list.length; i < len; i++) {
        el = element_list[i];
        ctx.add(el, arg_mult);
      }
      ctx_orig.set(ctx);
      return true;
    }
    return false;
  };
  while (true) {
    if (easy("NHHH", /^amine/)) {
      break;
    }
    if (easy("PHHH", /^phosphine/)) {
      break;
    }
    if (easy(["As", "H", "H", "H"], /^arsine/)) {
      break;
    }
    return false;
  }
  ctx_orig.set(ctx);
  return true;
};

ether_case = function(ctx_orig, arg_mult = 1) {
  var ctx;
  ctx = ctx_orig.clone();
  while (true) {
    if (!ram(ctx, arg_mult)) {
      break;
    }
  }
  if (!regex(ctx, /^ether/)) {
    return false;
  }
  ctx.add("O", 1);
  ctx.add("H", 2);
  ctx_orig.set(ctx);
  return true;
};

probe_parse = function(ctx) {
  if (ram_opt_radical_terminated(ctx)) {
    return true;
  }
  if (oate_case(ctx)) {
    return true;
  }
  if (x_ine_case(ctx)) {
    return true;
  }
  if (ether_case(ctx)) {
    return true;
  }
  return false;
};

Ctx = (function() {
  class Ctx {
    constructor() {
      this.r = {
        C: 0,
        H: 0
      };
    }

    add(letter, count) {
      var base;
      if ((base = this.r)[letter] == null) {
        base[letter] = 0;
      }
      this.r[letter] += count;
    }

    clone() {
      var ret;
      ret = new Ctx();
      ret.name = this.name;
      Object.assign(ret.r, this.r);
      return ret;
    }

    set(t) {
      this.name = t.name;
      Object.assign(this.r, t.r);
    }

  };

  Ctx.prototype.name = "";

  Ctx.prototype.r = {
    C: 0,
    H: 0
  };

  return Ctx;

}).call(this);

parse = function(name) {
  var ctx;
  console.log(`name=${name}`);
  ctx = new Ctx();
  ctx.name = name;
  probe_parse(ctx);
  if (ctx.name) {
    console.log(`not parsed ${ctx.name}`);
  }
  if (!ctx.r.C) {
    delete ctx.r.C;
  }
  return ctx.r;
};
_________________________________________________________
/* ------------------ GLOBAL VARIABLES ------------------ */

var s, fLeftmost;

/* -------------- REGEXP-RELATED FUNCTIONS  ------------- */

const notNull              = x             => x !== null
const to_s                 = x             => x instanceof RegExp ? x.source : x;
const rReset               = r             => r.lastIndex = 0;
const rGroup               = r             => RegExp("(" + r.source + ")");
const rZeroOrOne           = r             => rConcat("(", r.source, ")?");
const rConcat              = (...r)        => rGroup(RegExp(r.reduce((r, s) => r + to_s(s), "")));
const rOr                  = (...r)        => rGroup(RegExp(r.map(r => to_s(r)).join("|")));
const eat                  = (s, r)        => {rReset(r); let res = r.exec(s); remain = s.slice(res[0].length); return [res[0], remain];}
const jump                 = (s, r)        => taste(s,r) ? eat(s,r)[1] : s;
const taste                = (s, r)        => {if (s == "") return false; rReset(r); return !(((res = r.exec(s)) === null || res.index != 0));}
const tasteAdd             = (s, t, c, a)  => {if (taste(s, t)) [x, s] = eat(s, t), fAdd(a, c(x)); return s;}

/* ---------- ORGANIC CHEMISTRY SPECIFICATIONS ---------- */
 const VALENCE             = [["Br", "Cl", "F", "H", "I"], ["O", "S"], ["As", "N", "P"], ["C"]]
 const RADICALS            = [null, 'meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec', 'undec', 'dodec', 'tridec', 'tetradec', 'pentadec', 'hexadec', 'heptadec', 'octadec', 'nonadec', 'benzene', 'phen']
 const MULTIPLIERS         = [null, null , 'di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona', 'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca', 'octadeca', 'nonadeca']
 const REORDER_RADICALS    = [null, 'undec', 'dodec', 'tridec', 'tetradec', 'pentadec', 'hexadec', 'heptadec', 'octadec', 'nonadec', 'benzene', 'phen', 'meth', 'eth', 'prop', 'but', 'pent', 'hex', 'hept', 'oct', 'non', 'dec']
 const REORDER_MULTIPLIERS = ['deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca', 'octadeca', 'nonadeca', 'di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona']
 const ELEMENTS            = ["C", "H", "O", "N", "F", "Cl", "Br", "I", "S", "As", "P"];
 const SUFFIXES            = ['oic acid', 'oate', 'ol', 'al', 'one', 'oic acid', 'carboxylic acid', 'oate', 'ether', 'amide', 'amine', 'imine', 'benzene', 'thiol', 'phosphine', 'arsine']
 const PREFIXES            = ['hydroxy', 'oxo', 'carboxy', 'oxycarbonyl', 'oyloxy', 'formyl', 'oxy', 'amido', 'amino', 'imino', 'phenyl', 'mercapto', 'phosphino', 'arsino', 'fluoro', 'chloro', 'bromo', 'iodo']
 const FUNCTION            = [
     {
       F:   ["fluoro"                    ],
       Cl:  ["chloro"                    ],
       Br:  ["bromo"                     ],
       I:   ["iodo"                      ],
       S:   ["mercapto",  "thiol"        ],
       N:   ["amine",     "amino"        ],
       As:  ["arsine",    "arsino"       ],
       P:   ["phosphine", "phosphino"    ],
       O:   ["oxy",       "hydroxy", "ol"],
     },
     {
       CO:  ["formyl"                                         ],
       N:   ["imino",     "imine"                             ],
       ON:  ["amide",     "amido"                             ],
       O:   ["al",        "one",         "oxo"                ],
       CO2: ["carboxy",   "oxycarbonyl", "carboxylic acid"    ],
       O2:  ["oyloxy",    "oate",        "oic acid", "oicacid"],
     }
   ]
/* ----------------------- TOKENS ----------------------- */

const tPositions           = /(\d+,)*\d+/;
const tHyphen              = /\-/;
const tOpen                = /\[/;
const tSpace               = / /;
const tCyclo               = /cyclo/;
const tAlkane              = /ane?/;
const tAlkyl               = /yl/;
const tAlkene              = /ene?/;
const tAlkyne              = /yne?/;
const tLikedAlkane         = (token) => rConcat(rZeroOrOne(rConcat(tHyphen, tPositions, tHyphen)),rConcat(rZeroOrOne(tMultipliers), token));
const tRadicals            = rConcat(rZeroOrOne(tCyclo),rOr(...REORDER_RADICALS.filter(notNull)));
const tMultipliers         = rOr(rOr(...REORDER_MULTIPLIERS), rConcat(rOr(...REORDER_MULTIPLIERS), /n/)) ;
const tOrderMultipliers    = rOr(rOr(...MULTIPLIERS.filter(notNull)), rConcat(rOr(...MULTIPLIERS.filter(notNull)), /n/)) ;
const tPrefixFunction      = rOr(...PREFIXES);
const tSuffixFunction      = rOr(...SUFFIXES);
const tAlkeneFunction      = tLikedAlkane(tAlkene);
const tAlkyneFunction      = tLikedAlkane(tAlkyne);
const tAlkylExtent         = rOr(tPrefixFunction, rConcat(tRadicals,
                                                         rZeroOrOne(tAlkeneFunction),
                                                         rZeroOrOne(tAlkyneFunction),
                                                         rZeroOrOne(tAlkane),
                                                         rOr(tAlkyl, tPrefixFunction)));

/* ----------------- FORMULAR MANIPULATION ----------------- */

const fNew          = ()        => {return {branches: [], delta: 0}};
const fComplete     = (a)       => {let [x, _, n, c] = [...Array(4)].map((_,i) => VALENCE[i].map(e => a[e] || 0).reduce((r,e) => r + e,0)); a.H = ~~((c - x/2 + n/2 + 1 - a.delta)*2);}
const fClean        = (a)       => {fComplete(a); let res = ELEMENTS.reduce((r, e) => {a[e] && (r[e] = a[e]); return r},{}); res.H = res.H || 0; return res;}
const fCopy         = (a)       => to_f(f2s(a), a.delta);
const f2s           = (a)       => {let res = ""; for (const e of ELEMENTS) if (a[e] !== undefined && a[e] != 0) res += `${e}${a[e] == 1 ? '' :  a[e]}`; return res + `[${a.delta}]`;}
const to_f          = (s, d)    => {let m, r = /([A-Z][a-z]?)(\-?\d*)/g, res = fNew(); while (match = r.exec(s)) res[match[1]] = !match[2] ? 1 : parseInt(match[2]); res.delta = d; return res;}
const fAdd          = (a, b)    => {a.delta += b.delta; for (let e in b) if (ELEMENTS.indexOf(e) != -1) a[e] = (a[e] || 0) + b[e];}
const fAddN         = (a, b, n) => [...Array(n)].reduce((r,_) => fAdd(a,b),a);

/* ----------------------- CONVERTER ----------------------- */

const iRadicals     = s => RADICALS.indexOf(s);

const iMultipliers  = s => s === undefined ? 1 : MULTIPLIERS.indexOf(s);

const cRadicals     = s => {
  if (s == "benzene" || s == "phen") return to_f("C6",4);
  let m = tRadicals.exec(s);
  let [n, hasCyclo] = [iRadicals(m[4]), !!m[2]];
  return to_f(`C${n}`, hasCyclo);
}

const cLikedAnkane  = s => {
  let multiple;

  s = jump(s, tHyphen);
  s = jump(s, tPositions);
  s = jump(s, tHyphen);

  if (taste(s, tMultipliers, 1)) {
    [multiple, s] = eat(s, tMultipliers);
  }
  return to_f("", iMultipliers(multiple) * (taste(s, tAlkene, 1) ? 1 : 2))
}

const cFunction = (t) => {
  for (const delta of [0, 1])
    for (const formula in FUNCTION[delta])
      if (FUNCTION[delta][formula].indexOf(t) != -1)
        return to_f(formula, delta);
}

/* ----------------------- PARSERS ----------------------- */

function findClose(s) {
  for (let i = 0, depth = 0; i < s.length; i++) {
    if (s[i] == "[") depth++;
    else if (s[i] == "]" && !--depth) return i;
  }
}

function getBranch(s, outer, previous) {
  let pos, multiple, prefix, t, r, children = [], _save = s, res = {}, f = fNew(), cur = fNew();

  s = jump(s, tSpace);
  s = jump(s, tHyphen);

  if (taste(s, tPositions, 1)) {
    [pos, s] = eat(s, tPositions, 1);
  }

  s = jump(s, tHyphen);

  if (taste(s, tMultipliers, 1) ) {
      const reset = () => {s = multiple + s; multiple = undefined;}
      [multiple, s] = eat(s, tMultipliers);
      let m = iMultipliers(multiple);
      if (pos) {
        let n = pos.split(",").length;
        if (n != m) {
          reset();
          [multiple, s] = eat(s, tOrderMultipliers);
          m = iMultipliers(multiple);
          if (n != m) reset();
        }
      } else if (m > 2 && (outer || taste(s, /dec/)))
      reset();
    }

  if (taste(s, tOpen, 1)) {
    closeBracket = findClose(s);
    children.push(s.slice(1, closeBracket));
    s = s.slice(closeBracket+1);
  }

  if (!taste(s, tAlkylExtent, 1)) return {result: false, remain: _save};

  [prefix, s] = eat(s, tAlkylExtent);

  // CONVERT

  for (const child of children)
    fAdd(cur, getBranch(child, prefix).f);

  prefix = tasteAdd(prefix, tRadicals,   cRadicals,    cur);
  prefix = tasteAdd(prefix, tAlkeneFunction, cLikedAnkane, cur);
  prefix = tasteAdd(prefix, tAlkyneFunction, cLikedAnkane, cur);

  if (!taste(prefix, tAlkyl))
    prefix = tasteAdd(jump(prefix, tAlkane), tPrefixFunction, cFunction, cur);

  if (taste(s, tSpace)) {
    fLeftmost = fCopy(cur);
    multiple = undefined;
  }

  fAddN(f, cur, iMultipliers(multiple));

  while ((r = getBranch(s, outer, true)).result)
    fAdd(f, r.f), s = r.remain;
  return {f: f, result: true, remain: s};
}

function getSuffix (s, outer) {
  let multiple, children = [], res, cur = fNew(), f = fNew();

  s = jump(s, tHyphen   );
  s = jump(s, tPositions);
  s = jump(s, tHyphen   );

  if (taste(s, tMultipliers, 1) ) {
    [multiple, s] = eat(s, tMultipliers);
  }

  if (taste(s, tOpen, 1)) {
    closeBracket = findClose(s);
    children.push(s.slice(1, closeBracket));
    s = s.slice(closeBracket+1);
  }

  multiple = iMultipliers(multiple);

  if (!taste(s, tSuffixFunction)) return {result: false};

  [t, s] = eat(s, tSuffixFunction);
  cur = cFunction(t);

  for (const child of children)
    fAdd(cur, getBranch(child, t).f);

  fAddN(f, cur, multiple);

  res = {f: f, remain: s, result: true};
  if (t == "oate") res.multiple = multiple;
  return res;
}

function parse (_s) {
  s = _s, fLeftmost = fNew();
  let fMain = fNew(), fPrefix = fNew(), fSuffix = fNew(), r, t ;

  while ((r = getBranch(s)).result)
    fAdd(fPrefix, r.f), s = r.remain;

  if (s == "ether") {
    fAdd(fPrefix, to_f("O",0));
    return fClean(fPrefix);
  }

  s = jump(s, tSpace);
  s = tasteAdd(s, tRadicals, cRadicals, fMain);
  s = jump(s, tAlkane);
  s = tasteAdd(s, tAlkeneFunction, cLikedAnkane, fMain);
  s = tasteAdd(s, tAlkyneFunction, cLikedAnkane, fMain);

  while ((r = getSuffix(s)).result) {
    if (r.multiple) {
      t = fNew();
      fAddN(t, fLeftmost, r.multiple-1);
      fLeftmost = t;
    }
    fAdd(fSuffix, r.f);
    s = r.remain
  }

  fAdd(fMain, fLeftmost);
  fAdd(fMain, fPrefix  );
  fAdd(fMain, fSuffix  );

  return fClean(fMain);
}
_______________________________________________________
let name;
let index;
let closes;


function matchAt(regex) {
  console.assert(index <= name.length, "past end, index", index, "length", name.length);
  regex.lastIndex = index;
  const exec = regex.exec(name);
  if (exec === null || exec.index !== index) return null;
  index += exec[0].length;
  return exec[0];
}

function add(base, addend, multcity = 1) {
  for (const atom in addend) {
    base[atom] = (base[atom] || 0) + addend[atom] * multcity;
  }
  return base;
}

const locRegex = /-?\d+(,\d+)*-/g;
const multerRegex = /di|(un|do)deca|(tri|tetra|penta|hexa|hepta|octa|nona)(deca)?/g;
const multcities = { di: 2, tri: 3, tetra: 4, penta: 5, hexa: 6, hepta: 7, octa: 8, nona: 9, deca: 10, undeca: 11, dodeca: 12, trideca: 13, tetradeca: 14, pentadeca: 15, hexadeca: 16, heptadeca: 17, octadeca: 18, nonadeca: 19 };
const multers = [ null, "", "di", "tri", "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca" ];
function mult() {
  const locMatch = matchAt(locRegex);
  if (locMatch === null) {
    const multerMatch = matchAt(multerRegex);
    if (multerMatch === null) return 1;
    return multcities[multerMatch];
  }
  const multcity = locMatch.split(",").length
  const multer = multers[multcity];
  console.assert(name.slice(index, index += multer.length) === multer, "no expected multer \"" + multer + ", index", index - multer.length);
  return multcity;
}

const stemRegex = /m?eth|prop|but|(un|do|tri|tetra)?dec|(pent|hex|hept|oct|non)(adec)?/g;
const stems = { meth: { C: 1, H: 4 }, eth: { C: 2, H: 6 }, prop: { C: 3, H: 8 }, but: { C: 4, H: 10 }, pent: { C: 5, H: 12 }, hex: { C: 6, H: 14 }, hept: { C: 7, H: 16 }, oct: { C: 8, H: 18 }, non: { C: 9, H: 20 }, dec: { C: 10, H: 22 }, undec: { C: 11, H: 24 }, dodec: { C: 12, H: 26 }, tridec: { C: 13, H: 28 }, tetradec: { C: 14, H: 30 }, pentadec: { C: 15, H: 32 }, hexadec: { C: 16, H: 34 }, heptadec: { C: 17, H: 36 }, octadec: { C: 18, H: 38 }, nonadec: { C: 19, H: 40 } };
const en = { H: -2 };
const yn = { H: -4 };
function parseChain() {
  const base = {};
  if (name.slice(index, index + 5) === "cyclo") {
    index += 5;
    base.H = -2;
  }
  const stem = matchAt(stemRegex);
  if (stem === null) return null;
  const chain = add(base, stems[stem]);
  for (let k = 0; k < 2; k++) {
    const i = index;
    const multcity = mult();
    const bond = name.slice(index, index += 2);
    if (bond === "en") add(chain, en, multcity);
    else if (bond === "yn") add(chain, yn, multcity);
    else if (bond !== "an") {
      index = i;
      break;
    }
  }
  return chain;
}

const priPreRegex = /hydroxy|oxo|carboxy|formyl|amido|amino|imino|phenyl|mercapto|phosphino|arsino|fluoro|chloro|bromo|iodo/g;
const priPres = { hydroxy: { O: 1 }, oxo: {H: -2, O: 1 }, carboxy: { C: 1, O: 2 }, formyl: { C: 1, O: 1 }, amido: { H: -1, N: 1, O: 1 }, amino: { H: 1, N: 1 }, imino: { H: -1, N: 1 }, phenyl: { C: 6, H: 4 }, mercapto: { S: 1 }, phosphino: { H: 1, P: 1 }, arsino: { H: 1, As: 1 }, fluoro: { H: -1, F: 1 }, chloro: { H: -1, Cl: 1 }, bromo: { H: -1, Br: 1 }, iodo: { H: -1, I: 1 } };
const yl = { H: -2 };
const secPreRegex = /(oyl)?oxy(carbonyl)?/g;
const secPres = { oxy: { H: -2, O: 1 }, oxycarbonyl: { C: 1, H: -2, O: 2 }, oyloxy: { H: -4, O: 2 } };
function parsePre() {
  if (name[index] === "[") {
    const open = index++;
    const subs = parsePres();
    console.log("Subs", subs);
    console.assert(index++ === closes[open], "not at corr ], open", open, "close", closes[open], "index", index - 1);
    const main = parsePre();
    return add(subs, main);
  }
  const priPre = matchAt(priPreRegex);
  if (priPre !== null) return priPres[priPre];
  const i = index;
  const chain = parseChain();
  if (chain === null) {
    index = i;
    return null;
  }
  if (name.slice(index, index += 2) === "yl") return add(chain, yl);
  index -= 2;
  const secPre = matchAt(secPreRegex);
  if (secPre !== null) return add(chain, secPres[secPre]);
  index = i;
  return null;
}

function parsePres() {
  const combined = {};
  while (true) {
    let prefix;
    let multcity = 1;
    let i = index;
    const chain = parseChain();
    if (chain !== null) {
      if (name.slice(index, index + 2) === "yl") {
        index += 2;
        prefix = add(chain, yl);
      }
      else {
        const secPre = matchAt(secPreRegex);
        if (secPre !== null) prefix = add(chain, secPres[secPre]);
      }
      
    }
    if (!prefix) {
      index = i;
      multcity = mult();
      prefix = parsePre();
      if (prefix === null) {
        index = i;
        break;
      }
    }
    console.log("Prefix", prefix, "mult", multcity);
    add(combined, prefix, multcity);
  }
  return combined;
}

const parentRegex = /amine|phosphine|arsine|ether|benzene/g;
const parents = { amine: { H: 3, N: 1 }, phosphine: { H: 3, P: 1 }, arsine: { H: 3, As: 1 }, ether: { H: 2, O: 1 }, benzene: { C: 6, H: 6 } };
function parseParent() {
  const parent = matchAt(parentRegex);
  if (parent !== null) return parents[parent];
  const chain = parseChain();
  console.log(chain);
  console.assert(chain !== null, "no parent, index", index);
  return chain;
}

const suffixRegex = /ol|al|one|(o|carboxyl)ic acid|oate|amide|amine|imine|thiol|phosphine|arsine/g;
const suffixes = { ol: { O: 1 }, al: { H: -2, O: 1 }, one: { H: -2, O: 1 }, "oic acid": { H: -2, O: 2 }, "carboxylic acid": { C: 1, O: 2 }, oate: { H: -2, O: 2 }, amide: { H: -1, N: 1, O: 1 }, amine: { H: 1, N: 1 }, imine: { H: -1, N: 1 }, thiol: { S: 1 }, phosphine: { H: 1, P: 1 }, arsine: { H: 1, As: 1 } };
function parseSuffix() {
  if (index === name.length) return {};
  if (name[index] === "e" && index === name.length - 1) {
    index++;
    return {};
  }
  const multcity = mult();
  if (name[index] === "[") {
    const open = index++;
    const subs = parsePres();
    console.assert(index++ === closes[open], "not at corr ], open", open, "close", closes[open], "index", index);
    const main = parseSuffix();
    const subbed = add(subs, main);
    return add({}, subbed, multcity);
  }
  const suffix = matchAt(suffixRegex);
  console.assert(suffix !== null, "no suffix, index", index);
  return add({}, suffixes[suffix], multcity);
}

function parseYlOate(alkyl) {
  const prefixes = parsePres();
  const parent = parseParent();
  const oateCity = mult();
  console.assert(name.slice(index) === "oate", "not left with oate, index", index);
  index += 4;
  const oate = add({}, suffixes.oate, oateCity);
  const oated = add(oate, parent);
  const alkoate = add(oated, prefixes);
  const ester = add(alkoate, alkyl, oateCity);
  return ester;
}

const ylOateRegex = /^\S+yl \S+oate$/;
function parseMolec() {
  const prefixes = parsePres();
  if (ylOateRegex.test(name)) {
    console.assert(name[index++] === " ", "not at space in yl-oate, index", index - 1);
    return parseYlOate(prefixes);
  }
  const parent = parseParent();
  const suffix = parseSuffix();
  console.log(suffix);
  const suffed = add(suffix, parent);
  const full = add(suffed, prefixes);
  return full;
}

function parse(_name) {
  name = _name;
  index = 0;
  closes = {};
  const stack = [];
  for (let i = 0; i < name.length; i++) {
    if (name[i] === "[") stack.push(i);
    else if (name[i] === "]") closes[stack.pop()] = i;
  }
  const molecule = parseMolec();
  console.assert(index === name.length, "Not at end, index", index, "length", name.length);
  return molecule;
}
