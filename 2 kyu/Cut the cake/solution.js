const cut = cake => {
  const num = cake.match(/o/g).length;  
  const cakeArray = cake.split('\n').map(e => e.split``);
  const rows = cakeArray.length;
  const cols = cakeArray[0].length;
  const size = (rows * cols) / num;
  return run(cakeArray, size, []);
}

const run = (cake, size, slices) => {
  const corner = findFirstTopLeftCorner(cake);
  if (null == corner) return slices;
  let x = corner[1];
  let y = corner[0];

  for (let width = size; width >= 1; width--) {
    for (let height = 1; height <= size; height++) {
      if ((height * width) !== size) continue;
      const slice = isAValidSlice(cake, x, y, width, height);
      if (!slice) continue;
      const newSlices = Object.assign([], slices);
      newSlices.push(slice);
      let newCake = doCut(JSON.parse(JSON.stringify(cake)), x, y, width, height);
      let r = run(newCake, size, newSlices);
      if (r.length) return r;
    }
  }

  return [];
}

const findFirstTopLeftCorner = cake => {
  for (let i = 0; i < cake.length; i++) 
    for (let j = 0; j < cake[i].length; j++) 
      if (cake[i][j] !== 'x') 
        return [i,j];
}

const isAValidSlice = (cake, x, y, width, height) => {
  if ((x + width) > cake[0].length) return false;
  if ((y + height) > cake.length) return false;
  const slice = cake.slice(y, y + height).map(e => e.slice(x, x + width));
  const sliceStr = stringify(slice);  
  if (sliceStr.match(/x/)) return false;
  const numberOfO = (sliceStr.match(/o/g) || []).length;
  if (numberOfO !== 1) return false;
  return sliceStr;
}

const stringify = cake => cake.map(e => e.join``).join`\n`;

const doCut = (cake, x, y, width, height) => {
  for (let i = y; i < (y + height); i++) 
    for (let j = x; j < (x + width); j++) 
      cake[i][j] = 'x';
  return cake;
}

_____________________________________________________
const getValidSliceDimensions = (sliceArea, maxLength, maxWidth) => {
  const result = [];
  for (let width = maxWidth; width > 0; width--) {
    const length = sliceArea / width;
    if (sliceArea % width === 0 && length <= maxLength) result.push([length, width]);
  }
  return result;
}

const setCharAt = (str, idx, char) => `${str.substr(0, idx)}${char}${str.substr(idx + 1)}`

const cut = (ck) => {
  const cake = ck.split('\n');
  const cakeLength = cake.length;
  const cakeWidth = cake[0].length;
  const cakeArea = cakeLength * cakeWidth;
  const numberOfRaisins = ck.split('').filter((char) => char === 'o').length;
  
  if (cakeArea % numberOfRaisins !== 0) return [];
  
  const sliceArea = cakeArea / numberOfRaisins;
  const validSliceDimensions = getValidSliceDimensions(sliceArea, cakeLength, cakeWidth);

  const evenSlices = [];
  
  const solve = (r, c) => {
    let col = c === cakeWidth ? 0 : c;
    let row = c === cakeWidth ? r + 1 : r;
    const isCakeFullyDivided = cake.join('').split('').filter((char) => char !== 'x').length === 0;
    
    if (isCakeFullyDivided) return true;
    
    while (cake[row][col] === 'x') {
      col++;
      if (col === cakeWidth) {col = 0; row++;}
      if (row === cakeLength) return false;
    }
      
    for (let i = 0; i < validSliceDimensions.length; i++) {
      const [length, width] = validSliceDimensions[i];
      const sliceIsInBounds = row + length <= cakeLength && col + width <= cakeWidth;
      const targetSlice = cake.map((r) => r.slice(col, col + width)).filter((_, idx) => idx >= row && idx < row + length);
      const numberOfRaisinsInSlice = targetSlice.join('').split('').filter((char) => char === 'o').length;
      const sliceOverlapsAnotherSlice = Boolean(targetSlice.join('').split('').filter((char) => char === 'x').length);

      if (numberOfRaisinsInSlice === 1 && sliceIsInBounds && !sliceOverlapsAnotherSlice) {
        evenSlices.push(targetSlice.join('\n'));
        for (let sliceY = row; sliceY < row + length; sliceY++) {
          for (let sliceX = col; sliceX < col + width; sliceX++) {
            cake[sliceY] = setCharAt(cake[sliceY], sliceX, 'x');
          }
        }

        if (solve(row, col + 1)) return true;

        evenSlices.pop();
        for (let sliceY = row; sliceY < row + length; sliceY++) {
          for (let sliceX = col; sliceX < col + width; sliceX++) {
            cake[sliceY] = setCharAt(cake[sliceY], sliceX, targetSlice[sliceY - row][sliceX - col]);
          }
        }
      }
    }
    
    return false;
  } 

  return solve(0, 0) ? evenSlices : [];
}

