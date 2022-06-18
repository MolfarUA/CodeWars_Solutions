export const narcissistic = (value: number): boolean =>
  value ===
  value
    .toString()
    .split('')
    .reduce((acc, n, _, xs) => acc + parseInt(n) ** xs.length, 0);
________________________
export function narcissistic(value: number): any {
  const separatedNums: number[] = Array.from(value.toString(), Number);
  const multiplicator = separatedNums.length;
  const processedNum = separatedNums.reduce((acc, curr) => acc += curr ** multiplicator, 0)
  return processedNum === value; 
}
________________________
export function narcissistic(value: number): boolean {
  const digits = String(value).split('');
  
  return digits.reduce((acc, current) =>
    acc + Math.pow(Number(current), digits.length), 0) === value;
}
________________________
export function narcissistic(value: number): boolean {
  const str = String(value);
  let acc = 0;
  str.split('').forEach((x) => acc += Math.pow(+x, str.length))
  return acc === value;
}
________________________
export function narcissistic(value: number): boolean {
   return [...""+value].reduce((sum, x) => sum + Math.pow(+x, String(value).length), 0) === value
}
