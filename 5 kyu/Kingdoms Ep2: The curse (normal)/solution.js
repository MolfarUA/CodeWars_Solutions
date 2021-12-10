function translate(speech, vocabulary) {
  while (speech.includes('*')) {
    speech = speech.replace(/[\w\*]*\*[\w\*]*/g, s => {
      let r = new RegExp(`^${s.replace(/\*/g, '.')}$`);
      let l = vocabulary.filter(x => r.test(x));
      if (l.length > 1) return s
      vocabulary = vocabulary.filter(x => x !== l[0]);
      return l[0];
    });
  }
  return speech
}

##############
const match = (w1, w2) => {
  let l = w1.length;
  if ( l !== w2.length ) return false;
  for ( let i=0; i<l; i++ ) if ( w1[i]!='*' && w1[i]!=w2[i] ) return false;
  return true;
}

const getMatches = (w1, voc) => voc.filter( w2 => match(w1, w2) )

const alph = '*abcdefghijklmnopqrstuvwxyz';

const translate = (s, voc) => {
  while ( s.includes('*') ) {
    for ( let i=0, w=''; i<s.length+1; i++ ){
      if ( alph.includes(s[i]) ) { w += s[i]; } 
      else if ( w.length ){
        W2 = getMatches(w, voc)
        if ( W2.length==1 ) {
          w2 = W2[0]
          s = s.slice(0, i-w.length) + w2 + s.slice(i);
          voc.splice(voc.indexOf(w2), 1);
        }
      w = '';
      }
    } 
  }
  return s;
}

#################
function translate(speech, vocabulary) {
    if (speech.length===0){ return ''}
    var words = speech.split(' ')
    var arr = words.map((el,ind) => {
        var wordCleen = el.replace(/[?!,.]/,'')
        var reg = new RegExp( wordCleen.replace(/\*/g,'\\S'))
        var goodWord =[ind]
        for(var i=0; i<vocabulary.length; i++){
            if( (vocabulary[i].length === wordCleen.length) && (vocabulary[i].search(reg)!==-1)){

                goodWord.push(vocabulary[i])
            }
        }
        return goodWord
    })
    arr.sort((a,b)=>a.length-b.length)
    for(var i = 1; i<arr.length; i++){
     var check = arr[i-1][1]
        for (var j=i; j<arr.length; j++){
            if( arr[j].includes(check)){
                arr[j].splice(arr[j].indexOf(check),1)
            }
        }
    }
    arr.sort((a,b)=>a[0]-b[0])
    return words.map((el,ind)=>el.replace(new RegExp( el.replace(/\*/g,'\\S').replace(/[?!,.]/,'')),arr[ind][1] )).join(' ')
}

#######################
function translate(speech,[...vocabulary]) {
  let spoken = speech.match( /[\w*]+/g ) || [] ;
  let corrected = {};
  let t; // store the single word when we find it instead of having to find it again
  while ( spoken.length ) {
    const i = spoken.findIndex( spoke => (t = vocabulary.filter( word => new RegExp( '^' + spoke.replace( /\*/g, '.' ) + '$' ).test(word) )).length===1 );
    corrected[spoken[i]] = t[0];
    spoken.splice(i,1);
    vocabulary.splice( vocabulary.indexOf(t[0]), 1 );
  }
  return speech.replace( /[\w*]+/g, word => corrected[word] );
}

###################
function translate(speech, vocabulary) {
  while (speech.includes('*')) {
    speech = speech.replace(/[\w\*]+/g, s => {
      const r = new RegExp(`^${s.replace(/\*/g, '.')}$`);
      const matched = vocabulary.filter(w => r.test(w));
      if (matched.length == 1) {
        vocabulary.splice(vocabulary.indexOf(matched[0]), 1);
        return matched[0];
      }
      return s;
    });
  }
  return speech;
}
####################
function translate(speech, vocabulary) {
  let dic = vocabulary
  let res = speech
  while (res.includes('*')) {
    // ?!,.
    res = res
      .split(' ')
      .map(x => x
        .split('?')
        .map(y => y
          .split('!')
          .map(z => z
            .split(',')
            .map(h => h
              .split('.')
              .map(ast => {
                if (!ast.includes('*')) return ast
                let matches = dic.filter(w => match(ast, w))
                if (matches.findIndex(m => m != matches[0]) > -1) return ast
                let fstocc = dic.findIndex(v => v == matches[0])
                dic = dic.slice(0, fstocc).concat(dic.slice(fstocc + 1))
                return matches[0]
              })
              .join('.')
            )
            .join(',')
          )
          .join('!')
        )
        .join('?')
      )
      .join(' ')
  }
  return res
}

function match(ast,wor) {
  return ast.length == wor.length && ast
    .split('')
    .findIndex((a,i) => a != '*' && a != wor[i])
    == -1
}

#############################
function translate(speech, vocabulary) {
    if (speech.length===0){ return ''}
    var words = speech.split(' ')
    var arr = words.map((el,ind) => {
        var wordCleen = el.replace(/[?!,.]/,'')
        var reg = new RegExp( wordCleen.replace(/\*/g,'\\S'))
        var goodWord =[ind]
        for(var i=0; i<vocabulary.length; i++){
            if( (vocabulary[i].length === wordCleen.length) && (vocabulary[i].search(reg)!==-1)){

                goodWord.push(vocabulary[i])
            }
        }
        return goodWord
    })
    arr.sort((a,b)=>a.length-b.length)
    for(var i = 1; i<arr.length; i++){
     var check = arr[i-1][1]
        for (var j=i; j<arr.length; j++){
            if( arr[j].includes(check)){
                arr[j].splice(arr[j].indexOf(check),1)
            }
        }
    }
    arr.sort((a,b)=>a[0]-b[0])
    return words.map((el,ind)=>el.replace(new RegExp( el.replace(/\*/g,'\\S').replace(/[?!,.]/,'')),arr[ind][1] )).join(' ')
}
