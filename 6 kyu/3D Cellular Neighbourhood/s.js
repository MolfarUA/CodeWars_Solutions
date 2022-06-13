function getNeighbourhood(type, m, coor, dist = 1) {
    if (m[0][0].length == 0 || dist == 0 || m[coor[0]] === undefined || m[coor[0]][coor[1]] === undefined || m[coor[0]][coor[1]][coor[2]] === undefined) return []

    let res = []
    for (let i = 0; i < m.length; i++) {
        for (let j = 0; j < m[i].length; j++) {
            for (let k = 0; k < m[i][j].length; k++) {
                if (checkDist([i,j,k],coor,type) <= dist && checkDist([i,j,k],coor,type) > 0) {
                    res.push(m[i][j][k])
                }
            }
        }
    }
    return res
}

function checkDist(cur,start,type) {
    let difference = cur.map((e,i)=>Math.abs(e-start[i])) //?
    if (type == 'moore') {
        return Math.max(...difference)
    } else {
        return difference.reduce((s,e)=> s += e,0)
    }
}
_______________________________
const getNeighbourhood = ([t], m, [z, y, x], r = 1) => {
  if (!(z in m && y in m[0] && x in m[0][0]))
    return [];
  const f = { m: (i, j, k) => Math.max(Math.abs(z - i), Math.abs(y - j), Math.abs(x - k)), v: (i, j, k) => Math.abs(z - i) + Math.abs(y - j) + Math.abs(x - k) }[t];
  const n = [];
  for (let i = 0; i < m.length; i++) {
    for (let j = 0; j < m[i].length; j++) {
      for (let k = 0; k < m[i][j].length; k++) {
        const d = f(i, j, k);
        if (0 < d && d <= r) {
          n.push(m[i][j][k]);
        }
      }
    }
  }
  return n;
}
_______________________________
const getNeighbourhood = ([type], matrix, [z, y, x], distance = 1) => {
  if (z < 0 || y < 0 || x < 0 || z >= matrix.length || y >= matrix[0].length || x >= matrix[0][0].length || distance <= 0)
    return [];
  const getDistance = { m: (i, j, k) => Math.max(Math.abs(z - i), Math.abs(y - j), Math.abs(x - k)), v: (i, j, k) => Math.abs(z - i) + Math.abs(y - j) + Math.abs(x - k), }[type];
  const neighbourhood = [];
  for (let i = 0; i < matrix.length; i++) {
    for (let j = 0; j < matrix[i].length; j++) {
      for (let k = 0; k < matrix[i][j].length; k++) {
        const d = getDistance(i, j, k);
        if (0 < d && d <= distance) {
          neighbourhood.push(matrix[i][j][k]);
        }
      }
    }
  }
  return neighbourhood;
}
