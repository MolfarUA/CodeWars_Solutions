import java.util.*;
import java.util.function.BiFunction;
import java.util.regex.*;
import java.util.stream.Collectors;


public class AssemblerInterpreter {
    
    
    private static Pattern TOKENIZER  = Pattern.compile(";.*|(?<cmd>('.*?'|-?\\w+))[:,]?\\s*");
    
    private static Map<String,BiFunction<Integer,Integer,Boolean>> CMP_FUNCS = new HashMap<String,BiFunction<Integer,Integer,Boolean>>();
    static {  CMP_FUNCS.put("jmp", (x,y) ->  true  );
              CMP_FUNCS.put("jne", (x,y) -> x != y );
              CMP_FUNCS.put("je",  (x,y) -> x == y );
              CMP_FUNCS.put("jge", (x,y) -> x >= y );
              CMP_FUNCS.put("jg",  (x,y) -> x >  y );
              CMP_FUNCS.put("jle", (x,y) -> x <= y );
              CMP_FUNCS.put("jl",  (x,y) -> x <  y );
    }

    private static Map<String,BiFunction<Integer,Integer,Integer>> MATH_BI_FUNCS   = new HashMap<String,BiFunction<Integer,Integer,Integer>>(),
                                                                   MATH_MONO_FUNCS = new HashMap<String,BiFunction<Integer,Integer,Integer>>();
    static {  MATH_BI_FUNCS.put("add", (x,y) -> x + y );
              MATH_BI_FUNCS.put("sub", (x,y) -> x - y );
              MATH_BI_FUNCS.put("mul", (x,y) -> x * y );
              MATH_BI_FUNCS.put("div", (x,y) -> x / y );
              
              MATH_MONO_FUNCS.put("inc", MATH_BI_FUNCS.get("add") );
              MATH_MONO_FUNCS.put("dec", MATH_BI_FUNCS.get("sub") );
    }
    
    private static Set<String> JUMPS_CMD = new HashSet<String>(CMP_FUNCS.keySet());
    static {  JUMPS_CMD.add("call");  }
    
    private static Set<String> ALL_CMDS = new HashSet<String>(JUMPS_CMD);
    static {  ALL_CMDS.addAll(Arrays.asList("ret", "end", "mov", "cmp", "msg"));
              ALL_CMDS.addAll(MATH_BI_FUNCS.keySet());
              ALL_CMDS.addAll(MATH_MONO_FUNCS.keySet());
    }
    
    
    private static int pointer;
    private static Map<String,Integer> registers, jumpsLbl;
    private static Map<String,Boolean> cmpDct;
    private static StringBuilder output;
    private static Stack<Integer> callStackP;
    private static List<List<String>> instructions;
    
    
    
    public static String interpret(final String input) {
        
        pointer    = 0;
        registers  = new HashMap<String,Integer>();
        cmpDct     = new HashMap<String,Boolean>();
        output     = new StringBuilder();
        callStackP = new Stack<Integer>();
        
        tokenizeProgram(input);
        seekJumpLabels();
        updateCmp("0", "0");
        
        while (0 <= pointer && pointer < instructions.size()) {
            String cmd = instructions.get(pointer).get(0);
            
            if      (CMP_FUNCS.containsKey(cmd))            pointer = moveTo(cmd, label());
            else if (MATH_BI_FUNCS.containsKey(cmd))        updateRegs(MATH_BI_FUNCS.get(cmd),   x(), y());
            else if (MATH_MONO_FUNCS.containsKey(cmd))      updateRegs(MATH_MONO_FUNCS.get(cmd), x(), "1");
            else if (cmd.equals("mov"))                     registers.put( x(), isNum(y()) ? Integer.parseInt(y()) : registers.get(y()));
            else if (cmd.equals("cmp"))                     updateCmp(x(), y());
            else if (cmd.equals("call"))                  { callStackP.push(pointer); pointer = moveTo("jmp", label()); }
            else if (cmd.equals("ret"))                     pointer = callStackP.pop();
            else if (cmd.equals("msg"))                     output.append(formatMessage( instructions.get(pointer).subList(1, instructions.get(pointer).size()) ));
            else if (cmd.equals("end"))                     return output.toString();
            
            pointer++;
        }
        return null;
    }


