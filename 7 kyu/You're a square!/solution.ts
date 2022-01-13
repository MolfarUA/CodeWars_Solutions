export default function isSquare(n: number): boolean {
  return Number.isInteger(Math.sqrt(n));
};
__________________________________
export default function isSquare(n: number): boolean {
  return Math.sqrt(n) % 1 == 0; // fix me
};
__________________________________
export default function isSquare(n: number): boolean {
  return Number.isInteger(n ** 0.5)
};
__________________________________
export default function isSquare(n: number): boolean {
  const root = Math.sqrt(n)
  return Math.trunc(root) === root
};
__________________________________
export default function isSquare(n: number): boolean {
  return n >= 0 && Math.sqrt(n) % 1 == 0 ? true : false;
};
