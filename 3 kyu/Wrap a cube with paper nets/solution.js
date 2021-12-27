//just modified my solution from kata 'Folding a cube' 
//I indexed cube in a way that oposite faces are 0-3, 1-4, 2-5
//from which faces to which ones we could get and how (in (counter)clockwise order):
var paths = [[1,2,4,5],[0,5,3,2],[0,1,3,4],[1,5,4,2],[0,2,3,5],[0,4,3,1]];
var directions = [[1, 0], [0, 1], [-1, 0], [0, -1]];

var wrap_cube = function(shape) {
  let net = shape.split('\n').map(s => [...s]);
  let faces = new Array(6).fill().map(() => []);//what we already wrapped
  let check = new Set;
  let problem = false;
  function wrap(dirFrom, faceFrom, face, x, y, firstCall = false){
    if (!net[y] || !net[y][x] || net[y][x] == ' ') return;//we are not in net
    if (check.has(y+'|'+x)) return problem = true; //returned to the same point
    faces[face].push(net[y][x]);
    check.add(y+'|'+x);
    let path = paths[face];
    let faceI = path.indexOf(faceFrom);
    for (let i = 0; i < 4; ++i){
      let dirI = (dirFrom + 2 + i) % 4;//+2 cause to return to 'faceFrom' we should go opposite way to dirFrom
      let pathI = (faceI + i) % 4;
      if (firstCall || (dirI != (dirFrom + 2) % 4))
        wrap(dirI, face, path[pathI], x + directions[dirI][0], y + directions[dirI][1]);
    }
  }
  let x0 , y0;
  y0 = net.findIndex(e => -1 != (x0 = e.findIndex(s => s != ' ')));
  wrap(0, 1, 0, x0, y0, true);
  return problem ? null : faces.filter(x => x.length > 1);
};

#######################
const pos3d = {
    FRONT: "front",
    BACK: "back",
    TOP: "top",
    BOTTOM: "bottom",
    LEFT: "left",
    RIGHT: "right",
}

const pos2d = {
    TOP: "top",
    RIGHT: "right",
    LEFT: "left",
    BOTTOM: "bottom"
}

const coveredSides = {
    [pos3d.FRONT]: [],
    [pos3d.BACK]: [],
    [pos3d.TOP]: [],
    [pos3d.BOTTOM]: [],
    [pos3d.LEFT]: [],
    [pos3d.RIGHT]: [],
};

const pos3dDerivation = [
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},
];

let hasLoop;

function getPos3d(prev, move2d) {
    return pos3dDerivation.find(x => x.prev[0] === prev[0] && x.prev[1] === prev[1] && x.pos2d === move2d).pos3d;
}

function clone(matrix) {
    const matrix2 = [...matrix]
    matrix2.forEach((row, rowIndex) => matrix2[rowIndex] = [...row])
    return matrix2;
}

function rotateLeft(matrix, x, y) {
    matrix = matrix.map((row, rowIndex) => row.map((_, colIndex) => matrix[colIndex][row.length - 1 - rowIndex]));
    let temp = x;
    x = matrix[0].length - 1 - y;
    y = temp;
    return {matrix, x, y}
}

function rotateRight(matrix, x, y) {
    matrix = matrix.map((row, rowIndex) => row.map((_, colIndex) => matrix[matrix[0].length - 1 - colIndex][rowIndex]));
    let temp = y;
    y = matrix.length - 1 - x;
    x = temp;
    return {matrix, x, y}
}

class CubeSide {

    constructor(matrix, x, y, pos3d, prevPos3d) {
        this.matrix = matrix;
        this.x = x;
        this.y = y;
        this.pos3d = pos3d;
        this.prevPos3d = prevPos3d;
    }

    process() {
        if (hasLoop) {
            return;
        }

        for (const key of Object.keys(coveredSides)) {
            if (coveredSides[key].findIndex(x => x === this.matrix[this.x][this.y]) > -1) {
                hasLoop = true;
                return;
            }
        }

        coveredSides[this.pos3d].push(this.matrix[this.x][this.y]);

        // process top
        if (this.x > 0 &&
            this.matrix[this.x - 1][this.y] !== " ") {
            new CubeSide(clone(this.matrix), this.x - 1, this.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.TOP), this.pos3d).process();
        }

        // process left
        if (this.y > 0 &&
            this.matrix[this.x][this.y - 1] !== " ") {
            const rotated = rotateRight(this.matrix, this.x, this.y);
            new CubeSide(rotated.matrix, rotated.x - 1, rotated.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.LEFT), this.pos3d).process();
        }

        // process right
        if (this.y < this.matrix[0].length - 1 &&
            this.matrix[this.x][this.y + 1] !== " ") {
            const rotated = rotateLeft(this.matrix, this.x, this.y);
            new CubeSide(rotated.matrix, rotated.x - 1, rotated.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.RIGHT), this.pos3d).process();
        }
    }
}