    private static String  label()                          { return x(); }
    private static String  x()                              { return instructions.get(pointer).get(1); }
    private static String  y()                              { return instructions.get(pointer).get(2); }
    
    private static boolean isNum(String s)                  { return s.matches("^-?\\d+$"); }
    private static int     moveTo(String cmd, String label) { return cmpDct.get(cmd) ? jumpsLbl.get(label) : pointer; }
    

    private static void tokenizeProgram(String input) {
        
        instructions = new ArrayList<List<String>>();
        
        int last = -1;
        for (String line: input.split("\\n\\s*")) { last++;
        
            Matcher mTok = TOKENIZER.matcher(line);
            instructions.add(new ArrayList<String>());
            
            while (mTok.find()) {
                String tok = mTok.group("cmd"); 
                if (tok != null && tok.length() != 0)
                    instructions.get(last).add(mTok.group("cmd"));
            }
            if (instructions.get(last).size() == 0) {
                instructions.remove(last);
                last--;
            }
        }
    }


    private static void seekJumpLabels() {
        
        jumpsLbl = new HashMap<String,Integer>();
        int i = -1;
        for (List<String> cmd: instructions) { i++;
            if (!ALL_CMDS.contains(cmd.get(0))) jumpsLbl.put(cmd.get(0), i);
        }
    }


    private static void updateCmp(String xS, String yS) {
        
        for (String f: CMP_FUNCS.keySet()) {
            int x = registers.getOrDefault(xS, 0),
                y = isNum(yS) ? Integer.parseInt(yS) : registers.get(yS); 
            cmpDct.put(f, CMP_FUNCS.get(f).apply(x, y) );
        }
    }
    

    private static void    updateRegs(BiFunction<Integer,Integer,Integer> op, String x, String y) {
        registers.put( x(), op.apply(registers.get(x),
                                     isNum(y) ? Integer.parseInt(y) : registers.get(y) ));
    }


    private static String formatMessage(List<String> lst) {
        return lst.stream().map( s -> registers.containsKey(s) ? String.valueOf(registers.get(s))
                                                               : s.substring(1, s.length()-1))
                           .collect(Collectors.joining());
    }
}

____________________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;

public class AssemblerInterpreter {
  
