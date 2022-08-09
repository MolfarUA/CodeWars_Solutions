568d0dd208ee69389d000016


export function rentalCarCost(d: number): number {
  if (d >= 7) return d * 40 - 50;
  if (d >= 3) return d * 40 - 20
  return d * 40;
}
__________________________
export function rentalCarCost(d: number): number {
  let total = d*40
  if(d >= 3 && d < 7) total -= 20
  if(d >= 7) total -= 50
  
  return total
}
__________________________
export const rentalCarCost = (d: number): number => {
  return d < 3 ? 40 * d : d >= 3 && d < 7 ? 40 * d - 20 : 40 * d - 50;
}
