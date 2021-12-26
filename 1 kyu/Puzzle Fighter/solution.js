seeStates = false;

/// ############################# helpers #############################
const angleToRad = (angle) => (Math.PI / 180) * angle;
class Vec2 {
  constructor(x = 0, y = 0) {
    this.x = x;
    this.y = y;
  }
  
  set(vec2) {
    this.x = vec2.x;
    this.y = vec2.y;
    return this;
  }
  add(vec2) {
    this.x += vec2.x;
    this.y += vec2.y;
    return this;
  }
  sub(vec2) {
    this.x -= vec2.x;
    this.y -= vec2.y;
    return this;
  }

  rotateOfVec2(vec2, rad) {
    return this.sub(vec2).rotate(rad).add(vec2);
  }
  rotate(rad) {
    const x = this.x;
    const y = this.y;
    const cos = Math.cos(rad);
    const sin = Math.sin(rad);
    this.x = cos * x + sin * y;
    this.y = cos * y - sin * x;
    return this;
  }
  round() {
    this.x = Math.round(this.x);
    this.y = Math.round(this.y);
    return this;
  }
  hash() {
    return `${this.x}-${this.y}`;
  }
  
  clone() {
    return new this.constructor(this.x, this.y);
  }
  
  toObj() {
    return {x: this.x, y: this.y};
  }
  toArray() {
    return [this.x, this.y];
  }
  
  static fromObject(obj) {
    return new this(obj.x, obj.y);
  }
  static fromArray(array) {
    return new this(array[0], array[1]);
  }
}
const arrayDeleteItem = (array, item) => {
  const i = array.indexOf(item);
  if ( i < 0 )
    return false;
  
  array.splice(i, 1);
  return true;
}
/// ###################################################################

const GAME_WIDTH = 6;
const GAME_HEIGHT = 12;



const GEM_NORMAL  = 1;
const GEM_CRASH   = 2;
const GEM_RAINBOW = 3;

const GEM_COLOR_R = 1;
const GEM_COLOR_G = 2;
const GEM_COLOR_B = 3;
const GEM_COLOR_Y = 4;

const GEM_COLOR_MAP = [
  ["R", GEM_COLOR_R,],
  ["G", GEM_COLOR_G,],
  ["B", GEM_COLOR_B,],
  ["Y", GEM_COLOR_Y,],
];
const GEM_COLOR_FROM_CHAR_MAP = new Map(GEM_COLOR_MAP);
const GEM_CHAR_FROM_COLOR_MAP = new Map(GEM_COLOR_MAP.map(a => a.reverse()));

class GeometryBBox {
  constructor() {
    this.pos = new Vec2(0, 0);
    this._mins = new Vec2(Number.POSITIVE_INFINITY, Number.POSITIVE_INFINITY);
    this._maxs = new Vec2(Number.NEGATIVE_INFINITY, Number.NEGATIVE_INFINITY);
  }
  
  updateBBox() {
    this._mins.add(this.pos);
    this._maxs.add(this.pos);
    this.pos.x = 0;
    this.pos.y = 0;
    return this;
  }
  
  get mins() {
    return this._mins.clone().add(this.pos);
  }
  get maxs() {
    return this._maxs.clone().add(this.pos);
  }

  get width() {
    return this.maxs.x - this.mins.x + 1;
  }
  get height() {
    return this.maxs.y - this.mins.y + 1;
  }
  get square() {
    return this.width * this.height;
  }


  includesPoint(p) {
    return (
      this.mins.x <= p.x &&
      this.mins.y <= p.y &&
      this.maxs.x >= p.x &&
      this.maxs.y >= p.y 
    );
  }
  intersectBBox(bbox, twoMode = true) {
    const p1 = bbox.mins.clone();
    const p2 = bbox.mins.clone();
    p2.x = bbox.maxs.x;
    
    const p3 = bbox.mins.clone();
    p3.y = bbox.maxs.y;
    const p4 = bbox.maxs.clone();
    
    return (
      this.includesPoint(p1) ||
      this.includesPoint(p2) ||
      this.includesPoint(p3) ||
      this.includesPoint(p4)
    ) && (twoMode ? bbox.intersectBBox(this, false) : true);
  }
  includesBBox(bbox) {
    return (
      this.mins.x <= bbox.mins.x &&
      this.mins.y <= bbox.mins.y &&
      this.maxs.x >= bbox.maxs.x &&
      this.maxs.y >= bbox.maxs.y 
    );
  }
}
class Gem extends GeometryBBox {
  constructor(type, color) {
    super();
    this._mins = new Vec2(0, 0);
    this._maxs = new Vec2(0, 0);

    this.type = type;
    this.color = color;
    this.pos = new Vec2();
  }

  toString() {
    switch(this.type) {
      case GEM_NORMAL : return GEM_CHAR_FROM_COLOR_MAP.get(this.color);
      case GEM_CRASH  : return GEM_CHAR_FROM_COLOR_MAP.get(this.color).toLowerCase();
      case GEM_RAINBOW: return "0";
    }
  }
  
  static fromChar(char) {
    if ( char === "0" )
      return new this(GEM_RAINBOW);

    const charUpper = char.toUpperCase();
    if ( !GEM_COLOR_FROM_CHAR_MAP.has(charUpper) )
      throw new Error(`Invalid gem char '${char}'`);
    
    return new this(char === charUpper ? GEM_NORMAL : GEM_CRASH, 
      GEM_COLOR_FROM_CHAR_MAP.get(charUpper) );
  }
}
class PowerGem extends GeometryBBox {
  constructor(type, color, gems = []) {
    super();
    this.gems = [];

    this.type = type;
    this.color = color;
    
    this.addGems(gems);
  }

  addGems(gems) {
    this.updateBBox();
    this._mins.x = Math.min(this._mins.x, ...gems.map(gem => gem.mins.x));
    this._maxs.x = Math.max(this._maxs.x, ...gems.map(gem => gem.mins.x));
    this._mins.y = Math.min(this._mins.y, ...gems.map(gem => gem.mins.y));
    this._maxs.y = Math.max(this._maxs.y, ...gems.map(gem => gem.mins.y));
    this.gems.push(...gems);
  }
  addPowerGem(powerGem) {
    this.updateBBox();
    this._mins.x = Math.min(this._mins.x, powerGem.mins.x);
    this._maxs.x = Math.max(this._maxs.x, powerGem.maxs.x);
    this._mins.y = Math.min(this._mins.y, powerGem.mins.y);
    this._maxs.y = Math.max(this._maxs.y, powerGem.maxs.y);
    this.gems.push(...powerGem.gems);
  }