function mapStringToMatrix(string) {
    const arr = string.split("\n").filter(x => x.length);
    const numberOfCols = arr.reduce((x, y) => x.length > y.length ? x : y).length;
    const numberOfRows = arr.length;
    const max = Math.max(numberOfCols, numberOfRows);

    const matrix = arr.map(x => x.padEnd(max, " ").split(""));
    while (matrix.length < max) {
        matrix.push(Array(max).fill(" "));
    }
    return matrix;
}

function findStartingPoint(matrix) {
    for (let x = matrix.length - 1; x >= 0; x--) {
        for (let y = 0; y < matrix[0].length; y++) {
            if (matrix[x][y] !== " ") {
                return {x, y};
            }
        }
    }
    return null;
}

const wrap_cube = function (shape) {

    const result = [];
    for (const key of Object.keys(coveredSides)) {
        coveredSides[key] = [];
    }
    hasLoop = false;

    const matrix = mapStringToMatrix(shape);
    const startingPoint = findStartingPoint(matrix);
    new CubeSide(matrix, startingPoint.x, startingPoint.y, pos3d.FRONT, pos3d.BOTTOM).process();

    if (hasLoop) {
        return null;
    }

    Object.values(coveredSides).forEach(x => {
        if (x.length > 1) {
            result.push(x)
        }
    });

    return result;
}


##############################
const pos3d = {
    FRONT: "front",
    BACK: "back",
    TOP: "top",
    BOTTOM: "bottom",
    LEFT: "left",
    RIGHT: "right",
}

const pos2d = {
    TOP: "top",
    RIGHT: "right",
    LEFT: "left",
    BOTTOM: "bottom"
}

const coveredSides = {
    [pos3d.FRONT]: [],
    [pos3d.BACK]: [],
    [pos3d.TOP]: [],
    [pos3d.BOTTOM]: [],
    [pos3d.LEFT]: [],
    [pos3d.RIGHT]: [],
};

const pos3dDerivation = [
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.BACK], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.FRONT], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.TOP], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.RIGHT},
    {prev: [pos3d.LEFT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.LEFT},
    {prev: [pos3d.RIGHT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.RIGHT},
    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.LEFT},

    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.LEFT, pos3d: pos3d.LEFT},
    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.BOTTOM], pos2d: pos2d.RIGHT, pos3d: pos3d.RIGHT},

    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},

    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.LEFT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.BACK},
    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.TOP, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.FRONT},

    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.FRONT},
    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.TOP},
    {prev: [pos3d.BOTTOM, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.BACK},

    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.TOP},
    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.BACK},
    {prev: [pos3d.FRONT, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.BOTTOM},

    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.LEFT, pos3d: pos3d.BOTTOM},
    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.TOP, pos3d: pos3d.FRONT},
    {prev: [pos3d.BACK, pos3d.RIGHT], pos2d: pos2d.RIGHT, pos3d: pos3d.TOP},
];

let hasLoop;

function getPos3d(prev, move2d) {
    return pos3dDerivation.find(x => x.prev[0] === prev[0] && x.prev[1] === prev[1] && x.pos2d === move2d).pos3d;
}

function clone(matrix) {
    const matrix2 = [...matrix]
    matrix2.forEach((row, rowIndex) => matrix2[rowIndex] = [...row])
    return matrix2;
}

function rotateLeft(matrix, x, y) {
    matrix = matrix.map((row, rowIndex) => row.map((_, colIndex) => matrix[colIndex][row.length - 1 - rowIndex]));
    let temp = x;
    x = matrix[0].length - 1 - y;
    y = temp;
    return {matrix, x, y}
}

function rotateRight(matrix, x, y) {
    matrix = matrix.map((row, rowIndex) => row.map((_, colIndex) => matrix[matrix[0].length - 1 - colIndex][rowIndex]));
    let temp = y;
    y = matrix.length - 1 - x;
    x = temp;
    return {matrix, x, y}
}

class CubeSide {

    constructor(matrix, x, y, pos3d, prevPos3d) {
        this.matrix = matrix;
        this.x = x;
        this.y = y;
        this.pos3d = pos3d;
        this.prevPos3d = prevPos3d;
    }

    process() {
        if (hasLoop) {
            return;
        }

        for (const key of Object.keys(coveredSides)) {
            if (coveredSides[key].findIndex(x => x === this.matrix[this.x][this.y]) > -1) {
                hasLoop = true;
                return;
            }
        }

        coveredSides[this.pos3d].push(this.matrix[this.x][this.y]);

        // process top
        if (this.x > 0 &&
            this.matrix[this.x - 1][this.y] !== " ") {
            new CubeSide(clone(this.matrix), this.x - 1, this.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.TOP), this.pos3d).process();
        }

