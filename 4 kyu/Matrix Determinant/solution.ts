export function determinant(m: number[][]): number {
    if (m.length > 2) {
        return m[0].reduce(function (sum: number, val: number, idx: number): number {
            let add = (idx & 1) == 0 ? 1 : -1;
            let sub = m.slice(1).map(elem => elem.filter((_, i) => i != idx))
            return sum + add * val * determinant(sub);
        }, 0);
    } else if (m.length == 2) {
        return m[0][0] * m[1][1] - m[0][1] * m[1][0];
    } else {
        return m[0][0];
    }
}
_____________________________________________
export function determinant(m) {
  if (m.length === 1) {
    return m[0][0];
  } else {
    var res = 0;
    m[0].forEach((e, i) => {
      res += Math.pow(-1, i) * e * determinant(minor(m,i));
    });
    return res;
  }
}

function minor(m, i) {
  return m.slice(0).splice(1).map(e => e.filter((_, idx) => i != idx));
}
_____________________________________________
export const determinant = (m) => m.length === 1 ? 
  m[0][0] : 
  m[0].reduce((result, value, index) => result + Math.pow(-1, index) * value * determinant(minor(m, index)), 0);

const minor = (m, i) => m.slice(0).splice(1).map(e => e.filter((_, k) => i != k));
_____________________________________________
export function determinant(matrix: number[][]) {
  if (matrix.length === 1) {
    return matrix[0][0];
  }
  
  return matrix[0]
    .reduce(
      (d, e, index) => d + determinant(minor(matrix, index)) * e * sign(index),
      0
    );
}

function minor(matrix: number[][], target: number): number[][] {
  return removeFirstRow(matrix).map(row => removeColumn(row, target));
}

function removeFirstRow(matrix: number[][]): number[][] {
  return matrix.slice(1);
}

function removeColumn(row: number[], index: number): number[] {
  return [
    ...row.slice(0, index),
    ...row.slice(index + 1)
  ];
}

function sign(index: number): 1 | -1 {
  return index % 2 ? -1 : 1;
}
_____________________________________________
export function determinant(givenMatrix: number[][]): number {
    let determinantValue: number = 0;

    if (givenMatrix.length === 1) {
        determinantValue = givenMatrix[0][0];
    } else if (givenMatrix.length === 2) {
        determinantValue = (givenMatrix[0][0] * givenMatrix[1][1]) - (givenMatrix[1][0] * givenMatrix[0][1]);
    } else {
        const topValues: number[] = givenMatrix.splice(0, 1)[0];

        for (let i = 0; i < topValues.length; i++) {
            const numberSign: number = i % 2 === 0 ? 1 : -1;

            const newMatrix = givenMatrix.map(val => {
                return val.slice(0, i).concat(val.slice(i+1));
            });
            
            const currentValue = numberSign * (topValues[i] * determinant(newMatrix));

            determinantValue += currentValue;
        }
    }

    return determinantValue;
}