  toString() {
    return Gem.prototype.toString.bind(this)();
  }
}

class GemPair {
  constructor(gem1, gem2) {
    this.gems = [gem1, gem2];
    this.gems[0].pos.set(new Vec2(3, 0));
    this.gems[1].pos.set(new Vec2(3, 1));
  }

  normalizeX() {
    const moveVector = new Vec2();
    for(const gem of this.gems) {
      if ( gem.pos.x < 0 ) {
        moveVector.x++;
        break;
      }
      if ( gem.pos.x >= GAME_WIDTH ) {
        moveVector.x--;
        break;
      }
    }

    this.gems.map(gem => gem.pos.add(moveVector));
  }
  normalizeY() {
    const moveVector = new Vec2();
    for(const gem of this.gems) {
      if ( gem.pos.y < 0 ) {
        moveVector.y++;
        break;
      }
      if ( gem.pos.y >= GAME_HEIGHT ) {
        moveVector.y--;
        break;
      }
    }

    this.gems.map(gem => gem.pos.add(moveVector));
  }
  moveX(dist) {
    this.gems.map(gem => gem.pos.x += dist);
    this.normalizeX();
  }
  rotate(angle) {
    const [gem1, gem2] = this.gems;
    gem2.pos.rotateOfVec2(gem1.pos, angleToRad(angle)).round();
    this.normalizeX();
  }
  
  evalInstruction(cmdChar) {
    switch(cmdChar) {
      case "L": return this.moveX(-1);
      case "R": return this.moveX(+1);
      case "A": return this.rotate(+90);
      case "B": return this.rotate(-90);
      default : throw new Error(`Invalid gem cmd '${cmdChar}'`);
    }
  }
  evalInstructions(cmdChars) {
    [...cmdChars].map(cmdChar => this.evalInstruction(cmdChar));
    this.normalizeY();
  }

  static fromChars(chars) {
    return new this(Gem.fromChar(chars[0]), Gem.fromChar(chars[1]));
  }
}

class Game {
  constructor() {
    this.objects = [];
  }
  
  get gems() {
    return this.objects.filter(obj => obj instanceof Gem);
  }
  get powerGems() {
    return this.objects.filter(obj => obj instanceof PowerGem);
  }

  canAddObject(obj) {
    return this.objects
      .every(obj2 => !obj2.intersectBBox(obj));
  }
  addObject(obj) {
    this.objects.push(obj);
  }
  delObject(obj) {
    return arrayDeleteItem(this.objects, obj);
  }

  getGemByPosRaw(x, y) {
    return this.getGemByPos(new Vec2(x, y));
  }
  getGemByPos(pos) {
    const obj = this.getObjectByPos(pos);
    return obj instanceof Gem ? obj : null;
  }
  getGemsAroundPos(pos) {
    return this
      .getObjectsAroundPos(pos)
      .filter(obj => obj instanceof Gem);
  }

  getObjectByPos(pos) {
    return this.objects.find(obj => obj.includesPoint(pos))
  }
  getObjectByPosRaw(x, y) {
    return this.getObjectByPos(new Vec2(x, y));
  }
  getObjectsAroundPos(pos) {
    const rules = [
      [ 0, 1],
      [ 0,-2],
      [ 1, 1],
      [-2, 0],
    ];
    
    const pos2 = pos.clone();
    return rules.map(rule => {
      pos2.x += rule[0];
      pos2.y += rule[1];
      return this.getObjectByPos(pos2);
    }).filter(Boolean);
  }
  getObjectsAroundObj(obj) {
    const points = [];
    for(let x = obj.mins.x; x <= obj.maxs.x; x++)
      points.push( new Vec2(x, obj.mins.y - 1), new Vec2(x, obj.maxs.y + 1) )
    for(let y = obj.mins.y; y <= obj.maxs.y; y++)
      points.push( new Vec2(obj.mins.x - 1, y), new Vec2(obj.maxs.x + 1, y) );
    
    return points
      .map(p => this.getObjectByPos(p))
      .filter(Boolean);
  }

  updateGravity() {
    return this.objects
      .sort((l, r) => r.maxs.y - l.maxs.y)
      .filter(obj => obj.maxs.y < GAME_HEIGHT - 1)
      .filter(obj => {
        for(let x = obj.mins.x; x <= obj.maxs.x; x++)
          if ( this.getObjectByPosRaw(x, obj.maxs.y + 1) )
            return false;
        return true;
      })
      .map(obj => obj.pos.y++)
      .length;
  }

  /// crash gem logic
  deleteObjsFromCrashGem(crashObj) {
    this.delObject(crashObj);
    this.getObjectsAroundObj(crashObj)
      .filter(obj => obj.color === crashObj.color)
      .map(obj => this.deleteObjsFromCrashGem(obj));
  }
  updateCrashGems() {
    return this.gems
      .filter(gem => gem.type === GEM_CRASH)
      .filter(gemCrash =>
        this.getObjectsAroundObj(gemCrash)
          .find(gem => gem.color === gemCrash.color) )
      .map(gemCrash =>
        this.deleteObjsFromCrashGem(gemCrash) )
      .length;
  }

  /// rainbow gem logic
  updateRainbowGems() {
    return this.gems
      .filter(gem => gem.type === GEM_RAINBOW)
      .sort((l, r) => l.maxs.y - r.maxs.y)
      .map(rainbowGem => {
        this.delObject(rainbowGem);

        const downObject = this.getObjectByPosRaw(rainbowGem.mins.x, rainbowGem.mins.y + 1);
        if ( !downObject || ![GEM_NORMAL, GEM_CRASH].includes(downObject.type) )
          return;
        
        this.objects
          .filter(obj => obj.color === downObject.color)
          .map(obj => this.delObject(obj));
      })
      .length;
  }
  
