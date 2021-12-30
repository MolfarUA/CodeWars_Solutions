extension String {
    var strip: String {
        return trimmingCharacters(in: .whitespacesAndNewlines)
    }
}

enum ArgType {
    case register, integer, string
}

struct Arg {
    let type: ArgType
    let value: String
}

struct Cmd {
    let op: String
    let args: [Arg]
}


func makeCmd(line: String) -> Cmd? {
    guard let op = line.split(separator: " ").first else {
        return nil
    }

    let lineChars = Array(line)

    var args: [Arg] = []

    var i = op.utf16.count
    while i < lineChars.count {
        guard !lineChars[i].isWhitespace && lineChars[i] != "," else {
            i += 1
            continue
        }

        guard lineChars[i] != "'" else {
            i += 1

            let j = i

            while i < lineChars.count && lineChars[i] != "'" {
                i += 1
            }

            guard i < lineChars.count else {
                args = []
                break
            }

            let arg = String(lineChars[j..<i])
            args.append(Arg(type: .string, value: arg))

            i += 1
            continue
        }

        let j = i

        while i < lineChars.count && !lineChars[i].isWhitespace && lineChars[i] != "," {
            i += 1
        }

        guard i > j else {
            continue
        }

        let arg = String(lineChars[j..<i])
        let type: ArgType = lineChars[j].isNumber ? .integer : .register

        args.append(Arg(type: type, value: arg))
    }

    return Cmd(op: String(op), args: args)
}

enum InterpreterError: Error {
    case unrecognizedCommand
    case badArgumentList
    case undefinedRegister
    case unrecognizedLabel
    case notInSubroutine
    case finishedWithoutEndStatement
}

func regOrConstValue(for arg: String, registers: [String: Int]) throws -> Int {
    guard let result = Int(arg) else {
        return try regValue(for: arg, registers: registers)
    }
    return result
}

func regValue(for arg: String, registers: [String: Int]) throws -> Int {
    guard let result = registers[arg] else {
        throw InterpreterError.undefinedRegister
    }
    return result
}

