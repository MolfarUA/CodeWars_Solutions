5aaa1aa8fd577723a3000049


var to100 = Array(10).fill(null).map(() => Array(10).fill(0)).map((x, y) => x.map((i, j) => y * 10 + j));
var toxy = Array(100).fill(0).map((i, j) => [Math.floor(j / 10), j % 10])

function build_wall(start_point, dir, input_mask, value) {
    var res = [...input_mask];
    var [y, x] = toxy[start_point];
    var [dx, dy] = dir;
    while (true) {
        x = x + dx;
        y = y + dy;
        if (x < 0 || x > 9 || y < 0 || y > 9) break;
        if (res[to100[y][x]] > 0) break;
        res[to100[y][x]] = value;
    }
    return res;
}

function remove_mask(mask, value) {
    for (let i in mask) {
        if (mask[i] == value) mask[i] = 0;
    }
}

function add2_mask(mask, index_list, value) {
    for (let i of index_list) {
        if (mask[i] == 0) mask[i] = value;
    }
}

function getDirections(i) {
    var dirs = new Set([1, -1, 10, -10]);
    if (i < 10) dirs.delete(-10);
    if (i % 10 == 0) dirs.delete(-1);
    if (i % 10 == 9) dirs.delete(1);
    if (i > 89) dirs.delete(10);
    return dirs;
}

function findpath(mask, from, to, keep_away_list) {
    var dist = new Array(100).fill(10000);
    dist[from] = 0;
    var tasks = [from] //    tasks.push_back(to_index);
    const mask_backup = mask[to];
    mask[to] = 0;
    while (tasks.length > 0) {
        let i = tasks.shift();
        let dirs = getDirections(i);
        for (let d of dirs) {
            let t = d + i;
            if (mask[t] == 0) {
                if (dist[t] == 10000) {
                    tasks.push(t);
                }
                let distance = dist[i] + 100;
                if (dist[t] > distance) {
                    dist[t] = distance;
                }
            }
        }

    }
    mask[to] = mask_backup;
    if (dist[to] == 10000) return null;
    var res = [];
    var i = to;
    while (i != from) {
        let dirs = getDirections(i);
        let next = 0;
        let min_distance = 10000;
        for (let d of dirs) {
            if (dist[i + d] < min_distance) {
                min_distance = dist[i + d];
                next = i + d;
            }
        }
        res.push(next);
        i = next;
    }
    res.reverse();
    res.shift();
    return [...res, to];
}

function fourPass(s) {
    const seqs = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0]
    ];
    const pairs = [
        [0, 1],
        [1, 2],
        [2, 3]
    ];
    const dirs = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1]
    ];

    var mask = Array(100).fill(0);
    for (let i = 0; i < 4; i++) {
        mask[s[i]] = i + 1;
    };
    var res = [];
    for (let seq of seqs) {
        let [i2, i3] = pairs[seq[2]]
        let s2 = s[i2];
        let s3 = s[i3];
        for (let dir4 of dirs) {
            const mask4 = build_wall(s3, dir4, mask, 14);
            for (let dir3 of dirs) {
                let scenario_mask = build_wall(s2, dir3, mask4, 13)
                let paths = [null, null, null]
                for (let i = 0; i < 3; i++) {
                    let pair = seq[i]
                    let [from_station, to_station] = pairs[pair]
                    const path = findpath(scenario_mask,
                        s[from_station], s[to_station], []);
                    if (path == null) break;
                    if (i == 0) { remove_mask(scenario_mask, 13); }
                    if (i == 1) { remove_mask(scenario_mask, 14); }
                    add2_mask(scenario_mask, path, 23);
                    paths[pair] = path;

                }
                if (paths.includes(null)) continue;
                res.push([s[0], ...paths[0], ...paths[1], ...paths[2]])
            }
        }
    }
    if (res.length == 0) return null;
    return res.sort((a, b) => a.length - b.length)[0]
}

#######################################
function printBoard(board) {
  for (let i = 0; i < 10; i++) {
    console.log(board.slice(10*i, 10*(i+1)).join('') + "\n");  
  }
}

function cloneBoard(board) {
  return [...board];
}

function neighbors(n) {
  let dest = [];
  if (n % 10 !== 0) dest.push(n - 1);
  if (n % 10 !== 9) dest.push(n + 1);
  if (n <= 90) dest.push(n + 10);
  if (n >= 10) dest.push(n - 10);
  return dest;
}

function shortestPath(a, b, board) {
  const INFINITY = 100000;
  let dist = {};
  let prev = {};
  let Q = new Set();
  
  for (let i = 0; i < 100; i++) {
    if (board[i] === ' . ' || i === a || i === b) {
      dist[i] = INFINITY;
      prev[i] = undefined;
      Q.add(i);
    }
  }

  dist[a] = 0;
  
  while (Q.size > 0) {
    // Find u with min dist
    let u = undefined;
    let uMin = 2*INFINITY
    for (let v of Q) {
      if (dist[v] < uMin) {
        u = v;
        uMin = dist[v];
      }
    }
    
    Q.delete(u);

    for (let v of neighbors(u)) {
      if (! Q.has(v)) continue;
      if (board[v] !== ' . ' && v !== b) continue;
      let alt = dist[u] + 1;
      if (alt < dist[v]) {
        dist[v] = alt;
        prev[v] = u;
      }
    }
  }
  
  if (prev[b] === undefined) return [INFINITY, []];
     
  let c = b;
  while (c != a) {
    if (c !== b) board[c] = ' * ';
    c = prev[c];
  }
  
  return [dist[b], prev]
}

const permutations = [
  [0, 1, 2],
  [0, 2, 1],
  [1, 0, 2],
  [1, 2, 0],
  [2, 0, 1],
  [2, 1, 0]
]

function fourPass(stations){
  console.log('-------------------------------\n\n');
  
  const board = [...Array(100)].map(() => ' . ')
  stations.forEach((s, i) => {
    board[s] = '*' + i.toString() + '*';
  })
  
  
  printBoard(board);
  console.log('\n');

  let minP = undefined;
  let minPL = 100000;
  for (const p of permutations) {
    const boardClone = cloneBoard(board);
    let d = 0;
    for (let i of p) {
      let [dis, prev] = shortestPath(stations[i], stations[i + 1], boardClone);
      d += dis;
    }
    
    if (d < minPL) {
      minPL = d;
      minP = p;
    }
  }
  
  if (minP === undefined) return null;

  let b = {};
  const boardClone = cloneBoard(board);
  for (let i of minP) {
    let [dis, prev] = shortestPath(stations[i], stations[i + 1], boardClone);
    b[i + 1] = prev;
  }
  printBoard(boardClone);

  let path = [];
  for (let s = 3; s > 0; s--) {
    const end = stations[s];
    const start = stations[s - 1];
    
    let c = end;
    while (c != start) {
      path.push(c);
      c = b[s][c];
    }
  }
  path.push(stations[0]);


  const ret = path.reverse();
  return ret;
}
//if you prefer to see an overhead view of the factory floor with any failed test results, uncomment the line below:
//show_graph_debug = true;

