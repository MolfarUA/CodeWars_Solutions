559b8e46fa060b2c6a0000bf


const factorial = (n: number): number => n ? n * factorial(n - 1) : 1;

export const diagonal = (n: number, p: number): number => Math.round(factorial(n + 1) / (factorial(n - p) * factorial(p + 1)));
_____________________________
export function diagonal(line: number, diagonalIndex: number): number {
    let currentDiagonal: number[] = [];
    for (let i = 0; i <= diagonalIndex; i++) {
        const previousDiagonal = currentDiagonal;
        currentDiagonal = [1];

        const lineOfDiagonal = line - (diagonalIndex - 1);
        for (let j = 1; j < lineOfDiagonal; j++) {
            const previousBinomial = currentDiagonal[j - 1];
            const previousDiagonalBinomial = previousDiagonal[j] || 0;

            currentDiagonal.push(previousBinomial + previousDiagonalBinomial);
        }
    }
    return currentDiagonal.reduce((acc, cur) => acc += cur, 0);
}
_____________________________
export function diagonal(n: number, p: number): number {
  const triangle = [[1], [1, 1]];
  for (let i = 2; i <= n; i++) {
    const line = [];
    line.push(1);
    for (let j = 0; j < triangle[i - 1].length - 1; j++) {
      line.push(triangle[i - 1][j] + triangle[i - 1][j + 1]);
    }
    line.push(1);
    triangle.push(line);
  }
  const result = triangle.reduce((acc, cur) => acc + cur[p] || 0, 0);
  return result
}