func assemblerInterpreter(_ program: String) throws -> String {
    var lines = program
        .components(separatedBy: ["\n"])
        .compactMap { $0.components(separatedBy: ";").first }
        .map { $0.strip }
        .filter { !$0.isEmpty }

    var labels: [String: Int] = [:]

    var i = 0, j = 0
    while (i < lines.count) {
        let line = lines[i]
        i += 1

        guard !line.hasSuffix(":") else {
            labels[String(line.dropLast())] = j
            continue
        }

        lines[j] = lines[i - 1]
        j += 1
    }

    lines.removeLast(i - j)

    var registers: [String: Int] = [:]

    var cmp = 0

    var callStack: [Int] = []

    var output: String = ""

    let binArithOps: [String: (Int, Int) -> Int] = [
        "add": { $0 + $1 }, "sub": { $0 - $1 },
        "mul": { $0 * $1 }, "div": { $0 / $1 }
    ]
    let uniArithOps: [String: (Int) -> Int] = [
        "inc": { $0 + 1 }, "dec": { $0 - 1 }
    ]
    let jumpChecks: [String: (Int) -> Bool] = [
        "jmp": { _ in true },
        "jne": { $0 != 0 }, "je": { $0 == 0 },
        "jge": { $0 >= 0 }, "jg": { $0 > 0 },
        "jle": { $0 <= 0 }, "jl": { $0 < 0 }
    ]

    var ip = 0
    while ip < lines.count {
        let line = lines[ip]
        ip += 1

        guard let cmd = makeCmd(line: line) else {
            throw InterpreterError.unrecognizedCommand
        }

        switch cmd.op {
        case "mov":
            guard cmd.args.count == 2 else {
                throw InterpreterError.badArgumentList
            }
            registers[cmd.args[0].value] = try regOrConstValue(for: cmd.args[1].value, registers: registers)

        case "inc", "dec":
            guard cmd.args.count == 1 else {
                throw InterpreterError.badArgumentList
            }
            registers[cmd.args[0].value] = try uniArithOps[cmd.op]!(regValue(for: cmd.args[0].value, registers: registers))

        case "add", "sub", "mul", "div":
            guard cmd.args.count == 2 else {
                throw InterpreterError.badArgumentList
            }
            registers[cmd.args[0].value] = try binArithOps[cmd.op]!(
                regValue(for: cmd.args[0].value, registers: registers),
                regOrConstValue(for: cmd.args[1].value, registers: registers))

        case "jmp", "jne", "je", "jge", "jg", "jle", "jl":
            guard cmd.args.count == 1 else {
                throw InterpreterError.badArgumentList
            }
            guard jumpChecks[cmd.op]!(cmp) else {
                continue
            }
            guard let labelIndex = labels[cmd.args[0].value] else {
                throw InterpreterError.unrecognizedLabel
            }
            ip = labelIndex

        case "cmp":
            guard cmd.args.count == 2 else {
                throw InterpreterError.badArgumentList
            }
            cmp = try regOrConstValue(for: cmd.args[0].value, registers: registers)
                - regOrConstValue(for: cmd.args[1].value, registers: registers)

        case "call":
            guard cmd.args.count == 1 else {
                throw InterpreterError.badArgumentList
            }
            guard let labelIndex = labels[cmd.args[0].value] else {
                throw InterpreterError.unrecognizedLabel
            }

            callStack.append(ip)
            ip = labelIndex

        case "ret":
            guard cmd.args.count == 0 else {
                throw InterpreterError.badArgumentList
            }
            guard let retIndex = callStack.popLast() else {
                throw InterpreterError.notInSubroutine
            }
            ip = retIndex

        case "msg":
            output = try cmd.args.map {
                $0.type == .string ? $0.value : try String(regValue(for: $0.value, registers: registers))
            }.joined()

        case "end":
            return output

        default:
            throw InterpreterError.unrecognizedCommand
        }
    }

    throw InterpreterError.finishedWithoutEndStatement
}

____________________________________________________
import Foundation

enum VMError : Error{
    case Failed
}
enum Command : String, CaseIterable{
    case empty, label, mov, inc, msg, dec, add, sub, mul, div, call, ret, end, cmp, jmp, jne, je, jge, jg, jle, jl

    static func create(_ cmdString : String) -> Command{
        if let c = cmdString.last{
            if (c == ":"){
                return .label
            }
        }
        return allCases.filter({$0.rawValue == cmdString}).first ?? .empty
    }
}

enum Register : String, CaseIterable{
    case empty, a, b, c, d, e, f, g, h, k, t, s, m, n

    static func create(_ regString: String) -> Register{
        return allCases.filter({$0.rawValue == regString}).first ?? .empty
    }
}

struct Argument{
    var register : Register?
    var stringData : String?
    var numData : Int?

    init(argument : String){
        if (Register.create(argument) != .empty){
            register = Register.create(argument);
        } else {
            numData = Int(argument)
            
            if numData == nil {
                    stringData = argument
            }
        }
    }
}

struct CodeElement{
    var cmd : Command
    var args = [Argument]()

    init(cmd : Command){
        self.cmd = cmd
    }

    init(cmd : Command, arg : Argument){
        self.cmd = cmd
        args.append(arg)
    }

    init(cmd : Command, argOne : Argument, argTwo : Argument){
        self.cmd = cmd
        args.append(argOne)
        args.append(argTwo)
    }

}
enum ConditionalFlag {
    case equal, greater, less
    
    static func check(_ arg_one : Int, _ arg_two : Int) -> ConditionalFlag{
        if arg_one == arg_two{
            return .equal
        }

        if arg_one < arg_two{
            return .less
        }else {
            return .greater
        }
        
    }

    
}
class VirtMashin {
    var dirMashin : [Command : ([Argument])->Bool?] = [:]

