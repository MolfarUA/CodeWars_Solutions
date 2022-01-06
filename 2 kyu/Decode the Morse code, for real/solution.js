function classify(items, centroids) {
  var clusters = [];
  for (let i = 0; i < centroids.length; i++) {
    clusters.push([]);
  }

  items.forEach(item => {
    var distances = [];
    var cluster_index = 0;
    
    for (let i = 0; i < centroids.length; i++) {
      distances.push(Math.sqrt(Math.pow(item.length - centroids[i], 2)));
      //distances.push(Math.abs(item.length - centroids[i]));
    }

    for (let i = 0, min = Math.min(...distances); i < distances.length; i++) {
      if (distances[i] === min) {
         if (i === 2 && item[0] === '1') 
          cluster_index = 1;
         else
          cluster_index = i;
        break;
      };
    }

    clusters[cluster_index].push(item);
  });
  
  return clusters;
}

function mean(items) {
  if (!items.length) return 0;
  return items.reduce((sum, item) => sum + item.length, 0) / items.length;
}

function kmeans(data, centroids, iterations = Infinity) {
  var clusters = null, moved = false;
  
  do {
    clusters = classify(data, centroids);
    for (let i = 0, m; i < clusters.length; i++) {
      m = mean(clusters[i]);
      if (centroids[i] !== m) {
        centroids[i] = m;
        moved = true;
        continue;
      }
      moved = false;
    }
  }
  while (iterations-- && moved)

  return { clusters: clusters, centroids: centroids }
}

function decodeBitsAdvanced(bits){
    var map = {};
    var bits = bits.replace(/^0+|0+$/g, '').match(/1+|0+/g);
    if (!bits) return '';
    
    var result = kmeans(bits, [1,3,7], 100);
    var clusters = result.clusters; 
    var averages = [
      (Math.max(...clusters[0].map(item => item.length)) + Math.min(...clusters[0].map(item => item.length))) / 2,
      (Math.max(...clusters[1].map(item => item.length)) + Math.min(...clusters[1].map(item => item.length))) / 2,
      (Math.max(...clusters[2].map(item => item.length)) + Math.min(...clusters[2].map(item => item.length))) / 2,
    ]

    var centroids = [
      (averages[0] + averages[1]) / 2 || averages[0] || averages[1],
      (averages[1] + averages[2]) / 2 || averages[1] || averages[0] * 3,
    ]

    bits.reduce((map, signal) => {
      signal = signal.length;

      if (signal <= centroids[0]) {
        map['1'.repeat(signal)] = '.';
        map['0'.repeat(signal)] = '';
      }

      else if (signal <= centroids[1]) {
        map['1'.repeat(signal)] = '-';
        map['0'.repeat(signal)] = ' ';
      }

      else if (signal > centroids[1]) {
        map['1'.repeat(signal)] = '-';
        map['0'.repeat(signal)] = '   ';
      }

      return map;
    }, map)

    console.log(centroids, result.centroids);
    
    return bits.map(signal => {
      return map[signal];
    }).join('');
}

function decodeMorse(morseCode){
    if (!morseCode.length) return '';
    return morseCode.split('   ').map(word => {
      return word.trim().split(' ').map(code => {
        return MORSE_CODE[code] || code
      }).join('');
    }).join(' ');
}
_______________________________________________
var decodeBitsAdvanced = function(bits){
    bits = bits.replace(/(^0+|0+$)/g, "");
    if(!bits) return bits;
    if(!bits.replace(/1+/g, "")) return '.';
    
    let length = bits.match(/0+|1+/g).map(s=>s.length).sort((x, y)=> x-y);
    let [min, max] = [length.shift(), length.pop()];
    let unit = (max / 7 + min) / 2;
    let seven = Math.floor(7 * unit);
    let three = Math.round(3 * unit);
    
    return bits
            .replace(new RegExp("0".repeat(seven) + "+", "g"), "   ")
            .replace(new RegExp("1".repeat(three) + "+", "g"), "-")
            .replace(new RegExp("0".repeat(three) + "+", "g"), " ")
            .replace(/1+/g, ".")
            .replace(/0+/g, "")
}

