58738d518ec3b4bf95000192


function execute(code) {
    if (code.includes('(')) {
        const a = code.lastIndexOf('('), b = code.indexOf(')', a)
        const n = (code.slice(b+1).match(/^\d+/)||[''])[0]
        const x = n === '0' ? 0 : +n || 1
        return execute(
          code.slice(0,a) + code.slice(a+1,b).repeat(x) + code.slice(b+1+(n ? n : '').length))
    }
    code = code.replace(/[LFR]\d+/g, m => m[0].repeat(+m.slice(1)))
    const dir = [[0,1],[1,0],[0,-1],[-1,0]], robot = {r:0,c:0,d:0}, points = new Set([robot.r+','+robot.c])
    let l = 0, r = 0, u = 0, d = 0
    ;[...code].forEach(c => {
        if (c === 'F') {
            robot.r += dir[robot.d][0]
            robot.c += dir[robot.d][1]
            d = Math.max(d,robot.r)
            u = Math.min(u,robot.r)
            r = Math.max(r,robot.c)
            l = Math.min(l,robot.c)
            points.add(robot.r+','+robot.c)
        } else 
            robot.d = (robot.d + (c === 'L' ? 3 : 1)) % 4
    })
    return [...Array(d-u+1)].map((_,y) => 
             [...Array(r-l+1)].map((v,x) => 
               points.has((y+u)+','+(x+l)) ? '*' : ' ').join``
             ).join`\r\n`
}
__________________________
function execute(c) {
  console.log(c);
  var code = c;
  while (/\(([FLR0-9]+)\)([0-9]+)/.test(code)) code = code.replace(/\(([FLR0-9]+)\)([0-9]+)/, (m, s, t) => s.repeat(+t));
  code = code.replace(/\(|\)/g, "");
  code = code.replace(/[FLR][0-9]+/g, s => s[0].repeat(parseInt(s.slice(1))));
  var directions = ["right", "down", "left", "up"];
  var directionIndex = 0;
  var grid = [[0]];
  var robot = {x: 0, y: 0};
  grid[robot.y][robot.x] = 1;
  for (var i = 0; i < code.length; i++) {
    switch (code[i]) {
      case "R":
      directionIndex = (directionIndex + 1) % 4;
      break;
      case "L":
      directionIndex = (directionIndex + 3) % 4;
      break;
      case "F":
      switch (directions[directionIndex]) {
        case "right":
        robot.x++;
        if (robot.x >= grid[robot.y].length) {
          for (var k = 0; k < grid.length; k++) grid[k].push(0);
        }
        break;
        case "down":
        robot.y++;
        if (robot.y >= grid.length) grid.push(Array(grid[0].length).fill(0));
        break;
        case "left":
        robot.x--;
        if (robot.x < 0) {
          for (var k = 0; k < grid.length; k++) grid[k] = [0].concat(grid[k]);
          robot.x++;
        }
        break;
        case "up":
        robot.y--;
        if (robot.y < 0) {
          grid = [Array(grid[0].length).fill(0)].concat(grid);
          robot.y++;
        }
        break;
      }
      grid[robot.y][robot.x] = 1;
      break;
    }
  }
  return grid.map(r => r.map(s => s === 1 ? "*" : " ").join("")).join("\r\n");
}
__________________________
function execute(c) {
  var code = c;
  while (/\(([FLR0-9]+)\)([0-9]+)/.test(code)) code = code.replace(/\(([FLR0-9]+)\)([0-9]+)/, (m, s, t) => s.repeat(+t));
  code = code.replace(/\(|\)/g, "");
  code = code.replace(/[FLR][0-9]+/g, s => s[0].repeat(parseInt(s.slice(1))));
  var directions = ["right", "down", "left", "up"];
  var directionIndex = 0;
  var grid = [[0]];
  var robot = {x: 0, y: 0};
  grid[robot.y][robot.x] = 1;
  for (var i = 0; i < code.length; i++) {
    switch (code[i]) {
      case "R":
      directionIndex = (directionIndex + 1) % 4;
      break;
      case "L":
      directionIndex = (directionIndex + 3) % 4;
      break;
      case "F":
      switch (directions[directionIndex]) {
        case "right":
        robot.x++;
        if (robot.x >= grid[robot.y].length) {
          for (var k = 0; k < grid.length; k++) grid[k].push(0);
        }
        break;
        case "down":
        robot.y++;
        if (robot.y >= grid.length) grid.push(Array(grid[0].length).fill(0));
        break;
        case "left":
        robot.x--;
        if (robot.x < 0) {
          for (var k = 0; k < grid.length; k++) grid[k] = [0].concat(grid[k]);
          robot.x++;
        }
        break;
        case "up":
        robot.y--;
        if (robot.y < 0) {
          grid = [Array(grid[0].length).fill(0)].concat(grid);
          robot.y++;
        }
        break;
      }
      grid[robot.y][robot.x] = 1;
      break;
    }
  }
  return grid.map(r => r.map(s => s === 1 ? "*" : " ").join("")).join("\r\n");
}
