59f9cad032b8b91e12000035


import java.util.*;

public class TBF {
    private final String[] lines;

    private TBF(String code) {
        lines = code.split("\n");
    }

    private enum Operation {
        SET("OI"),
        LSET("OII", "[>>[>>+<<-]<<-[>>+<<-]+>>]>[-]>[<+>-]<<<<[-<<]>>"),
        LGET("OIO", "[-[>>+<<-]+>>]>[>+<-]>[<+<+>>-]<<<<[->>[<<+>>-]<<<<]>>"),
        INC("OI"),
        DEC("OI"),
        ADD("IIO", "0[1+0-]1[2+1-]"),
        SUB("IIO", "0[1-0-]1[2+1+]"),
        MUL("IIO", "0[1[2+3+1-]3[1+3-]0-]1[-]"),
        DIVMOD("IIOO", "1[4+1-]0[3+4-[6+5]>[<]6-[2+3[4+3-]6+]0-]4[-]"),
        DIV("IIO", "1[3+1-]0[1+3-[5+4]>[<]5-[2+1[3+1-]5+]0-]1[-]3[-]"),
        MOD("IIO", "1[3+1-]0[2+3-[5+4]>[<]5-[2[3+2-]5+]0-]3[-]"),
        CMP("IIO", "1[3+1-]3[-0[2+1]>[<]0-2-[0+1+3[-]2+]3]-1[2-3+1-]3[0[2+0[-]]3+]"),
        A2B("IIIO", "0{-48}[1{10}0-]1{-48}[2{10}1-]2{-48}[3+2-]"),
        B2A("IOOO", "4{10}0[3+4-[6+5]>[<]6-[2+3[-]4{10}6+]0-]4[-]{10}2[0+2-]"
                + "0[2+4-[6+5]>[<]6-[1+2[-]4{10}6+]0-]4[-]1{48}2{48}3{48}"),
        READ("O", "0,"),
        IFEQ("II", "3+0[1-0-]1[2+1+]2[3-2[-]]3[-", "3]"),
        IFNEQ("II", "0[1-0-]1[2+1+]2[[-]", "2]"),
        WNEQ("II", "3+[-", "0[1-0-]1[2+1+]2[[-]", "3+2]3]"),
        END(),
        CALL(),
        MSG(),
        VAR(),
        PROC(),
        REM();
        final boolean[] allowConstParam; // true for VarNameOrNumber, false for VarName
        final boolean[] inputParam; // true for input parameter, false for output parameter
        final String prefixCode;
        final String code;
        final String postfixCode;

        Operation() { // special operations
            allowConstParam = new boolean[0];
            inputParam = null;
            prefixCode = null;
            code = null;
            postfixCode = null;
        }

        Operation(String paramIOstr) { // ordinary operations with optimized execution (SET, INC, DEC)
            this(paramIOstr, null, null, null);
        }

        Operation(String paramIOstr, String code) { // ordinary operations
            this(paramIOstr, null, code, null);
        }

        Operation(String paramIOstr, String code, String postfixCode) { // block operations IFEQ and IFNEQ
            this(paramIOstr, null, code, postfixCode);
        }

        Operation(String paramIOstr, String prefixCode, String code, String postfixCode) { // WNEQ
            int paramCount = paramIOstr.length();
            allowConstParam = new boolean[paramCount];
            inputParam = new boolean[paramCount];
            for (int i = 0; i < paramCount; i++)
                allowConstParam[i] = inputParam[i] = paramIOstr.charAt(i) == 'I';
            if (postfixCode != null) // IFEQ, IFNEQ, WNEQ
                allowConstParam[0] = false;
            this.prefixCode = prefixCode;
            this.code = code;
            this.postfixCode = postfixCode;
        }
    }

    private static final Map<String, Operation> strToOp = new HashMap<>(Operation.values().length);
    static {
        for (Operation op : Operation.values())
            strToOp.put(op.name(), op);
    }

    private enum TokenType {
        IDENTIFIER, NUMBER, LEFT_BRACKET, RIGHT_BRACKET, STRING_LITERAL, ILLEGAL, NONE
    }

    private static final int ASCII_SIZE = 0x80;
    private static final TokenType[] CH_TYPE = new TokenType[ASCII_SIZE];
    static {
        Arrays.fill(CH_TYPE, TokenType.ILLEGAL);
        CH_TYPE['$'] = CH_TYPE['_'] = TokenType.IDENTIFIER;
        for (char c = 'a'; c <= 'z'; c++)
            CH_TYPE[c] = TokenType.IDENTIFIER;
        for (char c = 'A'; c <= 'Z'; c++)
            CH_TYPE[c] = TokenType.IDENTIFIER;
        CH_TYPE['-'] = CH_TYPE['\''] = TokenType.NUMBER;
        for (char c = '0'; c <= '9'; c++)
            CH_TYPE[c] = TokenType.NUMBER;
        CH_TYPE['['] = TokenType.LEFT_BRACKET;
        CH_TYPE[']'] = TokenType.RIGHT_BRACKET;
        CH_TYPE['"'] = TokenType.STRING_LITERAL;
    }

    private static class VarOrNumber {
        final boolean isVarIndex; // true for a variable, false for a number or a string literal's index
        final int value; // immediate value for a number, non-negative index for a string literal,
        // non-negative index for a global variable, negative index for a procedure parameter

        VarOrNumber(int value) {
            isVarIndex = false;
            this.value = value;
        }

        VarOrNumber(boolean isGlobalVar, int index) {
            isVarIndex = true;
            value = isGlobalVar ? index : -index;
        }
    }

    private static class Statement {
        final Operation op;
        final VarOrNumber[] params;

        Statement(Operation op) {
            this.op = op;
            params = new VarOrNumber[op.allowConstParam.length];
        }

        Statement(Operation operation, VarOrNumber[] parameters) {
            op = operation;
            params = parameters;
        }
    }

    private static class Variable {
        final int size;
        int address; // in compiled program

        Variable(int size) {
            assert size >= 0 && size <= 256;
            this.size = size;
        }

        boolean isList() {
            return size > 0;
        }
    }

    private static class Procedure {
        final String name;
        final List<Variable> globalVariables;
        final Variable[] parameters;
        final List<Statement> statements = new ArrayList<>();
        int csi; // current statement index
        Procedure callerProc;

        Procedure(String name, int parameterCount, List<Variable> globalVariables) {
            this.name = name;
            this.globalVariables = globalVariables;
            parameters = new Variable[parameterCount];
        }

        Variable getVar(int index) {
            return index >= 0 ? globalVariables.get(index) : parameters[-index - 1];
        }

        Procedure call(Procedure caller, Statement callStatement) {
            if (callerProc != null) {
                StringBuilder callChain = new StringBuilder(name);
                do {
                    callChain.insert(0, caller.name + " > ");
                    caller = caller.callerProc;
                } while (caller != null);
                callChain.insert(0, "Recursive call:\n");
                throw new IllegalArgumentException(callChain.toString());
            }
            callerProc = caller;
            csi = 0;
            VarOrNumber[] callParams = callStatement.params;
            for (int i = 1, len = callParams.length; i < len; i++)
                parameters[i - 1] = caller.getVar(callParams[i].value);
            return this;
        }

        Statement nextStatement() {
            if (csi < statements.size())
                return statements.get(csi++);
            else
                return null;
        }

        Procedure returnFrom() {
            Procedure result = callerProc;
            callerProc = null;
            return result;
        }
    }

    private String line;
    private int length;
    private int index;
    private final List<Procedure> procedures = new ArrayList<>();
    private final List<String> stringLiterals = new ArrayList<>();

    private IllegalArgumentException error(String msg) {
        return new IllegalArgumentException(msg + (line == null ? "" : (", erroneous line:\n" + line)));
    }

    private IllegalArgumentException idError() {
        return error("Identifier expected");
    }

    private IllegalArgumentException argError() {
        return error("The number of arguments does not match the number of parameters");
    }

    private IllegalArgumentException listError(boolean listExpected) {
        return error(listExpected ? "Expected a list but got a variable" : "Expected a variable but got a list");
    }

    private static final String[] COMMENT_PREFIXES = { "//", "--", "#" };

    private boolean isComment() {
        for (String prefix : COMMENT_PREFIXES)
            if (line.startsWith(prefix, index))
                return true;
        return false;
    }

    private boolean findNonSpace() {
        while (index < length && Character.isWhitespace(line.charAt(index)))
            index++;
        return index < length && !isComment();
    }

    private TokenType findNextToken() {
        if (findNonSpace()) {
            char c = line.charAt(index);
            if (c < ASCII_SIZE) {
                TokenType type = CH_TYPE[c];
                if (type == TokenType.IDENTIFIER || type == TokenType.NUMBER) {
                    c = line.charAt(index - 1);
                    if (!Character.isWhitespace(c)) {
                        if (type == TokenType.IDENTIFIER && c != '"')
                            throw error("No whitespace separator before an identifier");
                        if (type == TokenType.NUMBER && c != '[')
                            throw error("No whitespace separator before a number");
                    }
                }
                return type;
            } else
                return TokenType.ILLEGAL;
        } else
            return TokenType.NONE;
    }

    private Operation getOperation() {
        int begin = index;
        String upLine = line.toUpperCase();
        if (upLine.startsWith("END", index)) {
            index += 3;
            if (findNonSpace())
                throw error("The 'end' instruction doesn't imply arguments");
            else
                index = begin + 3;
        } else if (upLine.startsWith("MSG\"", index))
            index += 3;
        else
            while (index < length && !Character.isWhitespace(upLine.charAt(index)))
                index++;
        String opStr = upLine.substring(begin, index);
        Operation result = strToOp.get(opStr);
        if (result == null)
            throw error("Unknown operation: '" + opStr + "'");
        return result;
    }

    // index must point to the first char, which should be of right type
    private String getIdentifier() {
        int begin = index;
        for (index++; index < length; index++) {
            char c = line.charAt(index);
            if (!(c < ASCII_SIZE && (CH_TYPE[c] == TokenType.IDENTIFIER || c >= '0' && c <= '9')))
                break;
        }
        return line.substring(begin, index).toLowerCase();
    }

    private String nextIdentifier(boolean mustExist) {
        switch (findNextToken()) {
            case IDENTIFIER:
                return getIdentifier();
            case NONE:
                if (mustExist)
                    throw idError();
                else
                    return null;
            default:
                throw idError();
        }
    }

    private VarOrNumber varReference(String varName, Map<String, Integer> globalVarIndices,
            Map<String, Integer> localVarIndices) {
        Integer localIndex = localVarIndices.get(varName);
        if (localIndex == null) {
            Integer globalIndex = globalVarIndices.get(varName);
            if (globalIndex == null)
                throw error("Unknown variable: " + varName);
            return new VarOrNumber(true, globalIndex);
        } else
            return new VarOrNumber(false, localIndex);
    }

    private char getCharElement(boolean inString) {
        if (index < length) {
            char c = line.charAt(index++);
            switch (c) {
                case '\\':
                    if (index < length) {
                        c = line.charAt(index++);
                        switch (c) {
                            case '\\':
                            case '\'':
                            case '"':
                                return c;
                            case 'n':
                                return '\n';
                            case 'r':
                                return '\r';
                            case 't':
                                return '\t';
                            default:
                                throw error("Illegal escape: '\\" + c + "'");
                        }
                    }
                    break;
                case '\'':
                    throw error(inString ? "Unescaped quote in string literal" : "Empty char literal");
                case '"':
                    if (inString)
                        return 0;
                    else
                        throw error("Unescaped quote in char literal");
                default:
                    return c;
            }
        }
        throw error("Unclosed " + (inString ? "string" : "char") + " literal");
    }