#####################################
class BinaryHeap {
  constructor(scoreFunction) {
    this.heap = [];
    this.scoreFunction = scoreFunction;
    this.bubbleUp = this.bubbleUp.bind(this);
    this.sinkDown = this.sinkDown.bind(this);
  }

  push(value) {
    this.heap.push(value);
    this.bubbleUp(this.heap.length - 1);
  }

  bubbleUp(index) {
    let element = this.heap[index],
      score = this.scoreFunction(element);
    while (index > 0) {
      let parentIndex = Math.floor((index + 1) / 2) - 1,
        parent = this.heap[parentIndex];
      if (score >= this.scoreFunction(parent)) break;
      this.heap[parentIndex] = element;
      this.heap[index] = parent;
      index = parentIndex;
    }
  }

  pop(index) {
    let result = this.heap[0];
    let end = this.heap.pop();
    if (this.heap.length > 0) {
      result = end;
      this.sinkDown(0);
    }
    return result[index];
  }

  sinkDown(index) {
    let element = this.heap[index], elemScore = this.scoreFunction(element);
    const length = this.heap.length;

    while (true) {
      let child2Index = (index + 1) * 2, child1Index = child2Index - 1;
      let swap = null;
      if (child1Index < length) {
        let child1 = this.heap[child1Index],
          child1Score = this.scoreFunction(child1);
        if (child1Score < elemScore) swap = child1Index;
      }
      if (child2Index < length) {
        let child2 = this.heap[child2Index],
          child2Score = this.scoreFunction(child2);
        if (child2Score < (swap == null ? elemScore : child1Score)) swap = child2Index;
      }
      if (swap == null) break;
      this.heap[index] = this.heap[swap];
      this.heap[swap] = element;
      index = swap;
    }
  }
}

class Queue {
  constructor() {
    this.elements = [];
  }

  ifEmpty() {
    return this.elements.length === 0;
  }

  put(x) {
    this.elements.push(x);
  }

  get() {
    return this.elements.shift();
  }
}

class SquareGrid {
  constructor(map) {
    this.map = map;
    this.height = map.length;
    this.width = map[0].length;
    this.obstacles = [];
    this.inBounds = this.inBounds.bind(this);
    this.passable = this.passable.bind(this);
    this.neighbours = this.neighbours.bind(this);
  }

  inBounds(id) {
    let { x, y } = id;
    return 0 <= x && x < this.width && 0 <= y && y < this.height;
  }

  passable(id) {
    let { x, y } = id;
    let tile = this.map[y][x];
    return !this.obstacles.includes(tile);
  }

  neighbours(id) {
    let { x, y } = id;
    let results = [{ x: x + 1, y: y }, { x: x, y: y - 1 }, { x: x - 1, y: y }, { x: x, y: y + 1 }];
    if ((x + y) % 2 === 0) results.reverse();
    results = results.filter(this.inBounds);
    results = results.filter(this.passable);
    return results;
  }
}

class GridWithWeights extends SquareGrid {
  constructor(map) {
    super(map);
    this.cost = this.cost.bind(this);
  }

  cost(fromNode, toNode, goalNode) {
    const [x1, y1] = fromNode;
    const [x2, y2] = toNode;
    const [x3, y3] = goalNode;
    if (Math.abs(x1 - x3) >= Math.abs(x2 - x3)) return 0;
    if (Math.abs(y1 - y3) >= Math.abs(y2 - y3)) return 0;
    if (Math.abs(x1 - x3) < Math.abs(x2 - x3) || Math.abs(y1 - y3) < Math.abs(y2 - y3)) return 100;
  }
}

class PriorityQueue {
  constructor() {
    this.elements = new BinaryHeap(x => x[0]);
  }

  ifEmpty() {
    return this.elements.length === 0;
  }

  put(item, priority) {
    let arr = [priority, item];
    this.elements.push(arr);
  }

  get(index) {
    return this.elements.pop(index);
  }
}

const coordinatesStartAndGoal = (start, goal, stations) => {
  const first = stations[start];
  const second = stations[goal];
  let xS = +first[1] || +first[0];
  let yS = first.length > 1 ? +first[0] : 0;
  const xG = +second[1] || +second[0];
  const yG = second.length > 1 ? +second[0] : 0;
  return [xS, yS, xG, yG];
}

const reconstructPath = (cameFrom, start, goal, factory, marker) => {
  let current = goal;
  let { xS, yS } = start;
  const path = [];
  while (current && current.x !== xS && current.y !== yS) {
    let { x, y } = current;
    path.push(+`${y}${x}`);
    if ( current !== goal ) factory[y][x] = marker;
    current = cameFrom[`x: ${x}, y: ${y}`];
  }
  path.reverse();
  return path;
}

