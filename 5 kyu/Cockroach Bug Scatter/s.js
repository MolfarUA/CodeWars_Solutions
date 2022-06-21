59aac7a9485a4dd82e00003e


function cockroaches(room) {
  var holes=[0,0,0,0,0,0,0,0,0,0],w=room[0].length,h=room.length
  for(var i=0;i<h;i++)
    for(var j=0;j<w;j++)
      if("UDLR".includes(room[i][j])) holes[goto(room[i][j],i,j)]++
  return holes
  
  function goto(s,x,y){
    switch(s){
      case"U":
        while(room[0][y]=="-") y--
        return /\d/.test(room[0][y])?+room[0][y]:goto("L",1,1)
      case"D":
        while(room[h-1][y]=="-") y++
        return /\d/.test(room[h-1][y])?+room[h-1][y]:goto("R",h-2,w-2)
      case"L":
        while(room[x][0]=="|") x++
        return /\d/.test(room[x][0])?+room[x][0]:goto("D",h-2,1)
      case"R":
        while(room[x][w-1]=="|") x--
        return /\d/.test(room[x][w-1])?+room[x][w-1]:goto("U",1,w-2)
    }
  }
}
________________________________
function cockroaches(room) {
  const rows = room.length;
  const cols = room[0].length;
  const walls = [
    ...room.map(r => r[0]),
    ...room[rows - 1],
    ...room.map(r => r[cols - 1]).reverse(),
    ...room[0].reverse(),
  ].join('').repeat(2);

  const counts = new Array(10).fill(0);
  room.forEach((r, i) => {
    r.forEach((e, j) => {
      const start = (e === 'L' && i)
      || (e === 'D' && rows + j)
      || (e === 'R' && 2 * rows + cols - i - 1)
      || (e === 'U' && 2 * rows + 2 * cols - j - 1)
      || 0;
      if (start) {
        const hole = walls.substring(start).match(/\d/);
        counts[hole]++;
      }
    });
  });
  return counts;
}
________________________________
function cockroaches(room) {
    let arr = new Array(10).fill(0);

    for (let i = 1; i < room.length - 1; i++) {
        let str = room[i];
        for (let j = 1; j < str.length - 1; j++) {
            let cockroach;
            if (str[j] != ' ') {
                cockroach = str[j];
                let newI = i, newJ = j;
                let flag = false;
                while (!flag) {
                    switch (cockroach) {
                        case 'U':
                            let u;
                            for (u = newI - 1; u >= 0; u--) {
                                let char = room[u][newJ];
                                if (+char >= 0 && +char <= 9 && char !== ' ') {
                                    arr[char] += 1;
                                    flag = true;
                                    break;
                                } else if (char == '+' || char == '-') {
                                    cockroach = 'L';
                                    break
                                } else {
                                    continue;
                                }
                            }
                            newI = u;
                            break;
                        case 'D':
                            let d;
                            for (d = newI + 1; d < room.length; d++) {
                                let char = room[d][newJ];
                                if (+char >= 0 && +char <= 9 && char !== ' ') {
                                    arr[char] += 1;
                                    flag = true;
                                    break;
                                } else if (char == '+' || char == '-') {
                                    cockroach = 'R';
                                    break;
                                } else {
                                    continue;
                                }
                            }
                            newI = d;
                            break;
                        case 'L':
                            let l;
                            for (l = newJ - 1; l >= 0; l--) {
                                let char = room[newI][l];
                                if (+char >= 0 && +char <= 9 && char !== ' ') {
                                    arr[char] += 1;
                                    flag = true;
                                    break;
                                } else if (char == '+' || char == '|') {
                                    cockroach = 'D';
                                    break;
                                } else {
                                    continue;
                                }
                            }
                            newJ = l;
                            break;
                        case 'R':
                            let r;
                            for (r = newJ + 1; r < str.length; r++) {
                                let char = room[newI][r];
                                if (+char >= 0 && +char <= 9 && char !== ' ') {
                                    arr[char] += 1;
                                    flag = true;
                                    break;
                                } else if (char == '+' || char == '|') {
                                    cockroach = 'U';
                                    break;
                                } else {
                                    continue;
                                }
                            }
                            newJ = r;
                            break;
                    }
                }
            }
        }
    }
    return arr;
}
