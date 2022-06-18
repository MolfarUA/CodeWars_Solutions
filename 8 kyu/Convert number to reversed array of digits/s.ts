export const digitize = (n: number): number[] => {
  return [...n.toString()].map(Number).reverse();
};
________________________
export const digitize = (n: number): number[] => {
 return [...n.toString()].reverse().map(Number)
};
________________________
export const digitize = (n: number): number[] => {
  const arr = [...`${n}`].reverse()
  return arr.map(_ => Number(_))
};
________________________
export const digitize = (n: number): number[] => {
  let x = `${n}`.split('').reverse();
  let a = []
  for(let i = 0; i < x.length; i++){
    a.push( Number(x[i]) ) 
  }
  return a
};
________________________
export const digitize = (n: number): number[] => {
  return [...String(n)].reverse().map(x => +x);
};
