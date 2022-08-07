54b72c16cd7f5154e9000457


export const decodeBits = (bits: string) => {
  bits = bits.replace(/(^0+|0+$)/g,'');
  var sets:string[] =  bits.match(/(1+|0+)/g);
  var unit:number = sets[0].length;
  for(let i:number = 0; i < sets.length -1; i++){
    if(sets[i].length > sets[i+1].length){
      unit = sets[i+1].length;
      break;
    }
  }
  return bits.replace(new RegExp('1{'+unit*3+'}','g'),'-')
             .replace(new RegExp('1{'+unit+'}','g'),'.')
             .replace(new RegExp('0{'+unit*7+'}','g'),'   ')
             .replace(new RegExp('0{'+unit*3+'}','g'),' ')
             .replace(/0+/g,'');    
};

export const decodeMorse = (morseCode: string) => {
  return morseCode.replace(/\s{3}/g,' | ')
                   .split(' ')
                   .map((v,i,a)=>v==='|'? ' ':MORSE_CODE[v])
                   .join('');
};
_____________________________
const determinePace = (bits: string) => {
    return (bits.match(/1+|0+/g) || [])
        .reduce((a, b) => ((b.length < a) ? b.length : a), 9999);
}

export const decodeBits = (bits: string) => {
    // ToDo: Accept 0's and 1's, return dots, dashes and spaces
    bits = bits.replace(/^0+|0+$/g, '');
    const pace = determinePace(bits);
    return bits.replace(new RegExp('1{'+pace*3+'}','g'),'-')
             .replace(new RegExp('1{'+pace+'}','g'),'.')
             .replace(new RegExp('0{'+pace*7+'}','g'),'  ')
             .replace(new RegExp('0{'+pace*3+'}','g'),' ')
             .replace(/0+/g,'');
};

export const decodeMorse = (morseCode: string) => {
    return morseCode.replace('  ', ' | ').split(' ').map(c => (MORSE_CODE[c] || ' ')).join('');
};
_____________________________
export const decodeBits = (bits: string) => {
    const trimmedBits = bits.substring(bits.indexOf("1"), bits.lastIndexOf("1") + 1);

    let length = Number.POSITIVE_INFINITY;
    let i = 0;
    while(i < trimmedBits.length) {
        let currentBit = trimmedBits[i];
        let currentLength = 1;
        while (trimmedBits[++i] === currentBit) currentLength++;
        if (currentLength < length) length = currentLength;
    }

    return trimmedBits.split("0".repeat(length * 7)).map(word => word.split("0".repeat(length * 3))
            .map(ch => ch.split("0".repeat(length)).map(u => u.length / length > 1 ? "-" : ".").join("")).join(" "))
        .join("   ");
};

export const decodeMorse = (morseCode: string) =>
    morseCode.trim().split("   ").map(word => word.split(" ").map(code => MORSE_CODE[code]).join("")).join(" ");