const heuristic = (start, goal, next) => {
  const { x: x0, y: y0 } = start;
  const { x: x1, y: y1 } = goal;
  const { x: x2, y: y2 } = next;
  const dx1 = x2 - x1;
  const dy1 = y2 - y1;
  const dx2 = x0 - x1;
  const dy2 = y0 - y1;
  let heuristic = Math.abs(x1 - x2) + Math.abs(y1 - y2);
  const cross = Math.abs(dx1 * dy2 - dx2 * dy1);
  return heuristic += cross;
}
const areaMaker = (start, end, placeholder, stations, factory) => {
  let area = false;
  let opened = false;
  let first = stations[start];
  let second = stations[end];
  factory.forEach((el, i) => {
    for (let j = 0; j < el.length; j++) {
      if (!area && first[0] == i && second[1] == j) {
        opened = !opened;
      }
      else if (!area && second[0] == i && first[1] == j) {
        opened = !opened;
      }
      else if (!opened && first[0] == i && first[1] == j) {
        area = !area;
      }
      else if (!opened && second[0] == i && second[1] == j) {
        area = !area;
      }
      if (area &&
        ((j >= first[1] && j <= second[1]) || (j <= first[1] && j >= second[1]))
      ) {
        el[j] = (el[j] != 'S') ? placeholder : el[j];
      }
      else if (opened &&
        ((j >= first[1] && j <= second[1]) || (j <= first[1] && j >= second[1]))
      ) {
        el[j] = (el[j] != 'S') ? placeholder : el[j];
      }
    }
  });
}
function fourPass(stations) {
  stations.forEach((el, i) => {
    stations[i] = el < 10 ?
      `0${el}` : `${el}`;
  });
  const factory = new Array(10).fill(' ');
  factory.forEach((el, i) => {
    factory[i] = new Array(10).fill(' ');
  });
  factory.forEach((el, i) => {
    el.forEach((subEl, subI) => {
      el[subI] = stations.includes(`${i}${subI}`) ?
        'S' : subEl;
    });
  });

  areaMaker(0, 1, '|', stations, factory);
  areaMaker(2, 3, '-', stations, factory);

  const breadthFirst = (graph, start, goal, marker) => {
    let [xS, yS, xG, yG] = coordinatesStartAndGoal(start, goal, stations);
    let frontier = new Queue();
    frontier.put({ x: xS, y: yS });
    const cameFrom = {};
    cameFrom[`x: ${xS}, y: ${yS}`] = null;

    while (!frontier.ifEmpty()) {
      current = frontier.get();
      if (current.x === xG && current.y === yG) {
        let { x, y } = current;
        break;
      }
      for (let { x, y } of graph.neighbours(current)) {
        if (!cameFrom.hasOwnProperty(`x: ${x}, y: ${y}`)) {
          frontier.put({ x, y });
          cameFrom[`x: ${x}, y: ${y}`] = current;
        }
      }
    }
    let path = reconstructPath(cameFrom, { x: xS, y: yS }, { x: xG, y: yG }, factory, marker);
    return path;
  }

  const aStarSearch = (graph, start, goal, marker) => {
    let [xS, yS, xG, yG] = coordinatesStartAndGoal(start, goal, stations);
    let frontier = new PriorityQueue();
    frontier.put({ x: xS, y: yS }, 0);
    const cameFrom = {};
    const costSoFar = {};
    cameFrom[`x: ${xS}, y: ${yS}`] = null;
    costSoFar[`x: ${xS}, y: ${yS}`] = 0;

    while (!frontier.ifEmpty()) {
      let current = frontier.get(1);
      if (current.x === xG && current.y === yG) {
        let { x, y } = current;
        break;
      }
      for (let { x, y } of graph.neighbours(current)) {
        let nextString = `x: ${x}, y: ${y}`;
        let currentString = `x: ${current.x}, y: ${current.y}`;
        let newCost = costSoFar[currentString] 
        + graph.cost([current.x, current.y], [x, y], [xG, yG]);
        if (!costSoFar.hasOwnProperty(nextString) || newCost < costSoFar[nextString]) {
          let priority = newCost + heuristic({ x: xS, y: yS }, { x: xG, y: yG }, { x: x, y: y });
          costSoFar[nextString] = priority;
          frontier.put({ x, y }, priority);
          cameFrom[nextString] = current;
        }
      }
    }
    let path = reconstructPath(cameFrom, { x: xS, y: yS }, { x: xG, y: yG }, factory, marker);
    return path;
  }
  let answer = [];
  let g = new GridWithWeights(factory);
  g.obstacles = ['-', ' '];
  let path = aStarSearch(g, 0, 1, '1');
  path.forEach(el => answer.push(el));
  answer.pop();
  g.obstacles = [' ', '1'];
  path = breadthFirst(g, 1, 2, '2');
  path.forEach(el => answer.push(el));
  answer.pop();
  g.obstacles = ['|', ' ', '1', '2'];
  path = aStarSearch(g, 2, 3, '3');
  path.forEach(el => answer.push(el));
  answer.pop();
  return answer;
}
try{
  fourPass([1, 69, 55, 39]);
  }
finally {
  return null;
}

