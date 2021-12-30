function assemblerInterpreter(program) {
  var ip = 0, stack = [], reg = {}, labels = {}, c, output = '';

  var code = program.split('\n').reduce((p, v) => {
    let m = v.replace(/(?<='[^']*'.*)*;.*/g, '').replace(/^(\w+):/, (m, g) => (labels[g] = p.length, '')).trim().match(/(\w+)( +.*)?/);
    if(m && m[1]){
      let args = [];
      m[2] && m[2].replace(/('[^']*'|[^,']+)(,|$)/g, (m, g) => (args.push(g.trim().replace(/^'|'$/g, '')), ''));
      p.push([m[1], args]);
    }
    return p;
  }, []);

  const instructions = {
    mov:  (x, y)    => {reg[x]  = isNaN(+y) ? reg[y] : +y, ip++},
    inc:  (x)       => {reg[x]++, ip++},
    dec:  (x)       => {reg[x]--, ip++},
    add:  (x, y)    => {reg[x] += isNaN(+y) ? reg[y] : +y, ip++},
    sub:  (x, y)    => {reg[x] -= isNaN(+y) ? reg[y] : +y, ip++},
    mul:  (x, y)    => {reg[x] *= isNaN(+y) ? reg[y] : +y, ip++},
    div:  (x, y)    => {reg[x] /= isNaN(+y) ? reg[y] : +y, reg[x] |= 0, ip++},
    jmp:  (lbl)     => {ip = labels[lbl]},
    cmp:  (x, y)    => {c = (isNaN(+x) ? reg[x] : +x) - (isNaN(+y) ? reg[y] : +y), ip++},
    jne:  (lbl)     => {c != 0 ? ip = labels[lbl] : ip++},
    je:   (lbl)     => {c == 0 ? ip = labels[lbl] : ip++},
    jge:  (lbl)     => {c >= 0 ? ip = labels[lbl] : ip++}, 
    jg:   (lbl)     => {c >  0 ? ip = labels[lbl] : ip++}, 
    jle:  (lbl)     => {c <= 0 ? ip = labels[lbl] : ip++}, 
    jl:   (lbl)     => {c <  0 ? ip = labels[lbl] : ip++}, 
    call: (lbl)     => {stack.push(ip + 1), ip = labels[lbl]},
    ret:  ()        => {ip = stack.pop()},
    msg:  (...args) => {output += args.reduce((s, v) => s + (reg[v] !== undefined ? reg[v] : v), ''), ip++},
  };
  
  while(ip < code.length){
    let [name, args] = code[ip];
    if(name === 'end') return output;
    instructions[name](...args);
  }

  return -1;
}

____________________________________________________
function assemblerInterpreter(program) {
  return interprete(compile(parse(program)))
}

function parse(program) {
  let instructions = []
  for (const raw of program.split(/\n/)) {
    let line = raw.replace(/;.*/, "").trim()
    let match =
      RegExp(`^(msg)${"(?: +([a-z]|'[^']*'),?)?".repeat(10)}`).exec(line) ||
      /^(ret|end)/.exec(line) ||
      /^(inc|dec) +([a-z])/.exec(line) ||
      /^(mov|add|sub|mul|div) +([a-z]), +([a-z]|-?[\d]+)/.exec(line) ||
      /^(cmp) +([a-z]|-?\d+), +([a-z]|-?\d+)/.exec(line) ||
      /^(call|jmp|jn?e|j[gl]e?) +(\w+)/.exec(line) ||
      /^(\w+)(:)/.exec(line)
    if (match) {
      let instruction = match.slice(1)
      if (instruction[1] === ":") {
        instruction = ["label", instruction[0]]
      }
      instructions.push(instruction.filter(Boolean))
    }
  }
  return instructions
}

