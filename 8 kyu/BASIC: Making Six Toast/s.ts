5834fec22fb0ba7d080000e8


export function sixToast(num:number):number {
  return Math.abs(6-num);
}
________________________
export const sixToast = ($:number):number => $ > 6 ? $ - 6 : 6 - $
________________________
export const sixToast = (num: number): number => Math.abs(6 - num)