  /// collect power gems from gems
  searchPowerGemForGem(gem) {
    const rows = [];
    for(let y = gem.pos.y; y < GAME_HEIGHT; y++) {
      const row = [];
      for(let x = gem.pos.x; x < GAME_WIDTH; x++) {
        const gem2 = this.getGemByPosRaw(x, y);
        if ( !gem2 || gem2.color !== gem.color || gem2.block )
          break;
        
        row.push(gem2);
      }
      if ( row.length < 2 )
        break;
      
      rows.push(row);
    }
    
    if ( rows.length < 2 )
      return null;

    const minRowLength = Math.min(...rows.map(row => row.length));
    rows.map(row => row.splice(minRowLength));
    
    return new PowerGem(gem.type, gem.color, [].concat(...rows));
  }
  searchPowerGemsFromGems() {
    const powerGems = this.gems
      .map(gem => this.searchPowerGemForGem(gem))
      .filter(Boolean);
    
    const removeIncludesPowerGems = powerGems => {
      powerGems.sort((l, r) => r.square - l.square);

      const set = new Set();
      for(let i = 0; i < powerGems.length - 1; i++)
        for(let j = i + 1; j < powerGems.length; j++) {
          if ( powerGems[i].includesBBox(powerGems[j]) )
            set.add(powerGems[j]);
        }
        
      return powerGems.filter(powerGem => !set.has(powerGem));
    }
    
    const powerGemsObjColor = powerGems.reduce((obj, powerGem) => 
      ( (obj[powerGem.color] = obj[powerGem.color] || []).push(powerGem), obj ), {});
    
    return [].concat(...Object.entries(powerGemsObjColor).map(([color, powerGems]) => {
      powerGems = removeIncludesPowerGems( powerGems.sort((l, r) => r.square - l.square) );
      
      const resultPowerGems = [];
      while(powerGems.length) {
        const powerGem = powerGems.shift();
        const intersectPowerGems = [
          powerGem,
          ...powerGems.filter(powerGem2 => powerGem.intersectBBox(powerGem2))
        ];
        
        powerGems = powerGems.filter(powerGem => !intersectPowerGems.includes(powerGem));
        
        intersectPowerGems.sort((l, r) => l.mins.y - r.mins.y);
        const finalPowerGem = intersectPowerGems.shift();
        resultPowerGems.push(finalPowerGem);
      }
      
      return resultPowerGems;
    }));
  }
  collectPowerGemsFromGems() {
    let count = 0;
    while(1) {
      const tmpPowerGems = this.searchPowerGemsFromGems();
      if ( !tmpPowerGems.length )
        break;
      
      tmpPowerGems.map(powerGem => powerGem.gems.map(gem => this.delObject(gem)) );
      tmpPowerGems.map(powerGem => this.addObject(powerGem));
      
      count += tmpPowerGems.length;
    }
    return count;
  }

  expandPowerGemsFromGems() {
    let count = 0;
    const powerGems = this.powerGems;

    const getGems = (gemsGroups, color, length) => 
      [].concat(...gemsGroups
        .map(gems =>
          gems
            .filter(gem => gem instanceof Gem)
            .filter(gem => gem.color === color) )
          .filter(gems => gems.length === length) );

    for(const powerGem of powerGems) {
      const gemsGroups = [[], []];
      for(let y = powerGem.mins.y; y <= powerGem.maxs.y; y++) {
        gemsGroups[0].push(this.getObjectByPosRaw(powerGem.mins.x - 1, y));
        gemsGroups[1].push(this.getObjectByPosRaw(powerGem.maxs.x + 1, y));
      }
      
      const gems = getGems(gemsGroups, powerGem.color, powerGem.height);
      if ( !gems.length )
        continue;

      count++;
      powerGem.addGems(gems);
      gems.map(gem => this.delObject(gem));
    }
    for(const powerGem of powerGems) {
      const gemsGroups = [[], []];
      for(let x = powerGem.mins.x; x <= powerGem.maxs.x; x++) {
        gemsGroups[0].push(this.getObjectByPosRaw(x, powerGem.mins.y - 1));
        gemsGroups[1].push(this.getObjectByPosRaw(x, powerGem.maxs.y + 1));
      }
      
      const gems = getGems(gemsGroups, powerGem.color, powerGem.width);
      if ( !gems.length )
        continue;

      count++;
      powerGem.addGems(gems);
      gems.map(gem => this.delObject(gem));
    }
    
    return count;
  }
  expandPowerGemsFromPowerGems() {
    let count = 0;
    
    repeat:
    while(1) {
      for(const powerGem of this.powerGems) {
        const powerGems2 = this.powerGems
          .filter(powerGem2 => powerGem2 !== powerGem)
          .filter(powerGem2 => powerGem2.color ===  powerGem.color)
          .filter(powerGem2 => (
              (powerGem2.maxs.x === powerGem.mins.x - 1 ||
                powerGem2.mins.x === powerGem.maxs.x + 1) &&
              powerGem2.maxs.y === powerGem.maxs.y &&
              powerGem2.mins.y === powerGem.mins.y 
            ) || (
              (powerGem2.maxs.y === powerGem.mins.y - 1 ||
                powerGem2.mins.y === powerGem.maxs.y + 1) &&
              powerGem2.maxs.x === powerGem.maxs.x &&
              powerGem2.mins.x === powerGem.mins.x 
            ));
        
        if ( !powerGems2.length )
          continue;
        
        powerGem.addPowerGem(powerGems2[0]);
        this.delObject(powerGems2[0]);
        count++;
        continue repeat;
      }
      break;
    }
    
    return count;
  }

  tick() {
    while(this.updateGravity()) {}
    
    return 0 |
      this.updateCrashGems() |
      this.updateRainbowGems() |
      
      this.collectPowerGemsFromGems() |
      this.expandPowerGemsFromGems() |
      this.expandPowerGemsFromPowerGems();
  }
  tickAll() {
    while(this.tick()) {}
  }

  toString() {
    const map = Array.from(Array(GAME_HEIGHT), () => Array(GAME_WIDTH).fill(" "));
    for(const obj of this.objects)
      for(let y = obj.mins.y; y <= obj.maxs.y; y++)
        for(let x = obj.mins.x; x <= obj.maxs.x; x++)
          map[y][x] = obj.toString();

    return map.map(a => a.join("")).join("\n");
  }
  