function compile(instructions) {
  let code = []
  let jumps = []
  let labels = new Map()
  let constants = new Map()
  let constant = k =>
    constants.has(k)
      ? constants.get(k)
      : constants.set(k, constants.size) && constants.size - 1
  for (let i = 0; i < instructions.length; ++i) {
    let instruction = instructions[i]
    if (instruction[0] == "label") {
      labels.set(instruction[1], code.length)
    } else if (instruction[0] === "call" || instruction[0][0] == "j") {
      jumps.push([code.length, instruction[1]])
      code.push([instruction[0], -1])
    } else {
      let op = instruction[0]
      let args = instruction.slice(1).map(operand => {
        if (/^'/.test(operand)) return 100 + constant(eval(operand))
        if (/\d/.test(operand)) return 100 + constant(parseInt(operand, 10))
        return operand.charCodeAt(0) - 97
      })
      if (op === "msg") {
        for (let arg of args) {
          code.push([op, arg])
        }
      } else {
        code.push([op, ...args])
      }
    }
  }
  for (let [from, to] of jumps) {
    code[from][1] = labels.get(to)
  }
  return [Array.from(constants.keys()), code]
}

function interprete([pool, code]) {
  const RK = a => (a >= 100 ? pool[a - 100] : registers[a])
  const registers = new Int32Array(26)
  const stack = []
  let output = ""
  let PC = 0
  let ZF = 0
  for (;;) {
    if (PC >= code.length) return -1
    let [op, a, b] = code[PC++]
    if (op === "end") break
    else if (op === "mov") registers[a] = RK(b)
    else if (op === "inc") registers[a]++
    else if (op === "dec") registers[a]--
    else if (op === "add") registers[a] += RK(b)
    else if (op === "sub") registers[a] -= RK(b)
    else if (op === "mul") registers[a] *= RK(b)
    else if (op === "div") registers[a] /= RK(b)
    else if (op === "cmp") ZF = RK(a) - RK(b)
    else if (op === "jmp") PC = a
    else if (op === "jne") ZF !== 0 && (PC = a)
    else if (op === "je") ZF === 0 && (PC = a)
    else if (op === "jle") ZF <= 0 && (PC = a)
    else if (op === "jl") ZF < 0 && (PC = a)
    else if (op === "jge") ZF >= 0 && (PC = a)
    else if (op === "jg") ZF > 0 && (PC = a)
    else if (op === "call") stack.push(PC) && (PC = a)
    else if (op === "ret") PC = stack.pop()
    else if (op === "msg") output += RK(a)
  }
  return output
}

____________________________________________________
    let registers = {};
    let labels = {};
    let callStack = [];
    let operationStack = [];
    let programOutput;

    const labelRegex = /^([a-zA-Z0-9_]+):/;

function assemblerInterpreter(program) {

        // First step is to split the "program" into an array using \n as delimiter
        let programLines = program.split('\n');

        // Do a "pre-parse" step to identify labels and remove comments
        let preParsedProgram = preprocess(programLines);

        let instructionIndex = 0;
        let programFinishedWithEnd = false;
        while (instructionIndex < preParsedProgram.length && !programFinishedWithEnd) {
            let currentLine = preParsedProgram[instructionIndex];

            // Skip blank lines and labels
            if (currentLine.length === 0 || labelRegex.test(currentLine)) {
                instructionIndex++;
                continue;
            }

            console.log(`Executing: ${currentLine}`);
            let matches = /(\w+)(\s+(.*))?$/.exec(currentLine);
            let currentInstruction = matches[1];
            let argumentTokens = (matches.length > 2 && matches[2]) ?
                matches[3].split(/,(?=(?:[^\']*\'[^\']*\')*[^\']*$)/).map(token => token.trim()) :
                null;
            let operand1, destinationLabel;
            switch (currentInstruction) {

                case 'mov':
                    operand1 = getOperand(argumentTokens[1]);
                    console.log(`Moving value = ${operand1} to register ${argumentTokens[0]}`);
                    registers[argumentTokens[0]] = operand1;
                    instructionIndex++;
                    break;

                case 'inc':
                case 'dec':
                    doIncrementDecrement(currentInstruction, argumentTokens);
                    instructionIndex++;
                    break;

                case 'add':
                case 'sub':
                case 'mul':
                case 'div':
                    doRegisterArithmetic(currentInstruction, argumentTokens);
                    instructionIndex++;
                    break;

                case 'jnz':
                    operand1 = getOperand(argumentTokens[0]);
                    instructionIndex = (operand1 !== 0) ?
                        instructionIndex + parseInt(argumentTokens[1]) :
                        instructionIndex + 1;
                    break;

                case 'jmp':
                    destinationLabel = argumentTokens[0];
                    if (labels[destinationLabel]) {
                        instructionIndex = labels[destinationLabel];
                    }
                    else {
                        throw `Invalid destination for jmp: ${destinationLabel}`;
                    }
                    break;

                case 'cmp':
                    operationStack.push(getOperand(argumentTokens[0]));
                    operationStack.push(getOperand(argumentTokens[1]));
                    instructionIndex++;
                    break;

                case 'jne':
                case 'je':
                case 'jge':
                case 'jg':
                case 'jle':
                case 'jl':
                    instructionIndex = doConditionalJump(currentInstruction, argumentTokens, instructionIndex);
                    break;

                case 'call':
                    destinationLabel = argumentTokens[0];
                    if (labels[destinationLabel]) {
                        callStack.push(instructionIndex);
                        console.log(`calling ${destinationLabel} at index = ${labels[destinationLabel]} with return at index = ${instructionIndex}`);
                        instructionIndex = labels[destinationLabel];
                    }
                    else {
                        throw `Invalid destination for call: ${destinationLabel}`;
                    }
                    break;

                case 'ret':
                    let returnIndex = callStack.pop() + 1;
                    console.log(`returning from subroutine to index = ${returnIndex}`);
                    instructionIndex = returnIndex;
                    break;

                case 'msg':
                    programOutput = formatMessage(argumentTokens);
                    instructionIndex++;
                    break;

                case 'end':
                    return programOutput;
            }
        }
        return -1;  
}


    function getOperand(operandToken) {
        return (isNaN(operandToken)) ?
            getRegister(operandToken) :
            parseInt(operandToken);
    }

    function getRegister(registerId) {
        if (!registers.hasOwnProperty(registerId)) {
            console.log(`Initializing register ${registerId} to 0`);
            registers[registerId] = 0;
        }
        return registers[registerId];
    }

    function preprocess(rawProgram) {
        let resultantProgram = [];
        for (let instructionIndex = 0; instructionIndex < rawProgram.length; instructionIndex++) {
            let currentInstruction = rawProgram[instructionIndex];

            // Remove any comments
            let commentTokens = currentInstruction.split(';');
            if (commentTokens.length > 1)
                currentInstruction = commentTokens[0];

            // test for a label, if we find one insert the name and the
            // instruction index in the labels hash
            let labelMatch = labelRegex.exec(currentInstruction);
            if (labelMatch !== null) {
                let labelName = labelMatch[1];
                labels[labelName] = instructionIndex;
            }

            // Trim leading space from instruction
            resultantProgram.push(currentInstruction.trim());
        }
        return resultantProgram;
    }

    function doRegisterArithmetic(instruction, arguments) {
        let operand2 = getOperand(arguments[1]);
        let operand1 = getRegister(arguments[0]);
        let newValue;
        switch (instruction) {
            case 'add':
                newValue = operand2 + operand1;
                break;
            case 'sub':
                newValue = operand1 - operand2;
                break;
            case 'mul':
                newValue = operand2 * operand1;
                break;
            case 'div':
                newValue = Math.floor(operand1 / operand2);
                break;
        }
        console.log(`${instruction} register ${arguments[0]} = ${operand1} with ${operand2} for ${newValue}`);
        registers[arguments[0]] = newValue;
    }

    function doIncrementDecrement(instruction, arguments) {
        let operand1 = getRegister(arguments[0]);
        let newValue = (instruction === 'inc') ?
            operand1 + 1 :
            operand1 - 1;
        console.log(`${instruction} register ${arguments[0]} to ${newValue}`);
        registers[arguments[0]] = newValue;
    }

    function doConditionalJump(instruction, arguments, currentIndex) {
        let destinationLabel = arguments[0];
        if (!labels[destinationLabel]) {
            throw `Invalid destination for ${instruction}: ${destinationLabel}`;
        }
        let operand2 = operationStack.pop();
        let operand1 = operationStack.pop();
        let comparisonResult;
        switch (instruction) {
            case 'jne':
                comparisonResult = (operand1 !== operand2);
                break;

            case 'je':
                comparisonResult = (operand1 === operand2);
                break;

            case 'jge':
                comparisonResult = (operand1 >= operand2);
                break;

            case 'jg':
                comparisonResult = (operand1 > operand2);
                break;

            case 'jle':
                comparisonResult = (operand1 <= operand2);
                break;

            case 'jl':
                comparisonResult = (operand1 < operand2);
                break;
        }
        return (comparisonResult) ? labels[destinationLabel] : currentIndex + 1;
    }

    function formatMessage(arguments) {
        let output = "";
        for (let argument of arguments) {
            if (argument.substr(0, 1) === '\'') {
                output += argument.substr(1, argument.length - 2);
            }
            else {
                let value = getRegister(argument);
                output += value.toString();
            }
        }
        return output;
    }
