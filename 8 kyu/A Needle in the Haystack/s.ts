export function findNeedle(haystack: any[]):string {
  return "found the needle at position " + haystack.indexOf('needle');
}
________________________
export function findNeedle(haystack: any[]): string {
  return `found the needle at position ${haystack.indexOf('needle')}`;
}
________________________
export function findNeedle(haystack: any[]):string {
  
  let items: string[] = haystack.map((item) => { return (typeof item === "string" ? item.toString() : "") });
  
  return `found the needle at position ${items.findIndex(a => a == 'needle')}`;
}
________________________
export const findNeedle = (haystack: any[]):string => `found the needle at position ${haystack.indexOf("needle")}`
________________________
export function findNeedle(haystack: any[]):string {
  return "found the needle at position " + haystack.indexOf("needle").toString()
}
