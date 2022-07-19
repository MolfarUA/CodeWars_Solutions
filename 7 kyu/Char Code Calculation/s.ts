57f75cc397d62fc93d000059


export function calc(str: string): number {
  const charCodes = str.split('').map((char) => char.charCodeAt(0));
  return sum(charCodes) - sum(charCodes.map(replace7with1));
}

function sum(arr: number[]): number {
  return arr.reduce((total, x) => total + x, 0);
}

function replace7with1(num: number): number {
  return parseInt(num.toString().replace(/7/g, '1'));
}
__________________________________
export function calc(str: string): number{
 return [...str].map(x => x.charCodeAt(0)).join('').split('').filter(x => x === '7').length * 6
}
__________________________________
export const calc = (str: string): number => {
  return [...str].map(c => c.charCodeAt(0)).join('').replace(/[^7]/g, '').length * 6;
}
__________________________________
export const calc = (x: string): number => {
  return (x.replace(/./g,(x)=>x.charCodeAt(0).toString()).match(/7/g)||[]).length*6
}
