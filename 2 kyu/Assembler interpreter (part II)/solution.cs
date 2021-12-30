using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public class AssemblerInterpreter
{
  private static readonly Regex labelExpression = new Regex(@"^(?<label>\w+):");
  private static readonly Regex instructions = new Regex(string.Join("|"
    , "^" 
    + @"(?<mov>mov +(?<x>[a-z]), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<inc>inc +(?<x>[a-z]))"
    , @"(?<dec>dec +(?<x>[a-z]))"
    , @"(?<add>add +(?<x>[a-z]), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<sub>sub +(?<x>[a-z]), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<mul>mul +(?<x>[a-z]), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<div>div +(?<x>[a-z]), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<jmp>jmp +(?<label>\w+))"
    , @"(?<cmp>cmp +((?<x>-?\d+)|(?<regX>[a-z])), ((?<y>-?\d+)|(?<regY>[a-z])))"
    , @"(?<jne>jne +(?<label>\w+))"
    , @"(?<je>je +(?<label>\w+))"
    , @"(?<jge>jge +(?<label>\w+))"
    , @"(?<jg>jg +(?<label>\w+))"
    , @"(?<jle>jle +(?<label>\w+))"
    , @"(?<jl>jl +(?<label>\w+))"
    , @"(?<call>call +(?<label>\w+))"
    , @"(?<ret>ret)"
    , @"(?<msg>msg +((?<message>('[^']*')|[a-z])(, )?)+)"
    , @"(?<end>end)"
    ));

  public static string Interpret(string input)
  { 
    var program = input.Split("\n", StringSplitOptions.RemoveEmptyEntries).Select(line => line.Trim()).Where(line => !line.StartsWith(";")).ToArray();
    
    var labels = new Dictionary<string, int>();
    for (int i = 0; i < program.Length; i++)
    {
      var match = labelExpression.Match(program[i]);
      if (match.Success) labels[match.Groups["label"].Value] = i;
    }

    var registers = new Dictionary<string, int>();
    var calls = new Stack<int>();

    var msg = string.Empty;
    int cmp = 0;
    for (int i = 0; i < program.Length; i++)
    {
      var _ = instructions.Match(program[i]).Groups;
      
      if (_["mov"].Success) registers[_["x"].Value] = ValueOrRegisterValue(_, "y", "regY");
      else if (_["inc"].Success) registers[_["x"].Value]++;
      else if (_["dec"].Success) registers[_["x"].Value]--;
      else if (_["add"].Success) registers[_["x"].Value] += ValueOrRegisterValue(_, "y", "regY");
      else if (_["sub"].Success) registers[_["x"].Value] -= ValueOrRegisterValue(_, "y", "regY");
      else if (_["mul"].Success) registers[_["x"].Value] *= ValueOrRegisterValue(_, "y", "regY");
      else if (_["div"].Success) registers[_["x"].Value] /= ValueOrRegisterValue(_, "y", "regY");
      else if (_["jmp"].Success) i = labels[_["label"].Value];
      else if (_["cmp"].Success) cmp = ValueOrRegisterValue(_, "x", "regX") - ValueOrRegisterValue(_, "y", "regY");
      else if (_["jne"].Success && cmp != 0) i = labels[_["label"].Value];
      else if (_["je"].Success && cmp == 0) i = labels[_["label"].Value];
      else if (_["jge"].Success && cmp >= 0) i = labels[_["label"].Value];
      else if (_["jg"].Success && cmp > 0) i = labels[_["label"].Value];
      else if (_["jle"].Success && cmp <= 0) i = labels[_["label"].Value];
      else if (_["jl"].Success && cmp < 0) i = labels[_["label"].Value];
      else if (_["call"].Success)
      {
        calls.Push(i);
        i = labels[_["label"].Value];
      }
      else if (_["ret"].Success) i = calls.Pop();
      else if (_["msg"].Success)
      {
        msg += string.Concat(_["message"].Captures.Select(arg => arg.Value.StartsWith("'") ? arg.Value.Trim('\'') : registers[arg.Value].ToString()));
      }
      else if (_["end"].Success) return msg;
    }

    return null;
    
    int ValueOrRegisterValue(GroupCollection groups, string val, string register) => int.TryParse(groups[val].Value, out int x) ? x : registers[groups[register].Value];
  }
}