  _devPrintGems() {
    const WG = gem => ` ${gem} `;
    
    const borderItem = WG("*");
    
    let map = Array.from(Array(GAME_HEIGHT), () => Array(GAME_WIDTH).fill(WG(" ")));
    
    const map2 = [];
    
    for(const obj of this.objects)
      for(let y = obj.mins.y; y <= obj.maxs.y; y++)
        for(let x = obj.mins.x; x <= obj.maxs.x; x++)
          if ( obj instanceof PowerGem ) {
            if ( y === obj.mins.y ) {
              let y2 = y*2;
              map2[y2] = map2[y2] || [];
              map2[y2][x] = 1;
            } else
            if ( y === obj.maxs.y ) {
              let y2 = y*2 + 2;
              map2[y2] = map2[y2] || [];
              map2[y2][x] = 1;
            }

            if ( x === obj.mins.x )
              map[y][x] = `(${obj} `;
            else
            if ( x === obj.maxs.x )
              map[y][x] = ` ${obj})`;
            else
              map[y][x] = ` ${obj} `;
          } else
            map[y][x] = ` ${obj} `;
    
    map = map.map(row => [borderItem, ...row, borderItem]);
    for(let i = map.length; i >= 0; i--)
      map.splice(i, 0, Array(GAME_WIDTH+2).fill(borderItem));
      
    for(let y = 0; y < map.length; y += 2)
      map[y] = map[y].map((v, x) =>
        (map2[y] && map2[y][x - 1]) ? " - " : v
      );

    return map.map(a => a.join("")).join("\n");
  }
}

const DEV_MODE = false;
function puzzleFighter(inputArray, expected) {
  const game = new Game();

  for(let i = 0; i < inputArray.length; i++) {
    const [gemPairChars, instructions] = inputArray[i];
    
    const gemPair = GemPair.fromChars(gemPairChars);
    gemPair.evalInstructions(instructions);
    if ( !gemPair.gems.every(gem => game.canAddObject(gem)) )
      break;
    
    gemPair.gems.map(gem => game.addObject(gem));
    game.tickAll();
    
    if ( DEV_MODE ) {
      console.log([gemPairChars, instructions]);
      console.log(game._devPrintGems());
    }
  }
  
  return game.toString();
}


#########################################
let _pgid = 0;
let range=n=>[...Array(n).keys()];
let matrix=(h,w,fn)=>range(h).map((_,i)=>range(w).map((_,j)=>fn(i,j)));

class Pair {
  constructor(syms,moves,w,y0=0,x0=3,y1=1,x1=3) {
    this.y0 = y0;
    this.x0 = x0;
    this.y1 = y1;
    this.x1 = x1;
    this.w = w;
    this.moves = moves;
    this.sym0 = syms[0];
    this.sym1 = syms[1];
    for (let move of [...moves]) {
      switch (move) {
        case 'L': this.left(); break;
        case 'R': this.right(); break;
        case 'B': this.rotr(); break;
        case 'A': this.rotl(); break;
      }
    }
  }
  gems() {
    return [new Gem(this.sym0), new Gem(this.sym1)];
  }
  align() {
    let miny = Math.min(this.y0,this.y1);
    let minx = Math.min(this.x0,this.x1);
    let maxx = Math.max(this.x0,this.x1);
    if (miny<0) { this.y0++; this.y1++; }
    if (miny>0) { this.y0--; this.y1--; }
    if (minx<0) { this.x0++; this.x1++; }
    if (maxx>=this.w) { this.x0--; this.x1--; }
  }
  left() {
    this.x0--;
    this.x1--;
    this.align();
  }
  right() {
    this.x0++;
    this.x1++;
    this.align();
  }
  rotr() {
    let dy = this.y1-this.y0;
    let dx = this.x1-this.x0;
    [dy,dx] = [dx,-dy];
    this.y1 = this.y0+dy;
    this.x1 = this.x0+dx;
    this.align();
  }
  rotl() {
    let dy = this.y1-this.y0;
    let dx = this.x1-this.x0;
    [dy,dx] = [-dx,dy];
    this.y1 = this.y0+dy;
    this.x1 = this.x0+dx;
    this.align();
  }
}

class Gem {
  constructor(sym,h=1,w=1) {
    this.sym = sym;
    this.y = null;
    this.x = null;
    this.board = null;
    this.h = h;
    this.w = w;
    this.color = sym.toUpperCase();
    this.hasCrashEffect = sym!=this.color;
    this.hasRainbowEffect = sym=='0';
    this.pgid=this.isPowerGem()?_pgid++:-1;
  }
  hasEffects() {
    return this.hasCrashEffect||this.hasRainbowEffect;
  }
  canAddTo(board,y0,x0) {
    if (y0<0||x0<0||y0+this.h>board.h||x0+this.w>board.w) return false;
    for (let y=y0; y<y0+this.h; y++)
      for (let x=x0; x<x0+this.w; x++)
        if (board.grid[y][x].content!=null)
          return false;
    return true;
  }
  addTo(board,y,x) {
    if (!this.canAddTo(board,y,x)) return false;
    this.board = board;
    this.y = y;
    this.x = x;
    this.restore();
    this.board.gems.add(this);
    return true;
  }
  remove() {
    if (this.board==null) return false;
    this.board.gems.delete(this);
    this.suspend();
    this.board = null;
    this.y = null;
    this.x = null;
    return true;
  }
  fits(y,x,h,w) {
    return this.y>=y&&this.x>=x&&this.y+this.h<=y+h&&this.x+this.w<=x+w;
  }
  canDrop() {
    let node = this.bottomLeft();
    if (node.down==null) return false;
    while (node!=null&&node.content==this) {
      if (node.down.content!=null) return false;
      node = node.right;
    }
    return true;
  }
  drop() {
    if (!this.canDrop()) return false;
    this.suspend();
    this.y++;
    this.restore();
    return true;
  }
  fall() {
    let depth = 0;
    while (this.drop()) depth++;
    return depth;
  }
  suspend() {
    for (let y=this.y; y<this.y+this.h; y++)
      for (let x=this.x; x<this.x+this.w; x++)
        this.board.grid[y][x].content=null;
  }
  restore() {
    for (let y=this.y; y<this.y+this.h; y++)
      for (let x=this.x; x<this.x+this.w; x++)
        this.board.grid[y][x].content=this;
  }
  topLeft() {
    return this.board.grid[this.y][this.x];
  }
  bottomLeft() {
    let node = this.topLeft();
    while (node.down!=null&&node.down.content==this)
      node = node.down;
    return node;
  }
  isPowerGem() {
    return this.h>1&&this.w>1;
  }
  render() {
    return this.isPowerGem()?this.sym+this.pgid:this.sym;
  }
}

class Node {
  constructor(y,x) {
    this.y = y;
    this.x = x;
    this.content = null;
    this.left = this.right = this.up = this.down = null;
  }
  render() {
    return (this.content==null?'°':this.content.render()).padStart(2+String(_pgid).length,' ');
  }
}