    // index must point to the first char
    private int getNumber() {
        int n;
        if (line.charAt(index) == '\'') {
            index++;
            n = getCharElement(false);
            if (index == length || line.charAt(index) != '\'')
                throw error("Unclosed char literal");
            index++;
        } else {
            int begin = index;
            while (++index < length) {
                char c = line.charAt(index);
                if (c < '0' || c > '9')
                    break;
            }
            n = Integer.parseInt(line.substring(begin, index));
        }
        return n & 0xff;
    }

    // index must point to the opening quote
    private String getString() {
        StringBuilder result = new StringBuilder();
        index++;
        while (true) {
            char c = getCharElement(true);
            if (c == 0)
                break;
            result.append(c);
        }
        return result.toString();
    }

    private Procedure parse() {
        List<Variable> variables = new ArrayList<>();
        Procedure root = new Procedure("", 0, variables);
        procedures.add(root);
        Map<String, Integer> procIndices = new HashMap<>();
        procIndices.put("", 0);
        Map<String, Integer> globalVarIndices = new HashMap<>(); // maps to indices in the `variables` list
        Map<String, Integer> localVarIndices = new HashMap<>(); // maps to virtual indices (procedure parameters)
        Procedure currentProc = root;
        Deque<Boolean> blockStack = new ArrayDeque<>();
        for (int li = 0, lineCount = lines.length; li < lineCount; li++) {
            line = lines[li];
            length = line.length();
            index = 0;
            if (!findNonSpace())
                continue;
            Operation op = getOperation();
            Statement statement = null;
            int paramCount = op.allowConstParam.length;
            if (paramCount == 0) // special operations
                switch (op) {
                    case VAR:
                        if (currentProc != root)
                            throw error("Variable declaration inside a procedure block");
                        String varName = nextIdentifier(true);
                        do {
                            if (globalVarIndices.put(varName, variables.size()) != null)
                                throw error("Duplicate variable: '" + varName + "'");
                            int varSize = 0;
                            switch (findNextToken()) {
                                case IDENTIFIER:
                                    varName = getIdentifier();
                                    break;
                                case NONE:
                                    varName = null;
                                    break;
                                case LEFT_BRACKET:
                                    index++;
                                    if (findNextToken() != TokenType.NUMBER)
                                        throw error("Number expected for list size");
                                    varSize = getNumber();
                                    if (varSize == 0)
                                        varSize = 256;
                                    if (findNextToken() != TokenType.RIGHT_BRACKET)
                                        throw error("']' expected");
                                    index++;
                                    varName = nextIdentifier(false);
                                    break;
                                default:
                                    throw idError();
                            }
                            variables.add(new Variable(varSize));
                        } while (varName != null);
                        break;
                    case PROC:
                        if (currentProc != root)
                            throw error("Nested procedure");
                        String procName = nextIdentifier(true);
                        while (true) {
                            String paramName = nextIdentifier(false);
                            if (paramName == null)
                                break;
                            if (localVarIndices.put(paramName, ++paramCount) != null)
                                throw error("Duplicate parameter name: '" + paramName + "'");
                        }
                        Integer procIndex = procIndices.get(procName);
                        if (procIndex == null) {
                            currentProc = new Procedure(procName, paramCount, variables);
                            procIndices.put(procName, procedures.size());
                            procedures.add(currentProc);
                        } else {
                            currentProc = procedures.get(procIndex);
                            if (currentProc.csi == 0)
                                throw error("Duplicate procedure name: '" + procName + "'");
                            currentProc.csi = 0;
                            if (currentProc.parameters.length != paramCount)
                                throw argError();
                        }
                        blockStack.push(true);
                        break;
                    case END:
                        if (blockStack.isEmpty())
                            throw error("'end' before beginning a block");
                        if (blockStack.pop() == true) { // end of a procedure
                            localVarIndices.clear();
                            currentProc = root;
                        } else // end of a conditional block
                            statement = new Statement(op, null);
                        break;
                    case CALL:
                        procName = nextIdentifier(true);
                        procIndex = procIndices.get(procName);
                        boolean forwardDefinition = procIndex == null;
                        if (forwardDefinition) {
                            procIndex = procedures.size();
                            procIndices.put(procName, procIndex);
                        }
                        List<VarOrNumber> params = new ArrayList<>();
                        params.add(new VarOrNumber(true, procIndex));
                        while (true) {
                            varName = nextIdentifier(false);
                            if (varName == null)
                                break;
                            params.add(varReference(varName, globalVarIndices, localVarIndices));
                        }
                        paramCount = params.size();
                        statement = new Statement(op, params.toArray(new VarOrNumber[paramCount--]));
                        if (forwardDefinition) {
                            Procedure called = new Procedure(procName, paramCount, variables);
                            called.csi--;
                            procedures.add(called);
                        } else if (procedures.get(procIndex).parameters.length != paramCount)
                            throw argError();
                        break;
                    case MSG:
                        params = new ArrayList<>();
                        loop:
                        while (true)
                            switch (findNextToken()) {
                                case IDENTIFIER:
                                    params.add(varReference(getIdentifier(), globalVarIndices, localVarIndices));
                                    break;
                                case STRING_LITERAL:
                                    params.add(new VarOrNumber(stringLiterals.size()));
                                    stringLiterals.add(getString());
                                    break;
                                case NONE:
                                    break loop;
                                default:
                                    throw error("Identifier or string literal expected");
                            }
                        if (params.isEmpty())
                            throw error("'msg' instruction without arguments");
                        statement = new Statement(op, params.toArray(new VarOrNumber[params.size()]));
                        break;
                    case REM:
                        break;
                    default:
                        throw new RuntimeException("Shouldn't reach here");
                }
            else {
                statement = new Statement(op);
                boolean[] allowConstParam = op.allowConstParam;
                for (int i = 0; i < paramCount; i++) {
                    VarOrNumber param;
                    switch (findNextToken()) {
                        case IDENTIFIER:
                            param = varReference(getIdentifier(), globalVarIndices, localVarIndices);
                            break;
                        case NUMBER:
                            if (allowConstParam[i]) {
                                param = new VarOrNumber(getNumber());
                                break;
                            }
                            //$FALL-THROUGH$
                        default:
                            throw error("Identifier" + (allowConstParam[i] ? " or number" : "") + " expected");
                    }
                    statement.params[i] = param;
                }
                if (findNonSpace())
                    throw error("Too many arguments");
                if (op.postfixCode != null)
                    blockStack.push(false);
            }
            if (statement != null)
                currentProc.statements.add(statement);
        }
        line = null;
        if (!blockStack.isEmpty())
            throw error("Unclosed block");
        for (Procedure proc : procedures)
            if (proc.csi != 0)
                throw error("Undefined procedure: '" + proc.name + "'");
        return root;
    }

    private static final int TEMP_VAR_COUNT = 10;
    private final StringBuilder codeBuilder = new StringBuilder();
    private int dataPtr;

    private void goTo(int newPtr) {
        if (newPtr != dataPtr)
            if (dataPtr < newPtr)
                do
                    codeBuilder.append('>');
                while (++dataPtr < newPtr);
            else
                do
                    codeBuilder.append('<');
                while (--dataPtr > newPtr);
    }

    private void addConst(int value) {
        if (value != 0)
            if (value > 0)
                do
                    codeBuilder.append('+');
                while (--value > 0);
            else
                do
                    codeBuilder.append('-');
                while (++value < 0);
    }

    private void apply(String code) {
        for (int i = 0, len = code.length(); i < len; i++) {
            char c = code.charAt(i);
            if (c >= '0' && c <= '9')
                goTo(c - '0');
            else if (c == '{') {
                int j = i + 1;
                i = code.indexOf('}', j);
                addConst(Integer.parseInt(code.substring(j, i)));
            } else
                codeBuilder.append(c);
        }
    }

    private void move(int srcPtr, int destPtr, boolean clearDest) {
        assert srcPtr != destPtr;
        if (clearDest) {
            goTo(destPtr);
            codeBuilder.append("[-]");
        }
        goTo(srcPtr);
        codeBuilder.append('[');
        goTo(destPtr);
        codeBuilder.append('+');
        goTo(srcPtr);
        codeBuilder.append("-]");
    }

    private void copy(Variable srcVar, int destPtr) { // destPtr must refer to a temporary variable
        destPtr++;
        assert destPtr < TEMP_VAR_COUNT;
        int vPtr = srcVar.address;
        move(vPtr, destPtr, false);
        goTo(destPtr);
        codeBuilder.append('[');
        goTo(destPtr - 1);
        codeBuilder.append('+');
        goTo(vPtr);
        codeBuilder.append('+');
        goTo(destPtr);
        codeBuilder.append("-]");
    }

    private void loadStore(Statement stat, Procedure proc, boolean load) {
        VarOrNumber[] params = stat.params;
        boolean[] inputParam = stat.op.inputParam;
        for (int i = 0, len = params.length; i < len; i++)
            if (load == inputParam[i]) {
                VarOrNumber vn = params[i];
                if (vn.isVarIndex) {
                    Variable v = proc.getVar(vn.value);
                    if (v.isList())
                        throw listError(false);
                    if (load)
                        copy(v, i);
                    else
                        move(i, v.address, true);
                } else {
                    assert load;
                    goTo(i);
                    addConst(vn.value);
                }
            }
    }

    private int getVarAddr(Statement stat, int paramIndex, Procedure proc, boolean list) {
        VarOrNumber vn = stat.params[paramIndex];
        assert vn.isVarIndex;
        Variable v = proc.getVar(vn.value);
        if (v.isList() != list)
            throw listError(list);
        return v.address;
    }

    private String compile(Procedure proc) {
        List<Variable> lists = new ArrayList<>();
        dataPtr = TEMP_VAR_COUNT;
        for (Variable v : proc.globalVariables)
            if (v.isList())
                lists.add(v);
            else
                v.address = dataPtr++;
        dataPtr += 2; // for each list, we need an empty cell at its address - 2
        for (Variable v : lists) {
            // The cell at v.address and addresses of the same parity are auxiliary cells
            // (empty when no list operation is conducted). The cell at v.address + 1 holds
            // the first element of the list, at v.address + 3 holds the second and so on.
            v.address = dataPtr;
            dataPtr += 2 * v.size;
        }
        dataPtr = 0;
        Deque<String> blockStack = new ArrayDeque<>();
        while (true) {
            Statement stat = proc.nextStatement();
            if (stat == null) {
                proc = proc.returnFrom();
                if (proc == null)
                    break;
                else
                    continue;
            }
            Operation op = stat.op;
            if (op.inputParam != null) {
                if (op.prefixCode != null)
                    apply(op.prefixCode);
                loadStore(stat, proc, true);
            }
            switch (op) {
                case CALL:
                    proc = procedures.get(stat.params[0].value).call(proc, stat);
                    break;
                case MSG:
                    char c0 = 0;
                    for (VarOrNumber vn : stat.params)
                        if (vn.isVarIndex) {
                            goTo(proc.getVar(vn.value).address);
                            codeBuilder.append('.');
                        } else {
                            String s = stringLiterals.get(vn.value);
                            goTo(0);
                            for (int i = 0, len = s.length(); i < len; i++) {
                                char c = s.charAt(i);
                                addConst(c - c0);
                                codeBuilder.append('.');
                                c0 = c;
                            }
                        }
                    if (c0 != 0) {
                        goTo(0);
                        codeBuilder.append("[-]");
                    }
                    break;
                case SET:
                    move(1, getVarAddr(stat, 0, proc, false), true);
                    break;
                case INC:
                    move(1, getVarAddr(stat, 0, proc, false), false);
                    break;
                case DEC:
                    int destPtr = getVarAddr(stat, 0, proc, false);
                    goTo(1);
                    codeBuilder.append('[');
                    goTo(destPtr);
                    codeBuilder.append('-');
                    goTo(1);
                    codeBuilder.append("-]");
                    break;
                case LSET:
                    int listPtr = getVarAddr(stat, 0, proc, true);
                    move(1, listPtr, false);
                    move(2, listPtr + 2, false);
                    goTo(listPtr);
                    apply(op.code);
                    break;
                case LGET:
                    listPtr = getVarAddr(stat, 0, proc, true);
                    move(1, listPtr, false);
                    goTo(listPtr);
                    apply(op.code);
                    move(listPtr, getVarAddr(stat, 2, proc, false), true);
                    break;
                case END:
                    apply(blockStack.pop());
                    break;
                default:
                    apply(op.code);
                    loadStore(stat, proc, false);
                    if (op.postfixCode != null)
                        blockStack.push(op.postfixCode);
                    break;
            }
        }
        return codeBuilder.toString();
    }