____________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

  public class AssemblerInterpreter
  {
    public static string Interpret(string input)
    {
      var registers = new Dictionary<string, int>();
      var lines = input.Split(Environment.NewLine).
        Where(line => !string.IsNullOrEmpty(line) && !line.StartsWith(";")).ToArray();
      var instructions = lines.Select(line => new Command(line)).ToArray();
      var interpreter = new AssemblerInterpreter(registers);
      interpreter.FillLabels(lines);
      for (int position = 0; position < instructions.Length;)
      {
        position = interpreter.Run(instructions[position], position);
        if (position == int.MaxValue)
          return interpreter.message;
      }
      return null;
    }

    private void FillLabels(IReadOnlyList<string> lines)
    {
      for (var commandNumber = 0; commandNumber < lines.Count; commandNumber++)
      {
        var line = lines[commandNumber];
        if (line.EndsWith(":"))
          labels.Add(line[..^1], commandNumber);
      }
    }

    private AssemblerInterpreter(Dictionary<string, int> registers) =>
      this.registers = registers;
    private readonly Dictionary<string, int> registers;
    private string message = "";

    public readonly struct Command
    {
      public Command(string line)
      {
        string[] tokens = line.Split(new[] { ' ', ',', ';' },
          StringSplitOptions.RemoveEmptyEntries);
        Keyword = tokens[0];
        Register = tokens.Length > 1 ? tokens[1] : "";
        Value = Keyword == "msg"
          ? line.Split(';')[0].Trim().Substring(4).Trim()
          : tokens.Length > 2
            ? tokens[2]
            : "";
      }

      public string Keyword { get; }
      public string Register { get; }
      public string Value { get; }

      public override string ToString() =>
        "Command Keyword=" + Keyword + ", Register=" + Register + ", Value=" + Value;
    }
    
    private int Run(Command command, int position)
    {
      //Console.WriteLine("Run: " + command + ", registers=" + registers.Count + ", " +
      //  string.Join(',', registers.Keys) + "=" + string.Join(',', registers.Values));
      switch (command.Keyword)
      {
      case "mov":
        Mov(command);
        break;
      case "inc":
        Inc(command);
        break;
      case "dec":
        Dec(command);
        break;
      case "add":
        Add(command);
        break;
      case "sub":
        Sub(command);
        break;
      case "mul":
        Mul(command);
        break;
      case "div":
        Div(command);
        break;
      case "jmp":
        return Jmp(command);
      case "cmp":
        Cmp(command);
        break;
      case "jne":
        return Jne(command, position);
      case "je":
        return Je(command, position);
      case "jge":
        return Jge(command, position);
      case "jg":
        return Jg(command, position);
      case "jle":
        return Jle(command, position);
      case "jl":
        return Jl(command, position);
      case "call":
        return Call(command, position);
      case "ret":
        return Ret();
      case "msg":
        Msg(command);
        break;
      case "end":
        return int.MaxValue;
      }
      return position + 1;
    }
    
    private int GetCommandRegisterValue(Command command) =>
      int.TryParse(command.Register, out int result)
        ? result
        : registers[command.Register];

    private int GetCommandValue(Command command) =>
      int.TryParse(command.Value, out int result)
        ? result
        : registers[command.Value];

    private void Mov(Command command) =>
      registers[command.Register] = GetCommandValue(command);

    private void Dec(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = --value;
    }

    private void Inc(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = ++value;
    }
    
    private void Add(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = value + GetCommandValue(command);
    }
    
    private void Sub(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = value - GetCommandValue(command);
    }
    
    private void Mul(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = value * GetCommandValue(command);
    }

    private void Div(Command command)
    {
      if (registers.TryGetValue(command.Register, out int value))
        registers[command.Register] = value / GetCommandValue(command);
    }

    private readonly Dictionary<string, int> labels = new Dictionary<string, int>();
    private int Jmp(Command command) => labels[command.Register];

    private void Cmp(Command command) =>
      cmpResult = GetCommandRegisterValue(command) - GetCommandValue(command);
    private int cmpResult;

    private int Jne(Command command, int position) =>
      cmpResult != 0
        ? labels[command.Register]
        : position+1;

    private int Je(Command command, int position) =>
      cmpResult == 0
        ? labels[command.Register]
        : position+1;

    private int Jge(Command command, int position) =>
      cmpResult >= 0
        ? labels[command.Register]
        : position+1;

    private int Jg(Command command, int position) =>
      cmpResult > 0
        ? labels[command.Register]
        : position+1;

    private int Jle(Command command, int position) =>
      cmpResult <= 0
        ? labels[command.Register]
        : position+1;

    private int Jl(Command command, int position) =>
      cmpResult < 0
        ? labels[command.Register]
        : position+1;
    
    private int Call(Command command, int position)
    {
      returnPointers.Push(position);
      return labels[command.Register];
    }

    private readonly Stack<int> returnPointers = new Stack<int>();
    private int Ret() => returnPointers.Pop() + 1;

    private void Msg(Command command)
    {
      bool inString = false;
      for (var index=0; index<command.Value.Length; index++)
        if (command.Value[index] == '\'')
          inString = !inString;
        else if (inString)
          message += command.Value[index];
        else if (registers.ContainsKey(command.Value[index] + ""))
          message += registers[command.Value[index] + ""];
    }
  }
  
