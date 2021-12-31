const template = {};
for (let i = 1; i <= 9; i++) {
  template[i] = true;
}
function getIndexes(i) {
  if (i < 3) return [0, 1, 2];
  if (i < 6) return [3, 4, 5];
  return [6, 7, 8];
}
function sudoku(puzzle) {
  let flag = 1;
  while (flag) {
    flag = 0;
    for (let i = 0; i < 9; i++) {
      const quadX = getIndexes(i);
      for (let j = 0; j < 9; j++) {
        const quadY = getIndexes(j);

        if (!puzzle[i][j]) {
          flag = 1;
          puzzle[i][j] = { ...template };
        } else if (typeof puzzle[i][j] == "object") {
          const keys = Object.keys(puzzle[i][j]);
          if (keys.length == 1) {
            puzzle[i][j] = Number(keys[0]);
          } else {
            flag = 1;
            puzzle[i].map((horizontalVal) => {
              delete puzzle[i][j][horizontalVal];
            });
            puzzle.map((row, index) => {
              const verticalVal = row[j];
              delete puzzle[i][j][verticalVal];

              if (quadX.includes(index)) {
                quadY.map((el) => {
                  const quadVal = row[el];
                  delete puzzle[i][j][quadVal];
                });
              }
            });
          }
        } else {
          puzzle[i][j] = Number(puzzle[i][j]);
        }
      }
    }
  }
  return puzzle;
}

___________________________________________________
function getBlockIndex(number) {
  return Math.floor(number / 3);
}

function getPossibilityNumbersSet(mtx, rowIndex, colIndex, row) {
  let r = getBlockIndex(rowIndex) * 3;
  let c = getBlockIndex(colIndex) * 3;

  let excludeds = new Set(row.concat(mtx.map((r) => r[colIndex])));

  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 3; col++) {
      excludeds.add(mtx[r + row][c + col]);
    }
  }

  let poss = new Set();

  for (let i = 1; i < 10; i++) {
    if (!excludeds.has(i)) {
      poss.add(i);
    }
  }

  return poss;
}

function removeFoundedNumberOtherPossibilities(
  number,
  mtx,
  row,
  colIndex,
  rowIndex
) {
  row.forEach((item) => {
    if (item.possibility_items) {
      item.possibility_items.delete(number);
    }
  });

  for (let i = 0; i < mtx.length; i++) {
    const item = mtx[i][colIndex];
    if (item.possibility_items) {
      item.possibility_items.delete(number);
    }
  }

  let r = getBlockIndex(rowIndex) * 3;
  let c = getBlockIndex(colIndex) * 3;

  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 3; col++) {
      const item = mtx[r + row][c + col];
      if (item.possibility_items) {
        item.possibility_items.delete(number);
      }
    }
  }
}

function toPlain(mtx) {
  return mtx.map((row) => row.map((col) => col.item));
}
function sudoku(puzzle) {
  let c = 0;
  let mtx = puzzle.map((row, rowIndex) =>
    row.map((item, colIndex) => {
      if (item === 0) c++;

      return {
        item: item,
        possibility_items:
          item === 0 &&
          getPossibilityNumbersSet(puzzle, rowIndex, colIndex, row),
      };
    })
  );
  while (c) {
    for (let rowIndex = 0; rowIndex < mtx.length; rowIndex++) {
      const row = mtx[rowIndex];
      for (let colIndex = 0; colIndex < row.length; colIndex++) {
        const col = row[colIndex];
        if (col.possibility_items && col.possibility_items.size === 1) {
          col.item = col.possibility_items.keys().next().value;
          col.possibility_items = false;

          removeFoundedNumberOtherPossibilities(
            col.item,
            mtx,
            row,
            colIndex,
            rowIndex
          );
          c--;

          if (c === 0) {
            return toPlain(mtx);
          }
        }
      }
    }
  }
  return toPlain(mtx);
}

___________________________________________________
function sudoku(puzzle) {
  while(checkPuzzle(puzzle)){
    for(let r = 0; r < puzzle.length; r++){
      for(let c = 0; c < puzzle.length; c++){
        if(puzzle[r][c] == 0){
          let ch = checkPosition(puzzle, r, c)
          if(ch > 0){
            puzzle[r][c] = ch
          }
        }
      }
    }
  }
  return puzzle
}

let checkPuzzle = (puzzle) =>  puzzle.some(row => row.reduce((sum, v) => sum + v) < 45)

let checkPosition = (puzzle, row, column) => {
  let square = []
  squares(row).forEach(r => squares(column).forEach(c => square.push(puzzle[r][c])))
  let c = puzzle.map(r => r[column])
  let p = [1,2,3,4,5,6,7,8,9]
    .filter(n => !puzzle[row].includes(n))
    .filter(n => !c.includes(n))
    .filter(n => !square.includes(n))
  return p.length == 1 ? p[0] : 0
}

let squares = (nb) => {
  if(nb < 3) return [0,1,2]
  else if(nb < 6) return [3,4,5]
  else return [6,7,8]
}