    var registers : [Register : Int] = [ (.a) : 0,
                                         (.b) : 0,
                                         (.c) : 0,
                                         (.d) : 0,
                                         (.e) : 0]
    var code : [CodeElement] = []
    var currentExecutionPoint = 0;
    var endFlag = false;
    var callStack : [Int] = []
    var conditionalFlag : ConditionalFlag = ConditionalFlag.equal
    var returnString = ""
    
    
    func run(code : [CodeElement]) -> String?{
        self.code = code
        
        while endFlag != true{
            if let f = dirMashin[code[currentExecutionPoint].cmd] {
                if let executionResult = f(code[currentExecutionPoint].args) {
                    if executionResult == false {
                        return nil
                    }
                } else {
                    return nil
                }
            }
            
            currentExecutionPoint += 1
            if currentExecutionPoint >= code.count {
                return nil
            }
        }
        return returnString
    }
    init(){
        dirMashin[.jmp] = { arguments in
            return self.jmpToLabel(arguments, false)
        }
        
        dirMashin[.jne] = { arguments in
            return (self.conditionalFlag == .less || self.conditionalFlag == .greater) ? self.jmpToLabel(arguments, false) : true
        }
        dirMashin[.je] = {arguments in
            return (self.conditionalFlag == .equal) ? self.jmpToLabel(arguments, false) : true
        }
        dirMashin[.jge] = {arguments in
            return (self.conditionalFlag == .equal || self.conditionalFlag == .greater) ? self.jmpToLabel(arguments, false) : true
        }
        dirMashin[.jg] = {arguments in
            return (self.conditionalFlag == .greater) ? self.jmpToLabel(arguments, false) : true
        }
        dirMashin[.jle] = {arguments in
            return (self.conditionalFlag == .equal || self.conditionalFlag == .less) ? self.jmpToLabel(arguments, false) : true
        }
        dirMashin[.jl] = {arguments in
            return (self.conditionalFlag == .less) ? self.jmpToLabel(arguments, false) : true
        }
        
        
        
        
        dirMashin[.cmp] = { arguments in
            guard arguments.count == 2 else { return nil }
            guard arguments[0].stringData == nil, arguments[1].stringData == nil else {return nil}
            
            let argOne = arguments[0].numData ?? self.registers[arguments[0].register!]!
            let argTwo = arguments[1].numData ?? self.registers[arguments[1].register!]!
            
            self.conditionalFlag = ConditionalFlag.check(argOne, argTwo)
            return true
        }
        
        
        dirMashin[Command.mov] = { arguments in
            guard arguments.count == 2 else { return nil }

            if let leftReg = arguments[0].register, let rightData = arguments[1].numData {
                self.registers[leftReg] = rightData
            }
            if let leftReg = arguments[0].register, let rightReg = arguments[1].register {
                self.registers[leftReg] = self.registers[rightReg]
            }
            return true
        }

        dirMashin[Command.inc] = { arguments in
            guard arguments.count == 1 else {return nil}

            if let reg = arguments[0].register {
                self.registers[reg]! += 1
            } else {
                return nil
            }
            return true
        }
        
        dirMashin[Command.dec] = { arguments in
            guard arguments.count == 1 else {return nil}

            if let reg = arguments[0].register {
                self.registers[reg]! -= 1
            } else {
                return nil
            }
            return true
        }
        
        dirMashin[Command.add] = { arguments in
            guard arguments.count == 2 else { return nil }

            if let leftReg = arguments[0].register, let rightData = arguments[1].numData {
                self.registers[leftReg]! += rightData
            }
            if let leftReg = arguments[0].register, let rightReg = arguments[1].register {
                self.registers[leftReg]! += self.registers[rightReg]!
            }
            return true
        }
        dirMashin[Command.sub] = { arguments in
            guard arguments.count == 2 else { return nil }

            if let leftReg = arguments[0].register, let rightData = arguments[1].numData {
                self.registers[leftReg]! -= rightData
            }
            if let leftReg = arguments[0].register, let rightReg = arguments[1].register {
                self.registers[leftReg]! -= self.registers[rightReg]!
            }
            return true
        }
        dirMashin[Command.mul] = { arguments in
            guard arguments.count == 2 else { return nil }

            if let leftReg = arguments[0].register, let rightData = arguments[1].numData {
                self.registers[leftReg]! *= rightData
            }
            if let leftReg = arguments[0].register, let rightReg = arguments[1].register {
                self.registers[leftReg]! *= self.registers[rightReg]!
            }
            return true
        }
        dirMashin[Command.div] = { arguments in
            guard arguments.count == 2 else { return nil }

            if let leftReg = arguments[0].register, let rightData = arguments[1].numData {
                self.registers[leftReg]! /= rightData
            }
            if let leftReg = arguments[0].register, let rightReg = arguments[1].register {
                self.registers[leftReg]! /= self.registers[rightReg]!
            }
            return true
        }
        dirMashin[.ret] = { arguments in
            if self.callStack.count > 0{
                self.currentExecutionPoint = self.callStack.removeLast()
                
            } else {
                return nil
            }
            return true
        }
        
        dirMashin[.call] = { arguments in
            return self.jmpToLabel(arguments, true)
       }
        
    
        
        dirMashin[.end] = { arguments in
            self.endFlag = true
            return true
        }
        
        dirMashin[.msg] = { arguments in
            guard arguments.count == 1, let rawString = arguments[0].stringData else {return nil}
            
            
            var commaOpen = false
            var argString = ""
            var pos = 0
            while (pos < rawString.count){
                let idx = rawString.index(rawString.startIndex, offsetBy: pos)
                let c = rawString[idx]
                
                if c == "'" && commaOpen == false{
                    // starting string argument
                    argString = ""
                    commaOpen = true
                }else if c == "'" && commaOpen == true{
                    // new argument
                    self.returnString += argString
                    argString = ""
                    commaOpen = false
                } else if c == "," && commaOpen == false {
                    let ts = argString.trimmingCharacters(in: .whitespacesAndNewlines)
                    if (ts.count > 0){
                        let reg = Register.create(ts)
                        guard reg != .empty else {return nil}
                        self.returnString += String(self.registers[reg]!)
                        argString = ""
                    }
                } else {
                    argString += String(c)
                }
                pos += 1
            }
            
            let ts = argString.trimmingCharacters(in: .whitespacesAndNewlines)
            if (ts.count > 0){
                let reg = Register.create(ts)
                guard reg != .empty else {return nil}
                self.returnString += String(self.registers[reg]!)
                argString = ""
            }
        

            return true
        }
    }
    