    public static String interpret(final String input) {
      
        // convert input into a list of lines
        ArrayList<String> program = new ArrayList<String>(Arrays.asList(input.split("\n")));
        
        LinkedList <Integer> stack = new LinkedList<Integer>();
        HashMap<String, Integer> labels = new HashMap<String, Integer>();
        HashMap<String, Integer> registry = new HashMap<String, Integer>();
        int compare = 0;
        String output = new String();
      
        for(int i = 0; i < program.size(); i++) {
            // retrieve instruction line
            String instruction = program.get(i);
            // purge comments
            if(instruction.contains(";"))
                instruction = instruction.substring(0, instruction.indexOf(';'));
            // remove leading/trailing whitespaces
            instruction = instruction.trim();
            // remove excess spaces between parameters, excluding String literals
            instruction.replaceAll("[\\s]+(?=[^']*(?:'[^']*'[^']*)*$)", " ");
          
            if(instruction.contains(":")) {
                String temp = instruction.split(" ")[0];
                if(temp.endsWith(":")) {
                    labels.put(instruction.substring(0, instruction.indexOf(':')), i);
                    instruction = instruction.substring(temp.length());
                }
            }
            
            program.set(i, instruction);
            
        }
      
        // Execute Program
        for(int i = 0; i < program.size(); i++) {
            
            // Split statement by spaces 
            String[] statement = program.get(i).split("[, ]+(?=[^']*(?:'[^']*'[^']*)*$)");
            
            switch(statement[0]) {
                
                case "mov": registry.put(statement[1], valueOf(registry, statement[2])); break;
                
                case "inc": registry.put(statement[1], registry.get(statement[1]) + 1); break;
                case "dec": registry.put(statement[1], registry.get(statement[1]) - 1); break;
                
                case "add": registry.put(statement[1], registry.get(statement[1]) + valueOf(registry, statement[2])); break;
                case "sub": registry.put(statement[1], registry.get(statement[1]) - valueOf(registry, statement[2])); break;
                case "mul": registry.put(statement[1], registry.get(statement[1]) * valueOf(registry, statement[2])); break;
                case "div": registry.put(statement[1], registry.get(statement[1]) / valueOf(registry, statement[2])); break;
                
                case "jmp": i = labels.get(statement[1]) - 1; break;
                case "cmp": compare = valueOf(registry, statement[1]) - valueOf(registry, statement[2]); break;
                case "jne": if(compare != 0) i = labels.get(statement[1]) - 1; break;
                case "je":  if(compare == 0) i = labels.get(statement[1]) - 1; break;
                case "jge": if(compare >= 0) i = labels.get(statement[1]) - 1; break;
                case "jg":  if(compare > 0)  i = labels.get(statement[1]) - 1; break;
                case "jle": if(compare <= 0) i = labels.get(statement[1]) - 1; break;
                case "jl":  if(compare < 0)  i = labels.get(statement[1]) - 1; break;
                
                case "call": stack.add(i); i = labels.get(statement[1]) - 1; break;
                case "ret": i = stack.removeLast(); break;
                
                case "msg": for(int j = 1; j < statement.length; j++) output += (statement[j].contains("'"))
                      ? statement[j].substring(1, statement[j].length() - 1) 
                      : valueOf(registry, statement[j]); break;
                
                case "end": return output;
                
            }
            
        }
      
        return null;
      
    }
  
    private static int valueOf(HashMap<String, Integer> registry, String string) {
        try {
            return Integer.parseInt(string);
        } catch(NumberFormatException nfe) {
            return registry.get(string);
        }
    }
    
}

____________________________________________________
import java.util.*;

public class AssemblerInterpreter {
    private enum Operation {
        MOV(2), INC(1), DEC(1), ADD(2), SUB(2), MUL(2), DIV(2), JMP(1), CMP(2), JNE(1),
            JE(1), JGE(1), JG(1), JLE(1), JL(1), CALL(1), RET(0), MSG(-1), END(0);

        final int argCount;

        Operation(int argCount) {
            this.argCount = argCount;
        }
    }

    private static final Map<String, Operation> STR_OP_MAP = new HashMap<>();
    static {
        for (Operation op : Operation.values())
            STR_OP_MAP.put(op.name().toLowerCase(), op);
    }

    private static class Instruction {
        final Operation op;
        String arg1;
        String arg2;
        int argNum;

        Instruction(Operation op) {
            this.op = op;
        }

        static boolean isRegister(String arg) {
            return arg.length() == 1 && Character.isLetter(arg.charAt(0));
        }

        void adjustArgs() {
            switch (op) {
                case MOV:
                case ADD:
                case SUB:
                case MUL:
                case DIV:
                    if (!isRegister(arg2)) {
                        argNum = Integer.parseInt(arg2);
                        arg2 = null;
                    }
                    //$FALL-THROUGH$
                case INC:
                case DEC:
                    if (!isRegister(arg1))
                        throw new IllegalArgumentException("Invalid register name: " + arg1);
                    break;
                case CMP:
                    if (isRegister(arg1)) {
                        if (!isRegister(arg2)) {
                            argNum = Integer.parseInt(arg2);
                            arg2 = null;
                        }
                    } else {
                        argNum = Integer.parseInt(arg1);
                        arg1 = null;
                        if (!isRegister(arg2)) {
                            argNum = Integer.compare(argNum, Integer.parseInt(arg2));
                            arg2 = null;
                        }
                    }
                    break;
                case JMP:
                case JNE:
                case JE:
                case JGE:
                case JG:
                case JLE:
                case JL:
                case CALL:
                    if (arg1.indexOf(':') >= 0 || !Character.isLetter(arg1.charAt(0)))
                        throw new IllegalArgumentException("Invalid label: " + arg1);
                    break;
                case RET:
                case MSG:
                case END:
                    break;
            }
        }

