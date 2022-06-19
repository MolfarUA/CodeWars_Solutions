5b853229cfde412a470000d0


export function twiceAsOld(dad: number, son: number): number {
  return Math.abs(dad - son * 2)
}
______________________________
export const twiceAsOld = (dad: number, son: number): number => Math.abs(dad - 2 * son);
______________________________
export function twiceAsOld(dadAge: number, sonAge: number): number {
  return Math.abs(dadAge - sonAge * 2);
}