    private String ataksihtkcuf() {
        return compile(parse());
    }

    public static String kcuf(String code) {
        return new TBF(code).ataksihtkcuf();
    }
  
################################
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Map;
import java.util.HashMap;
import java.util.Deque;
import java.util.ArrayDeque;
import java.util.Set;
import java.util.HashSet;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.stream.Collectors;

public class TBF {
  
  public static String kcuf(String code) {
    Tokenizer tokenizer = new Tokenizer();
    List<Token> tokens = tokenizer.tokenize(code);
    
    Parser parser = new Parser(tokens);
    List<Statement> statements = parser.parse();
    
    Program program = new Program(statements);
    String result = program.toString();
    return result;
  }
  
  
  /*
   *  TRANSPILATION
   */
  
  private interface BFOperator {
    
    String toString();
  }
  
  private enum BFSingleOperator implements BFOperator {
    INC("+"),
    DEC("-"),
    PTR_INC(">"),
    PTR_DEC("<"),
    JUMP("["),
    JUMP_BACK("]"),
    READ(","),
    WRITE(".");
    
    private final String symbol;
    
    private BFSingleOperator(String symbol) {
      this.symbol = symbol;
    }
    
    @Override
    public String toString() {
      return symbol;
    }
  }
  
  private static class BFRepeatedOperator implements BFOperator {
    
    private final BFOperator operator;
    private final int times;
    
    public BFRepeatedOperator(BFOperator operator, int times) {
      this.operator = operator;
      this.times = times;
    }
    
    @Override
    public String toString() {
      return operator.toString().repeat(times);
    }
  }
  
  private static abstract class AllocatedValue {
    
    protected int address;
    
    public AllocatedValue(int address) {
      this.address = address;
    }
    
    public Integer getAddress() {
      return address;
    }
    
    public abstract String toString();
  }
  
  private static class VariableValue extends AllocatedValue {
    
    public VariableValue(int address) {
      super(address);
    }
    
    @Override
    public String toString() {
      return String.format("Variable(%d)", address);
    }
  }
  
  private static class ListValue extends AllocatedValue {
    
    private final int size;
    
    public final static int CELL_SIZE = 2;
    public final static int CELLS_BEFORE = 3;
    
    public ListValue(int address, int size) {
      super(address);
      this.size = size;
    }
    
    public int getSize() {
      return size;
    }
    
    @Override
    public String toString() {
      return String.format("List(%d)", address);
    }
  }
  
  private static class Allocator {
    
    private int index = 0;
    
    public VariableValue allocateVariable() {
      return new VariableValue(index++);
    }
    
    public List<VariableValue> allocateVariables(int n) {
      List<VariableValue> list = new ArrayList<VariableValue>(n);
      for (int i = 0; i < n; ++i)
        list.add(new VariableValue(index++));
      return list;
    }
    
    public ListValue allocateList(int size) {
      ListValue list = new ListValue(index, size);
      index += size * ListValue.CELL_SIZE + ListValue.CELLS_BEFORE;
      return list;
    }
  }
  
  private static class Procedure {
    
    private final List<String> parameterNames = new ArrayList<>();
    private final List<Statement> statements = new ArrayList<>();
    
    public List<String> getParameterNames() {
      return parameterNames;
    }
    
    public List<Statement> getStatements() {
      return statements;
    }
    
    public void addParameterName(String parameterName) {
      if (parameterNames.contains(parameterName))
        throw new RuntimeException("Duplicate parrameter names");
      parameterNames.add(parameterName);
    }
    
    public void addStatement(Statement statement) {
      statements.add(statement);
    }
  }
  
  private static class Program {
    
    private final Allocator allocator;
    private final Map<String, AllocatedValue> globalScope;
    private final Map<String, Procedure> procedures;
    private final Deque<Runnable> endCallbacks;
    private final Set<String> calledProcedures;
    
    private int pointer;
    
    private final List<VariableValue> REGISTERS;
    private final VariableValue COPY_BUFFER;
    private final VariableValue ADD_RESULT;
    private final VariableValue SUB_RESULT;
    private final VariableValue MUL_RESULT;
    private final VariableValue MUL_COUNTER;
    private final List<VariableValue> DIV_REGISTERS;
    private final VariableValue DIV_RESULT;
    private final VariableValue MOD_RESULT;
    private final List<VariableValue> CMP_REGISTERS;
    private final VariableValue CMP_RESULT;
    private final VariableValue A2B_RESULT;
    private final List<VariableValue> B2A_RESULT;
    private final VariableValue REG_A;
    private final VariableValue REG_B;
    private final VariableValue REG_C;
    private final VariableValue NUMBER_48;
    private final VariableValue NUMBER_10;
    
    private final List<BFOperator> brainfuck;
    
    public Program(List<Statement> statements) {
      this.allocator = new Allocator();
      this.globalScope = new HashMap<>();
      this.procedures = new HashMap<>();
      this.endCallbacks = new ArrayDeque<>();
      this.calledProcedures = new HashSet<>();
      this.pointer = 0;
      this.brainfuck = new ArrayList<>();
      
      this.REGISTERS = allocator.allocateVariables(10);
      this.COPY_BUFFER = new VariableValue(REGISTERS.get(0).getAddress());
      this.ADD_RESULT = new VariableValue(REGISTERS.get(1).getAddress());
      this.SUB_RESULT = new VariableValue(REGISTERS.get(1).getAddress());
      this.MUL_RESULT = new VariableValue(REGISTERS.get(1).getAddress());
      this.MUL_COUNTER = new VariableValue(REGISTERS.get(2).getAddress());
      this.DIV_REGISTERS = REGISTERS.subList(1, 7);
      this.DIV_RESULT = new VariableValue(DIV_REGISTERS.get(5).getAddress());
      this.MOD_RESULT = new VariableValue(DIV_REGISTERS.get(1).getAddress());
      this.CMP_REGISTERS = REGISTERS.subList(1, 9);
      this.CMP_RESULT = new VariableValue(CMP_REGISTERS.get(4).getAddress());
      this.A2B_RESULT = new VariableValue(REGISTERS.get(7).getAddress());
      this.B2A_RESULT = REGISTERS.subList(7, 10);
      this.REG_A = allocator.allocateVariable();
      this.REG_B = allocator.allocateVariable();
      this.REG_C = allocator.allocateVariable();
      this.NUMBER_48 = allocator.allocateVariable();
      this.NUMBER_10 = allocator.allocateVariable();
      
      List<Statement> statementsCopy = new LinkedList<>(statements);
      loadProcedures(statementsCopy);
      
      for (Statement statement : statementsCopy) {
        handleStatement(statement, globalScope);
      }
    }
    
    public String toString() {
      return brainfuck.stream().map(op -> op.toString()).collect(Collectors.joining(""));
    }
    
    private void loadProcedures(List<Statement> statements) {
      for (int i = 0; i < statements.size(); ++i) {
        Statement statement = statements.get(i);
        if (statement instanceof ProcStatement) {
          Procedure procedure = new Procedure();
          String procName = ((ProcStatement)statement).getName().getName();
          if (procedures.containsKey(procName))
            throw new RuntimeException("Duplicated proc name");
          procedures.put(procName, procedure);
          for (ProcedureParameterOperand param : ((ProcStatement)statement).getParameters()) {
            procedure.addParameterName(param.getName());
          }
          statements.remove(i);
          
          int depth = 1;
          while (i < statements.size() && depth > 0) {
            statement = statements.get(i);
            if (statement instanceof ProcStatement)
              throw new RuntimeException("Proc in proc");
            if (statement instanceof VarStatement)
              throw new RuntimeException("Var in proc");
            if (statement instanceof CallStatement && 
                ((CallStatement)statement).getName().getName().equals(procName))
              throw new RuntimeException("Recursion");
            
            if (statement instanceof BlockStatement) {
              ++depth;
            } else if (statement == ConstStatement.END) {
              --depth;
            }
            if (depth != 0)
              procedure.addStatement(statement);
            statements.remove(i);
          }
          if (depth != 0)
            throw new RuntimeException("No end after proc");
          --i;
        }
      }
    }
    
    private void handleStatement(Statement statement, Map<String, AllocatedValue> scope) {
      if (statement instanceof VarStatement) {
        handleVarStatement((VarStatement)statement);
      } else if (statement instanceof SetStatement) {
        handleSetStatement((SetStatement)statement, scope);
      } else if (statement instanceof IncStatement) {
        handleIncStatement((IncStatement)statement, scope);
      } else if (statement instanceof DecStatement) {
        handleDecStatement((DecStatement)statement, scope);
      } else if (statement instanceof AddStatement) {
        handleAddStatement((AddStatement)statement, scope);
      } else if (statement instanceof SubStatement) {
        handleSubStatement((SubStatement)statement, scope);
      } else if (statement instanceof MulStatement) {
        handleMulStatement((MulStatement)statement, scope);
      } else if (statement instanceof DivModStatement) {
        handleDivModStatement((DivModStatement)statement, scope);
      } else if (statement instanceof DivStatement) {
        handleDivStatement((DivStatement)statement, scope);
      } else if (statement instanceof ModStatement) {
        handleModStatement((ModStatement)statement, scope);
      } else if (statement instanceof CmpStatement) {
        handleCmpStatement((CmpStatement)statement, scope);
      } else if (statement instanceof A2BStatement) {
        handleA2BStatement((A2BStatement)statement, scope);
      } else if (statement instanceof B2AStatement) {
        handleB2AStatement((B2AStatement)statement, scope);
      } else if (statement instanceof LSetStatement) {
        handleLSetStatement((LSetStatement)statement, scope);
      } else if (statement instanceof LGetStatement) {
        handleLGetStatement((LGetStatement)statement, scope);
      } else if (statement instanceof IfeqStatement) {
        handleIfeqStatement((IfeqStatement)statement, scope);
      } else if (statement instanceof IfneqStatement) {
        handleIfneqStatement((IfneqStatement)statement, scope);
      } else if (statement instanceof WneqStatement) {
        handleWneqStatement((WneqStatement)statement, scope);
      } else if (statement == ConstStatement.END) {
        handleEndStatement();
      } else if (statement instanceof CallStatement) {
        handleCallStatement((CallStatement)statement, scope);
      } else if (statement instanceof ReadStatement) {
        handleReadStatement((ReadStatement)statement, scope);
      } else if (statement instanceof MsgStatement) {
        handleMsgStatement((MsgStatement)statement, scope);
      } else {
        throw new RuntimeException("Illegal statement");
      }
    }
    