##############################
      function fourPass(stations) {
        const FILLER = '#';
        const EMPTY_INFESTOR_VALUE = -1;

        // создаем поле
        const createField = stations => {
          const field = new Array(10).fill(0).map((it) => new Array(10).fill(FILLER));

          const point1 = formatNumberToCoordinates(stations[0]);
          const point2 = formatNumberToCoordinates(stations[1]);
          const point3 = formatNumberToCoordinates(stations[2]);
          const point4 = formatNumberToCoordinates(stations[3]);
          field[point1.row][point1.col] = 1;
          field[point2.row][point2.col] = 2;
          field[point3.row][point3.col] = 3;
          field[point4.row][point4.col] = 4;

          // console.log('point1 = ', point1)
          // console.log('point2 = ', point2)
          // console.log('point3 = ', point3)
          // console.log('point4 = ', point4)
          //
          // console.log('createField = ', field);

          return {field, path: {}};
        };

        // функция, которая преобразует координату из формата number в формат {row, col}
        const formatNumberToCoordinates = (number) => ({
          row: Math.floor(number / 10),
          col: number % 10,
        });

        // функция, которая преобзраует строку и столбец в единую коориднату
        const formatCoordinatesToNumber = (row, col) => row * 10 + col;

        // 0 - 0,0
        // 1 - 0,1
        // 6 - 0,6
        // 9 - 0,9
        // 10 - 1,0
        // 16 - 1,6
        // 53  - 5,3

        // находит кол-во звездочек в двухмерном массиве (считает длину пути)
        const findPathLength = (arr) => {
          // счетчик для результата
          let res = 0;

          // идем по строкам
          for (let row = 0; row < arr.length; row++) {
            // идем по элементам строки
            for (let col = 0; col < arr[row].length; col++) {
              // если значение элемента === *
              if (arr[row][col] === '*') {
                // увеличиваем счетчик на 1
                res++;
              }

            }

          }

          // возвращаем счетчик
          return res;

        };

        const findPathBetweenTwoPoints = (field, start, end, pathType, pointToSearch, pointStart) => {

          const fieldCopy = JSON.parse(JSON.stringify(field.field));

          // массив с координатами заразителей
          let infestorsField = new Array(10).fill(0).map((it) => new Array(10).fill(-1));

          // массив последних зараженных клеток - изначально тут будет клетка start
          let lastInfectedPoints = [start];

          const endCoordinates = formatNumberToCoordinates(end);

          // пока не дошли до точки end и пока есть зараженные клетки
          while (lastInfectedPoints.length > 0 && infestorsField[endCoordinates.row][endCoordinates.col] === EMPTY_INFESTOR_VALUE) {
            // идем по последним зараженным клеткам и заражаем соседние

            // пустой массив для последних зараженных клеток
            const lastInfectedPointsLocal = [];

            for (let i = 0; i < lastInfectedPoints.length; i++) {
              // если путь типа А, то
              if (pathType === 'A') {
                // идем по часовой стрелке, в первую очередь вверх и заражаем
                const { row, col } = formatNumberToCoordinates(lastInfectedPoints[i]);
                infectPoint(field.field, infestorsField, row, col, 'UP', pointToSearch, lastInfectedPointsLocal);
                // потом вправо
                infectPoint(field.field, infestorsField, row, col, 'RIGHT', pointToSearch, lastInfectedPointsLocal);
                // потом вниз
                infectPoint(field.field, infestorsField, row, col, 'DOWN', pointToSearch, lastInfectedPointsLocal);
                // потом влево
                infectPoint(field.field, infestorsField, row, col, 'LEFT', pointToSearch, lastInfectedPointsLocal);
              }

              // если путь типа B, то
              if (pathType === 'B') {
                const { row, col } = formatNumberToCoordinates(lastInfectedPoints[i]);
                // идем по часовой стрелке, в первую очередь влево
                // влево
                infectPoint(field.field, infestorsField, row, col, 'LEFT', pointToSearch, lastInfectedPointsLocal);
                // потом вниз
                infectPoint(field.field, infestorsField, row, col, 'DOWN', pointToSearch, lastInfectedPointsLocal);
                // потом вправо
                infectPoint(field.field, infestorsField, row, col, 'RIGHT', pointToSearch, lastInfectedPointsLocal);
                // потом вверх
                infectPoint(field.field, infestorsField, row, col, 'UP', pointToSearch, lastInfectedPointsLocal);

              }
            }

            lastInfectedPoints = lastInfectedPointsLocal.slice();

          }

          // если путь найти не удалось
          if (infestorsField[endCoordinates.row][endCoordinates.col] === EMPTY_INFESTOR_VALUE) {
            // возвращаем false, чтобы данный путь не учитывался
            return false;
          }

          // находим путь
          const path = findPathByInfestorsField(infestorsField, start, end);

          // путь в виде набора чисел 1, 54, 43
          const pathAsNumbers = []

          // заносим его в field
          // идем по всем точкам пути
          for (let i = 0; i < path.length; i++) {
            // помещаем в field звездочку на место данной клетки пути
            if (fieldCopy[path[i].row][path[i].col] === FILLER) {
              fieldCopy[path[i].row][path[i].col] = '*';
            }
            pathAsNumbers.push(formatCoordinatesToNumber(path[i].row, path[i].col))
          }

          // возвращаем field
          return {field: fieldCopy, path: {...field.path, [`${pointStart}-${pointToSearch}`]: pathAsNumbers.reverse()}};
        };

        // функция, которая "находит" путь на основании массива заразителей
        const findPathByInfestorsField = (infestorsField, start, end) => {
          // текущая рассматриваемая точка {row, col}
          let current = formatNumberToCoordinates(end);

          // конечная точка {row, col}
          let formattedStart = formatNumberToCoordinates(start);
          let formattedEnd = formatNumberToCoordinates(end);

          // массив точек, которые образуют нужный путь
          const path = [];

          // пока не дошли до точки start
          while (!(current.row === formattedStart.row && current.col === formattedStart.col)) {
            // заносим в массив точек текущую рассматриваемую точку
            path.push(current);
            // заносим в текущую рассматриваемую точку заразителя текущей рассматриваемой точки 43
            current = formatNumberToCoordinates(infestorsField[current.row][current.col]);
          }

          path.push(formattedStart)

          // возвращаем путь в формате [{row, col}]
          return path;
        };

        // !!!!!!!!!! ФУНКЦИЯ ПРОВЕРЯЕТ, ЧТО КООРДИНАТЫ ЛЕЖАТ ВНУТРИ ГРАНИЦ 0, 10 !!!!!!!!!!!!!!!!!!
        const areCoordinatesCorrect = (row, col) => {
          return row >= 0 && row <= 9 && col >= 0 && col <= 9;
        };

        // заражает клетку
        const infectPoint = (field, infestorsField, currentInfestorRow, currentInfestorCol, direction, pointToSearch, lastInfectedPointsLocal) => {

          let row = currentInfestorRow, col = currentInfestorCol;

          if (direction === 'UP') {
            row = currentInfestorRow - 1;
          } else if (direction === 'DOWN') {
            row = currentInfestorRow + 1;
          } else if (direction === 'RIGHT') {
            col = currentInfestorCol + 1;
          } else if (direction === 'LEFT') {
            col = currentInfestorCol - 1;
          }

          if (!areCoordinatesCorrect(row, col)) {
            return;
          }

          if (
            infestorsField[row][col] === EMPTY_INFESTOR_VALUE &&
            (field[row][col] === FILLER ||
              field[row][col] === pointToSearch)
          ) {
            infestorsField[row][col] = formatCoordinatesToNumber(currentInfestorRow, currentInfestorCol);
            lastInfectedPointsLocal.push(formatCoordinatesToNumber(row, col));
          }

        };

        const allCombinations = [
          [
            [3, 4],
            [2, 3],
            [1, 2],
          ],
          [
            [1, 2],
            [2, 3],
            [3, 4],
          ],
          [
            [1, 2],
            [3, 4],
            [2, 3],
          ],
          [
            [2, 3],
            [1, 2],
            [3, 4],
          ],
          [
            [2, 3],
            [3, 4],
            [1, 2],
          ],
          [
            [3, 4],
            [1, 2],
            [2, 3],
          ],
        ];
        // путь типа А - это горизонтальный путь
        // путь типа B - это вертикальный  путь

        // массив со всеми рабочими комбинациями
        const resCombinations = [];

        // объект со всеми возможными комбинациями вида {1-2: [], 2-3: [],3-4: []}
        let paths = {
          '1-2': [],
          '2-3': [],
          '3-4': [],
        };

        for (let combination = 0; combination < allCombinations.length; combination++) {
          let field = createField(stations);

          for (let pair = 0; pair < allCombinations[combination].length; pair++) {
            // если это первая пара, то
            if (pair === 0) {
              // нашли путь типа А от 1 до 2
              const field1 = findPathBetweenTwoPoints(
                field,
                stations[allCombinations[combination][pair][0] - 1],
                stations[allCombinations[combination][pair][1] - 1],
                'A',
                allCombinations[combination][pair][1],
                allCombinations[combination][pair][0]
              );
              // нашли путь типа B от 1 до 2
              const field2 = findPathBetweenTwoPoints(
                field,
                stations[allCombinations[combination][pair][0] - 1],
                stations[allCombinations[combination][pair][1] - 1],
                'B',
                allCombinations[combination][pair][1],
                allCombinations[combination][pair][0]
              );
              paths['1-2'] = [field1, field2].filter((it) => Boolean(it));
            }

            // если это вторая пара, то
            else if (pair === 1) {
              // идем по раннее найденным путям
              for (let path = 0; path < paths["1-2"].length; path++) {
                // находим путь от точки 2 до точки 3 типа А с учетом данного пути
                const field1 = findPathBetweenTwoPoints(
                  paths['1-2'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'A',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );

                // находим путь от точки 2 до точки 3 типа B с учетом данного пути
                const field2 = findPathBetweenTwoPoints(
                  paths['1-2'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'B',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );


                field1 ? paths['2-3'].push(field1) : null;
                field2 ? paths['2-3'].push(field2) : null;

              }
            }

            // если это третья пара, то
            else if (pair === 2) {
              // идем по раннее найденным путям
              for (let path = 0; path < paths["2-3"].length; path++) {
                // находим путь от точки 3 до точки 4 типа А с учетом данного пути
                const field1 = findPathBetweenTwoPoints(
                  paths['2-3'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'A',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );


                // находим путь от точки 3 до точки 4 типа B с учетом данного пути
                const field2 = findPathBetweenTwoPoints(
                  paths['2-3'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'B',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );

                field1 ? paths['3-4'].push(field1) : null;
                field2 ? paths['3-4'].push(field2) : null;
              }
            }
          }

          resCombinations.push(...paths['3-4'].filter(it => Boolean(it.field)));

          paths = {
            '1-2': [],
            '2-3': [],
            '3-4': [],
          };

        }

        let shortestLength = 10000000, shortestIndex = 0, shortestLengthLocal = 1000000;
        // console.log('resCombinations = ', resCombinations)
        // находим кратчайший путь
        for (let combination = 0; combination < resCombinations.length; combination++) {
          // находим длину данного пути
          shortestLengthLocal = findPathLength(resCombinations[combination].field);

          // сравниваем с текущей минимальной длинной, если короче, обновляем
          if (shortestLengthLocal < shortestLength) {
            shortestIndex = combination;
            shortestLength = shortestLengthLocal;
          }
        }

        const res = resCombinations[shortestIndex];

        if (!res || typeof res === 'undefined' || res.length === 0) {
          return null;
        } else {
          const point1 = formatNumberToCoordinates(stations[0]);
          const point2 = formatNumberToCoordinates(stations[1]);
          const point3 = formatNumberToCoordinates(stations[2]);
          const point4 = formatNumberToCoordinates(stations[3]);
          res.field[point1.row][point1.col] = "1";
          res.field[point2.row][point2.col] = "2";
          res.field[point3.row][point3.col] = "3";
          res.field[point4.row][point4.col] = "4";
          const resArr = Array.from(new Set(res.path['1-2'].concat(res.path['2-3']).concat(res.path['3-4'])))
          return resArr;
        }

      }

####################################
const performance = {timerify: fn => fn, mark: () => {}};

const SQUARE_SIZE = 10;
const EMPTY_CELL = ' ';

function printPath(graph, path) {
  let pathSymbol;
  const matrix = graphToMatrix(graph);
  const visited = {};
  for (const nodeName of path) {
    const row = Math.floor(nodeName / 10);
    const col = nodeName % 10;
    if (matrix[row][col] === EMPTY_CELL) matrix[row][col] = pathSymbol;
    else if (typeof matrix[row][col] === 'number') pathSymbol = String(matrix[row][col]);
    else if (matrix[row][col] !== EMPTY_CELL) matrix[row][col] = '?';

    if (visited[`${row}${col}`]) matrix[row][col] = '?';
    visited[`${row}${col}`] = true;
  }
  console.table(matrix);
}


function graphToMatrix(graph) {
  const matrix = createMatrix();
  for (const [nodeName, node] of Object.entries(graph.nodes)) {
    const row = Math.floor(nodeName / 10);
    const col = nodeName % 10;
    if (node.value) matrix[row][col] = node.value;
  }
  return matrix;
}

function createMatrix() {
  return Array(SQUARE_SIZE).fill().map((_, i) => Array(SQUARE_SIZE).fill().map((_, j) => EMPTY_CELL));
}

function stationsToMatrix(stations) {
  const matrix = createMatrix();
  for (let i = 0; i < stations.length; i++) {
    const n = stations[i];
    const row = Math.floor(n / 10);
    const col = n % 10;
    matrix[row][col] = i + 1;
  }
  return matrix;
}

function matrixToGraph(matrix) {
  const graph = {
    nodes: {},
    restricted: {},
    getRestricted: function () {
      return Object.entries(this.restricted).filter(([key, val]) => val).map(([key]) => key);
    }
  };
  for (let row = 0; row < matrix.length; row++) {
    for (let col = 0; col < matrix.length; col++) {
      const nodeName = `${row}${col}`;
      const value = matrix[row][col] !== EMPTY_CELL ? matrix[row][col] : undefined;
      const restricted = !!value;
      if (restricted) graph.restricted[nodeName] = true;
      graph.nodes[nodeName] = {
        adj: {},
        value,
      };
      const node = graph.nodes[nodeName];
      if (matrix[row + 1] && matrix[row + 1][col]) node.adj[`${row + 1}${col}`] = true;
      if (matrix[row - 1] && matrix[row - 1][col]) node.adj[`${row - 1}${col}`] = true;
      if (matrix[row][col + 1]) node.adj[`${row}${col + 1}`] = true;
      if (matrix[row][col - 1]) node.adj[`${row}${col - 1}`] = true;
    }
  }
  return graph;
}

var cloneGraph = performance.timerify(function cloneGraph(graph) {
  const shallow = Object.assign({}, graph);
  shallow.restricted = Object.assign({}, shallow.restricted);
  return shallow;
})


var getTuples = performance.timerify(function getTuples(nodes) {
  const tuples = [];
  for (let i = 0; i < nodes.length - 1; i++) {
    tuples.push([nodes[i], nodes[i + 1], i]);
  }
  return tuples;
})

var permutations = performance.timerify(function permutations(arr) {
  if (arr.length <= 1) return [arr];
  const results = [];
  for (let i = 0; i < arr.length; i += 1) {
    const rest = arr.slice();
    const [el] = rest.splice(i, 1);
    for (const p of permutations(rest)) {
      results.push([el].concat(p));
    }
  }
  return results;
})

var combinePaths = performance.timerify(function combinePaths(paths) {
  const res = [];
  for (const path of paths) {
    for (const node of path) {
      if (res[res.length - 1] !== node) res.push(node);
    }
  }
  return res;
})

var findAllShortestPaths = performance.timerify(function findAllShortestPaths(graph, from, to, cache = {}) {
  const hash = `${from}#${to}#${graph.getRestricted()}`;
  if (cache[hash]) return cache[hash];
  const fromBak = graph.restricted[from];
  const toBak = graph.restricted[to];
  graph.restricted[from] = false;
  graph.restricted[to] = false;
  let allPaths = new Set();

  const queue = [];
  const visited = { [from]: true };
  const parents = { [from]: undefined };
  queue.push([from, 0]);
  let currentLevel = 0;
  let previousLevel = -1;
  let previousLevelNodes = { from: true };
  let stop = false;
  outer:
  while (queue.length) {
    const [currentNodeName, level] = queue.shift();
    if (level !== previousLevel) {
      previousLevel = currentLevel;
      currentLevel += 1;
      if (stop) break;
      for (const nodeName of Object.keys(previousLevelNodes)) {
        visited[nodeName] = true;
      }
      previousLevelNodes = [];
    }
    previousLevelNodes[currentNodeName] = true;

    for (const nextNodeName of Object.keys(graph.nodes[currentNodeName].adj)) {
      if (!visited[nextNodeName]) {
        if (graph.restricted[nextNodeName]) {
          visited[nextNodeName] = true;
          continue;
        }
        if (!parents[nextNodeName]) parents[nextNodeName] = new Set();
        parents[nextNodeName].add(currentNodeName);
        if (nextNodeName === to) {
          stop = true;
        }

        let canAdd = true;
        for (const [node, level] of queue) {
          if (nextNodeName === node) canAdd = false;
        }
        if (canAdd) queue.push([nextNodeName, currentLevel]);
      }
    }
  }
  function recoverPaths(node, currentPath) {
    if (!node || node === from) {
      if (node === from) allPaths.add(currentPath);
      return;
    }
    if (!parents[node]) return;
    for (const currentNode of parents[node]) {
      recoverPaths(currentNode, [currentNode, ...currentPath]);
    }
  }
  recoverPaths(to, [to]);

  graph.restricted[from] = fromBak;
  graph.restricted[to] = toBak;
  allPaths = [...allPaths];
  cache[hash] = allPaths;
  return allPaths;
})

function sample(paths) {
  if (paths.length < 5) return paths;
  return [
    paths[0],
    paths[paths.length - 1],
    paths[Math.floor(paths.length / 2)]
  ];
}

var connectNodes = performance.timerify(function connectNodes(graph, nodes, cache,) {
  if (!cache) {
    cache = {
      'findShortestPath': {},
      'findAllShortestPaths': {},
      'findShortestPath': {},
    };
  }

  function recur(graph, nodeTuples, pathParts = [], foundPaths = []) {
    if (nodeTuples.length === 0) {
      foundPaths.push(combinePaths(pathParts));
      return true;
    };

    const [from, to, index] = nodeTuples[0];
    const allPaths = sample(findAllShortestPaths(graph, from, to, cache['findAllShortestPaths']));

    for (const path of allPaths) {
      const graphClone = cloneGraph(graph);
      for (const nodeName of path) graphClone.restricted[nodeName] = true;
      pathParts[index] = path;
      recur(
        graphClone,
        nodeTuples.slice(1),
        pathParts,
        foundPaths
      );
    }
  }

  const tuples = getTuples(nodes);
  const variants = permutations(tuples);
  let bestPath;
  const foundPaths = [];
  for (const variant of variants) {
    recur(graph, variant, [], foundPaths);
  }
  for (const path of foundPaths) {
    if (!bestPath || path.length < bestPath.length) bestPath = path;
  }
  return bestPath;
});

let globalGraph;
var fourPass = performance.timerify(function fourPass(stations) {
  const nodeNames = stations.map((x) => String(x).padStart(2, '0'));
  const matrix = stationsToMatrix(stations);
  const graph = matrixToGraph(matrix);
  globalGraph = graph;
  const path = connectNodes(graph, nodeNames);
  return path ? path.map((x) => Number(x)) : null;
});


################################################
function printBoard(board) {
  for (let i = 0; i < 10; i++) {
    console.log(board.slice(10*i, 10*(i+1)).join('') + "\n");  
  }
}

function cloneBoard(board) {
  return [...board];
}

function neighbors(n) {
  let dest = [];
  if (n % 10 !== 0) dest.push(n - 1);
  if (n % 10 !== 9) dest.push(n + 1);
  if (n <= 90) dest.push(n + 10);
  if (n >= 10) dest.push(n - 10);
  return dest;
}

function shortestPath(a, b, board) {
  const INFINITY = 100000;
  let dist = {};
  let prev = {};
  let Q = new Set();
  
  for (let i = 0; i < 100; i++) {
    if (board[i] === ' . ' || i === a || i === b) {
      dist[i] = INFINITY;
      prev[i] = undefined;
      Q.add(i);
    }
  }

  dist[a] = 0;
  
  while (Q.size > 0) {
    // Find u with min dist
    let u = undefined;
    let uMin = 2*INFINITY
    for (let v of Q) {
      if (dist[v] < uMin) {
        u = v;
        uMin = dist[v];
      }
    }
    
    Q.delete(u);

    for (let v of neighbors(u)) {
      if (! Q.has(v)) continue;
      if (board[v] !== ' . ' && v !== b) continue;
      let alt = dist[u] + 1;
      if (alt < dist[v]) {
        dist[v] = alt;
        prev[v] = u;
      }
    }
  }
  
  if (prev[b] === undefined) return [INFINITY, []];
     
  let c = b;
  while (c != a) {
    if (c !== b) board[c] = ' * ';
    c = prev[c];
  }
  
  return [dist[b], prev]
}

const permutations = [
  [0, 1, 2],
  [0, 2, 1],
  [1, 0, 2],
  [1, 2, 0],
  [2, 0, 1],
  [2, 1, 0]
]

function fourPass(stations){
  console.log('-------------------------------\n\n');
  
  const board = [...Array(100)].map(() => ' . ')
  stations.forEach((s, i) => {
    board[s] = '*' + i.toString() + '*';
  })
  
  
  printBoard(board);
  console.log('\n');

  let minP = undefined;
  let minPL = 100000;
  for (const p of permutations) {
    const boardClone = cloneBoard(board);
    let d = 0;
    for (let i of p) {
      let [dis, prev] = shortestPath(stations[i], stations[i + 1], boardClone);
      d += dis;
    }
    
    if (d < minPL) {
      minPL = d;
      minP = p;
    }
  }
  
  if (minP === undefined) return null;

  let b = {};
  const boardClone = cloneBoard(board);
  for (let i of minP) {
    let [dis, prev] = shortestPath(stations[i], stations[i + 1], boardClone);
    b[i + 1] = prev;
  }
  printBoard(boardClone);

  let path = [];
  for (let s = 3; s > 0; s--) {
    const end = stations[s];
    const start = stations[s - 1];
    
    let c = end;
    while (c != start) {
      path.push(c);
      c = b[s][c];
    }
  }
  path.push(stations[0]);


  const ret = path.reverse();
  return ret;
}

###########################
      function fourPass(stations) {
        const FILLER = '#';
        const EMPTY_INFESTOR_VALUE = -1;

        // создаем поле
        const createField = stations => {
          const field = new Array(10).fill(0).map((it) => new Array(10).fill(FILLER));

          const point1 = formatNumberToCoordinates(stations[0]);
          const point2 = formatNumberToCoordinates(stations[1]);
          const point3 = formatNumberToCoordinates(stations[2]);
          const point4 = formatNumberToCoordinates(stations[3]);
          field[point1.row][point1.col] = 1;
          field[point2.row][point2.col] = 2;
          field[point3.row][point3.col] = 3;
          field[point4.row][point4.col] = 4;

          // console.log('point1 = ', point1)
          // console.log('point2 = ', point2)
          // console.log('point3 = ', point3)
          // console.log('point4 = ', point4)
          //
          // console.log('createField = ', field);

          return {field, path: {}};
        };

        // функция, которая преобразует координату из формата number в формат {row, col}
        const formatNumberToCoordinates = (number) => ({
          row: Math.floor(number / 10),
          col: number % 10,
        });

        // функция, которая преобзраует строку и столбец в единую коориднату
        const formatCoordinatesToNumber = (row, col) => row * 10 + col;

        // 0 - 0,0
        // 1 - 0,1
        // 6 - 0,6
        // 9 - 0,9
        // 10 - 1,0
        // 16 - 1,6
        // 53  - 5,3

        // находит кол-во звездочек в двухмерном массиве (считает длину пути)
        const findPathLength = (arr) => {
          // счетчик для результата
          let res = 0;

          // идем по строкам
          for (let row = 0; row < arr.length; row++) {
            // идем по элементам строки
            for (let col = 0; col < arr[row].length; col++) {
              // если значение элемента === *
              if (arr[row][col] === '*') {
                // увеличиваем счетчик на 1
                res++;
              }

            }

          }

          // возвращаем счетчик
          return res;

        };

        const findPathBetweenTwoPoints = (field, start, end, pathType, pointToSearch, pointStart) => {

          const fieldCopy = JSON.parse(JSON.stringify(field.field));

          // массив с координатами заразителей
          let infestorsField = new Array(10).fill(0).map((it) => new Array(10).fill(-1));

          // массив последних зараженных клеток - изначально тут будет клетка start
          let lastInfectedPoints = [start];

          const endCoordinates = formatNumberToCoordinates(end);

          // пока не дошли до точки end и пока есть зараженные клетки
          while (lastInfectedPoints.length > 0 && infestorsField[endCoordinates.row][endCoordinates.col] === EMPTY_INFESTOR_VALUE) {
            // идем по последним зараженным клеткам и заражаем соседние

            // пустой массив для последних зараженных клеток
            const lastInfectedPointsLocal = [];

            for (let i = 0; i < lastInfectedPoints.length; i++) {
              // если путь типа А, то
              if (pathType === 'A') {
                // идем по часовой стрелке, в первую очередь вверх и заражаем
                const { row, col } = formatNumberToCoordinates(lastInfectedPoints[i]);
                infectPoint(field.field, infestorsField, row, col, 'UP', pointToSearch, lastInfectedPointsLocal);
                // потом вправо
                infectPoint(field.field, infestorsField, row, col, 'RIGHT', pointToSearch, lastInfectedPointsLocal);
                // потом вниз
                infectPoint(field.field, infestorsField, row, col, 'DOWN', pointToSearch, lastInfectedPointsLocal);
                // потом влево
                infectPoint(field.field, infestorsField, row, col, 'LEFT', pointToSearch, lastInfectedPointsLocal);
              }

              // если путь типа B, то
              if (pathType === 'B') {
                const { row, col } = formatNumberToCoordinates(lastInfectedPoints[i]);
                // идем по часовой стрелке, в первую очередь влево
                // влево
                infectPoint(field.field, infestorsField, row, col, 'LEFT', pointToSearch, lastInfectedPointsLocal);
                // потом вниз
                infectPoint(field.field, infestorsField, row, col, 'DOWN', pointToSearch, lastInfectedPointsLocal);
                // потом вправо
                infectPoint(field.field, infestorsField, row, col, 'RIGHT', pointToSearch, lastInfectedPointsLocal);
                // потом вверх
                infectPoint(field.field, infestorsField, row, col, 'UP', pointToSearch, lastInfectedPointsLocal);

              }
            }

            lastInfectedPoints = lastInfectedPointsLocal.slice();

          }

          // если путь найти не удалось
          if (infestorsField[endCoordinates.row][endCoordinates.col] === EMPTY_INFESTOR_VALUE) {
            // возвращаем false, чтобы данный путь не учитывался
            return false;
          }

          // находим путь
          const path = findPathByInfestorsField(infestorsField, start, end);

          // путь в виде набора чисел 1, 54, 43
          const pathAsNumbers = []

          // заносим его в field
          // идем по всем точкам пути
          for (let i = 0; i < path.length; i++) {
            // помещаем в field звездочку на место данной клетки пути
            if (fieldCopy[path[i].row][path[i].col] === FILLER) {
              fieldCopy[path[i].row][path[i].col] = '*';
            }
            pathAsNumbers.push(formatCoordinatesToNumber(path[i].row, path[i].col))
          }

          // возвращаем field
          return {field: fieldCopy, path: {...field.path, [`${pointStart}-${pointToSearch}`]: pathAsNumbers.reverse()}};
        };

        // функция, которая "находит" путь на основании массива заразителей
        const findPathByInfestorsField = (infestorsField, start, end) => {
          // текущая рассматриваемая точка {row, col}
          let current = formatNumberToCoordinates(end);

          // конечная точка {row, col}
          let formattedStart = formatNumberToCoordinates(start);
          let formattedEnd = formatNumberToCoordinates(end);

          // массив точек, которые образуют нужный путь
          const path = [];

          // пока не дошли до точки start
          while (!(current.row === formattedStart.row && current.col === formattedStart.col)) {
            // заносим в массив точек текущую рассматриваемую точку
            path.push(current);
            // заносим в текущую рассматриваемую точку заразителя текущей рассматриваемой точки 43
            current = formatNumberToCoordinates(infestorsField[current.row][current.col]);
          }

          path.push(formattedStart)

          // возвращаем путь в формате [{row, col}]
          return path;
        };

        // !!!!!!!!!! ФУНКЦИЯ ПРОВЕРЯЕТ, ЧТО КООРДИНАТЫ ЛЕЖАТ ВНУТРИ ГРАНИЦ 0, 10 !!!!!!!!!!!!!!!!!!
        const areCoordinatesCorrect = (row, col) => {
          return row >= 0 && row <= 9 && col >= 0 && col <= 9;
        };

        // заражает клетку
        const infectPoint = (field, infestorsField, currentInfestorRow, currentInfestorCol, direction, pointToSearch, lastInfectedPointsLocal) => {

          let row = currentInfestorRow, col = currentInfestorCol;

          if (direction === 'UP') {
            row = currentInfestorRow - 1;
          } else if (direction === 'DOWN') {
            row = currentInfestorRow + 1;
          } else if (direction === 'RIGHT') {
            col = currentInfestorCol + 1;
          } else if (direction === 'LEFT') {
            col = currentInfestorCol - 1;
          }

          if (!areCoordinatesCorrect(row, col)) {
            return;
          }

          if (
            infestorsField[row][col] === EMPTY_INFESTOR_VALUE &&
            (field[row][col] === FILLER ||
              field[row][col] === pointToSearch)
          ) {
            infestorsField[row][col] = formatCoordinatesToNumber(currentInfestorRow, currentInfestorCol);
            lastInfectedPointsLocal.push(formatCoordinatesToNumber(row, col));
          }

        };

        const allCombinations = [
          [
            [3, 4],
            [2, 3],
            [1, 2],
          ],
          [
            [1, 2],
            [2, 3],
            [3, 4],
          ],
          [
            [1, 2],
            [3, 4],
            [2, 3],
          ],
          [
            [2, 3],
            [1, 2],
            [3, 4],
          ],
          [
            [2, 3],
            [3, 4],
            [1, 2],
          ],
          [
            [3, 4],
            [1, 2],
            [2, 3],
          ],
        ];
        // путь типа А - это горизонтальный путь
        // путь типа B - это вертикальный  путь

        // массив со всеми рабочими комбинациями
        const resCombinations = [];

        // объект со всеми возможными комбинациями вида {1-2: [], 2-3: [],3-4: []}
        let paths = {
          '1-2': [],
          '2-3': [],
          '3-4': [],
        };

        for (let combination = 0; combination < allCombinations.length; combination++) {
          let field = createField(stations);

          for (let pair = 0; pair < allCombinations[combination].length; pair++) {
            // если это первая пара, то
            if (pair === 0) {
              // нашли путь типа А от 1 до 2
              const field1 = findPathBetweenTwoPoints(
                field,
                stations[allCombinations[combination][pair][0] - 1],
                stations[allCombinations[combination][pair][1] - 1],
                'A',
                allCombinations[combination][pair][1],
                allCombinations[combination][pair][0]
              );
              // нашли путь типа B от 1 до 2
              const field2 = findPathBetweenTwoPoints(
                field,
                stations[allCombinations[combination][pair][0] - 1],
                stations[allCombinations[combination][pair][1] - 1],
                'B',
                allCombinations[combination][pair][1],
                allCombinations[combination][pair][0]
              );
              paths['1-2'] = [field1, field2].filter((it) => Boolean(it));
            }

            // если это вторая пара, то
            else if (pair === 1) {
              // идем по раннее найденным путям
              for (let path = 0; path < paths["1-2"].length; path++) {
                // находим путь от точки 2 до точки 3 типа А с учетом данного пути
                const field1 = findPathBetweenTwoPoints(
                  paths['1-2'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'A',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );

                // находим путь от точки 2 до точки 3 типа B с учетом данного пути
                const field2 = findPathBetweenTwoPoints(
                  paths['1-2'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'B',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );


                field1 ? paths['2-3'].push(field1) : null;
                field2 ? paths['2-3'].push(field2) : null;

              }
            }

            // если это третья пара, то
            else if (pair === 2) {
              // идем по раннее найденным путям
              for (let path = 0; path < paths["2-3"].length; path++) {
                // находим путь от точки 3 до точки 4 типа А с учетом данного пути
                const field1 = findPathBetweenTwoPoints(
                  paths['2-3'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'A',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );


                // находим путь от точки 3 до точки 4 типа B с учетом данного пути
                const field2 = findPathBetweenTwoPoints(
                  paths['2-3'][path],
                  stations[allCombinations[combination][pair][0] - 1],
                  stations[allCombinations[combination][pair][1] - 1],
                  'B',
                  allCombinations[combination][pair][1],
                  allCombinations[combination][pair][0]
                );

                field1 ? paths['3-4'].push(field1) : null;
                field2 ? paths['3-4'].push(field2) : null;
              }
            }
          }

          resCombinations.push(...paths['3-4'].filter(it => Boolean(it.field)));

          paths = {
            '1-2': [],
            '2-3': [],
            '3-4': [],
          };

        }

        let shortestLength = 10000000, shortestIndex = 0, shortestLengthLocal = 1000000;
        // console.log('resCombinations = ', resCombinations)
        // находим кратчайший путь
        for (let combination = 0; combination < resCombinations.length; combination++) {
          // находим длину данного пути
          shortestLengthLocal = findPathLength(resCombinations[combination].field);

          // сравниваем с текущей минимальной длинной, если короче, обновляем
          if (shortestLengthLocal < shortestLength) {
            shortestIndex = combination;
            shortestLength = shortestLengthLocal;
          }
        }

        const res = resCombinations[shortestIndex];

        if (!res || typeof res === 'undefined' || res.length === 0) {
          return null;
        } else {
          const point1 = formatNumberToCoordinates(stations[0]);
          const point2 = formatNumberToCoordinates(stations[1]);
          const point3 = formatNumberToCoordinates(stations[2]);
          const point4 = formatNumberToCoordinates(stations[3]);
          res.field[point1.row][point1.col] = "1";
          res.field[point2.row][point2.col] = "2";
          res.field[point3.row][point3.col] = "3";
          res.field[point4.row][point4.col] = "4";
          const resArr = Array.from(new Set(res.path['1-2'].concat(res.path['2-3']).concat(res.path['3-4'])))
          return resArr;
        }

      }
