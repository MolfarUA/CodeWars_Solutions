55eea63119278d571d00006a


export function nextId(ids: number[]): number {
  let i = 0;
  
  while(ids.includes(i)) {
    i++
  }
  
  return i;
}
______________________
export function nextId(ids: number[]): number {
  const idsSet = new Set(ids);
  let i = 0;

  while (idsSet.has(i)) {
    i += 1;
  }

  return i;
}
______________________
export const nextId = (ids: any): any => {
  let i = 0
  
  while (ids.includes(i)) {
    i ++
  }
  
  return i
}