class Board {
  constructor(h,w) {
    this.h = h;
    this.w = w;
    this.gems = new Set();
    this.init();
  }
  init() {
    this.grid = matrix(this.h,this.w,(y,x)=>new Node(y,x));
    for (let y=0; y<this.grid.length; y++) {
      for (let x=0; x<this.grid[y].length; x++) {
        if (y>0) this.grid[y][x].up = this.grid[y-1][x];
        if (y+1<this.h) this.grid[y][x].down = this.grid[y+1][x];
        if (x>0) this.grid[y][x].left = this.grid[y][x-1];
        if (x+1<this.w) this.grid[y][x].right = this.grid[y][x+1];
      }
    }
  }
  cmpFall(a,b) {
    if (a.y>b.y) return -1;
    if (a.y<b.y) return 1;
    return 0;
  }
  fall() {
    let m = 0;
    let gems = [...this.gems].sort(this.cmpFall);
    for (let gem of gems) {
      m += gem.fall();
    }
    return m>0;
  }
  rainbow() {
    let gems = [...this.gems].filter(g=>g.hasRainbowEffect);
    for (let gem of gems) {
      let node = gem.topLeft();
      let gemsToDestroy = [gem];
      if (node.down!=null&&node.down.content!=null) {
        if (node.down.content.hasRainbowEffect) continue;
        let color = node.down.content.color;
        gemsToDestroy = gemsToDestroy.concat([...this.gems].filter(g=>g.color==color));
      }
      gemsToDestroy.forEach(g=>g.remove());
      return true;
    }
    return false;
  }
  crash() {
    let gems = [...this.gems].filter(g=>g.hasCrashEffect);
    for (let gem of gems) {
      let node = gem.topLeft();
      let cnt = 0;
      if (node.down!=null&&node.down.content!=null&&node.down.content.color==gem.color) cnt++;
      if (node.up!=null&&node.up.content!=null&&node.up.content.color==gem.color) cnt++;
      if (node.left!=null&&node.left.content!=null&&node.left.content.color==gem.color) cnt++;
      if (node.right!=null&&node.right.content!=null&&node.right.content.color==gem.color) cnt++;
      if (cnt==0) continue;
      let visitedNodes = new Set();
      let connectedGems = new Set();
      let queue = [gem.topLeft()];
      while (queue.length) {
        node = queue.pop();
        if (node==null||node.content==null||
            node.content.color!=gem.color||node.content.hasRainbowEffect||visitedNodes.has(node))
          continue;
        visitedNodes.add(node);
        connectedGems.add(node.content);
        queue.push(node.left);
        queue.push(node.right);
        queue.push(node.up);
        queue.push(node.down);
      }
      [...connectedGems].forEach(g=>g.remove());
      return true;
    }
    return false;
  }
  cmpPowerGemFormation(a,b) {
    if (a.y<b.y) return -1;
    if (a.y>b.y) return 1;
    if (a.x<b.x) return -1;
    if (a.x>b.x) return 1;
    return 0;
  }
  formatPowerGem(y0,x0,h,w,sym,predicate) {
    let gems = new Set();
    for (let y=y0; y<y0+h; y++) {
      for (let x=x0; x<x0+w; x++) {
        let node = this.grid[y][x];
        if (!predicate(y0,x0,h,w,node)) return false;
        gems.add(node.content);
      }
    }
    if (gems.size<2) return false;
    gems.forEach(g=>g.remove());
    let powerGem = new Gem(sym,h,w);
    powerGem.addTo(this,y0,x0);
    return true;
  }
  powerGemFormationWalker(predicateEligibleIn, predicateMatch) {
    let predicateEligible = g=>!g.hasEffects()&&predicateEligibleIn(g);
    let gems = [...this.gems].filter(predicateEligible).sort(this.cmpPowerGemFormation);
    for (let gem of gems) {
      let fn = n=>n!=null&&n.content!=null&&n.content.color==gem.color&&predicateEligible(n.content);
      let gn = (y,x,h,w,n)=>fn(n)&&predicateMatch(y,x,h,w,n.content);
      let topLeft = gem.topLeft();
      let topRight = topLeft;
      while (fn(topRight.right)) topRight = topRight.right;
      while (topRight.x>topLeft.x) {
        let bottomRight = topRight;
        while (fn(bottomRight.down)) bottomRight = bottomRight.down;
        while (bottomRight.y>topRight.y) {
          let [y,x,h,w] = [topLeft.y,topLeft.x,bottomRight.y-topLeft.y+1,topRight.x-topLeft.x+1];
          if (this.formatPowerGem(y,x,h,w,gem.sym,gn)) return true;
          bottomRight = bottomRight.up;
        }
        topRight = topRight.left;
      }
    }
    return false;
  }
  powerGemFormation() {
    let predicateEligible = g=>!g.isPowerGem();
    let predicateMatch = (y,x,h,w,g)=>true;
    return this.powerGemFormationWalker(predicateEligible, predicateMatch);
  }
  powerGemClusterFormation() {
    let predicateEligible = g=>true;
    let predicateMatch = (y,x,h,w,g)=>g.fits(y,x,h,w);
    return this.powerGemFormationWalker(predicateEligible, predicateMatch);
  }
  solveStep() {
    this.fall();
    for (;;) {
      while (this.rainbow());
      while (this.crash());
      while (this.powerGemFormation());
      while (this.powerGemClusterFormation());
      if (!this.fall()) break;
    }
  }
  solve(arr) {
    for (let [syms,moves] of arr) {
      let pair = new Pair(syms,moves,this.w);
      let [gemA, gemB] = pair.gems();
      if (!gemA.addTo(this,pair.y0,pair.x0)) break;
      if (!gemB.addTo(this,pair.y1,pair.x1)) { gemA.remove(); break; }
      this.solveStep();
    }
    return this.out();
  }
  out() {
    return this.grid.map(r=>r.map(c=>c.content==null?' ':c.content.sym).join``).join`\n`;
  }
  render() {
    return this.grid.map(r=>r.map(c=>c.render()).join``).join`\n`+`\n`;
  }
}

function puzzleFighter(arr) {
  let board = new Board(12,6);
  let res = board.solve(arr);
  return res;
}