    private func jmpToLabel(_  arguments: [Argument], _ saveCallStack : Bool) -> Bool?{
        guard arguments.count == 1, let argLbl = arguments[0].stringData else { return nil}
        
        for (index, ce) in self.code.enumerated() {
            if (ce.cmd == .label){
                if (argLbl == ce.args[0].stringData){
                    if saveCallStack{
                        self.callStack.append(self.currentExecutionPoint)
                    }
                    self.currentExecutionPoint = index
                    return true
                }
            }
        }
        return nil
    }
}

func assemblerInterpreter(_ program:String) throws -> String {
    var compiledCode = [CodeElement]()

    let strings = program.split(separator: "\n")
    for string in strings {
        
        var trimmedString = string.trimmingCharacters(in: .whitespacesAndNewlines)
        
        if let commentIndex = trimmedString.firstIndex(of: ";"){
            trimmedString.removeSubrange(commentIndex...)
            trimmedString = trimmedString.trimmingCharacters(in: .whitespacesAndNewlines)
        }
        
        if (trimmedString.last == ":"){
            let cmd = Command.create(trimmedString)
            if cmd == .label{
                compiledCode.append(CodeElement(cmd: cmd, arg: Argument(argument: String(trimmedString.dropLast()))))
            }
        } else {
            if let index = trimmedString.firstIndex(of: " "){
                let strCmd = String(trimmedString[..<index])
                let strArgs = String(trimmedString[index...]).trimmingCharacters(in: .whitespaces)

                let cmd = Command.create(strCmd)
                var compiledLineOfCode : CodeElement

                // hardcoded msg
                if (cmd == .msg){
                    compiledLineOfCode = CodeElement(cmd: cmd, arg: Argument(argument: strArgs))
                } else {
                    if let argSplitIndex = strArgs.firstIndex(of: ",") {
                            let argumentOne = Argument(argument:    String(strArgs[..<argSplitIndex]).trimmingCharacters(in: .whitespaces))
                            let argumentTwo = Argument(argument:    String(strArgs[argSplitIndex...]).dropFirst().trimmingCharacters(in: .whitespaces))
                            compiledLineOfCode = CodeElement(cmd: cmd, argOne: argumentOne, argTwo: argumentTwo)
                    } else {
                            let argumentOne = Argument(argument: strArgs.trimmingCharacters(in: .whitespaces))
                            compiledLineOfCode = CodeElement(cmd: cmd, arg: argumentOne)
                    }
                }

                compiledCode.append(compiledLineOfCode)
            } else {
                compiledCode.append(CodeElement(cmd: Command.create(trimmedString)))
            }
        }
        
    }

    
    if let rval = VirtMashin().run(code: compiledCode) {
        return rval
    } else {
        throw VMError.Failed
    }
    
}

