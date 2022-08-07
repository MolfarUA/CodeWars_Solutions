57cfdf34902f6ba3d300001e


export function twoSort(s: string[]): string {
  return s
    .sort()[0]
    .split("")
    .join("***");
}
___________________________
export function twoSort(s: string[]): string {
  return [...s.sort()[0]].join("***");
}
___________________________
export function twoSort(s: string[]): string {
  const sorted = s.sort()
  return sorted[0].split('').join('***')
}