######################################
function puzzleFighter(ar){
  const MN = [[-1,0],[0,1],[1,0],[0,-1]];
  const tome = Array.from({length:13},_ => Array(6).fill('')),
      pgData = {};
  let peak = 12,
    pgn = 0;
  const gameState = _ => tome.map(e => e.map(v => v ? v[0] : ' ').join('')).slice(0,12).join('\n');
  const refresh = _ => {
    let z,i,k,i2,i3,j2,
      crashG = [];
    for (i = 10; i >= peak; i--){
      for (let j = 0; j < 6; j++){
        z = tome[i][j];
        if (z && tome[i+1][j] === ''){
          if (z[1]){
            let n = z.slice(1),
              p = pgData[n],
              h = p[2][0] - p[1][0];
            j2 = p[1][1];
            k = p[2][1];
            i2 = i;
            while (tome[++i2].slice(j2,k).every(v => v === '')){}
            if (i2 === i + 1){j = k - 1; continue}
            for (i3 = p[1][0]; i3 < --i2 && i3 !== p[2][0]; i3++){
              if (tome[i2][p[1][1]]){break}
              for (j2 = p[1][1]; j2 < k; j2++){
                tome[i3][j2] = '';
                tome[i2][j2] = z}}
            p[1][0] = i3 === p[2][0] ? i2 + 1 : i3;
            p[2][0] = p[1][0] + h}
          else {
            k = i2 = i;
            while (tome[++i2][j] === ''){}
            i2--;
            while (k >= peak && (!tome[k][j] || !tome[k][j][1])){
              if (tome[k][j]){
                tome[i2--][j] = tome[k][j];
                tome[k][j] = ''}
              k--}}}}}
    while (++i < 12){
      if (tome[i].some(e => e)){peak = i; break}}
    for (i = peak; i < 12; i++){
      tome[i].forEach((e,j) => e && 'rgby'.includes(e) ? crashG.push([[i,j],e]) : false)}
    return crashG.length ? crashG : false};  
  const crashProc = ([x,y],clr) => {
    const clR = clr + clr.toUpperCase(),
        scout = ([x1,y1],[x2,y2]) => tome[x1+=x2] && tome[x1][y1+=y2] && clR.includes(tome[x1][y1][0]) ? [x1,y1] : null;
    let r = [],
      tr = [],
      z;
    MN.forEach(v => {
      z = scout(v,[x,y]);
      if (z){r.push(z)}});
    if (!r.length){return false}
    tome[x][y] = '';
    while (r.length){
      r.forEach(([xx,yy]) => {
        if (tome[xx][yy][1] && pgData[tome[xx][yy].slice(1)]){
          delete pgData[tome[xx][yy].slice(1)]}
        if (tome[xx][yy] === ''){return}
        tome[xx][yy] = '';
        MN.forEach(v => {
          z = scout(v,[xx,yy]);
          if (z){tr.push(z)}})});
      [r,tr] = [tr,[]]}
    return true};  
  const pgRangeCheck = (...r) => {
    let [rng,xy,end,inc,clr,pgr] = r;
    if (pgr.some(e => pgData[e] && pgData[e][1][xy] < rng[0] || pgData[e][2][xy] > rng[1])){
      return false}
    let scanRng = pgr.reduce((a,e) => inc ? Math.max(pgData[e][2][xy^1],a) : Math.min(pgData[e][1][xy^1],a),end),
      [ia,iz,ja,jz] = xy ? (inc ? [end,scanRng,...rng] : [scanRng,end,...rng]) : (inc ? [...rng,end,scanRng] : [...rng,scanRng,end]),
      v;
    for (let i = ia; i < iz; i++){
      for (let j = ja; j < jz; j++){
        v = tome[i][j];
        if (!v || v[0] !== clr){return false}
        if (v[1] && !pgr.includes(v.slice(1))){
          pgr.push(v.slice(1));
          if (!pgRangeCheck(...r)){return false}}}}
    return pgr};  
  const pgUpdate = _ => {
    let z,z0,i,j,i2,j2,vi,vj;
    for (i = peak; i < 12; i++){
      for (j = 0; j < 6; j++){
        z = tome[i][j];
        if (!z || z[1]){continue}
        if ([[i,j+1],[i+1,j],[i+1,j+1]].every(([x,y]) => tome[x][y] === z)){
          pgData[++pgn] = [z,[i,j]];
          i2 = i + 1;
          j2 = j + 1;
          while (tome[i][j2] === z && tome[i2][j2] === z){j2++}
          while (tome[++i2].slice(j,j2).every(v => v === z)){}
          for (vi = i; vi < i2; vi++){
            for (vj = j; vj < j2; vj++){
              tome[vi][vj] += pgn}}
          pgData[pgn].push([i2,j2])}}}
    for (let n in pgData){
      [z0,[i,j],[i2,j2]] = pgData[n];
      const nv = `${z0}${n}`;
      [[-1,-1],[1,6]].forEach(([inc,bnd],q) => {
        [vi,vj] = q ? [i,j2-1] : [i,j];
        expand:
        while ((vj+=inc) !== bnd && tome[i][vj].startsWith(z0)){
          while (vi !== i2 && tome[vi][vj].startsWith(z0)){
            if (tome[vi][vj][1]){
              const pgSet = [tome[vi][vj].slice(1)];
              let merge = q ? pgRangeCheck([i,i2],0,vj,1,z0,pgSet) : pgRangeCheck([i,i2],0,vj+1,0,z0,pgSet);
              if (merge){
                merge.forEach(e => {
                  vj = q ? Math.max(pgData[e][2][1]-1,vj) : Math.min(pgData[e][1][1],vj);
                  delete pgData[e]});
                vi = i2;
                break}
              else {break expand}}
            vi++}
          if (vi !== i2){break}
          vi = i}
        pgData[n][q+1][1] = vj + (q^1);
        q ? j2 = pgData[n][2][1] : j = pgData[n][1][1]});
      let [[pi,pj],[qi,qj]] = pgData[n].slice(1),
        jj = pj;
      for (; pi < qi; pi++){
        for (jj = pj; jj < qj; jj++){
          tome[pi][jj] = nv}}
      [[-1,-1],[1,12]].forEach(([inc,bnd],q) => {
        [vi,vj] = q ? [i2-1,j] : [i,j];
        expand:
        while ((vi+=inc) !== bnd && tome[vi][j].startsWith(z0)){
          while (vj !== j2 && tome[vi][vj].startsWith(z0)){
            if (tome[vi][vj][1]){
              const pgSet = [tome[vi][vj].slice(1)];
              let merge = q ? pgRangeCheck([j,j2],1,vi,1,z0,pgSet) : pgRangeCheck([j,j2],1,vi+1,0,z0,pgSet);
              if (merge){
                merge.forEach(e => {
                  vi = q ? Math.max(pgData[e][2][0]-1,vi) : Math.min(pgData[e][1][0],vi);//EDITED
                  delete pgData[e]});
                vj = j2;
                break}
              else {break expand}}
            vj++}
          if (vj !== j2){break}
          vj = j}
        pgData[n][q+1][0] = vi + (q^1);
        q ? i2 = pgData[n][2][0] : i = pgData[n][1][0]});
      [[pi,pj],[qi,qj]] = pgData[n].slice(1);
      jj = pj;
      for (; pi < qi; pi++){
        for (jj = pj; jj < qj; jj++){
          tome[pi][jj] = nv}}}};  
  tome[12].fill(0);
  for (let [pair,s] of ar){
    let y = 3,
      tail = 2,
      headXY,tailXY,
      gemCrash = false;
    for (let v of s){
      switch (v){
        case 'L': y--; break;
        case 'R': y++; break;
        case 'A': tail = (3 + tail) % 4; break;
        case 'B': tail = (tail + 1) % 4; break;
        default: throw new Error(`invalid instruction: "${v}"`)}
      y = y <= 0 ? (tail === 3 ? 1 : 0) : y >= 5 ? (tail === 1 ? 4 : 5) : y}
    headXY = [tome.findIndex(v => v[y] !== '') - 1,y];
    switch (tail){
      case 0: tailXY = [headXY[0]-1,y]; break;
      case 1: tailXY = [tome.findIndex(v => v[y+1] !== '')-1,y+1]; break;
      case 2: tailXY = [headXY[0],y]; headXY[0]--; break;
      case 3: tailXY = [tome.findIndex(v => v[y-1] !== '')-1,y-1]}
    if ([headXY,tailXY].some(e => e[0] < 0)){return gameState()}
    [headXY,tailXY].forEach(([x,y],c) => {
      tome[x][y] = pair[c];
      peak = Math.min(x,peak)});
    if (pair.includes('0')){
        let crashColor;
        [headXY,tailXY].forEach(([x,y],i) => {
          if (pair[i] === '0'){
            tome[x][y] = '';
            gemCrash = true;
            if (x === 11 || tome[x+1][y] === ''){return}
            crashColor = tome[x+1][y][0].toUpperCase();
            for (let j = peak; j < 12; j++){
              tome[j] = tome[j].map(e => {
                if (e && e[0].toUpperCase() === crashColor){
                  if (e[1]){delete pgData[e.slice(1)]}
                  return ''}
                else {return e}})}}})}
    [headXY,tailXY].forEach((v,c) => {
      if ('rgby'.includes(pair[c])){
        crashProc(v,pair[c]) ? gemCrash = true : false}
      else {
        MN.map(([x,y]) => [x+=v[0],y+=v[1]]).filter(([x,y]) => tome[x] && tome[x][y] && 'rgby'.includes(tome[x][y])).forEach(([x,y]) => gemCrash = crashProc([x,y],tome[x][y]) || gemCrash)}});
        pgUpdate();    
    while (gemCrash){
      gemCrash = refresh();
      gemCrash = gemCrash ? gemCrash.reduce((a,e) => crashProc(...e) || a,false) : false;
      pgUpdate()}
  }  
  return gameState();
}

