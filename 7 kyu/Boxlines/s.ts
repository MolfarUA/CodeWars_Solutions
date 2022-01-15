export const f = (x: number, y: number, z: number) => x+(x+2)*y*z + y+(y+2)*x*z + z+(z+2)*x*y;
_____________________________________
export const f = (x: number, y: number, z: number) =>
  x * -~y * -~z + y * -~z * -~x + z * -~x * -~y;
_____________________________________
export function f(x: number, y: number, z: number): number{
  return z*(3*x*y+1+2*(x+y))+2*x*y+x+y
}
_____________________________________
export function f(x: number, y: number, z: number): number {
  return 3*x*y*z + 2*(x*y + y*z + x*z) + x + y + z;
}
_____________________________________
export const f = (x: number, y: number, z: number) => 3 * x * y * z + 2 * (x * y +  x * z + y * z) + x + y + z;
_____________________________________
export function f(x: number, y: number, z: number): number{
  return x * (y + 1) * (z + 1)
    + y * (x + 1) * (z + 1)
    + z * (x + 1) * (y + 1)
}