____________________________________________________
struct InstructionArgument: Equatable {
  let intValue: Int?
  let stringValue: String?
  
  init(from string: String) {
    if let asInt = Int(string) {
      self.init(intValue: asInt)
      return
    }
    self.init(stringValue: string)
  }
  
  init(
    intValue: Int? = nil, 
    stringValue: String? = nil
  ) {
    self.intValue = intValue
    self.stringValue = stringValue
  }
}

final class Register {
  let name: String
  var value: Int?
  
  init(
    name: String,
    value: Int?
  ) { 
    self.name = name
    self.value = value
  }
}
enum Instruction: Equatable {
  // MARK: - Arithimetic
  case inc(String)
  case dec(String)
  case add(String, InstructionArgument)
  case sub(String, InstructionArgument)
  case mul(String, InstructionArgument)
  case div(String, InstructionArgument)
  case cmp(InstructionArgument, InstructionArgument)
  // MARK: - Jump
  case jmp(String)
  case jne(String)
//   case jge(String)
  case jg(String)
  case jle(String)
  case jl(String)
  case je(String)
  case jge(String)
  // MARK: - Flow
  case call(String)
  case mov(String, InstructionArgument)
  case label(String)
  case ret
  case end
  // MARK: - IO
  case msg(MessageParser)
}

protocol JumpDelegate: AnyObject {
  func jump(to label: String)
}

// MARK: - Parsing
struct InstructionParser {
  enum ParserError: Error {
     case formatError
     case instructionWithNoName
     case instructionWithNoArgs
   }
  