#############################
class Piece {
  constructor(color) {
    this.color = color;
    this.powerGem = false;
  }
}

class RegularPiece extends Piece {
  constructor(color) {
    super(color);
  }
}

class EmptyPiece extends Piece {
  constructor() {
    super(' ');
  }
}

class Gem {
  constructor(sx, sy, ex, ey, color) {
    this.startX = sx;
    this.startY = sy;
    this.endX = ex;
    this.endY = ey;
    this.color = color;
  }
}

class Spot {
  constructor(x, y, color = ' ') {
    this.x = x;
    this.y = y;
    this.piece = new Piece(color);
  }
  
  get occupied() {
    return this.piece.color !== ' ';
  }
  
  clear() {
    this.piece = new EmptyPiece();
  }
}

class Game {
  constructor(instructions) {
    this.instructions = instructions;
    this.board = [...Array(12)].map((_, i) => [...Array(6)].map(($, j) => new Spot(i, j)));
    this.gems = [];
    this.move = 0;
    this.continueEffects = true;
  }
  
  execute() {
    for (const [pair, instructions] of this.instructions) {
      this.move++;
      let ax = 0, ay = 3, bx = 1, by = 3;
      let pos = 0;
      for (let c of instructions) {
        switch(c) {
            case 'L': {
              if (ay && by) ay--, by--;
              break;
            }
            case 'R': {
              if (ay < 5 && by < 5) ay++, by++;
              break;
            }
            case 'A': {
              if (pos === 0) by++, bx--;
              if (pos === 1) bx++, by++;
              if (pos === 2) ax--, by--;
              if (pos === 3) ax++, by--;
              pos += 3;
              break;
            }
            case 'B': {
              if (pos === 0) bx--, by--;
              if (pos === 1) ax++, by++;
              if (pos === 2) ax--, by++;
              if (pos === 3) bx++, by--;
              pos++;
              break;
            }
        }
        pos %= 4;
        if (ay < 0 || by < 0) ay++, by++;
        if (ay > 5 || by > 5) ay--, by--;
      }
      
      if (this.board[ax][ay].occupied || this.board[bx][by].occupied) {
        // Top reached
        return;
      }
      this.board[ax][ay].piece = new Piece(pair[0]);
      this.board[bx][by].piece = new Piece(pair[1]);
      this.continueEffects = true;
      
      while (this.continueEffects) {
        this.continueEffects = false;
        this.dropPieces();
        this.performEffects();
        this.dropPieces();
      }
      //this.displayBoard();
    }
  }
  
  performEffects() {
    this.destroyGems();
    this.removeBrokenGems();
    this.mergeSingles();
    this.mergeSinglesWithGems();
    this.mergeGemsWithGems();
  }
  
  removeBrokenGems() {
    for (let i = this.gems.length - 1; i >= 0; i--) {
      let gem = this.gems[i];
      if (!this.board[gem.startX][gem.startY].occupied) {
        this.gems.splice(i, 1);
      }
    }
  }
  