___________________________________________________
function sudoku(puzzle) {
   const sudoku = puzzle.map(row => row.map(cell => !cell ? new Set() : cell))
   const getRow = x => sudoku[x].filter(cell => typeof cell === 'number'),
         getCol = y => sudoku.reduce((c, v) => c.concat(typeof v[y] === 'number' ? v[y] : []), [] ),
         getSqr = (x, y) => sudoku.slice(x - x % 3, x - x % 3 + 3)
                                  .reduce((c, v) => c.concat(v.slice( y - y % 3, y - y % 3 + 3)), [])
                                  .filter(cell => typeof cell === 'number')
     let zeroCount = puzzle.reduce((c, row) => c + row.filter(e => !e).length, 0)
     
   while (true){
     sudoku.forEach((row, x) => row.forEach((cell, y) => {
       if (typeof cell !== 'number') sudoku[x][y] = new Set(getRow(x).concat(getCol(y), getSqr(x,y)))
     }))
     
     sudoku.forEach((row, x) => row.forEach((cell, y) => {
       if (typeof cell !== 'number' && cell.size === 8) {
          sudoku[x][y] = 45 - [...cell].reduce((c, v) => c + v)
          zeroCount--
       }
     }))
     if (!zeroCount) return sudoku
   }
}

___________________________________________________
function sudoku(puzzle) {
  
  let solved = false
  
  let possibleNos = []
  
  for (let i = 0; i < 9; i++) {
    
    possibleNos[i] = []
    
    for (let j = 0; j < 9; j++) {
      
      if (puzzle[i][j] === 0) {
      
        possibleNos[i][j] = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}
        
      } else {
        
        possibleNos[i][j] = {[puzzle[i][j]]: puzzle[i][j]}
        
      }
      
    }
    
  }
  
  while (solved === false) {

    for (let i = 0; i < 9; i++) {

      for (let j = 0; j < 9; j++) {

        for (let k = 0; k < 9; k++) {

          if (possibleNos[i][j].hasOwnProperty(puzzle[k][j].toString()) && k !== i) {

            delete possibleNos[i][j][puzzle[k][j]]

          }

        }

        for (let k = 0; k < 9; k++) {

          if (possibleNos[i][j].hasOwnProperty(puzzle[i][k]) & k !== j) {

            delete possibleNos[i][j][puzzle[i][k]]

          }

        }

        let iThird = Math.floor(i / 3)
        let jThird = Math.floor(j / 3)

        for (let k = iThird * 3; k < iThird * 3 + 3; k++) {

          for (let l = jThird * 3; l < jThird * 3 + 3; l++) {

            if (k !== i || l !== j) {

              if (possibleNos[i][j].hasOwnProperty(puzzle[k][l])) {

                delete possibleNos[i][j][puzzle[k][l]]

              }

            }

          }

        }

      }

    }

    for (let i = 0; i < 9; i++) {

      for (let j = 0; j < 9; j++) {

        if (Object.keys(possibleNos[i][j]).length === 1) {

          puzzle[i][j] = parseInt(Object.keys(possibleNos[i][j])[0])

        }

      }

    }

    for (let i = 0; i < 9; i++) {

      for (let num = 1; num < 10; num ++) {

        let count = 0

        let tracker = 0

        for (let j = 0; j < 9; j++) {

          if (possibleNos[i][j].hasOwnProperty(num)) {

            count++

            tracker = j

          }

        }

        if (count === 1) {

          puzzle[i][tracker] = num

          possibleNos[i][tracker] = {[num]: num}

        }

      }

    }

    for (let j = 0; j < 9; j++) {

      for (let num = 1; num < 10; num ++) {

        let count = 0

        let tracker = 0

        for (let i = 0; i < 9; i++) {

          if (possibleNos[i][j].hasOwnProperty(num)) {

            count++

            tracker = i

          }

        }

        if (count === 1) {

          puzzle[tracker][j] = num

          possibleNos[tracker][j] = {[num]: num}

        }

      }

    }

    for (let iThird = 0; iThird < 3; iThird++) {

      for (let jThird = 0; jThird < 3; jThird++) {

        for (let num = 1; num < 10; num++) {

          let count = 0

          let trackerI = 0

          let trackerJ = 0

          for (let i = iThird * 3; i < iThird * 3 + 3; i++) {

            for (let j = jThird * 3; j < jThird * 3 + 3; j++) {

              if (possibleNos[i][j].hasOwnProperty(num)) {

                count++

                trackerI = i

                trackerJ = j

              }

            }

          }

          if (count === 1) {

            puzzle[trackerI][trackerJ] = num
            possibleNos[trackerI][trackerJ] = {[num]: num}

          }

        }

      }

    }
    
    let zeroFound = false
    
    for (let i = 0; i < 9; i++) {
      
      for (let j = 0; j < 9; j++) {
        
        if (puzzle[i][j] === 0) {
          
          zeroFound = true
          
        }
        
      }
      
    }
    
    if (zeroFound === false) {
      
      solved = true
      
    }
  
  }
  
  return puzzle
  
}