____________________________________________________
using System.Collections.Generic;
using System;
using static Utils;
using System.Linq;
using System.Text.RegularExpressions;

public class AssemblerInterpreter
    {
        private static string[] ParseProgram(string program)
        {
            const string pattern = @";.*";
            var instructions = program.Split("\n")
                .Select(s => Regex.Replace(s, pattern, ""))
                .Select(s => s.Trim())
                .ToList();
            instructions.RemoveAll(string.IsNullOrWhiteSpace);
            return instructions.ToArray();
        }

        public static string Interpret(string program)
        {
            ICpu cpu = new Cpu();
            var instructions = ParseProgram(program);

            var registers = Interpret(instructions, cpu);
        
            return registers == null ? null : cpu.GetOutput();
        }

        public static Dictionary<string, int> Interpret(string[] program, ICpu cpu = null)
        {
            cpu ??= new Cpu();

            var comparisonStatus = ComparisonStatus.None;
            var callerPointer = new Stack<int>();
            for (var opPointer = 0; opPointer < program.Length; opPointer++)
            {
                var op = program[opPointer];
                var operation = op.Split(' ', 2);
                switch (operation[0])
                {
                    case "mov":
                        Op_mov(cpu, operation[1]);
                        break;
                    case "inc":
                        Op_inc(cpu, operation[1]);
                        break;
                    case "dec":
                        Op_dec(cpu, operation[1]);
                        break;
                    case "jnz":
                        opPointer = Op_jnz(cpu, opPointer, operation);
                        break;
                    case "add":
                        Op_arithmetic(cpu, operation[1], (a, b) => a + b);
                        break;
                    case "sub":
                        Op_arithmetic(cpu, operation[1], (a, b) => a - b);
                        break;
                    case "mul":
                        Op_arithmetic(cpu, operation[1], (a, b) => a * b);
                        break;
                    case "div":
                        Op_arithmetic(cpu, operation[1], (a, b) => a / b);
                        break;
                    case "jmp":
                        opPointer = Op_jmp(cpu, program, operation[1]) ?? throw new InvalidProgramException("Label does not exist");
                        break;
                    case "cmp":
                        comparisonStatus = Op_cmp(cpu, operation[1]);
                        break;
                    case "jne":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.NotEqual)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "je":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.Equal)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "jge":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.Greater) || status.Is(ComparisonStatus.Equal)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "jg":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.Greater)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "jle":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.Lower) || status.Is(ComparisonStatus.Equal)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "jl":
                        opPointer = Op_conditionalJump(cpu, program, opPointer, operation[1], comparisonStatus,
                                        status => status.Is(ComparisonStatus.Lower)) ??
                                    throw new InvalidProgramException("Label does not exist");
                        break;
                    case "call":
                        callerPointer.Push(opPointer);
                        opPointer = Op_call(cpu, program, operation[1]) ?? throw new InvalidProgramException("Label does not exist");
                        break;
                    case "ret":
                        opPointer = callerPointer.Count > 0 ? callerPointer.Pop() : opPointer;
                        break;
                    case "msg":
                        Op_msg(cpu, operation[1]);
                        break;
                    case "end":
                        return cpu.GetRegisters();
                    default:
                        if (!op.EndsWith(':')) throw new NotImplementedException();

                        op = op.TrimEnd(':');
                        if (cpu.TryGetLabel(op, out _)) continue;
                        cpu.AddLabel(op, opPointer);
                        break;
                }
            }
            return null;
        }

        /// <summary>
        /// Prepares program output
        /// msg 'Something: ', x
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="messageFormat"></param>
        private static void Op_msg(ICpu cpu, string messageFormat)
        {
            const string pattern = "('.*?')|([a-zA-Z])";
            var regex = new Regex(pattern);
            var matches = regex.Matches(messageFormat);
            var output = "";
            foreach (Match arg in matches)
            {
                if (arg.Value.Contains("'")) output += arg.Value.Replace("'", "");
                else output += GetValue(cpu, arg.Value);
            }
            cpu.PrepareOutput(output);
        }

        /// <summary>
        /// Call a subroutine identified by a label and returns to the next instruction pointer after caller instruction pointer
        /// call lbl
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="program"></param>
        /// <param name="label"></param>
        /// <returns></returns>
        private static int? Op_call(ICpu cpu, IReadOnlyList<string> program, string label)
        {
            label = label.Trim();
            if (cpu.TryGetLabel(label, out var pointer)) return pointer;

            return SearchLabel(cpu, program, label, out var opCall) ? opCall : null;
        }

        /// <summary>
        /// Moves instruction pointer to label
        /// jump lbl
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="program"></param>
        /// <param name="label"></param>
        /// <returns></returns>
        private static int? Op_jmp(ICpu cpu, IReadOnlyList<string> program, string label)
        {
            label = label.Trim();
            if (cpu.TryGetLabel(label, out var pointer)) return pointer;
            return SearchLabel(cpu, program, label, out var opCall)
                ? opCall
                : throw new InvalidProgramException("Label does not exist");
        }

        private static bool SearchLabel(ICpu cpu, IReadOnlyList<string> program, string label, out int? opCall)
        {
            opCall = null;
            for (var i = 0; i < program.Count; i++)
            {
                if (program[i] != $"{label}:") continue;

                cpu.AddLabel(label, i);
                {
                    opCall = i;
                    return true;
                }
            }

            return false;
        }

        /// <summary>
        /// Jumps to a label based on last condition
        /// jne label
        /// je lbl
        /// jge lbl
        /// jg lbl
        /// jle lbl
        /// jl lbl
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="program"></param>
        /// <param name="opPointer"></param>
        /// <param name="label"></param>
        /// <param name="status"></param>
        /// <param name="condition"></param>
        /// <returns></returns>
        private static int? Op_conditionalJump(ICpu cpu, IReadOnlyList<string> program, int opPointer, string label, ComparisonStatus status, Func<ComparisonStatus, bool> condition)
        {
            return condition(status) ? Op_jmp(cpu, program, label) : opPointer;
        }

        /// <summary>
        /// Compares two values or registers
        /// cmp x, y
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="opArgs"></param>
        /// <returns></returns>
        private static ComparisonStatus Op_cmp(ICpu cpu, string opArgs)
        {
            var args = opArgs
                .Split(",")
                .Select(s => s.Trim())
                .ToArray();
            var a = GetValue(cpu, args[0]);
            var b = GetValue(cpu, args[1]);
            var status = Compare(a, b);
            return status;
        }

        /// <summary>
        /// Make an arithmetic operation with x register with y value
        /// add x, y
        /// sub x, y
        /// mul x, y
        /// div x, y
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="opArgs"></param>
        /// <param name="func">arithmetic function</param>
        private static void Op_arithmetic(ICpu cpu, string opArgs, Func<int, int, int> func)
        {
            var args = opArgs
                .Split(",")
                .Select(s => s.Trim())
                .ToArray();
            var left = args[0];
            var right = args[1];
            cpu.WriteReg(left, func(GetValue(cpu, left), GetValue(cpu, right)));
        }

        /// <summary>
        /// Jumps to an instruction y steps away (positive means forward, negative means backward, y can be a register or a constant), but only if x (a constant or a register) is not zero
        /// Note: the jnz instruction moves relative to itself. For example, an offset of -1 would continue at the previous instruction, while an offset of 2 would skip over the next instruction.
        /// jnz x, y
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="opPointer"></param>
        /// <param name="operation"></param>
        /// <returns></returns>
        private static int Op_jnz(ICpu cpu, int opPointer, IReadOnlyList<string> operation)
        {
            var args = operation[1]
                .Split(",")
                .Select(s => s.Trim())
                .ToArray();
            opPointer += GetValue(cpu, args[0]) != 0 ? GetValue(cpu, args[1]) - 1 : 0;
            return opPointer;
        }

        /// <summary>
        /// Decrement x register by 2
        /// dec x
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="register"></param>
        private static void Op_dec(ICpu cpu, string register)
        {
            register = register.Trim();
            cpu.WriteReg(register, cpu.ReadReg(register) - 1);
        }

        /// <summary>
        /// Increment x register by 1
        /// inc x
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="register"></param>
        private static void Op_inc(ICpu cpu, string register)
        {          
            register = register.Trim();
            cpu.WriteReg(register, cpu.ReadReg(register) + 1);
        }

        /// <summary>
        /// Moves y value to register x
        /// mov x, y
        /// </summary>
        /// <param name="cpu"></param>
        /// <param name="opArgs"></param>
        private static void Op_mov(ICpu cpu, string opArgs)
        {
            var args = opArgs
                .Split(",")
                .Select(s => s.Trim())
                .ToArray();
            cpu.WriteReg(args[0], GetValue(cpu, args[1]));
        }
        private static int GetValue(ICpu cpu, string val) => int.TryParse(val, out var num) ? num : cpu.ReadReg(val);
    }

