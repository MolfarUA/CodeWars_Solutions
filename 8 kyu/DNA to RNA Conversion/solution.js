function DNAtoRNA(dna){
  return dna.replace(/T/g, 'U');
}

_____________________________
const DNAtoRNA = dna => dna.replace(/T/g, 'U');

_____________________________
function DNAtoRNA(dna) {
  return dna.split("T").join("U");
}

_____________________________
function DNAtoRNA(dna) {
  var hold = ''
  for(var i =0;i<dna.length;i++) {
     if(dna[i]=="T") {
        hold+="U"
}
else{hold+=dna[i]}
}
return hold;
      
}