var decodeMorse = function(morseCode){
   let words = morseCode.split("   ")
              .map(word => word.split(" ")
              .map(letter => MORSE_CODE[letter]))
              .map(letters => letters.join(""))
              .join(" ")
    return words;
}
_______________________________________________
var decodeBitsAdvanced = function(bits){
    // ToDo: Accept 0's and 1's, return dots, dashes and spaces
  if (!bits.includes('1')) return '';
  
  const arrayOfOnes = bits.replace(/^0+|0+$/g, '').split(/0+/).map(symb => symb.length);
  const arrayOfZeroes = bits.replace(/^0+|0+$/g, '').replace(/^1+|1+$/g, '').split(/1+/).map(symb => symb.length || 100); 
  const arrayOfAll = [...arrayOfOnes, ...arrayOfZeroes.filter(num => num <= Math.max(...arrayOfOnes) )];
  
  let dotCenter    = Math.min(...arrayOfAll),
      dashCenter   = Math.max(...arrayOfAll),
      spaceCenter  = dashCenter + 3,
      middleCenter = (dotCenter + dashCenter) / 2,
      prevDotCenter, prevDashCenter;
  
  while (prevDotCenter !== dotCenter || prevDashCenter !== dashCenter) {
    if (dotCenter === dashCenter) { 
      spaceCenter = 3 + (dashCenter = dotCenter * 3 - 1);
      break;
    };
    
    [prevDotCenter, prevDashCenter] = [dotCenter, dashCenter];
    let dotDistances = 0, dashDistances = 0, dots = 0, dashes = 0;
    arrayOfOnes.forEach( num => num <= middleCenter ? (dotDistances += num) && (dots += 1) : (dashDistances += num) && (dashes += 1));
    dotCenter = (dotDistances / dots) || dotCenter;
    dashCenter = (dashDistances / dashes);
    middleCenter = (dotCenter + dashCenter) / 2;
  }
  
  middleCenter = Math.floor((dotCenter + dashCenter) / 2 * 1.1) + 1;
  
  return bits.replace(new RegExp(`1{${middleCenter},}`, 'g'), '-')
             .replace(/1+/g, '.')
             .replace(new RegExp(`0{${spaceCenter},}`, 'g'), '  ')
             .replace(new RegExp(`0{${middleCenter},}`, 'g'), ' ')
             .replace(/0+/g, '');
}

var decodeMorse = function(morseCode){
    // ToDo: Accept dots, dashes and spaces, return human-readable message
  return morseCode.split('  ').map(word => word.split(' ').map(symb => MORSE_CODE[symb]).join('')).join(' ').trim();
}
_______________________________________________
var correctOneBit = function( unit, maxOneLength ) {
  if( maxOneLength < 3 ) return '1';

  let middle = maxOneLength / 2;
  if( middle < 2 ) middle = 2;

  if( unit.length <= middle ) return '1';
  else return '111';
};

var correctZeroBit = function( unit, maxZeroLength ) {
  if( maxZeroLength < 2 ) return '0';

  let divider = 2.4;
  if( maxZeroLength > 10 ) divider = 3.6;
  
  let lowerEdge = maxZeroLength / divider;
  if( lowerEdge < 2 ) lowerEdge = 2;

  let upperEdge = ( maxZeroLength - lowerEdge ) / 2 + lowerEdge;
  if( upperEdge < 6 ) upperEdge = 6;

  if( unit.length < lowerEdge ) return '0';
  else if( unit.length >= lowerEdge && unit.length < upperEdge ) return '000';
  else return '0000000';
};

var decodeBitsAdvanced = function( bits ) {
  bits = bits.replace( /(^0+|0+$)/g, '' );
  if( bits === '' ) return '';

  let minOneLength = 0;
  let maxOneLength = 0;
  let minZeroLength = 0;
  let maxZeroLength = 0;
  let parsedBits = bits.match( /0+|1+/g );
  let timeUnit = Math.min.apply( null, parsedBits.map( bit => bit.length ) );
  let parsedUnits = parsedBits.map( bit => {
    let value = bit[ 0 ].indexOf( '1' ) !== -1 ? '1' : '0';
    let shortedLength = Math.ceil( bit.length / timeUnit );

    if( value === '1' && !minOneLength ) minOneLength = shortedLength;
    if( value === '0' && !minZeroLength ) minZeroLength = shortedLength;

    if( value === '1' ) {
      maxOneLength = Math.max( maxOneLength, shortedLength );
      minOneLength = Math.min( minOneLength, shortedLength );
    }
    if( value === '0' ) {
      maxZeroLength = Math.max( maxZeroLength, shortedLength );
      minZeroLength = Math.min( minZeroLength, shortedLength );
    }

    return {
      value: value,
      length: shortedLength
    };
  } );
  
  let correctedBits = parsedUnits.map( unit => {
    if( !minZeroLength ) return '1';

    switch( unit.value ) {
      case( '1' ):
        return correctOneBit( unit, maxOneLength );
        break;
      default:
        return correctZeroBit( unit, maxZeroLength ); 
        break;
    }
  } ).join( '' );
    
  return correctedBits
    .replace( new RegExp( '111', 'g' ), '-' )
    .replace( new RegExp( '1', 'g' ), '.' )
    .replace( new RegExp( '0000000', 'g' ), '   ' )
    .replace( new RegExp( '000', 'g' ), ' ' )
    .replace( new RegExp( '0', 'g' ), '' );
};

var decodeMorse = function( morseCode ) {
    return morseCode.replace( /   /g, ' __ ' )
      .split( ' ' )
      .map( letter => letter === '__' ? ' ' : MORSE_CODE[ letter ] )
      .join( '' );
};
