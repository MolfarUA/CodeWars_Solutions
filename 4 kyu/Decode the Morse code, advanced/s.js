54b72c16cd7f5154e9000457


function decodeBits(bits) {
  // Trim zeros
  bits = bits.replace(/(^0+|0+$)/g, '')
  
  // Find transmission rate
  var rate = Math.min.apply(null, bits.match(/0+|1+/g).map(function(b) { return b.length }))
  
  // Convert to morse code
  bits = bits
    .replace(new RegExp('(?:111){' + rate + '}(?:0{' + rate + '}|$)', 'g'), '-')
    .replace(new RegExp('1{' + rate + '}(?:0{' + rate + '}|$)', 'g'), '.')
    .replace(new RegExp('(?:000000){' + rate + '}', 'g'), '   ')
    .replace(new RegExp('(?:00){' + rate + '}', 'g'), ' ')
  
  return bits
}

function decodeMorse(message) {
  return message
    .replace(/   /g, ' _ ')
    .split(' ')
    .map(function(letter) { return letter === '_' ? ' ' : MORSE_CODE[letter] })
    .join('')
}
_____________________________
var decodeBits = function( bits ) {
  bits = bits.replace( /(^0+|0+$)/g, '' );
  let timeUnit = Math.min.apply( null, bits.match( /0+|1+/g ).map( item => item.length ) );
  
  return bits
    .replace( new RegExp( '0'.repeat( 7 * timeUnit ), 'g' ), '   ' )
    .replace( new RegExp( '0'.repeat( 3 * timeUnit ), 'g' ), ' ' )
    .replace( new RegExp( '1'.repeat( 3 * timeUnit ), 'g' ), '-' )
    .replace( new RegExp( '1'.repeat( 1 * timeUnit ), 'g' ), '.' )
    .replace( new RegExp( '0'.repeat( 1 * timeUnit ), 'g' ), '' );
};

var decodeMorse = function(morseCode){
    return morseCode.trim().split( '   ' )
      .reduce( ( res, word ) => res + ' ' + word.split( ' ' ).reduce( ( word, letter ) => word + MORSE_CODE[ letter ], '' ), '' )
      .trim();
};
_____________________________
function decodeBits (bits) {
  let codes = bits
    .replace(/^0+/, '')
    .replace(/0+$/, '')
    .match(/(0+|1+)/g)
  
  let counts = codes.map((e) => { return e.length })
  let min = Math.min(...counts)
  
  return codes
    .map((code) => {
      switch (code.slice(0, code.length / min)) {
        case '0'      : return ''
        case '1'      : return '.'
        case '111'    : return '-'
        case '000'    : return ' '
        case '0000000': return '   '
      }
    }).join('')
}

function decodeMorse (morse) {
  return morse.replace(/ ?[.-]+ ?/g, (e) => {
    return MORSE_CODE[e.trim()]
  }).trim()
}
