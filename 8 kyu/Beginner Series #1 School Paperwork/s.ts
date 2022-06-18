55f9b48403f6b87a7c0000bd


export function paperwork(n: number, m :number): number{
  return (n < 1 || m < 1) ? 0 : n * m;
}
__________________________
export function paperwork(n: number, m :number): number{
  return (n > 0 && m > 0) && (n * m) || 0;
}
__________________________
export function paperwork(n: number, m :number): number{
  return (Math.sign(n) + Math.sign(m)) > 0 ? n*m : 0;
}
__________________________
export const paperwork = (n: number, m :number) => n < 0 ? 0 : Math.max(n*m, 0);
__________________________
export function paperwork(classmates: number, pages :number): number{
  return classmates < 0 || pages < 0 ? 0 : classmates * pages;
}
