export function doubleton(num: number): number {
  num += 1
  while(new Set(""+num).size != 2){
    num++
  }
  return num
} 
__________________
export function doubleton(num: number) {
   while(num++){
        const numbers = String(num).split('')
        if(new Set(numbers).size === 2) {
            return +numbers.join('')
        }
   }
}
________________
export function doubleton(n: number): number {
  for(let i = n + 1; i < 1_000_000; i++){
    if((new Set(i.toString())).size==2)
        return i;
  }
  return 1
} 
___________________
export function doubleton(num: number): number {
  for (let n = num + 1; ; n++)
    if (new Set([...`${n}`]).size === 2)
      return n;
} 
_________________
export function doubleton(num: number): number {
  let num2 = (num + 1).toString()
  while ([...new Set(num2.split(''))].join('').length !== 2) num2 = ((+num2) + 1).toString()
  return +num2
} 
