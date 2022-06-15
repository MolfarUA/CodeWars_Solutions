export function plural(n:number):boolean {
  // any number that is different than 1 is plural
  return n !== 1;
}
__________________
export function plural(n:number):boolean {
  return (n===1) ? false : true;
}
__________________
export function plural(n:number):boolean {
  return !(n === 1);
}
__________________
export function plural(n:number):boolean {
  if (n === 0 || n === Number.POSITIVE_INFINITY) return true;
  if (Number.isInteger(n)) return n > 1;
  return n > 0;
}
__________________
export function plural(n:number):boolean {
 var plural:boolean=false
  if(n!=1) plural= true; 
  return plural;
}
__________________
export function plural(n:number):boolean {
    // ...
    // We need a simple function that determines if a plural is needed or not. It should take a number, and return true if a plural should be used with that number or false if not. This would be useful when printing out a string such as 5 minutes, 14 apples, or 1 sun.
// You only need to worry about english grammar rules for this kata, where anything that isn't singular (one of something), it is plural (not one of something).
// All values will be positive integers or floats, or zero.

    if (n === 1) {
        return false;
    }
    return true;
    

  }