public interface ICpu
    {
        /// <summary>
        /// Returns the value of the named register.
        /// </summary>
        /// <param name="name"></param>
        /// <returns></returns>
        int ReadReg(string name);

        /// <summary>
        /// Stores the value into the given register.
        /// </summary>
        /// <param name="name"></param>
        /// <param name="value"></param>
        void WriteReg(string name, int value);

        /// <summary>
        /// Returns a copy of current registers
        /// </summary>
        /// <returns></returns>
        Dictionary<string, int> GetRegisters();

        /// <summary>
        /// Add a label if it doesn't exist
        /// </summary>
        /// <param name="name"></param>
        /// <param name="pointer"></param>
        void AddLabel(string name, int pointer);

        /// <summary>
        /// Return pointer to the label
        /// </summary>
        /// <param name="name"></param>
        /// <param name="pointer"></param>
        /// <returns></returns>
        bool TryGetLabel(string name, out int pointer);

        /// <summary>
        /// Prepares the output of the program
        /// </summary>
        /// <param name="output"></param>
        void PrepareOutput(string output);

        /// <summary>
        /// Returns the output of the program
        /// </summary>
        /// <returns></returns>
        string GetOutput();
    }

public class Cpu : ICpu
    {
        private readonly Dictionary<string, int> _registers;
        private readonly Dictionary<string, int> _labels;
        private string _output;

        public Cpu()
        {
            _registers = new Dictionary<string, int>();
            _labels = new Dictionary<string, int>();
            _output = string.Empty;
        }

        /// <summary>
        /// Returns the value of the named register.
        /// </summary>
        /// <param name="name"></param>
        /// <returns></returns>
        public int ReadReg(string name)
        {
            return _registers.TryGetValue(name, out var value) ? value : 0;
        }

        /// <summary>
        /// Stores the value into the given register.
        /// </summary>
        /// <param name="name"></param>
        /// <param name="value"></param>
        public void WriteReg(string name, int value)
        {
            if (!_registers.TryAdd(name, value))
            {
                _registers[name] = value;
            }
        }

        /// <summary>
        /// Returns a copy of current registers
        /// </summary>
        /// <returns></returns>
        public Dictionary<string, int> GetRegisters() => _registers;

        /// <summary>
        /// Add a label if it doesn't exist
        /// </summary>
        /// <param name="name"></param>
        /// <param name="pointer"></param>
        public void AddLabel(string name, int pointer)
        {
            _labels.TryAdd(name, pointer);
        }

        /// <summary>
        /// Return pointer to the label
        /// </summary>
        /// <param name="name"></param>
        /// <param name="pointer"></param>
        /// <returns></returns>
        public bool TryGetLabel(string name, out int pointer) => _labels.TryGetValue(name, out pointer);

        /// <summary>
        /// Prepares the output of the program
        /// </summary>
        /// <param name="output"></param>
        public void PrepareOutput(string output)
        {
            _output += output;
        }

        /// <summary>
        /// Returns the output of the program
        /// </summary>
        /// <returns></returns>
        public string GetOutput() => _output;
    }
    
public static class Utils
    {
        [Flags]
        public enum ComparisonStatus
        {
            None = 0,
            Equal = 1,
            Greater = 2,
            Lower = 4,
            NotEqual = 8,
        }


        public static ComparisonStatus Compare(int a, int b)
        {
            var status = ComparisonStatus.None;
            if (a == b) status |= ComparisonStatus.Equal;
            if (a > b) status |= ComparisonStatus.Greater;
            if (a < b) status |= ComparisonStatus.Lower;
            if (a != b) status |= ComparisonStatus.NotEqual;
            return status;
        }

        public static bool Is(this ComparisonStatus current, ComparisonStatus value)
        {
            return (current & value) == value;
        }
    }