        // process left
        if (this.y > 0 &&
            this.matrix[this.x][this.y - 1] !== " ") {
            const rotated = rotateRight(this.matrix, this.x, this.y);
            new CubeSide(rotated.matrix, rotated.x - 1, rotated.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.LEFT), this.pos3d).process();
        }

        // process right
        if (this.y < this.matrix[0].length - 1 &&
            this.matrix[this.x][this.y + 1] !== " ") {
            const rotated = rotateLeft(this.matrix, this.x, this.y);
            new CubeSide(rotated.matrix, rotated.x - 1, rotated.y, getPos3d([this.prevPos3d, this.pos3d], pos2d.RIGHT), this.pos3d).process();
        }
    }
}

function mapStringToMatrix(string) {
    const arr = string.split("\n").filter(x => x.length);
    const numberOfCols = arr.reduce((x, y) => x.length > y.length ? x : y).length;
    const numberOfRows = arr.length;
    const max = Math.max(numberOfCols, numberOfRows);

    const matrix = arr.map(x => x.padEnd(max, " ").split(""));
    while (matrix.length < max) {
        matrix.push(Array(max).fill(" "));
    }
    return matrix;
}

function findStartingPoint(matrix) {
    for (let x = matrix.length - 1; x >= 0; x--) {
        for (let y = 0; y < matrix[0].length; y++) {
            if (matrix[x][y] !== " ") {
                return {x, y};
            }
        }
    }
    return null;
}

const wrap_cube = function (shape) {

    const result = [];
    for (const key of Object.keys(coveredSides)) {
        coveredSides[key] = [];
    }
    hasLoop = false;

    const matrix = mapStringToMatrix(shape);
    const startingPoint = findStartingPoint(matrix);
    new CubeSide(matrix, startingPoint.x, startingPoint.y, pos3d.FRONT, pos3d.BOTTOM).process();

    if (hasLoop) {
        return null;
    }

    Object.values(coveredSides).forEach(x => {
        if (x.length > 1) {
            result.push(x)
        }
    });

    return result;
}


