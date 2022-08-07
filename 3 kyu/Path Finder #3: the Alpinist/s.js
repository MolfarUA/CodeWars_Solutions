576986639772456f6f00030c


function pathFinder(area){
  let a = area.split('\n'),
    max = a.length - 1,
    cost = a.map(e => [...e].fill(1e5)),
    best = 1e5,
    go = (lastAlt, oldSum, y, x) => {
      let alt = a[y][x]
      let sum = oldSum + Math.abs(alt - lastAlt)
      if (sum >= best || sum >= cost[y][x]) return
      if (y == max && x == max) return best = sum
      cost[y][x] = sum
      if (x < max) go(alt, sum, y, x + 1)
      if (y < max) go(alt, sum, y + 1, x)
      if (y > 0) go(alt, sum, y - 1, x)
      if (x > 0) go(alt, sum, y, x - 1)
    }
  go(a[0][0], 0, 0, 0)
  return best
}
_____________________________
function pathFinder(area) {
    if (area.length === 1) return 0
    const zone = area.split('\n').map(x => x.split(''))
    const n = zone.length, coordDists = {}, q = [ [0,0,0] ], ext = new Set()
    for (let r = 0; r < n; r++)
        for (let c = 0; c < n; c++)
            coordDists[r+':'+c] = 1e9
            
    const distanceToGoal =(row,col)=> ((n-1-row)**2 + (n-1-col)**2)**0.5
    let result = 1e9
    while (q.length) {
        q.sort((a,b)=>a[0]-b[0])
        let p = q.shift(), r = p[1], c = p[2]
        ext.add(r+':'+c)
        for (let d of [[1,0],[-1,0],[0,1],[0,-1]]) {
            let R = r+d[0], C = c+d[1]
            if (0 <= R&&R < n && 0 <= C&&C < n && !ext.has(R+':'+C)) {
                let traversalCost = Math.abs(+zone[R][C] - +zone[r][c])
                let totalDist = traversalCost + p[0]
                if (totalDist >= coordDists[R+':'+C]) continue
                coordDists[R+':'+C] = totalDist
                q.push([totalDist,R,C])
            }
        }
    }
    return coordDists[(n-1)+':'+(n-1)]
}
_____________________________
function pathFinder(maze) {
    let map = maze.split('\n').map(s => [...s].map(x => +x))
    let n = map.length
    let m = map[0].length
    let space = [...Array(n)].map(i => [...Array(m)].fill(Infinity))

    function Node(i, j, cost) {
        this.i = i
        this.j = j
        this.cost = cost
    }

    let nodes = [new Node(0, 0, 0)]
    space[0][0] = 0

    let di = [0, -1, 0, 1]
    let dj = [-1, 0, 1, 0]
    while (nodes.length > 0) {
        let min = nodes[0].cost
        let minIndex = 0
        for (let k = 1; k < nodes.length; k++) {
            if (nodes[k].cost < min) {
                min = nodes[k].cost
                minIndex = k
            }
        }
        let cur = nodes.splice(minIndex, 1)[0]
        if (cur.i == n - 1 && cur.j == m - 1) {
            return cur.cost
        }
        for (let k = 0; k < 4; k++) {
            let i1 = cur.i + di[k]
            let j1 = cur.j + dj[k]
            let t = space[i1]
            if (!t || t[j1] === undefined) {
                continue
            }
            let cost = cur.cost + Math.abs(map[i1][j1] - map[cur.i][cur.j])
            if (cost < t[j1]) {
                t[j1] = cost
                nodes.push(new Node(i1, j1, cost))
            }
        }
    }

    return space[n - 1][m - 1]
}