    private void handleVarStatement(VarStatement statement) {
      for (NameOperand operand : statement.getVariables()) {
        if (globalScope.containsKey(operand.getName()))
          throw new RuntimeException("Name already defined");
        
        if (operand instanceof VarNameOperand) {
          globalScope.put(operand.getName(), allocator.allocateVariable());
        } else {
          ListNameOperand list = (ListNameOperand)operand;
          globalScope.put(list.getName(), allocator.allocateList(list.getSize()));
        }
      }
    }
    
    private void handleSetStatement(SetStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getA().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      
      if (statement.getB() instanceof NumberOperand) {
        int value = ((NumberOperand)statement.getB()).getValue();
        setValue(target, value);
      } else {
        String sourceName = ((NameOperand)statement.getB()).getName();
        VariableValue source = (VariableValue)scope.get(sourceName);
        copyValue(source, target);
      }
      movePointerTo(target);
    }
    
    private void handleIncStatement(IncStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getA().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      
      if (statement.getB() instanceof NumberOperand) {
        int value = ((NumberOperand)statement.getB()).getValue();
        movePointerTo(target);
        addInc(value);
      } else {
        String sourceName = ((NameOperand)statement.getA()).getName();
        VariableValue source = (VariableValue)scope.get(sourceName);
        incByValue(source.getAddress(), target.getAddress());
      }
    }
    
    private void handleDecStatement(DecStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getA().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      
      if (statement.getB() instanceof NumberOperand) {
        int value = ((NumberOperand)statement.getB()).getValue();
        movePointerTo(target);
        addDec(value);
      } else {
        String sourceName = ((NameOperand)statement.getA()).getName();
        VariableValue source = (VariableValue)scope.get(sourceName);
        decByValue(source.getAddress(), target.getAddress());
      }
    }
    
    private void handleAddStatement(AddStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      add(a, b);
      copyValue(ADD_RESULT, target);
    }
    
    private void handleSubStatement(SubStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      sub(a, b);
      copyValue(SUB_RESULT, target);
    }
    
    private void handleMulStatement(MulStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      mul(a, b);
      copyValue(MUL_RESULT, target);
    }
    
