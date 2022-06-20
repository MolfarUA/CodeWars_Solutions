539a0e4d85e3425cb0000a88


export default function add(x: number): any {
  const fn = (y: number) => add(x + y);
  fn.valueOf = () => x;
  return fn;
}
______________________
export default function add(x: number): any {
  // receives the next number in the sequence
  const addNum = (next: any) => {
    // returns the outer function, with cumulative number so far as the argument
    return add(x + next)
  }

  // sets value of method of inner function to return value of x for final number
  addNum.valueOf = () => {
    return x
  }

  // returns addNum function which will be called with next number as argument
  return addNum
}
______________________
export default function add(x: number): any {
  const result = (y: number) => add(x + y);
  result.valueOf = () => x;
  return result;
}
______________________
/**
 * Calculates the sum of numbers.
 *
 * @param x number
 * @returns number
 * The sum of numbers using closures.
 */
export default function add(x: number): any {
  let currentSum: number = x;

  function f(y: number): any {
    if (typeof(y) === "number") {
        currentSum += y;
        return f;
    }
  }

  // "f" is a function object and should include "toString" method.
  f.toString = function(): any {
    return currentSum;
  };

  return f;
}
