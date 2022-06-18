export const head = (xs: any[]) => xs.length ? xs[0] : undefined;
export const last = (xs: any[]) => xs.length ? xs[xs.length-1] : undefined;
export const init = (xs: any[]) => xs.length ? xs.slice(0, xs.length-1) : [];
export const tail = (xs: any[]) => xs.length ? xs.slice(1) : [];
_____________________________
export const head = (arr:number[]) => arr[0];
export const tail = (arr:number[]) => arr.slice(1);
export const init = (arr:number[]) => arr.slice(0, arr.length - 1);
export const last = (arr:number[]) => arr[arr.length - 1];