  mergeSingles() {
    for (let x = 0; x < 11; x++) {
      for (let y = 0; y < 5; y++) {
        let piece = this.board[x][y].piece;
        let color = piece.color;
        if (piece.powerGem || color === ' ') continue;
        let h = 0, w = 0;
        while (y + w < 5 
               && this.board[x][y + w + 1].piece.color === color
               && !this.board[x][y + w + 1].piece.powerGem
               && this.board[x + 1][y + w + 1].piece.color === color
               && !this.board[x + 1][y + w + 1].piece.powerGem) w++;
        if (w < 1) continue;
        for (; x + h < 11; h++) {
          let all = true;
          for (let k = x + h, l = y; l <= y + w; l++) {
            if (this.board[k+1][l].piece.color !== color
               || this.board[k+1][l].piece.powerGem) all = false;
          }
          if (!all) break;
        }
        if (h < 1) continue;
        const newGem = new Gem(x, y, x + h, y + w, color);
        this.gems.push(newGem);
        for (let i = x; i <= x + h; i++) {
          for (let j = y; j <= y + w; j++) {
            this.board[i][j].piece.powerGem = true;
          }
        }
      }
    }
  }
  
  mergeSinglesWithGems() {
    for (const gem of this.gems) {
      const color = gem.color;
      
      if (gem.startY > 0) {
        let all = true;
        for (let x = gem.startX, y = gem.startY - 1; x <= gem.endX; x++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.startY--;
          for (let x = gem.startX, y = gem.startY; x <= gem.endX; x++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles on LEFT
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.endY < 5) {
        let all = true;
        for (let x = gem.startX, y = gem.endY + 1; x <= gem.endX; x++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.endY++;
          for (let x = gem.startX, y = gem.endY; x <= gem.endX; x++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles on RIGHT
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.startX > 0) {
        let all = true;
        for (let x = gem.startX - 1, y = gem.startY; y <= gem.endY; y++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.startX--;
          for (let x = gem.startX, y = gem.startY; y <= gem.endY; y++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles ABOVE
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.endX < 11) {
        let all = true;
        for (let x = gem.endX + 1, y = gem.startY; y <= gem.endY; y++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.endX++;
          for (let x = gem.endX, y = gem.startY; y <= gem.endY; y++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles BELOW
          this.mergeSinglesWithGems();
        }
      }
      
    }
  }
  
  mergeGemsWithGems() {
    for (const gem of this.gems) {
      let right = this.gems.findIndex(other => other.color === gem.color && other.startX === gem.startX && other.endX === gem.endX && other.startY === gem.endY + 1);
      if (right !== -1) {
        // Merging 2 gems horizontally
        gem.endY = this.gems[right].endY;
        this.gems.splice(right, 1);
        this.mergeGemsWithGems();
      }
    }
    for (const gem of this.gems) {
      let below = this.gems.findIndex(other => other.color === gem.color && other.startY === gem.startY && other.endY === gem.endY && other.startX === gem.endX + 1);
      if (below !== -1) {
        // Merging 2 gems vertically
        gem.endX = this.gems[below].endX;
        this.gems.splice(below, 1);
        this.mergeGemsWithGems();
      }
    }
  }
  
  displayBoard() {
    console.log(`Board at move ${this.move}:`);
    console.log('-'.repeat(8));
    [...Array(12)].forEach((_, i) => console.log(`|${this.board[i].map(s => s.piece.color).join('')}|`));
    console.log('-'.repeat(8));
  }
  
  destroy(x, y, color) {
    if (x < 0 || y < 0 || x >= 12 || y >= 6) return;
    if (this.board[x][y].piece.color.toUpperCase() !== color.toUpperCase()) return;
    this.board[x][y].clear();
    for (const [dx, dy] of [ [0, -1], [-1, 0], [0, 1], [1, 0] ]) {
      this.destroy(x + dx, y + dy, color);
    }
  }
  
  destroyGems() {
    for (let x = 0; x < 12; x++) {
      for (let y = 0; y < 6; y++) {
        let color = this.board[x][y].piece.color;
        if (color === '0') {
          if (x !== 11 && this.board[x+1][y].occupied && this.board[x+1][y].piece.color !== '0') {
            let color = this.board[x+1][y].piece.color.toUpperCase();
            for (let i = 0; i < 12; i++) {
              for (let j = 0; j < 6; j++) {
                if (this.board[i][j].piece.color.toUpperCase() === color) {
                  this.board[i][j].clear();
                }
              }
            }
          }
          this.board[x][y].clear();
        } else if (/[rgby]/.test(color)) {
          for (const [dx, dy] of [ [0, -1], [-1, 0], [0, 1], [1, 0] ]) {
            let nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= 12 || ny >= 6) continue;
            let col = this.board[nx][ny].piece.color;
            if (col.toUpperCase() === color.toUpperCase()) {
              this.destroy(nx, ny, col);
              this.board[x][y].clear();
            }
          }
        }
      }
    }
  }
  
  dropPieces() {
    let modified = false;
    for (let i = 11; i >= 0; i--) {
      for (let j = 0; j < 6; j++) {
        if (this.board[i][j].piece.color !== ' ') {
          if (this.board[i][j].piece.powerGem) {
            const gem = this.gems.find(gem => i === gem.endX && j === gem.endY);
            if (!gem) continue;
            // move all powergem's pieces down
            for (let k = i + 1; k < 12; k++) {
              let isClearBelow = true;
              for (let l = gem.startY; l <= gem.endY; l++) {
                if (this.board[k][l].occupied) isClearBelow = false;
              }
              if (!isClearBelow) break;
              for (let l = k; l > gem.startX; l--) {
                for (let m = j; m >= gem.startY; m--) {
                  this.board[l][m].piece = this.board[l - 1][m].piece;
                  this.board[l - 1][m].piece = new EmptyPiece();
                }
              }
              gem.startX++;
              gem.endX++;
              modified = true;
            }
          } else {
            // non-powergem pieces
            for (let k = i + 1; k < 12; k++) {
              if (this.board[k][j].occupied) break;
              this.board[k][j].piece = this.board[k - 1][j].piece;
              this.board[k - 1][j].piece = new EmptyPiece();
              modified = true;
            }
          }
        }
      }
    }
    if (modified) {
      this.continueEffects = true;
      this.dropPieces();
    }
  }
  
  
  
  toString() {
    return this.board.map(row => row.map(spot => spot.piece.color).join('')).join('\n');
  }
}

function puzzleFighter(arr) {
  const board = [...Array(12)].map(_ => ' '.repeat(6));
  const game = new Game(arr);
  game.execute();
  return game.toString();
}