  func parse(_ str: String) throws -> Instruction {
    guard let splitted = str
      .components(separatedBy: ";").first?
      .components(separatedBy: " ")
      .filter({ $0 != "" })
    else { throw ParserError.formatError }
    
    guard let instructionName = splitted.first
    else { throw ParserError.instructionWithNoName }
    
    let rawArgs = splitted
      .dropFirst()
      .joined(separator: " ")
    let splittedArgs = rawArgs
      .components(separatedBy: ", ")
    
    guard let firstArg = splittedArgs.first
    else { throw ParserError.formatError }
    switch instructionName {
      case "mov": return .mov(firstArg, InstructionArgument(from: splitted.last!))
      case "inc": return .inc(firstArg)
      case "dec": return .dec(firstArg)
      case "mul": return .mul(firstArg, InstructionArgument(from: splitted.last!))
      case "add": return .add(firstArg, InstructionArgument(from: splitted.last!))
      case "sub": return .sub(firstArg, InstructionArgument(from: splitted.last!))
      case "div": return .div(firstArg, InstructionArgument(from: splitted.last!))
      case "call": return .call(firstArg)
      case "end": return .end
      case "ret": return .ret
      case "msg": return .msg(MessageParser(raw: rawArgs))
      case "cmp": return .cmp(InstructionArgument(from: firstArg), InstructionArgument(from: splitted.last!))
      case "jmp": return .jmp(firstArg)
      case "jne": return .jne(firstArg)
      case "jl" : return .jl(firstArg)
      case "jle": return .jle(firstArg)
      case "jg" : return .jg(firstArg)
      case "jge": return .jge(firstArg)
      case "je" : return .je(firstArg)
      default: break // TODO throw error for unknown instruciton
    }
    if instructionName.isLabel() {
      return .label(instructionName)
    }
    fatalError("Instruction not yet supported \(instructionName)")
  }
}
struct MessageParser: Equatable {
  let raw: String
  
  func parse(registers: [Register]) -> String {
    let placeholder = "&*^#@!"
    return raw
      .replacingOccurrences(of: "', '", with: placeholder)
      .components(separatedBy: ", ")
      .map { str in
            
            
        if let register = registers.filter({ $0.name == str}).first,
           let value = register.value {
          return String(value)
        }
        return str.replacingOccurrences(of: "'", with: "")
      }.joined(separator: "").replacingOccurrences(of: placeholder, with: ", ")
  }
}

// MARK - Command execution

final class Program: JumpDelegate {
  // MARK: - Inner types
  enum ProgramError: Error {
    case programEndedWithNoEnd
  }
  // MARK: - Dependencies
  private let instructions: [Instruction]
  private let cpu = CPU()
  
  // MARK: - Properties
  private var programCounter = 0 
  private var programStack: [Int] = []
  private var result: String = ""
  
  // MARK: - Initialization
  init(instructions: [Instruction]) {
    self.instructions = instructions
    self.cpu.delegate = self
  }
  
  // MARK: - Public API
  func run() throws -> String {
    while true {
      defer { programCounter += 1}
      popStackIfNeeded()
      guard let instruction = getCurrentInstruction()
      else { throw ProgramError.programEndedWithNoEnd }
      if case .end = instruction {
        return result
      }
      stackInstructionIfNeeded(instruction)
      if let res = try cpu.execute(instruction: instruction) {
        result =  res
      }
    }
    throw ProgramError.programEndedWithNoEnd
  }
  
  // MARK: - JumpDelegate
   func jump(to label: String) {
      guard let targetInstruction = instructions.filter({ 
              if case $0 = Instruction.label(label + ":") { return true }
              return false
            }).first,
            let index = instructions.firstIndex(of: targetInstruction)
      else { return }
      self.programCounter = index 
   }
  
  // MARK: - Stack managing
  private func popStackIfNeeded() {
    if getCurrentInstruction() == .ret,
       let stacked = programStack.popLast()    
    { self.programCounter = stacked }
  }
  
  private func stackInstructionIfNeeded(_ instruction: Instruction) {
    if case .call(let labelName) = instruction {
      guard let targetInstruction = instructions.filter({ 
              if case $0 = Instruction.label(labelName + ":") { return true }
              return false
            }).first,
            let index = instructions.firstIndex(of: targetInstruction)
      else { return }
      self.programStack.append(programCounter + 1)
      self.programCounter = index 
    }
  }
  
