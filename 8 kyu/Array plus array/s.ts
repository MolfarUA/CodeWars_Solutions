5a2be17aee1aaefe2a000151


import _ from 'lodash';

export function arrayPlusArray(...args: number[][]): number {
  return _(args).flatten().sum();
}
_________________________
export const arrayPlusArray = (arr1 : number[], arr2 : number[]) => arr1.concat(arr2).reduce((a, b) => a + b);
_________________________
export const arrayPlusArray = (arr1 : number[], arr2 : number[]) : number => {
    return [...arr1, ...arr2].reduce((a, b) => a + b)
}
_________________________
export const arrayPlusArray = (arr1: number[], arr2: number[]): number => {
    let sum = 0;
    for (let i = 0; i < arr1.length; i++) {
        sum = sum + arr1[i];
    }
    for (let i = 0; i < arr2.length; i++) {
        sum = sum + arr2[i];
    }
    return sum;
}
