587f0abdd8730aafd4000035


function sha256Cracker(hash, chars) {
  const crypto = require('crypto')
  let perms = permutations(chars)
  let out = null
  for (let i = 0; i < perms.length; i++) {
    let sum = crypto.createHash('sha256').update(perms[i]).digest('hex')
    if (sum == hash) {
      out = perms[i]
      break
    }
  }
  return out
}

function permutations(string) {
  if (string.length < 2 )
    return [string]

  let arr = []
  for (let i = 0; i < string.length; i++){
    if (string.indexOf(string[i]) === i) {
      let rest = string.slice(0, i) + string.slice(i + 1, string.length)
      for (let p of permutations(rest)){
        arr.push(string[i] + p)
      }
    }
  }
  return arr
}
_________________________
const permutator = permutation => {
    var length = permutation.length,
        result = [ permutation.slice() ],
        c = new Array( length ).fill( 0 ),
        i = 1, k, p;

    while ( i < length ) {
        if ( c[ i ] < i ) {
            k = i % 2 && c[ i ];
            p = permutation[ i ];
            permutation[ i ] = permutation[ k ];
            permutation[ k ] = p;
            ++c[ i ];
            i = 1;
            result.push( permutation.slice() );
        } else {
            c[ i ] = 0;
            ++i;
        }
    }
    return result;
}

const sha256Cracker = ( hash, chars ) => {
    const { createHash } = require( 'crypto' )
    const permutes = permutator( ( chars ).split( '' ) ).map( ( a ) => a.join( '' ) )
    for ( let permute of permutes ) {
        if ( createHash( 'sha256' ).update( permute ).digest( 'hex' ) == hash ) {
            return permute
        }
    }
    return null
}
_________________________
const { createHash } = require("node:crypto");

function sha256Cracker(hash, [...chars], pre = "") {
  return (
    (chars.length
      ? chars.reduce(
          (result, char, i) =>
            result ||
            sha256Cracker(
              hash,
              chars.slice(0, i).concat(chars.slice(i + 1)),
              pre + char
            ),
          null
        )
      : [pre].find(
          (x) =>
            createHash("sha256").update(x).digest().toString("hex") === hash
        )) || null
  );
}