  // MARK: - Helpers
  private func getCurrentInstruction() -> Instruction?
  { return instructions[safe: programCounter] }
  
  private func debug() {
    print("** DEBUG **\n", "Program counter: ", programCounter, "\n Program stack: ", programStack  )
    cpu.debug()
    print("************")
  }
}
final class CPU {
  // MARK: - Inner types
  enum ExecutionError: Error {
    case invalidInstruction
    case invalidArgument
    case conditionalJumpWithNoCompare
  }
  
  // MARK: - Dependencies
  weak var delegate: JumpDelegate?
  
  // MARK: - Properties
  private var registers: [Register] = []
  private var cmpValues: (InstructionArgument, InstructionArgument)?
  
  // MARK: - Public API
  func execute(instruction: Instruction) throws -> String? {
    switch instruction {
      // MARK: - Flow
      case .mov(let registerName, let value):
        mov( to: registerName, value: value)
      case .cmp(let x, let y):
        cmpValues = (x, y)
      // MARK: - Arithimetic
      case .inc(let registerName): 
        inc(registerName: registerName)
      case .dec(let registerName): 
        dec(registerName: registerName)
      case .add(let registerName, let value):
        add(to: registerName, value: value)
      case .sub(let registerName, let value):
        sub(to: registerName, value: value)
      case .mul(let registerName, let value):
        mul(to: registerName, value: value)
      case .div(let registerName, let value):
        div(to: registerName, value: value)
      case .msg(let parser):
        return parser.parse(registers: self.registers)
      case .jmp(let targetLabel):
        try jmp(to: targetLabel)
      case .jne(let targetLabel):
        try jne(to: targetLabel)
      case .jl(let targetLabel):
        try jl(to: targetLabel)
      case .jle(let targetLabel):
        try jle(to: targetLabel)
      case .jge(let targetLabel):
        try jge(to: targetLabel)
      case .jg(let targetLabel):
        try jg(to: targetLabel)
      case .je(let targetLabel):
        try je(to: targetLabel)
      case .call: break
      case .label: break
      case .ret: break
      case .end: break
    }
    return nil
  }
  
  // MARK: - Manipulation + arithimetic instructions
  private func mov(to registerName: String, value: InstructionArgument) {
    let destination = fetchRegisterAndCreateIfNeeded(named: registerName)
    if let sourceRegisterName = value.stringValue,
       let localRegister = registers.first(where: { $0.name == sourceRegisterName }){
         destination.value = localRegister.value
         return
       }
    if let value = value.intValue
    { destination.value = value }
  }
  private func inc(registerName: String) {
    if let register = fetchLocalRegister(registerName),
       let rValue = register.value
    { register.value = rValue + 1 }
  }
  private func dec(registerName: String) {
    if let register = fetchLocalRegister(registerName),
       let rValue = register.value
    { register.value = rValue - 1 }
  }
  private func add(to registerName: String, value: InstructionArgument) {
    let destination = fetchRegisterAndCreateIfNeeded(named: registerName)
    if let sourceRegisterName = value.stringValue,
       let localRegister = registers.first(where: { $0.name == sourceRegisterName }),
       let numerator = destination.value,
       let denominator = localRegister.value{
         destination.value = numerator + denominator
         return
       }
    if let value = value.intValue,
       let numerator = destination.value
    { destination.value = numerator + value }
  }
  private func sub(to registerName: String, value: InstructionArgument) {
    let destination = fetchRegisterAndCreateIfNeeded(named: registerName)
    if let sourceRegisterName = value.stringValue,
       let localRegister = registers.first(where: { $0.name == sourceRegisterName }),
       let numerator = destination.value,
       let denominator = localRegister.value{
         destination.value = numerator - denominator
         return
       }
    if let value = value.intValue,
       let numerator = destination.value
    { destination.value = numerator - value }
  }
  private func mul(to registerName: String, value: InstructionArgument) {
    let destination = fetchRegisterAndCreateIfNeeded(named: registerName)
    if let sourceRegisterName = value.stringValue,
       let localRegister = registers.first(where: { $0.name == sourceRegisterName }),
       let numerator = destination.value,
       let denominator = localRegister.value{
         destination.value = numerator * denominator
         return
       }
    if let value = value.intValue,
       let numerator = destination.value
    { destination.value = numerator * value }
  }
  private func div(to registerName: String, value: InstructionArgument) {
    let destination = fetchRegisterAndCreateIfNeeded(named: registerName)
    if let sourceRegisterName = value.stringValue,
       let localRegister = registers.first(where: { $0.name == sourceRegisterName }),
       let numerator = destination.value,
       let denominator = localRegister.value{
         destination.value = numerator / denominator
         return
       }
    if let value = value.intValue,
       let numerator = destination.value
    { destination.value = numerator / value }
  }
  
