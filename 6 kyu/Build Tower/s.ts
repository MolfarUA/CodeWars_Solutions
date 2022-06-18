576757b1df89ecf5bd00073b


export const towerBuilder = (nFloors: number): string[] => {
  let result = [];
  for (let i = 1; i <= nFloors; i++) {
    result.push(buildFloor(i, nFloors));
  }
  return result;
};

// build i'th floor for a tower of size n floors
function buildFloor(i: number, n: number): string {
  let middleSection = "*".repeat(2 * i - 1);
  let sideSection = " ".repeat(n - i);
  let floor = sideSection + middleSection + sideSection;
  return floor;
}
_____________________________
export const towerBuilder = (nFloors: number): string[] => {
  return Array.from({ length: nFloors }, (_, index) => {
    const spaces = " ".repeat(nFloors - 1 - index);
    return `${spaces}${"*".repeat(index * 2 + 1)}${spaces}`;
  });
};
_____________________________
export const towerBuilder = (nFloors: number): string[] => {
 return Array.from({length: nFloors}, (_, i) => `${" ".repeat(nFloors - i - 1)}${"*".repeat(2 * i + 1)}${" ".repeat(nFloors - i - 1)}`)
}
_____________________________
export const towerBuilder = (n: number): string[] => {
    const result: string[] = [];
    for (let i = 1; i <= n; i++) {
        result.push(' '.repeat(n - i)
                    + '*'.repeat(i * 2 - 1)
                    + ' '.repeat(n - i));
    }
    return result;
}
_____________________________
export const towerBuilder = (nFloors: number): string[] => {
  return Array.from(Array(nFloors).keys())
    .map((_el: unknown, i: number): string => {
      const whiteSpaces: string = " ".repeat(nFloors - i - 1);
      const stars: string = "*".repeat(((i + 1) * 2 - 1));
      
      return `${whiteSpaces}${stars}${whiteSpaces}`;
    });
}