_____________________________________________________
function cut(cake) {
  
  let area = cake.replace(/\n/g, '').length / cake.match(/[o]/g).length,
    areaRects = [],
    result = [],
    raisinsCords = [];

  if (area - (area >> 0)) return [];
  
  cake = cake.split('\n');
  let cakeW = cake[0].length,
    cakeH = cake.length;
  for (let i = 1; i <= area; i++) {
    let h = area / i;
    if (area % i === 0 && (cakeW % i === 0 || cakeW - i > 1) && (cakeH % h === 0 || cakeH - h > 1)) areaRects.push([i, h]);
  };

  if (areaRects.length === 0) return [];

  for (let i = 0; i < cakeH; i++) {
    for (let ind = 0; ind < cakeW; ind++) {
      if (cake[i][ind] === 'o') {
        raisinsCords.push(ind + i * cakeW);
      }
    }
  }

  function newRect(currentRects, virtualCake) {
    let nextCord = null;
    for (let i = 0; i < virtualCake.length; i++) {
      if (virtualCake[i] === 0) {
        nextCord = i;
        break;
      }
    }
    if (nextCord === null) {
      result = currentRects;
    } else {
      for (let i = 0; i < areaRects.length; i++) {
        if (result.length > 0 && areaRects.length === 0 && result[0][0] > areaRects[i][0]) continue;
        let piece = [],
          rais = [];
        for (let h = 0; h < areaRects[i][1]; h++) {
          for (let w = 0; w < areaRects[i][0]; w++) {
            let cord = nextCord + w + h * cakeW;
            if (raisinsCords.some(el => el === cord)) {
              rais.push(cord)
            }
            if (virtualCake[cord] === 0 && (rais.length === 1 || rais.length === 0)) {
              piece.push(cord);
            } else if (rais.length > 1 || virtualCake[cord] === 1) {
              piece = null;
              break;
            }
          }
          if (piece === null) break;
        }
        if (piece !== null && rais.length > 0) {
          let virtualCakeClone = virtualCake.slice(0);
          for (let ci = 0; ci < piece.length; ci++) {
            virtualCakeClone[piece[ci]] = 1;
          }
          newRect([...currentRects, [areaRects[i][0], areaRects[i][1], rais[0], piece]], virtualCakeClone);
        }
      }
    }
  }

  let virtualCake = [];
  for (let i = 0; i < cakeW * cakeH; i++) {
    virtualCake[i] = 0;
  }
  newRect([], virtualCake);
  result = result.map((elem) => {
    let piece = '';
    for (let i = 0; i < elem[3].length; i++) {
      piece += (elem[3][i] === elem[2]) ? 'o' : '.';
      if ((i + 1) % elem[0] === 0 && i + 1 !== elem[3].length) {
        piece += '\n';
      }
    }
    return piece;
  });

  return result;
}