  // MARK: - Logical instructions

  private func jmp(to label: String) throws {
    delegate?.jump(to: label)
  }
  
  private func jne(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 == $1 }
  }
  
  private func jl(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 >= $1 }
  }
  
  private func jle(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 > $1 }
  }  
  
  private func jge(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 < $1 }
  }
  
  private func jg(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 <= $1 }
  }
  private func je(to label: String) throws {
    try jumpIfNeeded(to: label) { $0 != $1 }
  }
  private func jumpIfNeeded(to label: String, _ comparator: (Int, Int) -> Bool ) throws {
    guard let (x, y) = cmpValues
    else { throw ExecutionError.conditionalJumpWithNoCompare }
    
    if let xRegName = x.stringValue,
       let yRegName = y.stringValue,
       let xReg = fetchLocalRegister(xRegName),
       let yReg = fetchLocalRegister(yRegName),
       let xValue = xReg.value,
       let yValue = yReg.value,
       comparator(xValue, yValue) { return }
        
    
    if let xReg = x.stringValue,
       let reg = fetchLocalRegister(xReg),
       let xValue = reg.value,
       let yValue = y.intValue,
       comparator(xValue, yValue) { return }
    
    if let yReg = y.stringValue,
       let reg = fetchLocalRegister(yReg),
       let yValue = reg.value,
       let xValue = x.intValue,
       comparator(xValue, yValue) { return }
    
    if let xValue = x.intValue,
       let yValue = y.intValue,
       comparator(xValue, yValue) { return }
    delegate?.jump(to: label)
  }
  
  
  func debug() {
    print("cmpValues", cmpValues!)
    printRegisters()
  }
  func printRegisters() {
    registers.forEach { print("REGISTERS", $0.name, $0.value ?? "NO value") }
  }
  
  private func fetchLocalRegister(_ name: String) -> Register? 
  { return registers.first(where: { $0.name == name }) }
  
  private func fetchRegisterAndCreateIfNeeded(named: String) -> Register {
    if let localRegister = registers.first(where: { $0.name == named })
    { return localRegister }
    let register = Register (
      name: named,
      value: nil
    )
    registers.append(register)
    return register
  }
}

// MARK: - Main
func assemblerInterpreter(_ program: String) throws -> String {
  let instructionParser = InstructionParser()
  let rawInstructions = program.components(separatedBy: "\n").filter { $0 != "" }
  let parsedInstructions = rawInstructions.compactMap { try? instructionParser.parse($0) }
  let program = Program(instructions: parsedInstructions)
  
  return try program.run() 
}

// MARK: - Extensions
protocol InstructionArgumentProtocol {}
extension String: InstructionArgumentProtocol {}
extension Int: InstructionArgumentProtocol {}

extension Collection {
    /// Returns the element at the specified index if it is within bounds, otherwise nil.
    subscript (safe index: Index) -> Element? {
        return indices.contains(index) ? self[index] : nil
    }
}
extension String {
  func isLabel() -> Bool { return last == ":" }
}