        int getValue2(Map<String, Integer> registers) {
            return arg2 == null ? argNum : registers.get(arg2);
        }
    }

    private static class InstructionParser {
        Instruction instr;
        String args;
        int i;
        int len;

        void error(String msg) {
            throw new IllegalArgumentException(msg + ": " + instr.op.name().toLowerCase() + args);
        }

        void nextNonWhitespace(boolean endExpected) {
            char c = 0;
            for (; i < len; i++) {
                c = args.charAt(i);
                if (!Character.isWhitespace(c))
                    break;
            }
            if (endExpected ^ (i == len || c == ';'))
                error(endExpected ? "Extra characters at the end" : "Missing required argument");
        }

        String nextToken() {
            nextNonWhitespace(false);
            int j = i;
            for (i++; i < len; i++) {
                char c = args.charAt(i);
                if (Character.isWhitespace(c) || c == ';' || c == ',')
                    break;
            }
            return args.substring(j, i);
        }

        Instruction parse(Operation op, String args) {
            instr = new Instruction(op);
            this.args = args;
            i = 0;
            len = args.length();
            int ac = op.argCount;
            if (ac >= 0) {
                if (ac > 0) {
                    instr.arg1 = nextToken();
                    if (ac > 1) {
                        nextNonWhitespace(false);
                        if (args.charAt(i) != ',')
                            error("Comma expected");
                        i++;
                        instr.arg2 = nextToken();
                    }
                }
                nextNonWhitespace(true);
            } else {
                nextNonWhitespace(false);
                instr.arg1 = args.substring(i);
            }
            instr.adjustArgs();
            return instr;
        }
    }

    private final List<Instruction> program = new ArrayList<>();
    private final Map<String, Integer> labels = new HashMap<>();

    public AssemblerInterpreter(String code) {
        String[] lines = code.split("\n");
        int iAddr = 0;
        InstructionParser parser = new InstructionParser();
        for (String line : lines) {
            Operation op = null;
            int len = line.length();
            int i = 0;
            while (i < len) {
                char c = line.charAt(i);
                if (Character.isWhitespace(c)) {
                    i++;
                    continue;
                }
                if (c == ';')
                    break;
                if (c == ':')
                    throw new IllegalArgumentException("Empty label: " + line);
                int j = i;
                while (++i < len) {
                    c = line.charAt(i);
                    if (Character.isWhitespace(c) || c == ':' || c == ';')
                        break;
                }
                String ident = line.substring(j, i);
                op = STR_OP_MAP.get(ident);
                if (op != null)
                    break;
                int k = line.indexOf(':', i);
                j = k - 1;
                while (j >= i && Character.isWhitespace(line.charAt(j)))
                    j--;
                if (k < 0 || j >= i)
                    throw new IllegalArgumentException(
                            "Unknown operation or label without colon: " + line);
                if (labels.put(ident, iAddr) != null)
                    throw new IllegalArgumentException("Duplicate label: " + ident);
                i = k + 1;
            } // this loop makes multiple labels possible at the beginning of a line
            if (op != null) {
                program.add(parser.parse(op, line.substring(i)));
                iAddr++;
            }
        }
    }

    private int getAddr(String label) {
        Integer addr = labels.get(label);
        if (addr == null)
            throw new IllegalArgumentException("Undefined label: " + label);
        return addr - 1; // to compensate pointer auto-increment in loop
    }

