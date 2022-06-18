const sumArr = (arr: number[]): number => arr.reduce((prevVal, val) => prevVal + val, 0);

export const findEvenIndex = (arr: number[]): number => arr.findIndex((v, index) => { 
    const leftSide = arr.slice(0, index);
    const rightSide = arr.slice(index + 1);
    
    return sumArr(leftSide) === sumArr(rightSide)
});
________________________
export function findEvenIndex(arr: number[]): number
{
  let i = 0, lSum = 0, rSum = arr.reduce((acc, cur) => acc + cur, 0);
  
  do {
    const n = arr[i];
    rSum -= n;
    if (lSum === rSum) {
      return i;
    }
    lSum += n;
    i++;
  } while (i < arr.length);
  
  return -1;
}
________________________
export function findEvenIndex(arr: number[]): number {
  if (arr.length <= 1) return 0
  
  let i = 0
  while (i <= arr.length - 1) {
    const left = arr.slice(0, i).reduce((acc, val) => (acc += val), 0) || 0
    const right = arr.slice(i + 1, arr.length).reduce((acc, val) => (acc += val), 0)

    if (left === right) return i
    i++
  }
  
  return -1
}
________________________
export function findEvenIndex(arr: number[]): number {
  const totalSum = arr.reduce((acc, cv) => acc += cv, 0);
  let leftSum = 0;
  return arr.findIndex(currentValue => {
    if (2 * leftSum + currentValue === totalSum) {
      return true;
    }
    leftSum += currentValue;
    return false;
  });
}
________________________
export function findEvenIndex(arr: number[]): number
{
  const sum = (a: number, e: number) => a + e;
  return arr.findIndex((e, i, arr) => arr.slice(0, i).reduce(sum, 0) === arr.slice(++i, arr.length).reduce(sum, 0));
}
