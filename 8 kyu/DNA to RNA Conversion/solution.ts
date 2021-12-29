export function DNAtoRNA(dna: string): string {
  return dna.replace(/T/g, 'U');
}

_____________________________
export const DNAtoRNA = ($: string): string => [...$].map(el => el === 'T' ? el = 'U' : el).join('') 

_____________________________
export const DNAtoRNA = (str:string):string => str.replace(/T/g, 'U')

_____________________________
export function DNAtoRNA(dna: string): string {
  let re = /\T/gi;
let result = dna.replace(re, "U");

return result
}

_____________________________
export function DNAtoRNA(dna: string): string {
  return dna.replace(/\T/g, 'U');
}

_____________________________
export function DNAtoRNA(dna: string): string {
  return dna.split('').map(nab => nab == 'T' ? 'U' : nab).join('')
}