    public String run() {
        Map<String, Integer> regs = new HashMap<>();
        Stack<Integer> stack = new Stack<>();
        int cmp = 0;
        StringBuilder output = new StringBuilder();
        for (int ip = 0, sz = program.size(); ip < sz; ip++) {
            Instruction instr = program.get(ip);
            String a1 = instr.arg1;
            switch (instr.op) {
                case MOV:
                    regs.put(a1, instr.getValue2(regs));
                    break;
                case ADD:
                    regs.compute(a1, (r, x) -> x + instr.getValue2(regs));
                    break;
                case SUB:
                    regs.compute(a1, (r, x) -> x - instr.getValue2(regs));
                    break;
                case MUL:
                    regs.compute(a1, (r, x) -> x * instr.getValue2(regs));
                    break;
                case DIV:
                    regs.compute(a1, (r, x) -> x / instr.getValue2(regs));
                    break;
                case INC:
                    regs.compute(a1, (r, x) -> x + 1);
                    break;
                case DEC:
                    regs.compute(a1, (r, x) -> x - 1);
                    break;
                case CMP:
                    if (a1 == null)
                        cmp = Integer.compare(instr.argNum, instr.arg2 == null ? 0 : regs.get(instr.arg2));
                    else
                        cmp = Integer.compare(regs.get(a1), instr.getValue2(regs));
                    break;
                case JMP:
                    ip = getAddr(a1);
                    break;
                case JNE:
                    if (cmp != 0)
                        ip = getAddr(a1);
                    break;
                case JE:
                    if (cmp == 0)
                        ip = getAddr(a1);
                    break;
                case JGE:
                    if (cmp >= 0)
                        ip = getAddr(a1);
                    break;
                case JG:
                    if (cmp > 0)
                        ip = getAddr(a1);
                    break;
                case JLE:
                    if (cmp <= 0)
                        ip = getAddr(a1);
                    break;
                case JL:
                    if (cmp < 0)
                        ip = getAddr(a1);
                    break;
                case CALL:
                    stack.push(ip);
                    ip = getAddr(a1);
                    break;
                case RET:
                    ip = stack.pop();
                    break;
                case MSG:
                    for (int i = 0, len = a1.length(); i < len; i++) {
                        char c = a1.charAt(i);
                        if (Character.isWhitespace(c) || c == ',')
                            continue;
                        if (c == ';')
                            break;
                        if (c == '\'') {
                            int j = i;
                            while (++i < len && a1.charAt(i) != '\'')
                                ;
                            if (i == len)
                                throw new IllegalArgumentException(
                                        "Matching ' delimiter is not found at the msg arg: " + a1);
                            output.append(a1.substring(j + 1, i));
                        } else {
                            int j = i;
                            while (++i < len) {
                                c = a1.charAt(i);
                                if (Character.isWhitespace(c) || c == ',')
                                    break;
                            }
                            output.append(regs.get(a1.substring(j, i)));
                        }
                    }
                    break;
                case END:
                    return output.toString();
            }
        }
        return null;
    }

    public static String interpret(final String input) {
        return new AssemblerInterpreter(input).run();
    }
}

____________________________________________________
import java.util.*;
import java.util.regex.*;

public class AssemblerInterpreter {
    private static Map<String,Integer> registers;
    private static Map<String,Integer> labels;
    private static Stack<Integer> callStack;
    private static StringBuilder output;
    private static int pointer;
    private static int cmpDiff;
    