    private void handleDivModStatement(DivModStatement statement, Map<String, AllocatedValue> scope) {
      String cName = statement.getC().getName();
      VariableValue c = (VariableValue)scope.get(cName);
      String dName = statement.getD().getName();
      VariableValue d = (VariableValue)scope.get(dName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      divmod(a, b);
      copyValue(DIV_RESULT, c);
      copyValue(MOD_RESULT, d);
    }
    
    private void handleDivStatement(DivStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      divmod(a, b);
      copyValue(DIV_RESULT, target);
    }
    
    private void handleModStatement(ModStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      divmod(a, b);
      copyValue(MOD_RESULT, target);
    }
    
    private void handleCmpStatement(CmpStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getC().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      cmp(a, b);
      copyValue(CMP_RESULT, target);
    }
    
    private void handleA2BStatement(A2BStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getD().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      VariableValue a;
      VariableValue b;
      VariableValue c;
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      if (statement.getB() instanceof NumberOperand) {
        c = REG_C;
        setValue(c, ((NumberOperand)statement.getC()).getValue());
      } else {
        c = (VariableValue)scope.get(((NameOperand)statement.getC()).getName());
      }
      
      a2b(a.getAddress(), b.getAddress(), c.getAddress());
      copyValue(A2B_RESULT, target);
    }
    
    private void handleB2AStatement(B2AStatement statement, Map<String, AllocatedValue> scope) {
      String bName = statement.getB().getName();
      String cName = statement.getC().getName();
      String dName = statement.getD().getName();
      VariableValue a;
      VariableValue b = (VariableValue)scope.get(bName);
      VariableValue c = (VariableValue)scope.get(cName);
      VariableValue d = (VariableValue)scope.get(dName);
      
      if (statement.getA() instanceof NumberOperand) {
        a = REG_A;
        setValue(a, ((NumberOperand)statement.getA()).getValue());
      } else {
        a = (VariableValue)scope.get(((NameOperand)statement.getA()).getName());
      }
       
      b2a(a.getAddress());
      copyValue(B2A_RESULT.get(0).getAddress(), b.getAddress());
      copyValue(B2A_RESULT.get(1).getAddress(), c.getAddress());
      copyValue(B2A_RESULT.get(2).getAddress(), d.getAddress());
    }
    
    private void handleLSetStatement(LSetStatement statement, Map<String, AllocatedValue> scope) {
      String aName = statement.getA().getName();
      ListValue a = (ListValue)scope.get(aName);
      VariableValue b;
      VariableValue c;
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
      
      if (statement.getC() instanceof NumberOperand) {
        c = REG_C;
        setValue(c, ((NumberOperand)statement.getC()).getValue());
      } else {
        c = (VariableValue)scope.get(((NameOperand)statement.getC()).getName());
      }
       
      lset(a.getAddress(), b.getAddress(), c.getAddress());
    }
    
    private void handleLGetStatement(LGetStatement statement, Map<String, AllocatedValue> scope) {
      String aName = statement.getA().getName();
      String cName = statement.getC().getName();
      ListValue a = (ListValue)scope.get(aName);
      VariableValue b;
      VariableValue c = (VariableValue)scope.get(cName);
      
      if (statement.getB() instanceof NumberOperand) {
        b = REG_B;
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
       
      lget(a.getAddress(), b.getAddress(), c.getAddress());
    }
    
    private void handleIfeqStatement(IfeqStatement statement, Map<String, AllocatedValue> scope) {
      String aName = statement.getA().getName();
      VariableValue a = (VariableValue)scope.get(aName);
      VariableValue b;
      
      if (statement.getB() instanceof NumberOperand) {
        b = allocator.allocateVariable();
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
       
      ifeq(a.getAddress(), b.getAddress());
    }
    
    private void handleIfneqStatement(IfneqStatement statement, Map<String, AllocatedValue> scope) {
      String aName = statement.getA().getName();
      VariableValue a = (VariableValue)scope.get(aName);
      VariableValue b;
      
      if (statement.getB() instanceof NumberOperand) {
        b = allocator.allocateVariable();
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
       
      ifneq(a.getAddress(), b.getAddress());
    }
    
    private void handleWneqStatement(WneqStatement statement, Map<String, AllocatedValue> scope) {
      String aName = statement.getA().getName();
      VariableValue a = (VariableValue)scope.get(aName);
      VariableValue b;
      
      if (statement.getB() instanceof NumberOperand) {
        b = allocator.allocateVariable();
        setValue(b, ((NumberOperand)statement.getB()).getValue());
      } else {
        b = (VariableValue)scope.get(((NameOperand)statement.getB()).getName());
      }
       
      wneq(a.getAddress(), b.getAddress());
    }
    
    private void handleEndStatement() {
      endCallbacks.pop().run();
    }
    
    private void handleCallStatement(CallStatement statement, Map<String, AllocatedValue> scope) {
      String procName = statement.getName().getName();
      if (calledProcedures.contains(procName))
        throw new RuntimeException("Recursion");
      calledProcedures.add(procName);
      
      Procedure procedure = procedures.get(procName);
      
      if (statement.getParameters().size() != procedure.getParameterNames().size())
        throw new RuntimeException("Invalid call");
        
      List<VariableValue> callParams = statement.getParameters().stream()
        .map(p -> (VariableValue)scope.get(p.getName()))
        .collect(Collectors.toList());
      List<String> paramNames = procedure.getParameterNames();
      Map<String, AllocatedValue> newScope = new HashMap<>(scope);
      for (int i = 0; i < paramNames.size(); ++i) {
        newScope.put(paramNames.get(i), callParams.get(i));
      }
      for (Statement substatement : procedure.getStatements()) {
        handleStatement(substatement, newScope);
      }
      
      calledProcedures.remove(procName);
    }
    
    private void handleReadStatement(ReadStatement statement, Map<String, AllocatedValue> scope) {
      String targetName = statement.getA().getName();
      VariableValue target = (VariableValue)scope.get(targetName);
      
      movePointerTo(target);
      addRead(1);
    }
    
    private void handleMsgStatement(MsgStatement statement, Map<String, AllocatedValue> scope) {
      for (Operand operand : statement.getOperands()) {
        if (operand instanceof VarNameOperand) {
          String sourceName = ((NameOperand)operand).getName();
          VariableValue source = (VariableValue)scope.get(sourceName);
          movePointerTo(source);
          addWrite(1);
        } else {
          String literal = ((StringOperand)operand).getValue();
          movePointerTo(COPY_BUFFER);
          literal.chars().forEach(c -> {
            setZero();
            addInc(c);
            addWrite(1);
          });
        }
      }
    }
    
    private void add(int addressA, int addressB) {
        movePointerTo(ADD_RESULT);
        setZero();
        incByValue(addressA, ADD_RESULT.getAddress());
        incByValue(addressB, ADD_RESULT.getAddress());
    }
    
    private void add(VariableValue a, VariableValue b) {
      add(a.getAddress(), b.getAddress());
    }
    
    private void sub(int addressA, int addressB) {
      movePointerTo(SUB_RESULT);
      setZero();
      incByValue(addressA, SUB_RESULT.getAddress());
      decByValue(addressB, SUB_RESULT.getAddress());
    }
    
    private void sub(VariableValue a, VariableValue b) {
      sub(a.getAddress(), b.getAddress());
    }
    
    private void mul(int addressA, int addressB) {
      movePointerTo(MUL_RESULT);
      setZero();
      copyValue(addressA, MUL_COUNTER.getAddress());
      
      movePointerTo(MUL_COUNTER);
      addJump(1);
      incByValue(addressB, MUL_RESULT.getAddress());
      movePointerTo(MUL_COUNTER);
      addDec(1);
      addJumpBack(1);
    }
    
    private void mul(VariableValue a, VariableValue b) {
      mul(a.getAddress(), b.getAddress());
    }
    
    private void divmod(int addressA, int addressB) {
      copyValue(addressA, DIV_REGISTERS.get(0).getAddress());
      movePointerTo(DIV_REGISTERS.get(1));
      setZero();
      movePointerTo(DIV_REGISTERS.get(2));
      setZero();
      movePointerTo(DIV_REGISTERS.get(3));
      setZero();
      copyValue(addressB, DIV_REGISTERS.get(4).getAddress());
      movePointerTo(DIV_REGISTERS.get(5));
      setZero();
      movePointerTo(DIV_REGISTERS.get(0));
      
      addJump(1);
        addDec(1);
        addPtrInc(1);
        addInc(1);
        addPtrInc(2);
        addInc(1);
        addPtrInc(1);
        addDec(1);
        
        addJump(1);
          addPtrDec(1);
          addDec(1);
        addJumpBack(1);
        addPtrDec(1);
        addJump(1);
          addPtrDec(2);
          addJump(1);
            addDec(1);
            addPtrInc(3);
            addInc(1);
            addPtrDec(3);
          addJumpBack(1);
          addPtrInc(4);
          addInc(1);
          addPtrDec(2);
          addDec(1);
          addPtrDec(1);
        addJumpBack(1);
        addPtrDec(2);
      addJumpBack(1);
    }
    
    private void divmod(VariableValue a, VariableValue b) {
      divmod(a.getAddress(), b.getAddress());
    }
    
    private void cmp(int addressA, int addressB) {
      movePointerTo(CMP_REGISTERS.get(0));
      setZero();
      copyValue(addressA, CMP_REGISTERS.get(1).getAddress());
      copyValue(addressB, CMP_REGISTERS.get(2).getAddress());
      for (int i = 3; i < 8; ++i) {
        movePointerTo(CMP_REGISTERS.get(i).getAddress());
        setZero();
      }
      movePointerTo(CMP_REGISTERS.get(2));
      
      addJump(1);
        addPtrDec(1);
        addJump(1);
          addDec(1);
          addPtrInc(1);
        addJumpBack(1);
        addPtrDec(1);
      addJumpBack(1);
      addPtrInc(2);
      addJump(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrDec(1);
      addInc(1);
      addPtrDec(2);
      addJump(1);
        addPtrInc(3);
        addInc(1);
        addPtrInc(1);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(2);
        addDec(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(4);
      addJumpBack(1);
      
      pointer = CMP_REGISTERS.get(7).getAddress();
    }
    
    private void cmp(VariableValue a, VariableValue b) {
      cmp(a.getAddress(), b.getAddress());
    }
    
    private void a2b(int addressA, int addressB, int addressC) {
      movePointerTo(A2B_RESULT);
      setZero();
      setValue(NUMBER_48, 48);
      
      sub(addressA, NUMBER_48.getAddress());
      for (int i = 0; i < 100; ++i)
        incByValue(SUB_RESULT, A2B_RESULT);
      sub(addressB, NUMBER_48.getAddress());
      for (int i = 0; i < 10; ++i)
        incByValue(SUB_RESULT, A2B_RESULT);
      sub(addressC, NUMBER_48.getAddress());
      incByValue(SUB_RESULT, A2B_RESULT);
    }
    
    private void b2a(int addressA) {
      for (int i = 0; i < 3; ++i) {
        movePointerTo(B2A_RESULT.get(i));
        setZero();
      }
      setValue(NUMBER_48, 48);
      setValue(NUMBER_10, 10);
      
      divmod(addressA, NUMBER_10.getAddress());
      copyValue(MOD_RESULT, B2A_RESULT.get(2));
      copyValue(DIV_RESULT, B2A_RESULT.get(1));
      
      add(NUMBER_48, B2A_RESULT.get(2));
      copyValue(ADD_RESULT, B2A_RESULT.get(2));
      
      divmod(B2A_RESULT.get(1), NUMBER_10);
      copyValue(MOD_RESULT, B2A_RESULT.get(1));
      copyValue(DIV_RESULT, B2A_RESULT.get(0));
      
      add(NUMBER_48, B2A_RESULT.get(1));
      copyValue(ADD_RESULT, B2A_RESULT.get(1));
      
      add(NUMBER_48, B2A_RESULT.get(0));
      copyValue(ADD_RESULT, B2A_RESULT.get(0));
    }
    
    private void lset(int addressA, int addressB, int addressC) {
      copyValue(addressB, addressA + 2);
      copyValue(addressC, addressA + 1);
      movePointerTo(addressA);
      
      addPtrInc(2);
      addJump(1);
        addJump(1);
          addPtrInc(2);
        addJumpBack(1);
        addInc(1);
        addJump(1);
          addPtrDec(2);
        addJumpBack(1);
        addPtrInc(2);
        addDec(1);
      addJumpBack(1);
      addInc(1);
      addJump(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrDec(1);
      addJump(1);
        addDec(1);
      addJumpBack(1);
      addPtrDec(1);
      addJump(1);
        addPtrDec(2);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(1);
        addJump(1);
          addPtrInc(2);
        addJumpBack(1);
        addPtrDec(1);
        addInc(1);
        addPtrDec(1);
        addJump(1);
          addPtrDec(2);
        addJumpBack(1);
        addPtrInc(1);
        addDec(1);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrDec(2);
      addJump(1);
        addDec(1);
        addPtrDec(2);
      addJumpBack(1);
    }
    
    private void lget(int addressA, int addressB, int addressC) {
      movePointerTo(addressC);
      setZero();
      movePointerTo(addressA + 1);
      setZero();
      copyValue(addressB, addressA + 2);
      movePointerTo(addressA);
      
      addPtrInc(2);
      addJump(1);
        addJump(1);
          addPtrInc(2);
        addJumpBack(1);
        addInc(1);
        addJump(1);
          addPtrDec(2);
        addJumpBack(1);
        addPtrInc(2);
        addDec(1);
      addJumpBack(1);
      addInc(1);
      addJump(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrDec(1);
      addJump(1);
        addPtrDec(1);
        addJump(1);
          addPtrDec(2);
        addJumpBack(1);
        addPtrInc(1);
        addInc(1);
        addPtrDec(1);
        movePointerTo(addressC);
        addInc(1);
        movePointerTo(addressA);
        addPtrInc(2);
        addJump(1);
          addPtrInc(2);
        addJumpBack(1);
        addPtrDec(1);
        addDec(1);
      addJumpBack(1);
      addPtrDec(1);
      addJump(1);
        addPtrDec(2);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(1);
        addJump(1);
          addPtrInc(2);
        addJumpBack(1);
        addPtrDec(1);
        addInc(1);
        addPtrDec(1);
        addJump(1);
          addPtrDec(2);
        addJumpBack(1);
        addPtrInc(1);
        addDec(1);
      addJumpBack(1);
      addPtrInc(1);
      addJump(1);
        addPtrInc(2);
      addJumpBack(1);
      addPtrDec(2);
      addJump(1);
        addDec(1);
        addPtrDec(2);
      addJumpBack(1);
    }
    
    private void ifeq(int addressA, int addressB) {
      List<VariableValue> flags = allocator.allocateVariables(2);
      sub(addressA, addressB);
      copyValue(SUB_RESULT, flags.get(0));
      setValue(flags.get(1), 1);
      movePointerTo(flags.get(0));
      
      addJump(1);
        addPtrInc(1);
        addDec(1);
        addPtrDec(1);
        setZero();
      addJumpBack(1);
      movePointerTo(flags.get(1));
      addJump(1);
        addDec(1);
      
      endCallbacks.push(() -> {
        movePointerTo(flags.get(1));
        addJumpBack(1);
      });
    }
    
    private void ifneq(int addressA, int addressB) {
      VariableValue flag = allocator.allocateVariable();
      sub(addressA, addressB);
      copyValue(SUB_RESULT, flag);
      movePointerTo(flag);
      
      addJump(1);
        setZero();
      
      endCallbacks.push(() -> {
        movePointerTo(flag);
        addJumpBack(1);
      });
    }
    
    private void wneq(int addressA, int addressB) {
      VariableValue flag = allocator.allocateVariable();
      sub(addressA, addressB);
      copyValue(SUB_RESULT, flag);
      movePointerTo(flag);
      
      addJump(1);
      
      endCallbacks.push(() -> {
        sub(addressA, addressB);
        copyValue(SUB_RESULT, flag);
        movePointerTo(flag);
        addJumpBack(1);
      });
    }
    
    private void movePointerTo(int address) {
      if (pointer == address)
        return;
      int diff = Math.abs(pointer - address);
      if (pointer < address) {
        addPtrInc(diff);
      } else {
        addPtrDec(diff);
      }
      pointer = address;
    }
    
    private void movePointerTo(AllocatedValue variable) {
      movePointerTo(variable.getAddress());
    }
    
    private void setZero() {
      addJump(1);
      addDec(1);
      addJumpBack(1);
    }
    
    private void setValue(int address, int value) {
      movePointerTo(address);
      setZero();
      addInc(Math.floorMod(value, 256));
    }
    
    private void setValue(AllocatedValue variable, int value) {
      setValue((int)variable.getAddress(), value);
    }
    
    private void copylikeOperation(int fromAddress, int toAddress, BFOperator op) {
      movePointerTo(COPY_BUFFER);
      setZero();
      
      movePointerTo(fromAddress);
      addJump(1);
      movePointerTo(COPY_BUFFER);
      addInc(1);
      movePointerTo(fromAddress);
      addDec(1);
      addJumpBack(1);
      
      movePointerTo(COPY_BUFFER);
      addJump(1);
      movePointerTo(fromAddress);
      addInc(1);
      movePointerTo(toAddress);
      addOperator(op, 1);
      movePointerTo(COPY_BUFFER);
      addDec(1);
      addJumpBack(1);
    }
    
    private void copyValue(int fromAddress, int toAddress) {
      movePointerTo(toAddress);
      setZero();
      copylikeOperation(fromAddress, toAddress, BFSingleOperator.INC);
    }
    
    private void copyValue(AllocatedValue source, AllocatedValue target) {
      copyValue(source.getAddress(), target.getAddress());
    }
    
    private void incByValue(int sourceAddress, int targetAddress) {
      copylikeOperation(sourceAddress, targetAddress, BFSingleOperator.INC);
    } 
    
    private void incByValue(AllocatedValue source, AllocatedValue target) {
      incByValue(source.getAddress(), target.getAddress());
    }
    
    private void decByValue(int sourceAddress, int targetAddress) {
      copylikeOperation(sourceAddress, targetAddress, BFSingleOperator.DEC);
    }
    
    private void decByValue(AllocatedValue source, AllocatedValue target) {
      decByValue(source.getAddress(), target.getAddress());
    }
    
    private void addOperator(BFOperator operator, int times) {
      if (times == 1) {
        brainfuck.add(operator);
      } else if (times > 1) {
        brainfuck.add(new BFRepeatedOperator(operator, times));
      }
    }
    
    private void addInc(int times) {
      addOperator(BFSingleOperator.INC, times);
    }
    
    private void addDec(int times) {
      addOperator(BFSingleOperator.DEC, times);
    }
    
    private void addPtrInc(int times) {
      addOperator(BFSingleOperator.PTR_INC, times);
    }
    
    private void addPtrDec(int times) {
      addOperator(BFSingleOperator.PTR_DEC, times);
    }
    
    private void addJump(int times) {
      addOperator(BFSingleOperator.JUMP, times);
    }
    
    private void addJumpBack(int times) {
      addOperator(BFSingleOperator.JUMP_BACK, times);
    }
    
    private void addRead(int times) {
      addOperator(BFSingleOperator.READ, times);
    }
    
    private void addWrite(int times) {
      addOperator(BFSingleOperator.WRITE, times);
    }
  }
  
  
  /*
   *  PARSING
   */
  
  private interface Operand {
    
    String toString();
  }
  
  private static abstract class NameOperand implements Operand {
    
    protected final String name;
    
    public NameOperand(String name) {
      this.name = name;
    }
    
    public String getName() {
      return name;
    }
    
    public abstract String toString(); 
  }
  
  private static class VarNameOperand extends NameOperand {
    
    public VarNameOperand(String name) {
      super(name);
    }
    
    @Override
    public String toString() {
      return String.format("VarName(%s)", name);
    }
  }
  
  private static class ListNameOperand extends NameOperand {
    
    private final int size;
    
    public ListNameOperand(String name, int size) {
      super(name);
      this.size = size;
    }
    
    public int getSize() {
      return size;
    }
    
    @Override
    public String toString() {
      return String.format("ListName(%s[%d])", name, size);
    }
  }
  
  private static class ProcedureNameOperand extends NameOperand {
    
    public ProcedureNameOperand(String name) {
      super(name);
    }
    
    @Override
    public String toString() {
      return String.format("ProcedureName(%s)", name);
    }
  }
  
  private static class ProcedureParameterOperand extends NameOperand {
    
    public ProcedureParameterOperand(String name) {
      super(name);
    }
    
    @Override
    public String toString() {
      return String.format("ProcedureParameter(%s)", name);
    }
  }
  
  private static class NumberOperand implements Operand {
    
    private final int value;
    
    public NumberOperand(int value) {
      this.value = value;
    }
    
    public int getValue() {
      return value;
    }
    
    @Override
    public String toString() {
      return String.format("Number(%d)", value);
    }
  }
  
  private static class StringOperand implements Operand {
    
    private final String value;
    
    public StringOperand(String value) {
      this.value = value;
    }
    
    public String getValue() {
      return value;
    }
    
    @Override
    public String toString() {
      return String.format("String(%s)", value);
    }
  }
  
  private interface Statement {
    
    String toString();
  }
  
  private enum ConstStatement implements Statement {
    END,
    REM;
    
    @Override
    public String toString() {
      return name();
    }
  }
  
  private static class VarStatement implements Statement {
    
    private final List<NameOperand> variables = new ArrayList<>();
    
    public List<NameOperand> getVariables() {
      return variables;
    }
    
    public void addVariable(NameOperand variable) {
      variables.add(variable);
    }
    
    @Override
    public String toString() {
      return String.format("Var(%s)", variables.toString());
    }
  }
  
  private static abstract class ShortOperatorStatement implements Statement {
    
    protected final VarNameOperand a;
    protected final Operand b;
    
    public ShortOperatorStatement(VarNameOperand a, Operand b) {
      this.a = a;
      this.b = b;
    }
    
    public VarNameOperand getA() {
      return a;
    }
    
    public Operand getB() {
      return b;
    }
    
    public abstract String toString();
  }
  
  private static class SetStatement extends ShortOperatorStatement {
  
    public SetStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Set(%s, %s)", a, b);
    }
  }
  
  private static class IncStatement extends ShortOperatorStatement {
  
    public IncStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Inc(%s, %s)", a, b);
    }
  }
  
  private static class DecStatement extends ShortOperatorStatement {
    
    public DecStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Dec(%s, %s)", a, b);
    }
  }
  
  private static abstract class LongOperatorStatement implements Statement {
    
    protected final Operand a;
    protected final Operand b;
    protected final VarNameOperand c;
    
    public LongOperatorStatement(Operand a, Operand b, VarNameOperand c) {
      this.a = a;
      this.b = b;
      this.c = c;
    }
    
    public Operand getA() {
      return a;
    } 
    
    public Operand getB() {
      return b;
    }
    
    public VarNameOperand getC() {
      return c;
    }
    
    public abstract String toString();
  }
  
  private static class AddStatement extends LongOperatorStatement {
    
    public AddStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Add(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class SubStatement extends LongOperatorStatement {
    
    public SubStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Sub(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class MulStatement extends LongOperatorStatement {
    
    public MulStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Mul(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class DivModStatement extends LongOperatorStatement {
    
    private final VarNameOperand d; 
    
    public DivModStatement(Operand a, Operand b, VarNameOperand c, VarNameOperand d) {
      super(a, b, c);
      this.d = d;
    }
    
    public VarNameOperand getD() {
      return d;
    }
    
    @Override
    public String toString() {
      return String.format("DivMod(%s, %s, %s, %s)", a, b, c, d);
    }
  }
  
  private static class DivStatement extends LongOperatorStatement {
    
    public DivStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Div(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class ModStatement extends LongOperatorStatement {
    
    public ModStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Mod(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class CmpStatement extends LongOperatorStatement {
    
    public CmpStatement(Operand a, Operand b, VarNameOperand c) {
      super(a, b, c);
    }
    
    @Override
    public String toString() {
      return String.format("Cmp(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class A2BStatement implements Statement {
    
    private final Operand a;
    private final Operand b;
    private final Operand c;
    private final VarNameOperand d;
    
    public A2BStatement(Operand a, Operand b, Operand c, VarNameOperand d) {
      this.a = a;
      this.b = b;
      this.c = c;
      this.d = d;
    }
    
    public Operand getA() {
      return a;
    }
    
    public Operand getB() {
      return b;
    }
    
    public Operand getC() {
      return c;
    }
    
    public VarNameOperand getD() {
      return d;
    }
    
    @Override
    public String toString() {
      return String.format("A2B(%s, %s, %s, %s)", a, b, c, d);
    }
  }
  
  private static class B2AStatement implements Statement {
    
    private final Operand a;
    private final VarNameOperand b;
    private final VarNameOperand c;
    private final VarNameOperand d;
    
    public B2AStatement(Operand a, VarNameOperand b, VarNameOperand c, VarNameOperand d) {
      this.a = a;
      this.b = b;
      this.c = c;
      this.d = d;
    }
    
    public Operand getA() {
      return a;
    }
    
    public VarNameOperand getB() {
      return b;
    }
    
    public VarNameOperand getC() {
      return c;
    }
    
    public VarNameOperand getD() {
      return d;
    }
    
    @Override
    public String toString() {
      return String.format("B2A(%s, %s, %s, %s)", a, b, c, d);
    }
  }
  
  private static class LSetStatement implements Statement {
    
    private final ListNameOperand a;
    private final Operand b;
    private final Operand c;
    
    public LSetStatement(ListNameOperand a, Operand b, Operand c) {
      this.a = a;
      this.b = b;
      this.c = c;
    }
    
    public ListNameOperand getA() {
      return a;
    }
    
    public Operand getB() {
      return b;
    }
    
    public Operand getC() {
      return c;
    }
    
    @Override
    public String toString() {
      return String.format("LSet(%s, %s, %s)", a, b, c);
    }
  }
  
  private static class LGetStatement implements Statement {
    
    private final ListNameOperand a;
    private final Operand b;
    private final VarNameOperand c;
    
    public LGetStatement(ListNameOperand a, Operand b, VarNameOperand c) {
      this.a = a;
      this.b = b;
      this.c = c;
    }
    
    public ListNameOperand getA() {
      return a;
    }
    
    public Operand getB() {
      return b;
    }
    
    public VarNameOperand getC() {
      return c;
    }
    
    @Override
    public String toString() {
      return String.format("LSet(%s, %s, %s)", a, b, c);
    }
  }
  
  private static abstract class BlockStatement implements Statement {
    
    public abstract String toString();
  }
  
  private static abstract class JumpStatement extends BlockStatement {
    
    protected final VarNameOperand a;
    protected final Operand b;
    
    public JumpStatement(VarNameOperand a, Operand b) {
      super();
      this.a = a;
      this.b = b;
    }
    
    public VarNameOperand getA() {
      return a;
    }
    
    public Operand getB() {
      return b;
    }
    
    public abstract String toString();
  }
  
  private static class IfeqStatement extends JumpStatement {
    
    public IfeqStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Ifeq(%s, %s)", a, b);
    }
  }
  
  private static class IfneqStatement extends JumpStatement {
    
    public IfneqStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Ifneq(%s, %s)", a, b);
    }
  }
  
  private static class WneqStatement extends JumpStatement {
    
    public WneqStatement(VarNameOperand a, Operand b) {
      super(a, b);
    }
    
    @Override
    public String toString() {
      return String.format("Wneq(%s, %s)", a, b);
    }
  }
  
  private static class ProcStatement extends BlockStatement {
    
    protected final ProcedureNameOperand name;
    protected final List<ProcedureParameterOperand> parameters;
    
    public ProcStatement(ProcedureNameOperand name) {
      super();
      this.name = name;
      this.parameters = new ArrayList<>();
    }
    
    public ProcedureNameOperand getName() {
      return name;
    }
    
    public List<ProcedureParameterOperand> getParameters() {
      return parameters;
    }
    
    public void addParameter(ProcedureParameterOperand parameter) {
      parameters.add(parameter);
    }
    
    @Override
    public String toString() {
      return String.format("Proc(%s, %s)", name, parameters);
    }
  }
  
  private static class CallStatement implements Statement {
    
    protected final ProcedureNameOperand name;
    protected final List<ProcedureParameterOperand> parameters;
    
    public CallStatement(ProcedureNameOperand name) {
      this.name = name;
      this.parameters = new ArrayList<>();
    }
    
    public ProcedureNameOperand getName() {
      return name;
    }
    
    public List<ProcedureParameterOperand> getParameters() {
      return parameters;
    }
    
    public void addParameter(ProcedureParameterOperand parameter) {
      parameters.add(parameter);
    }
    
    @Override
    public String toString() {
      return String.format("Call(%s, %s)", name, parameters);
    }
  }
  
  private static class ReadStatement implements Statement {
    
    private final VarNameOperand a;
    
    public ReadStatement(VarNameOperand a) {
      this.a = a;
    }
    
    public VarNameOperand getA() {
      return a;
    }
    
    @Override
    public String toString() {
      return String.format("Read(%s)", a);
    }
  }
  
  private static class MsgStatement implements Statement {
    
    private final List<Operand> operands = new ArrayList<>();
    
    public List<Operand> getOperands() {
      return operands;
    }
    
    public void addOperand(Operand operand) {
      operands.add(operand);
    }
    
    @Override
    public String toString() {
      return String.format("Msg(%s)", operands);
    }
  }
  
  private static class Parser {
    
    private final List<Token> tokens;
    private int index;
    
    public Parser(List<Token> tokens) {
      this.tokens = tokens;
      this.index = 0;
    }
    
    public List<Statement> parse() {
      List<Statement> statements = new ArrayList<>();
      while (index < tokens.size()) {
        Statement statement = parseStatement();
        if (statement != ConstStatement.REM)
          statements.add(statement);
        
        if (index != tokens.size() && tokens.get(index) != ConstToken.EOL) {
          throw new RuntimeException("Invalid args number");
        }
        
        ++index;
      }
      return statements;
    }
    
    private Statement parseStatement() {
      if (parseKeyword("var")) {
        return parseVarStatement();
      } else if (parseKeyword("set")) {
        return parseSetStatement();
      } else if (parseKeyword("inc")) {
        return parseIncStatement();
      } else if (parseKeyword("dec")) {
        return parseDecStatement();
      } else if (parseKeyword("add")) {
        return parseAddStatement();
      } else if (parseKeyword("sub")) {
        return parseSubStatement();
      } else if (parseKeyword("mul")) {
        return parseMulStatement();
      } else if (parseKeyword("divmod")) {
        return parseDivModStatement();
      } else if (parseKeyword("div")) {
        return parseDivStatement();
      } else if (parseKeyword("mod")) {
        return parseModStatement();
      } else if (parseKeyword("cmp")) {
        return parseCmpStatement();
      } else if (parseKeyword("a2b")) {
        return parseA2BStatement();
      } else if (parseKeyword("b2a")) {
        return parseB2AStatement();
      } else if (parseKeyword("lset")) {
        return parseLSetStatement();
      } else if (parseKeyword("lget")) {
        return parseLGetStatement();
      } else if (parseKeyword("ifeq")) {
        return parseIfeqStatement();
      } else if (parseKeyword("ifneq")) {
        return parseIfneqStatement();
      } else if (parseKeyword("wneq")) {
        return parseWneqStatement();
      } else if (parseKeyword("proc")) {
        return parseProcStatement();
      } else if (parseKeyword("end")) {
        return ConstStatement.END;
      } else if (parseKeyword("call")) {
        return parseCallStatement();
      } else if (parseKeyword("read")) {
        return parseReadStatement();
      } else if (parseKeyword("msg")) {
        return parseMsgStatement();
      } else if (parseKeyword("rem")) {
        takeUntilEol();
        return ConstStatement.REM;
      } else {
        throw new RuntimeException("Unknown command");
      }
    }
    
    private VarStatement parseVarStatement() {
      VarStatement statement = new VarStatement();
      do {
        takeWhitespace();
        NameOperand name = parseVarNameOrListName();
        if (name != null) {
          statement.addVariable(name);
        } else {
          throw new Error("VarSingle expected");
        }
      } while (index < tokens.size() && tokens.get(index) != ConstToken.EOL);
      return statement;
    }
    
    private SetStatement parseSetStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      return new SetStatement(a, b);
    }
    
    private IncStatement parseIncStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      return new IncStatement(a, b);
    }
    
    private DecStatement parseDecStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      return new DecStatement(a, b);
    }
    
    private AddStatement parseAddStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();;
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new AddStatement(a, b, c);
    }
    
    private SubStatement parseSubStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();;
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new SubStatement(a, b, c);
    }
    
    private MulStatement parseMulStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new MulStatement(a, b, c);
    }
    
    private DivModStatement parseDivModStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand d = parseVarName();
      if (d == null)
        throw new RuntimeException("Invalid args number");
      return new DivModStatement(a, b, c, d);
    }
    
    private DivStatement parseDivStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new DivStatement(a, b, c);
    }
    
    private ModStatement parseModStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null) 
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new ModStatement(a, b, c);
    }
    
    private CmpStatement parseCmpStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null) 
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new CmpStatement(a, b, c);
    }
    
    private A2BStatement parseA2BStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand c = parseVarNameOrNumber();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand d = parseVarName();
      if (d == null)
        throw new RuntimeException("Invalid args number");
      return new A2BStatement(a, b, c, d);
    }
    
    private B2AStatement parseB2AStatement() {
      takeWhitespace();
      Operand a = parseVarNameOrNumber();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand b = parseVarName();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand d = parseVarName();
      if (d == null)
        throw new RuntimeException("Invalid args number");
      return new B2AStatement(a, b, c, d);
    }
    
    private LSetStatement parseLSetStatement() {
      takeWhitespace();
      ListNameOperand a = parseListName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand c = parseVarNameOrNumber();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new LSetStatement(a, b, c);
    }
    
    private LGetStatement parseLGetStatement() {
      takeWhitespace();
      ListNameOperand a = parseListName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      VarNameOperand c = parseVarName();
      if (c == null)
        throw new RuntimeException("Invalid args number");
      return new LGetStatement(a, b, c);
    }
    
    private IfeqStatement parseIfeqStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      return new IfeqStatement(a, b);
    }
    
    private IfneqStatement parseIfneqStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      return new IfneqStatement(a, b);
    }
    
