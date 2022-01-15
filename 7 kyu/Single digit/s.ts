export function singleDigit(n: number): number {
  function bitCount (m: number): number {
    return (m.toString(2).match(/1/g)||[]).length;
  }
  return n > 9 ? singleDigit(bitCount(n)) : n;
}
__________________________
export function singleDigit(n: number): number {
  while(n > 9){
    n = n.toString(2).replace(/0/g, "").length
  }
  return n
}
__________________________
export const singleDigit = (n: number, s = n.toString(2)): number => {
  
  if (n <= 9) return n;
  
  const addOnes = (s: string): number => s.split('').reduce((sum, curr) => (curr === '1') ? ++sum : sum , 0);

  let digit = addOnes(s);

  while (digit > 9) {
    s = digit.toString(2);
    digit = addOnes(s);
  }

  return digit;
 
}
__________________________
export const singleDigit = (n: number): number =>
  n < 10 ? n : singleDigit([...n.toString(2)].reduce((a, b) => a + +b, 0));
__________________________
export function singleDigit(n: number): number {
  if (n < 10) {
    return n;
  }
  const result = Array.from(n.toString(2)).map(Number).reduce((x,y)=>x+y);
  return result >= 10 ? singleDigit(result) : result;
}
__________________________
export let singleDigit = (n: number): number => (n < 10) ? n : singleDigit((n.toString(2).match(/1/g) || []).length);