    public static String interpret(final String input) {
        // Init new "program"
        pointer = 0;
        registers = new HashMap<String,Integer>();
        callStack = new Stack<Integer>();
        output = new StringBuilder();                                          
        String[] program = Arrays.stream(input.split("\n")).map(s -> s.replaceAll(";.*|^[^a-zA-Z]+","")).toArray(String[]::new);        
        parseLabels(program);
        
        Pattern units = Pattern.compile("[a-zA-Z0-9-_]+");
        while(pointer < program.length) {
            String[] line = units.matcher(program[pointer]).results().map(s -> s.group()).toArray(String[]::new);
            if(line.length > 0) {
                switch(line[0]) {
                    case "mov":  mov(line);  break;
                    case "inc":  inc(line);  break;
                    case "dec":  dec(line);  break;
                    case "add":  add(line);  break;
                    case "sub":  sub(line);  break;
                    case "mul":  mul(line);  break;
                    case "div":  div(line);  break;
                    case "jmp":  jmp(line);  break;
                    case "cmp":  cmp(line);  break;
                    case "jne":  jne(line);  break;
                    case "je":  je(line);  break;
                    case "jge":  jge(line);  break;
                    case "jg":  jg(line);  break;
                    case "jle":  jle(line);  break;
                    case "jl":  jl(line);  break;
                    case "call":  call(line);  break;
                    case "ret":  ret();  break;
                    case "msg":  msg(program[pointer].substring(4));  break;
                    case "end":  return output.toString();
                }
            }
            pointer++;
        }
        
        return null;
    }
    
    // Instructions
    private static void mov(String[] line) {
        registers.put(line[1], parseValue(line[2]));
    }
    
    private static void inc(String[] line) {
        registers.put(line[1], registers.get(line[1]) + 1);
    }
    
    private static void dec(String[] line) {
        registers.put(line[1], registers.get(line[1]) - 1);        
    }
    
    private static void add(String[] line) {
        registers.put(line[1], registers.get(line[1]) + parseValue(line[2]));        
    }
    
    private static void sub(String[] line) {
        registers.put(line[1], registers.get(line[1]) - parseValue(line[2]));  
    }
    
    private static void mul(String[] line) {
        registers.put(line[1], registers.get(line[1]) * parseValue(line[2]));  
    }
    
    private static void div(String[] line) {
        registers.put(line[1], registers.get(line[1]) / parseValue(line[2]));  
    }
    
    private static void jmp(String[] line) {
        pointer = labels.get(line[1]);
    }
    
    private static void cmp(String[] line) {
        cmpDiff = parseValue(line[1]) - parseValue(line[2]);
    }
    
    private static void jne(String[] line) {
        if(cmpDiff != 0) pointer = labels.get(line[1]);
    }
    
    private static void je(String[] line) {
        if(cmpDiff == 0) pointer = labels.get(line[1]);
    }
    
    private static void jge(String[] line) {
        if(cmpDiff >= 0) pointer = labels.get(line[1]);        
    }
    
    private static void jg(String[] line) {
        if(cmpDiff > 0) pointer = labels.get(line[1]);        
    }
    
    private static void jle(String[] line) {
        if(cmpDiff <= 0) pointer = labels.get(line[1]);        
    }
    
    private static void jl(String[] line) {
        if(cmpDiff < 0) pointer = labels.get(line[1]);        
    }
    
    private static void call(String[] line) {
        callStack.push(pointer);
        pointer = labels.get(line[1]);
    }
    
    private static void ret() {
        pointer = callStack.pop();
    }
    
    private static void msg(String line) {
        Pattern.compile("'[^']*'|[a-zA-Z]+").matcher(line).results().map(s -> s.group()).forEach(s -> {
            if(s.matches("'[^']*'")) {
                output.append(s.substring(1, s.length() - 1));
            } else {
                output.append(registers.get(s));
            }
        });
    }
    
    // Utility functions    
    private static int parseValue(String s) {
        int result;
        try {
            result = Integer.parseInt(s);
        } catch (NumberFormatException e) {
            result = registers.get(s);
        }
        return result;
    }
    
    private static void parseLabels(String[] program) {
        labels = new HashMap<String,Integer>();
        for(int i = 0; i < program.length; i++){
            if(program[i].matches(".*:")) {
                labels.put(program[i].substring(0, program[i].length() - 1), i);
            }
        }
    }
}