##################################
var wrap_cube = function(shape) {
  
  // How about a game of reverse golf? ;)
  
  // The only way I could figure out how to do this is to look for four conditions on four rotations of six cube faces.
  // Thus a 24 part switch case statement which itself has four branching conditions each.
  
  let workingShape = shape
  let re = /\n/gi // Exclude the line returns.
  let regular = workingShape.replace(re, '')
  let territories = []
   
  // Put unique territories on each member of an array
  for (let i = 0; i < regular.length; i++){
    if (!territories.includes(regular.charAt(i)) && (regular.charAt(i) !== ' '))
      territories.push(regular.charAt(i))
  }
  
  let x = 0
  let y = 0
  let counter = 0
  let grid = []
  let max = 0
  let originX = null
  let originY = null

  grid[0] = []
  for (let i = 0; i < workingShape.length; i++){
    if (workingShape.charAt(i) === regular.charAt(counter)){
      grid[y][x] = workingShape.charAt(i)
      if ((originX === null) && (workingShape.charAt(i) !== ' ') && (workingShape.charAt(i) !== []))
        originX = x
      if ((originY === null) && (workingShape.charAt(i) !== ' ') && (workingShape.charAt(i) !== []))
        originY = y
      counter++
      x++
      if (x > max)
        max = x
    } else { // line break
      x = 0
      y++
      grid[y] = []   
    }
  }
    
  for (let y = 0; y < grid.length; y++){ // Debugging.  Output a tighter version of the field.
    for (let x = 0; x < max; x ++)
      if (grid[y][x] === undefined)
        process.stdout.write('')
      else
        process.stdout.write(grid[y][x] + " ")

    console.log('')
    }
  
  let flag = false
  let loopVisit = []
  
  function findLoop(x1, y1, fromX, fromY){
    fromX = fromX * -1 // opposite direction
    fromY = fromY * -1
    if (loopVisit.includes(grid[y1][x1])){
      flag = true
      return
    }
    loopVisit.push(grid[y1][x1])
    if (loopVisit.length > (territories.length)){
      return
    }
    //        [y, x]    up      right   down    left
    const iterator = [[-1, 0], [0, 1], [1, 0], [0, -1]]
      for (let i = 0; i < 4; i++)
        if ((iterator[i][1] + x1 >= 0) && (iterator[i][0] + y1 >= 0) && (iterator[i][1] + x1 < max) && (iterator[i][0] + y1 < grid.length))
          if (grid[iterator[i][0] + y1][iterator[i][1] + x1])
            if (grid[iterator[i][0] + y1][iterator[i][1] + x1] !== ' ')
              if (!((iterator[i][0] === fromY) && (iterator[i][1] === fromX)) || ((fromX === 0) && (fromY === 0)))
                findLoop(iterator[i][1] + x1, iterator[i][0] + y1, iterator[i][1], iterator[i][0])   
    return
  }
  
  findLoop(originX, originY, 0, 0)
  if (flag)
    return null 
  
  // Search for groups of four: a loop without a hole (not needeed)
/*  const cornerIterator = [[0, 1], [1, 1], [1, 0]]
  for (let y = 0; y < grid.length - 1; y++)
    for (let x = 0; x < max - 1; x++)
      if (grid[y][x])
        if (grid[y][x] !== ' '){
          flag = true
          for (let i = 0; i < 3; i++){
            if (!(grid[y + cornerIterator[i][0]][x + cornerIterator[i][1]])) // if data doesn't exist
              flag = false
            if (grid[y + cornerIterator[i][0]][x + cornerIterator[i][1]] === ' ') // if a space character exists
              flag = false
            } // next i
          if (flag)
            return null
          } // if no space
  */
  let front = []
  let left = []
  let right = []
  let top = []
  let bottom = []
  let back = []
  let visited = []
  
  function visit(condition, x1, y1){
    visited.push(grid[y1][x1])
    if (visited.length >= territories.length)
      return
    
    //        [y, x]    up      right   down    left
    const iterator = [[-1, 0], [0, 1], [1, 0], [0, -1]]
      for (let i = 0; i < 4; i++)
        if ((iterator[i][1] + x1 >= 0) && (iterator[i][0] + y1 >= 0) && (iterator[i][1] + x1 < max) && (iterator[i][0] + y1 < grid.length))
          if (grid[iterator[i][0] + y1][iterator[i][1] + x1])
            if (grid[iterator[i][0] + y1][iterator[i][1] + x1] !== ' ')
              if (!visited.includes(grid[iterator[i][0] + y1][iterator[i][1] + x1]))
              {
                switch(condition){
                  case 1: // Front face, top up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(5, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the right face
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(22, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the bottom face
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(15, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the left face
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(17, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 2: // Front face, top down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(16, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the left face
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(18, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the top face
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(6, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the right face
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(21, iterator[i][1] + x1, iterator[i][0] + y1) // Move to the bottom face
                    }
                    break
                  case 3: // Front face, top left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(23, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])  
                      visit(13, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(20, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(8, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 4: // Front face, top right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(19, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(7, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(24, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(14, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 5: // Right face, top up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(9, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(23, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(1, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(19, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 6: // Right face, top down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(2, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(20, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(10, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(24, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 7: // Right face, top right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(18, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(11, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(22, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(4, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 8: // Right face, top left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(21, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(3, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(17, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(12, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 9: // Back face, top up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(15, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(21, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(5, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(18, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 10: // Back face, top down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(6, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(17, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(16, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(22, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 11: // Back face, top right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(20, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(14, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(23, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(7, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 12: // Left face, top left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(24, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(8, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(19, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(13, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break                  
                  case 13: // Back face, top left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(22, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(12, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(18, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(3, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 14: // Left face, top right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(17, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(4, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(21, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(11, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 15: // Left face, top up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(1, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(24, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(9, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(20, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 16: // Left face, top down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(10, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      top.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(19, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(2, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      bottom.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(23, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 17: // Top face, back up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(8, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(1, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(14, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(10, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 18: // Top face, back down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(13, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(9, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(7, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(2, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 19: // Top face, back right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(12, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(5, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(4, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(16, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 20: // Top face, back left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(3, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(15, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(11, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(6, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 21: // Bottom face, back up
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(14, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(2, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(8, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(9, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 22: // Bottom face, back down
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(7, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(10, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(13, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(1, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 23: // Bottom face, back right
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(11, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(16, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(3, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(5, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  case 24: // Bottom face, back left
                    if (iterator[i][1] === 1 && iterator[i][0] === 0){ // +x
                      front.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(4, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === 1 && iterator[i][1] === 0){ // +y
                      right.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(6, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][1] === -1 && iterator[i][0] === 0){ // -x
                      back.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(12, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    if (iterator[i][0] === -1 && iterator[i][1] === 0){ // -y
                      left.push(grid[iterator[i][0] + y1][iterator[i][1] + x1])
                      visit(15, iterator[i][1] + x1, iterator[i][0] + y1)
                    }
                    break
                  }

              }

    return
  } // function visit
  
  for (y = 0; y < grid.length; y++)
    for (x = 0; x < max; x++){ // search for a valid data point
      if (grid[y][x]){
        if (grid[y][x] !== ' '){
          front.push(grid[y][x]) // Assign first found face as front
          visit(1, x, y)
          let answer = []
 
          if (front.length > 1)
            answer.push(front)
          
          if (right.length > 1)
            answer.push(right)
          
          if (back.length > 1)
            answer.push(back)
          
          if (left.length > 1)
            answer.push(left)
          
          if (top.length > 1)
            answer.push(top)
          
          if (bottom.length > 1)
            answer.push(bottom)
          
          return answer
        }
      }
    }
  
};


################################
var wrap_cube = function(shape) {
  const row=shape.split('\n')
  let arr=[]
  for(var i = 0; i<row.length;i++){
    arr.push([])
    for(var j = 0; j<row[i].length;j++){
      arr[i].push(row[i][j])
    }
  }
  var template=[[1,2,3,4],[5,2,6,4],[1,5,3,6]]
  var templateAnswer=[[5,6],[3,1],[4,2]]
  var cur=[]
  var res=[[],[],[],[],[],[]]
  //run
  for( var a =0;a< arr.length;a++){
    if(arr[a].length>0){
      for(var b=0;b< arr[a].length;b++){
        chec=true
        if(arr[a][b]!=' '){
          if(totalLength(res)==0){
            res[0].push(arr[a][b])//first auto set A
          }
          else if(totalLength(res)==1){// second auto B
            if(arr[a][b-1]==res[0][0]||( arr[a-1]&&arr[a-1].length>=b&&arr[a-1][b]==res[0][0])){
              res[1].push(arr[a][b])
            }
            else{
              cur.push([a,b])
              chec=false
            }
          }
          else {  //run
            var che = checkAdd(arr, res, a, b)
            if(che==null){
              return null
            }
            if(che!= -1){
              res[che-1].push(arr[a][b])
              var li=0
              while(li<cur.length){
                var la =checkAdd(arr, res,cur[li][0], cur[li][1])
                if(la==null){
                  return null
                }
                if(la!=-1){
                  res[la-1].push(arr[cur[li][0]][cur[li][1]])
                  cur.splice(li,1)
                  li=0
                }
                else{
                  li=li+1
                }
              }
            }
            else{
              cur.push([a,b])
            }
          }
        }
      }
    }
  } 
  var li=0
  while(li<cur.length){
    var la =checkAdd(arr, res,cur[li][0], cur[li][1])
    if(la==null){
      return null
    }
    if(la!=-1){
      res[la-1].push(arr[cur[li][0]][cur[li][1]])
      cur.splice(li,1)
      li=0
    }
    else{
      li=li+1
    }
  }
  var res2=[]
  res.map(i=>i.length>1?res2.push(i):null)
  return cur.length > 0?null:res2
};

var totalLength = function(arr) {
  var leng=0;
  for(var i of arr){
    leng=leng+i.length;
  }
  return leng
}

var checkLocate = function(arr,val) {
  for(var i=0;i<6;i++){
    if(arr[i].indexOf(val)>=0){
      return i
    }
  }
  return -1
}

var checkAround = function(arr, res,a,b){
  var a1,a2,a3,a4,l1,l2,l3,l4
  a1 = (a > 0 && (arr[a-1].length > b  && arr[a-1][b]!=' ')) ? arr[a-1][b] : null;
  a2 = (arr[a].length > b + 1 && arr[a][b+1] != ' ') ? arr[a][b+1] : null;
  a3 = (arr.length > a + 1 && arr[a+1].length>b && arr[a+1][b] != ' ') ? arr[a+1][b] : null;
  a4 = (b>0 && arr[a][b-1] != ' ')?arr[a][b-1]:null;
  l1 = a1 != null?checkLocate(res,a1):-1
  l2 = a2 != null?checkLocate(res,a2):-1
  l3 = a3 != null?checkLocate(res,a3):-1
  l4 = a4 != null?checkLocate(res,a4):-1
  return [l1,l2,l3,l4]
}

var checkAdd = function (arr,res,a,b){
  var template=[[1,2,3,4],[5,2,6,4],[1,5,3,6]]
  var templateAnswer=[[5,6],[3,1],[4,2]]
  var re = -1
  var ci=false
  var ca=checkAround(arr,res,a,b)
  for(var i=0;i<4;i++){
    if(ca[i]!=-1){
      var cb=checkAround(arr,res,a+(i-1)%2,b+(2-i)%2)
      for(var j=0;j<4;j++){
        if(cb[j]!=-1){
          for(var k=0;k<3;k++){
            var k1 = template[k].indexOf(ca[i]+1)
            var k2 = template[k].indexOf(cb[j]+1)
            if(k1!=-1 &&k2!=-1){
              if(j%2==i%2){
                var reC = (k1+1) % 4 == k2 ? template[k][(4+k1-1)%4]:template[k][(k1+1)%4]
                if(re==-1){
                  re=reC
                }
                else if(ci){
                  return null
                }
              }
              else{
                if((i+1)%4==j){
                  var reC = (k1+1) % 4 == k2 ? templateAnswer[k][0]: templateAnswer[k][1]
                  if(re==-1){
                    re=reC
                  }
                  else if(ci){
                    return null
                  }
                }
                else if((j+1)%4==i){
                  var reC = (k2+1) % 4 == k1 ? templateAnswer[k][0]: templateAnswer[k][1]
                  if(re==-1){
                    re=reC
                  }
                  else if(ci){
                    return null
                  }
                }
              }
            }
          }
        }
      }
    }
    if(re!=-1){
      ci=true
    }
  }
  return re
}

###########################
var wrap_cube = function(shape) {
  const row=shape.split('\n')
  let arr=[]
  for(var i = 0; i<row.length;i++){
    arr.push([])
    for(var j = 0; j<row[i].length;j++){
      arr[i].push(row[i][j])
    }
  }
  var template=[[1,2,3,4],[5,2,6,4],[1,5,3,6]]
  var templateAnswer=[[5,6],[3,1],[4,2]]
  var cur=[]
  var res=[[],[],[],[],[],[]]
  //run
  for( var a =0;a< arr.length;a++){
    if(arr[a].length>0){
      for(var b=0;b< arr[a].length;b++){
//       if(arr[a].length>b+1 && arr.length>a+1 && arr[a+1].length>b+1 && [null,' '].indexOf(arr[a][b])==-1 && [null,' '].indexOf(arr[a][b+1])==-1 && [null,' '].indexOf(arr[a+1][b])==-1 && [null,' '].indexOf(arr[a+1][b+1])==-1  ){
//          return null
//       }
        chec=true
        if(arr[a][b]!=' '){
          if(totalLength(res)==0){
            res[0].push(arr[a][b])//first auto set A
          }
          else if(totalLength(res)==1){// second auto B
            if(arr[a][b-1]==res[0][0]||( arr[a-1]&&arr[a-1].length>=b&&arr[a-1][b]==res[0][0])){
              res[1].push(arr[a][b])
            }
            else{
              cur.push([a,b])
              chec=false
            }
          }
          else {  //run
            var che = checkAdd(arr, res, a, b)
            if(che==null){
              return null
            }
            if(che!= -1){
              res[che-1].push(arr[a][b])
              var li=0
              while(li<cur.length){
                var la =checkAdd(arr, res,cur[li][0], cur[li][1])
                if(la==null){
                  return null
                }
                if(la!=-1){
                  res[la-1].push(arr[cur[li][0]][cur[li][1]])
                  cur.splice(li,1)
                  li=0
                }
                else{
                  li=li+1
                }
              }
            }
            else{
              cur.push([a,b])
            }
          }
        }
      }
    }
  }
  
              var li=0
              while(li<cur.length){
                var la =checkAdd(arr, res,cur[li][0], cur[li][1])
                if(la==null){
                  return null
                }
                if(la!=-1){
                  res[la-1].push(arr[cur[li][0]][cur[li][1]])
                  cur.splice(li,1)
                  li=0
                }
                else{
                  li=li+1
                }
              }
  var res2=[]
  res.map(i=>i.length>1?res2.push(i):null)
  return cur.length > 0?null:res2
};

var totalLength = function(arr) {
  var leng=0;
  for(var i of arr){
    leng=leng+i.length;
  }
  return leng
}

var checkLocate = function(arr,val) {
  for(var i=0;i<6;i++){
    if(arr[i].indexOf(val)>=0){
      return i
    }
  }
  return -1
}

var checkAround = function(arr, res,a,b){
  var a1,a2,a3,a4,l1,l2,l3,l4
  a1 = (a > 0 && (arr[a-1].length > b  && arr[a-1][b]!=' ')) ? arr[a-1][b] : null;
  a2 = (arr[a].length > b + 1 && arr[a][b+1] != ' ') ? arr[a][b+1] : null;
  a3 = (arr.length > a + 1 && arr[a+1].length>b && arr[a+1][b] != ' ') ? arr[a+1][b] : null;
  a4 = (b>0 && arr[a][b-1] != ' ')?arr[a][b-1]:null;
  l1 = a1 != null?checkLocate(res,a1):-1
  l2 = a2 != null?checkLocate(res,a2):-1
  l3 = a3 != null?checkLocate(res,a3):-1
  l4 = a4 != null?checkLocate(res,a4):-1
//   return [[a1, a2, a3, a4],[l1,l2,l3,l4]]
  return [l1,l2,l3,l4]
}

var checkAdd = function (arr,res,a,b){
  var template=[[1,2,3,4],[5,2,6,4],[1,5,3,6]]
  var templateAnswer=[[5,6],[3,1],[4,2]]
  var re = -1
  var ci=false
  var ca=checkAround(arr,res,a,b)
  for(var i=0;i<4;i++){
    if(ca[i]!=-1){
      var cb=checkAround(arr,res,a+(i-1)%2,b+(2-i)%2)
      for(var j=0;j<4;j++){
        if(cb[j]!=-1){
          for(var k=0;k<3;k++){
            var k1 = template[k].indexOf(ca[i]+1)
            var k2 = template[k].indexOf(cb[j]+1)
            if(k1!=-1 &&k2!=-1){
              if(j%2==i%2){
                var reC = (k1+1) % 4 == k2 ? template[k][(4+k1-1)%4]:template[k][(k1+1)%4]
                if(re==-1){
                  re=reC
                }
                else if(ci){
                  return null
                }
              }
              else{
                if((i+1)%4==j){
                  var reC = (k1+1) % 4 == k2 ? templateAnswer[k][0]: templateAnswer[k][1]
                  if(re==-1){
                    re=reC
                  }
                  else if(ci){
                    return null
                  }
                }
                else if((j+1)%4==i){
                  var reC = (k2+1) % 4 == k1 ? templateAnswer[k][0]: templateAnswer[k][1]
                  if(re==-1){
                    re=reC
                  }
                  else if(ci){
                    return null
                  }
                }
              }
            }
          }
        }
      }
    }
    if(re!=-1){
      ci=true
    }
  }
  return re
}


###################################

// -------------------------------------class Cube-------------------------------------------
/*
     d 
   f a e
     b 
     c 
*/

class Cube {
    constructor(a,b,c,d,e,f) {
        this._state = {a:a, b: b, c:c, d:d, e:e, f:f}
        this.diceStatus = []
    }

    show () {
        console.log(`  ${this._state.d}  `)
        console.log(`${this._state.f} ${this._state.a} ${this._state.e}`)
        console.log(`  ${this._state.b}  `)
        console.log(`  ${this._state.c}  `)
        console.log(" ")
    }

    rollback(){
        if (this.diceStatus.length===0) {
            console.error("***  rollback fail ***")
            return null
        }
        switch (this.diceStatus[this.diceStatus.length-1]) {
            case 'r': {
                let temp = this._state.e
                this._state = {...this._state, e:this._state.a, a:this._state.f, f:this._state.c, c:temp}
                this.diceStatus.pop()
                break
            }
            case 'd': {
                let temp = this._state.a
                this._state = {...this._state, a:this._state.d, d:this._state.c, c:this._state.b, b:temp}
                this.diceStatus.pop()
                break
            }
            case 'l': {
                let temp = this._state.e
                this._state = {...this._state, e:this._state.c, c:this._state.f, f:this._state.a, a:temp}
                this.diceStatus.pop()
                break
            }
            case 'u': {
                let temp = this._state.a
                this._state = {...this._state, a:this._state.b, b:this._state.c, c:this._state.d, d:temp}
                this.diceStatus.pop()
                break
            }
        } //end switch
        return this
    }// end rollback()

    //rotate right
    r(){
        let temp = this._state.e
        this._state = {...this._state, e:this._state.c, c:this._state.f, f:this._state.a, a:temp}
        this.diceStatus.push('r')
        return this
    }

    //rotate down
    d(){
        let temp = this._state.a
        this._state = {...this._state, a:this._state.b, b:this._state.c, c:this._state.d, d:temp}
        this.diceStatus.push('d')
        return this
    }

    //rotate left
    l(){
        let temp = this._state.e
        this._state = {...this._state, e:this._state.a, a:this._state.f, f:this._state.c, c:temp}
        this.diceStatus.push('l')
        return this
    }

    //rotate up
    u(){
        let temp = this._state.a
        this._state = {...this._state, a:this._state.d, d:this._state.c, c:this._state.b, b:temp}
        this.diceStatus.push('u')
        return this
    }

    //move the cube n times: ['r', 'r', 'd'] --> this.r().r().d()
    move(arr) {
        // arr.reverse()
        for (let i=0; i<arr.length;i++) {
            this[arr[i]]()
        }
        return this
    }

} // -------------------------------------end class Cube-------------------------------------------

// ----------------------------------------class Net-----------------------------------------------
class Net {
    constructor (matrix) {
        this.matrix = matrix.map(x=>[...x]) 
        this.path=[] // list in order of the elements (path)
        this.lowFace = ['A'] // list of the correspondent faces of the dice for each element in path
        this.invalid = false
        this.deep = -1
    }

    show() {
        for (let i =0; i<this.matrix.length;i++)
            console.log(this.matrix[i].join(''))
    }


    //return an array of 4 items [left, down, right, up] ej: [null, 'A', 'B', null]
    // if an item is it's inmediate parent return null 
    // check also if an item is an ancester (in this case we get a circular conection, ergo -> an invalid paper net) 
    // in other case return null
    findPath (coord, parent, dice){

        this.deep++

        if (dice===undefined) {
            dice = new Cube('A','B','C','D','E','F',)
        }
        const [x, y] = coord
        
        // console.log("-------CALL findPath--------")
        // console.log("coord=", coord, "value= <", this.matrix[x][y], ">")
        // console.log("deep=", this.deep)
        // console.log("parent=", parent)
        // console.log("diceFace=", dice._state.a, "diceLog=",dice.diceStatus )
        // console.log("---------findPath-----------")
        

        let result = [] // array of 4 elements containing info about the surroundings of current coord (element or null)

        const directions = [[x, y+1], [x+1, y],[x, y-1], [x-1, y]]

        if (x<0 || x>this.matrix.length-1 || y<0 || y>this.matrix[0].length-1) {
            console.log("coords outside the matrix boundaries...")
            this.invalid = true
            this.deep--
            return null // RETURN FINDPATH
        }
        this.path.push(this.matrix[x][y])

        // left of [x, y]
        const error = directions.map ((x,dirIndex)=> {

            const [i, j] = x
            

            // console.log ('surrounding=>',i, j)
            //check if outside the matrix
            if (i<0 || i>this.matrix.length-1 || j<0 || j>this.matrix[0].length-1) {
                result.push(null)
                return "outside" //return of the map
            }

            //check if the adyacent value === 0
            if (this.matrix[i][j]=== 0) {
                result.push(null)
                return "0 skipping" //return of the map
            }

            //check if the adyacent value is the parent
            if (this.matrix[i][j]=== parent) {
                result.push(null)
                return "parent" //return of the map
            }

            //check if there is any circular reference
            if (this.path.indexOf(this.matrix[i][j])!==-1) {
                return "circular" //return of the map
            }

            result.push(this.matrix[i][j])
            return "No error" //return of the map
        })

        // console.log ("result", result)
        if (error.indexOf("circular") !==-1) {
            console.log("SALIENDO POR REFERENCIA CIRCULAR")
            this.invalid=true
            this.deep--
            return null // RETURN FINDPATH
        }

        // test how many items in result are not null's...if every are null we habe an endpoint
        if (result.every(x=>(x===null))) {
            // console.log("endpoint!")
            this.deep--
            return "endpoint" // // RETURN FINDPATH
        }

        // console.log("result", result)
        
        // call recursive with all not null values
        result.forEach((val, dirIndex)=>{

            if (val !== null) {

                switch (dirIndex) {
                    case 0: {
                        dice.r()
                        // dice.show()
                        break
                    }
                    case 1: {
                        dice.d()
                        // dice.show()
                        break
                    }
                    case 2: {
                        dice.l()
                        // dice.show()
                        break
                    }
                    case 3: {
                        dice.u()
                        // dice.show()
                        break
                    }
                }

                this.lowFace.push(dice._state.a)

                // console.log("calling ", "val=",val)

                //directions[dirIndex] contain the coords for the result not null value
                let callResult = this.findPath(directions[dirIndex], this.matrix[x][y], dice) //return foreach
                // console.log("CALL RESULTTTTTTTTT=", callResult)


                dice.rollback()

                return callResult
            }
        }) 
        this.deep--
        return "bien"   // RETURN FINDPATH
    }// findPath

    // return a tree from the matrix (it coul'd be done in the constructor)
    // it has to transverse the matrix finding the first node and then follow the node surroundings
    // searching for new nodes and constructing the tree.
    // in the midtime cheking the tree searching for the next node in the ancesters in order to find cycles.

    wrap () {
        let empty = true
        let first = [0,0]
        for (let i =0; i<this.matrix.length;i++){
            for (let j=0; j<this.matrix[0].length;j++){
                if (this.matrix[i][j] !== 0) {
                    first = [i, j]
                    empty = false
                    break
                }

            }
            if (!empty) break
        }
            
        
        if (empty) {
            console.log ('matriz vacía...')
            return null
        }

        console.log("first =>", first)
        this.findPath(first, 0)

        console.log(this.path)
        console.log("lowface -V")
        console.log(this.lowFace)

        const caras = this.lowFace.filter((val, i)=> (this.lowFace.indexOf(val)===i))
        // console.log("caras=", caras)

        const groups = caras.map(cara=>{
            const acu = []
            for (let i=0;i<this.path.length;i++){
                // console.log("path[i]=", this.path[i], "i=", i, "cara=", cara)
                if (this.lowFace[i]===cara) {
                    acu.push(this.path[i])
                    // console.log("pushing... ", this.path[i])
                }
            }
            return acu
        })

        const awnser = groups.filter(x=>x.length >1)
        // console.log("groups=",groups)
        // console.log("awnser=", awnser)
        if (this.invalid) return null
        return awnser

    } //wrap()


}// --------------------------------------end class Net---------------------------------------------


function genMatrix(str) {
const rows = str.split('\n')
const matrixWithEmptys = rows.map(row=> row.split(''))
const matrixNotComplete = matrixWithEmptys.filter(row => row.length >0)
let size = 0
for (let i=0;i<matrixNotComplete.length;i++){
    if (matrixNotComplete[i].length > size)
        size= matrixNotComplete[i].length
}
const matrixComplete = matrixNotComplete.map (row=>{
    while (row.length<size){
        row.push(' ')
    }
    return row
})

const matrix = matrixComplete.map(row=>row.map(elem=>{
    if (elem === ' ') return 0
    else return elem
}))

return matrix
}



var wrap_cube = function(shape) {

const matrix = genMatrix(shape)
console.log("***********************************************************************INICIO")
console.log( matrix.map(row=>row.join(" ")).join("\n"))
const net = new Net(matrix)
return net.wrap()
};
    