    private WneqStatement parseWneqStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      
      takeWhitespace();
      Operand b = parseVarNameOrNumber();
      if (b == null)
        throw new RuntimeException("Invalid args number");
      return new WneqStatement(a, b);
    }
    
    private ProcStatement parseProcStatement() {
      takeWhitespace();
      ProcedureNameOperand name = parseProcedureName();
      if (name == null)
        throw new RuntimeException("Invalid args number");
      
      ProcStatement statement = new ProcStatement(name);
      while (index < tokens.size() && tokens.get(index) != ConstToken.EOL) {
        takeWhitespace();
        ProcedureParameterOperand parameter = parseProcedureParameter();
        if (parameter != null) {
          statement.addParameter(parameter);
        } else {
          throw new Error("VarSingle expected");
        }
      }
      return statement;
    }
    
    private CallStatement parseCallStatement() {
      takeWhitespace();
      ProcedureNameOperand name = parseProcedureName();
      if (name == null)
        throw new RuntimeException("Invalid args number");
      
      CallStatement statement = new CallStatement(name);
      while (index < tokens.size() && tokens.get(index) != ConstToken.EOL) {
        takeWhitespace();
        ProcedureParameterOperand parameter = parseProcedureParameter();
        if (parameter != null) {
          statement.addParameter(parameter);
        } else {
          throw new Error("VarSingle expected");
        }
      }
      return statement;
    }
    
