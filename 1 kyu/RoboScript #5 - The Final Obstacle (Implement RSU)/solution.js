class RSUProgram {
  
  constructor(source) {
    this.source=source;
  }

  execute() {
    return this.executeRaw(this.convertToRaw(this.getTokens(this.source)));
  }
  
  getTokens(){
    return this.source
      .replace(/\/\*.*\*\//ms," ")
      .replace(/\/\/.*/g,"")
      .replace(/\s\d/,m=>{throw "unallowed token : "+m;})
      .replace(/\D0\d/,m=>{throw "unallowed postfix : "+m;})
      .replace(/[^RLF\d\spqP()+]/,m=>{throw "unallowed stray comment : ["+m+"]";})
      .replace(/\D\d*/g,m=>m+" ")
      .replace(/\s+/gms," ")
      .replace(/[pP] /ms,m=>{throw "unallowed pattern missing id";})
      .replace(/ \d+/ms,m=>{throw "unallowed stray numbers : ["+m+"]";})
      .trim().split(" ");
  }

  convertToRaw(tokenizedCode) {
    var code = this.handlePatterns(tokenizedCode,{},0).join("");
    while(code.includes("(")) code=code.replace(/\(([^()]*)\)(\d*)/g,(m,n,o)=>n.repeat(o||1));
    return code.replace(/[FLR]\d+/g,m=>m[0].repeat(m.slice(1))).split("");
  }  
  
  handlePatterns(tokenizedCode, parentPatterns, depth){
    var patterns={};
    var level=0, brackets=0, patternBrackets=0;
    var currentPattern=[];
    
    var tokenizedCode = tokenizedCode.reduce((code,token)=>{
      switch(token[0]){
          case "p":
            level++;
            if(brackets) throw "nested pattern definition";
            break;
          case "q":level--;break;
          case "(":brackets++;break;
          case ")":brackets--;break;
      }
      if(level==0){
        if(token=="(")patternBrackets++;
        if(token[0]==")")patternBrackets--;
        if(token=="q"){
          patterns[currentPattern[0].toUpperCase()] = currentPattern.slice(1);
          currentPattern=[];
        }else code.push(token);
      }else currentPattern.push(token);
      return code;
    },[]);
    
    if(patternBrackets!=0) throw "bracketing mismatch : "+tokenizedCode;
    
    var availablePatterns = {...parentPatterns,...patterns};
   
    tokenizedCode = tokenizedCode.reduce((x,t)=>{
      if(t[0]=="P"){
        if(!availablePatterns[t])throw "undefined pattern : "+t+availablePatterns[t];
        else return x.concat(this.handlePatterns(availablePatterns[t],availablePatterns,depth+1));
      }else{ x.push(t);return x};
    },[]);
    
    return tokenizedCode
  }
  
  executeRaw(tokenizedCode){
    let direction = 1; // 0=north, 1=east ...
    let x=0, y=0, minx=0, miny=0, maxx=0, maxy=0;

    const coords = tokenizedCode.reduce((coords,order) => {
      switch(order){
        case "L": direction = (direction+3)%4;break;
        case "R": direction = (direction+1)%4;break;
        case "F": 
          if( direction==0 ) miny = Math.min(miny,--y);
          else if( direction==1 ) maxx = Math.max(maxx,++x);
          else if( direction==2 ) maxy = Math.max(maxy,++y);
          else if( direction==3 ) minx = Math.min(minx,--x);
          coords.push([x,y]);
      }
      return coords;
    },[[0,0]]);
    
    var grid = Array(maxy-miny+1).fill(null).map(x => Array(maxx-minx+1).fill(" "));
    coords.forEach( coord=>grid[coord[1]-miny][coord[0]-minx]="*" );
    return grid.map(line=>line.join("")).join("\r\n");
    
  }
}
_________________________________________________
class RSUProgram {
  constructor(source) {
    this._source = source;
  }
  getTokens() {
    let source = this._source, result = [];
    for (let i = 0; i < source.length; i++) {
      var token;
      switch (source[i]) {
        case 'F':
        case 'L':
        case 'R':
        case ')':
          token = source[i++];
          while (/\d/.test(source[i])) token += source[i++];
          i--;
          if (token.length > 2 && token[1] == '0') throw new SyntaxError('Invalid token detected');
          result.push(token);
          break;
        case '(':
        case 'q':
          result.push(source[i]);
          break;
        case 'p':
        case 'P':
          token = source[i++];
          while (/\d/.test(source[i])) token += source[i++];
          i--;
          if (token.length < 2 || (token.length > 2 && token[1] == '0')) throw new SyntaxError('Invalid token detected');
          result.push(token);
          break;
        case '/':
          if (source[i + 1] === '/') {
            while (source[i] != '\n' && i < source.length) i++;
          } else if (source[i + 1] === '*') {
            i++;
            while ((source[i + 1] != '*' || source[i + 2] != '/') && i < source.length - 2) i++;
            if (source[i + 1] != '*' || source[i + 2] != '/') throw new SyntaxError('Invalid token detected');
            i += 2;
          } else throw new SyntaxError('Invalid token detected');
          break;
        default:
          if (/[^\s\r\t\n]/.test(source[i])) throw new SyntaxError('Invalid token encountered');
      }
    }
    return result;
  }
  convertToRaw(tokens) {
    var _convert = function (tokens, patterns) {
      patterns = JSON.parse(JSON.stringify(patterns));
      var stack = [], decls = new Set();
      for (var i = 0; i < tokens.length; i++) {
        switch (tokens[i][0]) {
          case '(':
            stack.push(tokens[i]);
            break;
          case ')':
            if (stack.length && stack[stack.length - 1][0] === '(') stack.pop();
            else stack.push(tokens[i]);
            break;
          case 'p':
            if (stack.length && stack[stack.length - 1][0] === '(') throw new SyntaxError('Pattern definitions may not be nested within bracketed sequences!');
            if (!stack.length) {
              if (decls.has(tokens[i].toUpperCase())) throw new Error('A pattern may not be defined more than once in the same scope!');
              decls.add(tokens[i].toUpperCase());
            }
            stack.push(tokens[i]);
            break;
          case 'q':
            if (stack.length && stack[stack.length - 1][0] === 'p') stack.pop();
            else stack.push(tokens[i]);
            break;
        }
      }
      if (stack.length) throw new SyntaxError('Unmatched brackets and/or pattern definitions found');
      var result;
      for (var _ = 0; _ < 2; _++) {
        result = [];
        for (var i = 0; i < tokens.length; i++) {
          if (tokens[i][0] === 'p') {
            var pid = tokens[i].toUpperCase(), patternDefinition = [], unmatched = 1;
            while (unmatched) {
              i++;
              if (tokens[i][0] === 'p') unmatched++;
              else if (tokens[i][0] === 'q') unmatched--;
              if (tokens[i][0] != 'q' || unmatched) patternDefinition.push(tokens[i]);
            }
            try {
              patterns[pid] = _convert(patternDefinition, patterns);
            } catch (e) {}
          } else result.push(tokens[i]);
        }
      }
      for (var _ = 0; _ < 10; _++) {
        var temp = [];
        for (var i = 0; i < result.length; i++) {
          switch (result[i][0]) {
            case 'F':
            case 'L':
            case 'R':
              var repeats = result[i].slice(1).length ? +result[i].slice(1) : 1;
              for (var j = 0; j < repeats; j++) temp.push(result[i][0]);
              break;
            case '(':
              var subprogram = [], brackets = 1;
              while (brackets) {
                i++;
                if (result[i][0] === '(') brackets++;
                else if (result[i][0] === ')') brackets--;
                subprogram.push(result[i]);
              }
              subprogram.pop();
              var repeats = result[i].slice(1).length ? +result[i].slice(1) : 1;
              for (var j = 0; j < repeats; j++) temp.splice(temp.length, 0, ...subprogram);
              break;
            case 'P':
              if (typeof patterns[result[i]] != 'undefined') temp.splice(temp.length, 0, ...patterns[result[i]]);
              else temp.push(result[i]);
              break;
          }
        }
        if (temp.every(s => s === 'F' || s === 'L' || s === 'R')) return temp;
        result = temp;
      }
      return result;
    }, result = _convert(tokens, {});
    if (result.some(s => s !== 'F' && s !== 'L' && s !== 'R')) throw new Error('Something went wrong');
    return result;
  }
  executeRaw(cmds) {
    var code = cmds.join``;
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
  execute() {
    return this.executeRaw(this.convertToRaw(this.getTokens()));
  }
}