    private ReadStatement parseReadStatement() {
      takeWhitespace();
      VarNameOperand a = parseVarName();
      if (a == null)
        throw new RuntimeException("Invalid args number");
      return new ReadStatement(a);
    }
    
    private MsgStatement parseMsgStatement() {
      MsgStatement statement = new MsgStatement();
      do {
        takeWhitespace();
        Operand operand = parseVarNameOrString();
        if (operand != null) {
          statement.addOperand(operand);
        } else {
          throw new RuntimeException("VarName or String expected");
        }
      } while (index < tokens.size() && tokens.get(index) != ConstToken.EOL);
      return statement;
    }
    
    private boolean parseKeyword(String keyword) {
      StringBuilder sb = new StringBuilder();
      int i;
      for (i = 0; index + i < tokens.size(); ++i) {
        Token token = tokens.get(index + i);
        if (token instanceof VarPrefixToken || token instanceof VarSuffixToken || 
            token instanceof CharElementToken) {
          
          sb.append(((SimpleToken)token).getValue());
        } else if (token instanceof NumberToken) {
          sb.append(Integer.toString(((NumberToken)token).getValue()));
        } else if (token == ConstToken.WHITESPACE || token == ConstToken.EOL) {
          break;
        } else {
          return false;
        }
      }
      
      if (sb.toString().toLowerCase().equals(keyword)) {
        index += i;
        return true;
      } else {
        return false;
      }
    }
    
    private VarNameOperand parseVarName() {
      if (index == tokens.size()) {
        throw new RuntimeException("EOF reached");
      }
      
      if (!(tokens.get(index) instanceof VarPrefixToken)) {
        return null;
      }
      
      StringBuilder sb = new StringBuilder();
      sb.append(((SimpleToken)tokens.get(index)).getValue());
      int i;
      for (i = 1; index + i < tokens.size(); ++i) {
        Token token = tokens.get(index + i);
        if (token instanceof VarPrefixToken || token instanceof VarSuffixToken) {
          sb.append(((SimpleToken)token).getValue());
        } else if (token instanceof NumberToken) {
          int value = ((NumberToken)token).getValue();
          if (value < 0)
            return null;
          sb.append(Integer.toString(value));
        } else if (token == ConstToken.WHITESPACE || token == ConstToken.EOL) {
          break;
        } else {
          return null;
        }
      }
      
      index += i;
      return new VarNameOperand(sb.toString().toLowerCase());
    }
    
    private ListNameOperand parseListNameWithSize() {
      if (index == tokens.size()) {
        throw new RuntimeException("EOF reached");
      }
      
      if (!(tokens.get(index) instanceof VarPrefixToken)) {
        return null;
      }
      
      StringBuilder sb = new StringBuilder();
      sb.append(((SimpleToken)tokens.get(index)).getValue());
      int i;
      int size = 0;
      boolean whitespace = false;
      for (i = 1; index + i < tokens.size(); ++i) {
        Token token = tokens.get(index + i);
        if (!whitespace && (token instanceof VarPrefixToken || token instanceof VarSuffixToken)) {
          sb.append(((SimpleToken)token).getValue());
        } else if (!whitespace && token instanceof NumberToken) {
          int value = ((NumberToken)token).getValue();
          if (value < 0)
            return null;
          sb.append(Integer.toString(value));
        } else if (!whitespace && token == ConstToken.WHITESPACE) {
          whitespace = true;
        } else if (token instanceof CharElementToken && 
                   ((CharElementToken)token).getValue().equals("[")) {
           
          ++i;
          if (index + i >= tokens.size())
            return null;
          token = tokens.get(index + i);
          if (!(token instanceof NumberToken)) {
            if (token == ConstToken.WHITESPACE) {
              ++i;
              if (index + i >= tokens.size())
                return null;
              token = tokens.get(index + i);
              if (!(token instanceof NumberToken))
                return null;
            } else {
              return null;
            }
          }
          size = ((NumberToken)token).getValue();
          ++i;
          if (index + i >= tokens.size())
            return null;
          token = tokens.get(index + i);
          if (token == ConstToken.WHITESPACE) {
            ++i;
            if (index + i >= tokens.size())
              return null;
            token = tokens.get(index + i);
          }
          if (!(token instanceof CharElementToken) || 
              !((CharElementToken)token).getValue().equals("]")) {
            
            return null;
          }
          break;
        } else {
          return null;
        }
      }
      
      index += i + 1;
      return new ListNameOperand(sb.toString().toLowerCase(), size);
    }
    
    private ListNameOperand parseListName() {
      VarNameOperand varName = parseVarName();
      if (varName != null) {
        return new ListNameOperand(varName.getName(), -1);
      } else {
        return null;
      }
    }
    
    private ProcedureNameOperand parseProcedureName() {
      VarNameOperand varName = parseVarName();
      if (varName != null) {
        return new ProcedureNameOperand(varName.getName());
      } else {
        return null;
      }
    }
    
    private ProcedureParameterOperand parseProcedureParameter() {
      VarNameOperand varName = parseVarName();
      if (varName != null) {
        return new ProcedureParameterOperand(varName.getName());
      } else {
        return null;
      }
    }
    
    private NumberOperand parseNumber() {
      if (tokens.get(index) instanceof NumberToken) {
        return new NumberOperand(Math.floorMod(((NumberToken)tokens.get(index++)).getValue(), 256));
      } else {
        return null;
      }
    }
    
    private StringOperand parseString() {
      if (tokens.get(index) instanceof StringToken) {
        return new StringOperand(((StringToken)tokens.get(index++)).getValue());
      } else {
        return null;
      }
    }
    
    private NameOperand parseVarNameOrListName() {
      NameOperand variable = parseListNameWithSize();
      if (variable == null) {
        variable = parseVarName();
      }
      return variable;
    }
    
    private Operand parseVarNameOrNumber() {
      Operand operand = parseVarName();
      if (operand == null) {
        operand = parseNumber();
      }
      return operand;
    }
    
    private Operand parseVarNameOrString() {
      Operand operand = parseVarName();
      if (operand == null) {
        operand = parseString();
      }
      return operand;
    }
    
    private void takeWhitespace() {
      if (index == tokens.size()) {
        throw new RuntimeException("EOF reached");
      }
      
      if (tokens.get(index) == ConstToken.WHITESPACE) {
        ++index;
      } else {
        throw new RuntimeException("Whitespace expected");
      }
    }
    
    private void takeUntilEol() {
      while (index < tokens.size() && tokens.get(index) != ConstToken.EOL)
        ++index;
    }
  }
  
  
  /*
   * TOKENIZETION
   */
  
  private static interface Token {
    
    String toString(); 
  }
  
  private enum ConstToken implements Token {
    EOL,
    CHAR_QUOTE,
    STRING_QUOTE,
    COMMENT_PREFIX,
    COMMENT,
    MINUS,
    WHITESPACE;
    
    @Override
    public String toString() {
      return name();
    }
  }
  
  private static abstract class SimpleToken implements Token {
    
    private final String value;
    
    public SimpleToken(String value) {
      this.value = value;
    }
    
    public String getValue() {
      return value;
    }
    
    public abstract String toString();
  }
  
  private static class DigitToken extends SimpleToken {
    
    public DigitToken(String value) {
      super(value);
    }
    
    public int getIntValue() {
      return Integer.valueOf(getValue());
    }
    
    @Override
    public String toString() {
      return String.format("Digit(%s)", getValue());
    }
  }
  
  private static class VarPrefixToken extends SimpleToken {
    
    public VarPrefixToken(String value) {
      super(value);
    }
    
    @Override
    public String toString() {
      return String.format("VarPrefix(%s)", getValue());
    }
  }
  
  private static class VarSuffixToken extends SimpleToken {
    
    public VarSuffixToken(String value) {
      super(value);
    }
    
    @Override
    public String toString() {
      return String.format("VarSuffix(%s)", getValue());
    }
  }
  
  private static class CharElementToken extends SimpleToken {
    
    public CharElementToken(String value) {
      super(value);
    }
    
    public char getCharValue() {
      switch (getValue()) {
        case "\\\\":
          return '\\';
        case "\\'":
          return '\'';
        case "\\\"":
          return '"';
        case "\\n":
          return '\n';
        case "\\r":
          return '\r';
        case "\\t":
          return '\t';
        default:
          return getValue().charAt(0);
      }
    }
    
    @Override
    public String toString() {
      return String.format("CharElement(%s)", getValue());
    }
  }
  
  private static class CharToken implements Token {
    
    private final char value;
    
    public CharToken(char value) {
      this.value = value;
    }
    
    public char getValue() {
      return value;
    }
    
    public int getIntValue() {
      return (int)value;
    }
    
    @Override
    public String toString() {
      return String.format("Char(%s)", getValue());
    }
  }
  
  private static class StringToken implements Token {
    
    private final String value;
    
    public StringToken(String value) {
      this.value = value;
    }
    
    public String getValue() {
      return value;
    }
    
    @Override
    public String toString() {
      return String.format("String(%s)", getValue());
    }
  }
  
  private static class NumberToken implements Token {
    
    private final int value;
    
    public NumberToken(int value) {
      this.value = value;
    }
    
    public int getValue() {
      return value;
    }
    
    @Override
    public String toString() {
      return String.format("Number(%s)", getValue());
    }
  }
  
  private interface TokenExtractor {
    
    Token extractToken(String code, int index);
    int lastTokenLength();
  }
  
  private static abstract class EqualsExtractor implements TokenExtractor {
    
    @Override
    public Token extractToken(String code, int index) {
      String pattern = getPattern();
      for (int i = 0; i < pattern.length(); ++i) {
        if (pattern.charAt(i) != code.charAt(index + i)) {
          return null;
        }
      }
      return createToken();
    }
    
    @Override
    public int lastTokenLength() {
      return getPattern().length();
    }
    
    protected abstract Token createToken();
    protected abstract String getPattern();
  }
  
  private static class EolExtractor extends EqualsExtractor {
    
    private static final String pattern = "\n";
    
    @Override
    protected Token createToken() {
      return ConstToken.EOL;
    }
    
    @Override
    protected String getPattern() {
      return pattern;
    }
  }
  
  private static class CharQuoteExtractor extends EqualsExtractor {
    
    private static final String pattern = "'";
    
    @Override
    protected Token createToken() {
      return ConstToken.CHAR_QUOTE;
    }
    
    @Override
    protected String getPattern() {
      return pattern;
    }
  }
  
  private static class StringQuoteExtractor extends EqualsExtractor {
    
    private static final String pattern = "\"";
    
    @Override
    protected Token createToken() {
      return ConstToken.STRING_QUOTE;
    }
    
    @Override
    protected String getPattern() {
      return pattern;
    }
  }
  
  private static class MinusExtractor extends EqualsExtractor {
    
    private static final String pattern = "-";
    
    @Override
    protected Token createToken() {
      return ConstToken.MINUS;
    }
    
    @Override
    protected String getPattern() {
      return pattern;
    }
  }
  
  private static abstract class RegexExtractor implements TokenExtractor {
    
    private int lastLength = 0;
    
    @Override
    public Token extractToken(String code, int index) {
      Matcher matcher = getPattern().matcher(code.substring(index));
      if (matcher.find()) {
        String group = matcher.group();
        lastLength = group.length();
        return createToken(group);
      }
      return null;
    }
    
    @Override
    public int lastTokenLength() {
      return lastLength;
    }
    
    protected abstract Token createToken(String value);
    protected abstract Pattern getPattern();
  }
  
  private static class DigitExtractor extends RegexExtractor {
    
    private static final Pattern pattern = Pattern.compile("^[0-9]");
    
    @Override
    protected Token createToken(String value) {
      return new DigitToken(value);
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class CommentPrefixExtractor extends RegexExtractor {
    
    private static final Pattern pattern = Pattern.compile("^(?:(?://)|(?:--)|(?:#))");
    
    @Override
    protected Token createToken(String value) {
      return ConstToken.COMMENT_PREFIX;
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class VarPrefixExtractor extends RegexExtractor {
    
    private static final Pattern pattern = Pattern.compile("^[$_a-zA-Z]");
    
    @Override
    protected Token createToken(String value) {
      return new VarPrefixToken(value);
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class VarSuffixExtractor extends RegexExtractor {
    
    private static final Pattern pattern = Pattern.compile("^[$_a-zA-Z0-9]");
    
    @Override
    protected Token createToken(String value) {
      return new VarSuffixToken(value);
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class CharElementExtractor extends RegexExtractor {
    
    private static final Pattern pattern = 
      Pattern.compile("^(?:(?:.(?<=[^'\\\"\\\\]))|(?:\\\\\\\\)|(?:\\\\')|(?:\\\\\\\")|(?:\\\\n)|(?:\\\\r)|(?:\\\\t))");
    
    @Override
    protected Token createToken(String value) {
      return new CharElementToken(value);
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class WhitespaceExtractor extends RegexExtractor {
    
    private static final Pattern pattern = 
      Pattern.compile("^[ \t]+");
    
    @Override
    protected Token createToken(String value) {
      return ConstToken.WHITESPACE;
    }
    
    @Override
    protected Pattern getPattern() {
      return pattern;
    }
  }
  
  private static class CommentExtractor implements TokenExtractor {
    
    private final TokenExtractor commentPrefixExtractor = new CommentPrefixExtractor();
    private final TokenExtractor eolExtractor = new EolExtractor();
    private int lastLength = 0;
    
    @Override
    public Token extractToken(String code, int index) {
      lastLength = 0;
      if (commentPrefixExtractor.extractToken(code, index) != null) {
        lastLength += commentPrefixExtractor.lastTokenLength();
        while (index + lastLength < code.length() && 
               eolExtractor.extractToken(code, index + lastLength) == null) {
          
          lastLength += eolExtractor.lastTokenLength();
        }
        return ConstToken.COMMENT;
      }
      return null;
    }
    
    @Override
    public int lastTokenLength() {
      return lastLength;
    }
  }
  
  private static class CharExtractor implements TokenExtractor {
    
    private final TokenExtractor charQuoteExtractor = new CharQuoteExtractor();
    private final TokenExtractor charElementExtractor = new CharElementExtractor();
    private int lastLength = 0;
    
    @Override
    public Token extractToken(String code, int index) {
      lastLength = 0;
      if (charQuoteExtractor.extractToken(code, index) != null) {
        lastLength += charQuoteExtractor.lastTokenLength();
        CharElementToken token = 
          (CharElementToken)charElementExtractor.extractToken(code, index + lastLength);
        lastLength += charElementExtractor.lastTokenLength();
        if (token == null) {
          throw new RuntimeException("No char after char quote");
        }
        if (charQuoteExtractor.extractToken(code, index + lastLength) == null) {
          throw new RuntimeException("Unclosed char quote pair");
        }
        lastLength += charQuoteExtractor.lastTokenLength();
        return new CharToken(token.getCharValue());
      }
      return null;
    }
    
    @Override
    public int lastTokenLength() {
      return lastLength;
    }
  }
  
  private static class StringExtractor implements TokenExtractor {
    
    private final TokenExtractor stringQuoteExtractor = new StringQuoteExtractor();
    private final TokenExtractor charElementExtractor = new CharElementExtractor();
    private int lastLength = 0;
    
    @Override
    public Token extractToken(String code, int index) {
      lastLength = 0;
      if (stringQuoteExtractor.extractToken(code, index) != null) {
        lastLength += stringQuoteExtractor.lastTokenLength();
        StringBuilder sb = new StringBuilder();
        
        while (index + lastLength < code.length() && 
               stringQuoteExtractor.extractToken(code, index + lastLength) == null) {
          
          CharElementToken token = 
            (CharElementToken)charElementExtractor.extractToken(code, index + lastLength);
          lastLength += charElementExtractor.lastTokenLength();
          sb.append(token.getCharValue());
        }
        
        if (index + lastLength < code.length()) {
          lastLength += stringQuoteExtractor.lastTokenLength();
        } else {
          throw new RuntimeException("Unclosed string quote pair");
        }
        
        return new StringToken(sb.toString());
      }
      return null;
    }
    
    @Override
    public int lastTokenLength() {
      return lastLength;
    }
  }
  
  private static class NumberExtractor implements TokenExtractor {
    
    private final TokenExtractor minusExtractor = new MinusExtractor();
    private final TokenExtractor digitExtractor = new DigitExtractor();
    private final TokenExtractor charExtractor = new CharExtractor();
    private int lastLength = 0;
    
    @Override
    public Token extractToken(String code, int index) {
      lastLength = 0;
      int multiplier = 1;
      
      if (minusExtractor.extractToken(code, index) != null) {
        multiplier = -1;
        lastLength += minusExtractor.lastTokenLength();
      }
      
      DigitToken digitToken;
      int value = 0;
      boolean anyDigit = false;
      while ((digitToken = (DigitToken)digitExtractor.extractToken(code, index + lastLength)) != null) {
        anyDigit = true;
        value = value * 10 + digitToken.getIntValue();
        lastLength += digitExtractor.lastTokenLength();
      }
      
      if (anyDigit) {
        return new NumberToken(value * multiplier);
      } else {
        CharToken charToken = (CharToken)charExtractor.extractToken(code, index);
        if (charToken != null) {
          lastLength += charExtractor.lastTokenLength();
          return new NumberToken(charToken.getIntValue());
        }
      }
      
      if (multiplier == -1) {
        throw new RuntimeException("Minus without digit after it");
      }
      return null;
    }
    
    @Override
    public int lastTokenLength() {
      return lastLength;
    }
  }
  
  private static class Tokenizer {
    
    private final TokenExtractor[] extractors = new TokenExtractor[] {
      new EolExtractor(),
      new WhitespaceExtractor(),
      new CommentExtractor(),
      new StringExtractor(),
      new NumberExtractor(),
      new VarPrefixExtractor(),
      new VarSuffixExtractor(),
      new CharElementExtractor()
    };
    private int lastLength = 0;
    
    public List<Token> tokenize(String code) {
      int index = 0;
      List<Token> tokens = new ArrayList<>();
      while (index < code.length()) {
        Token token = extractToken(code, index);
        index += lastLength;
        if (token != null) {
          tokens.add(token);
        } else {
          throw new RuntimeException("Unable to tokenize");
        }
      }
      removeUnnecessary(tokens);
      return tokens;
    }
    
    private Token extractToken(String code, int index) {
      for (TokenExtractor extractor : extractors) {
        Token token = extractor.extractToken(code, index);
        if (token != null) {
          lastLength = extractor.lastTokenLength();
          return token;
        }
      }
      return null;
    }
    
    private void removeUnnecessary(List<Token> tokens) {
      for (int i = 0; i < tokens.size(); ++i) {
        Token token = tokens.get(i);
        if (token == ConstToken.COMMENT) {
          tokens.remove(i);
          i = i > 1 ? i - 2 : 0;
        } else if (token == ConstToken.WHITESPACE) {
          if (i + 1 < tokens.size() && (tokens.get(i + 1) == ConstToken.EOL || 
                                        tokens.get(i + 1) == ConstToken.COMMENT)) {
            tokens.remove(i);
            --i;
          }
        } else if (token == ConstToken.EOL) {
          if (i + 1 < tokens.size() && (tokens.get(i + 1) == ConstToken.WHITESPACE || 
                                        tokens.get(i + 1) == ConstToken.EOL)) {
            
            tokens.remove(i + 1);
            --i;
          } else if (i + 1 == tokens.size()) {
            tokens.remove(i);
          }
        } else if (token instanceof StringToken) {
          if (i - 1 >= 0 && tokens.get(i - 1) != ConstToken.WHITESPACE) {
            tokens.add(i, ConstToken.WHITESPACE);
          } else if (i + 1 < tokens.size() && tokens.get(i + 1) != ConstToken.WHITESPACE) {
            tokens.add(i + 1, ConstToken.WHITESPACE);
          }
        }
      }
    }
  }
}
