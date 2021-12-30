import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Interpreter {

    class Variable {
        Double value=null;
    }

    private Map<String, Variable> variables = new HashMap<>();

    interface ASTNode {
        double eval();
    }

    class LiteralNode implements ASTNode {
        private Double value;

        public LiteralNode(Double value) {
            this.value = value;
        }

        @Override
        public double eval() {
            return value;
        }
    }

    class VariableNode implements ASTNode {
        private Variable variable;

        public VariableNode(Variable variable) {
            this.variable = variable;
        }

        @Override
        public double eval() {
            if (variable.value==null)
                throw new IllegalArgumentException("ERROR: Variable not initialized");
            return variable.value;
        }
    }

    class UnaryNode implements ASTNode {
        private ASTNode subNode;
        private String op;

        public UnaryNode(String op, ASTNode subNode) {
            this.subNode = subNode;
            this.op = op;
        }

        @Override
        public double eval() {
            if (op.equals("-"))
                return -subNode.eval();
            else
                return subNode.eval();
        }
    }

    class BinaryNode implements ASTNode {
        private ASTNode left;
        private ASTNode right;
        private String op;

        public BinaryNode(ASTNode left, ASTNode right, String op) {
            this.left = left;
            this.right = right;
            this.op = op;
        }

        @Override
        public double eval() {
            double l = left.eval();
            double r = right.eval();
            switch (op) {
                case "+":
                    return l + r;
                case "-":
                    return l - r;
                case "*":
                    return l * r;
                case "/":
                    return l / r;
                case "%":
                    return l % r;
            }
            throw new IllegalArgumentException("ERROR: wrong binary operator '" + op + "'");
        }
    }

    class AssignmentNode implements ASTNode {
        private VariableNode left;
        private ASTNode right;

        public AssignmentNode(VariableNode left, ASTNode right) {
            this.left = left;
            this.right = right;
        }

        @Override
        public double eval() {
            return left.variable.value = right.eval();
        }
    }

    class Parser {

        private Deque<String> tokens;

        public Parser(Deque<String> tokens) {
            this.tokens = tokens;
        }

        private void skip(String token) {
            String s = tokens.poll();
            if (null == s || !s.equals(token))
                throw new IllegalArgumentException("ERROR: '" + token + "' expected");
        }

        private ASTNode parseFactor() {
            String token = tokens.poll();
            if (token == null)
                throw new IllegalArgumentException("ERROR: factor expected");
            switch (token) {
                case "(": {
                    ASTNode result = parseExpression();
                    skip(")");
                    return result;
                }
                case "+":
                case "-": {
                    return new UnaryNode(token, parseFactor());
                }
                default: {
                    char c = token.charAt(0);
                    if (c >= '0' && c <= '9') {
                        try {
                            return new LiteralNode(Double.parseDouble(token));
                        } catch (NumberFormatException ignored) {
                            throw new IllegalArgumentException("ERROR: wrong number " + token);
                        }
                    }
                    if (c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z') {
                        return new VariableNode(variables.computeIfAbsent(token, (name) -> new Variable()));
                    }
                    throw new IllegalArgumentException("ERROR: factor expected, but found " + token);
                }
            }
        }

        private ASTNode parseMul() {
            ASTNode result = parseFactor();
            while (true) {
                String next = tokens.peek();
                if (next == null || !next.equals("*") && !next.equals("/") && !next.equals("%"))
                    return result;
                tokens.poll();
                ASTNode right = parseFactor();
                result = new BinaryNode(result, right, next);
            }
        }

        private ASTNode parseSum() {
            ASTNode result = parseMul();
            while (true) {
                String next = tokens.peek();
                if (next == null || !next.equals("+") && !next.equals("-"))
                    return result;
                tokens.poll();
                ASTNode right = parseMul();
                result = new BinaryNode(result, right, next);
            }
        }

        private ASTNode parseExpression() {
            ASTNode result = parseSum();
            String next = tokens.peek();
            if (next == null || !next.equals("="))
                return result;
            tokens.poll();
            if (!(result instanceof VariableNode))
                throw new IllegalArgumentException("ERROR:Left side of assignment must be identifier");
            ASTNode right = parseExpression();
            result = new AssignmentNode((VariableNode) result, right);
            return result;
        }
    }

    public Double input(String input) {
        Deque<String> tokens = tokenize(input);
        if (tokens.isEmpty()) return null;
        ASTNode node = new Parser(tokens).parseExpression();
        if (!tokens.isEmpty())
            throw new IllegalArgumentException("ERROR: Unexpected tokens after expression: "+tokens.stream().collect(Collectors.joining(" ")));
        return node.eval();
    }

    private static Deque<String> tokenize(String input) {
        Deque<String> tokens = new LinkedList<>();
        Pattern pattern = Pattern.compile("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
        Matcher m = pattern.matcher(input);
        while (m.find()) {
            tokens.add(m.group());
        }
        return tokens;
    }
}

________________________________________________________
import java.util.*;
import java.util.function.BiFunction;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Interpreter {
    private static final Map<String, BiFunction<Double, Double, Double>> MAP_OPERATOR = initOpMap();
    private Map<String, Double> mapVariableStore = new HashMap<>();

    private static Map<String, BiFunction<Double, Double, Double>> initOpMap() {
        final Map<String, BiFunction<Double, Double, Double>> result = new HashMap<>();
        result.put("+", Double::sum);
        result.put("-", (a, b) -> a - b);
        result.put("*", (a, b) -> a * b);
        result.put("/", (a, b) -> a / b);
        result.put("%", (a, b) -> a % b);

        return result;
    }

    public Double input(final String input) {
        if (Objects.isNull(input) || input.trim().isEmpty()) {
            return null;
        }

        final Deque<Token> tokens = tokenize(input);
        if (tokens.size() == 1 && TokenCategory.VALUE.equals(tokens.getFirst().tokenCategory)) {
            return (Double)tokens.getFirst().object;
        }

        return parse(tokens);
    }

    private Double parse(final Deque<Token> tokens) {
        final Token token = tokens.pollFirst();
        if (Objects.isNull(token)) {
            return null;
        }

        if (TokenCategory.BRACKET_OPEN.equals(token.tokenCategory)) {
            return parse(tokens);
        }

        final Token nextToken = tokens.pollFirst();
        if (TokenCategory.IDENTIFIER.equals(token.tokenCategory) &&
                Objects.nonNull(nextToken) &&
                TokenCategory.ASSIGNMENT.equals(nextToken.tokenCategory)) {
            final Double value = parse(tokens);
            mapVariableStore.put(Objects.toString(token.object), value);
            return value;
        } else if (TokenCategory.IDENTIFIER.equals(token.tokenCategory) &&
                (Objects.isNull(nextToken) || TokenCategory.BRACKET_CLOSE.equals(nextToken.tokenCategory))) {

            if (mapVariableStore.containsKey(token.object.toString())) {
                return mapVariableStore.get(token.object.toString());
            }
            throw new RuntimeException("ERROR: Invalid identifier. No variable with name '" + token + "' was found.");
        } else if (TokenCategory.VALUE.equals(token.tokenCategory) && (Objects.isNull(nextToken) || TokenCategory.BRACKET_CLOSE.equals(nextToken.tokenCategory))) {
            return (Double)token.object;
        }

        if (Objects.nonNull(nextToken) && TokenCategory.OPERATOR.equals(nextToken.tokenCategory)) {
            if (!TokenCategory.VALUE.equals(token.tokenCategory) && !TokenCategory.IDENTIFIER.equals(token.tokenCategory)) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: " + token.tokenCategory);
            }
            if (tokens.isEmpty()) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: nothing");
            }

            final Double op1 = TokenCategory.VALUE.equals(token.tokenCategory) ? (Double)token.object : mapVariableStore.get(token.object.toString());
            final BiFunction<Double, Double, Double> operator = (BiFunction<Double, Double, Double>) nextToken.object;
            final Token op2Token = tokens.pollFirst();
            if (Objects.isNull(op2Token) || (!TokenCategory.VALUE.equals(op2Token.tokenCategory)
                    && !TokenCategory.IDENTIFIER.equals(op2Token.tokenCategory)
                    && !TokenCategory.BRACKET_OPEN.equals(op2Token.tokenCategory))) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: " + (Objects.isNull(op2Token) ? "null" : op2Token.tokenCategory));
            }
            final Double op2 = TokenCategory.BRACKET_OPEN.equals(op2Token.tokenCategory) ? parse(tokens) : (Double)op2Token.object;
            tokens.addFirst(new Token(TokenCategory.VALUE, operator.apply(op1, op2)));
            return parse(tokens);
        }

        if (Objects.nonNull(nextToken) && TokenCategory.OPERATOR_PRIO_2.equals(nextToken.tokenCategory)) {
            if (!TokenCategory.VALUE.equals(token.tokenCategory) && !TokenCategory.IDENTIFIER.equals(token.tokenCategory)) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: " + token.tokenCategory);
            }
            if (tokens.isEmpty()) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: nothing");
            }

            final Double op1 = TokenCategory.VALUE.equals(token.tokenCategory) ? (Double)token.object : mapVariableStore.get(token.object.toString());
            final BiFunction<Double, Double, Double> operator = (BiFunction<Double, Double, Double>) nextToken.object;
            final Double op2 = parse(tokens);
            tokens.addFirst(new Token(TokenCategory.VALUE, operator.apply(op1, op2)));
            return parse(tokens);
        }

        throw new RuntimeException("ERROR: Invalid Syntax");
    }

    private Deque<Token> tokenize(String input) {
        Deque<Token> tokens = new LinkedList<>();
        Pattern pattern = Pattern.compile("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
        Matcher m = pattern.matcher(input);
        while (m.find()) {
            final String token = m.group().trim();

            switch(token) {
                case "+": // Fall through
                case "-": tokens.add(new Token(TokenCategory.OPERATOR_PRIO_2, MAP_OPERATOR.get(token))); continue;
                case "*": // Fall through
                case "/": // Fall through
                case "%": tokens.add(new Token(TokenCategory.OPERATOR, MAP_OPERATOR.get(token))); continue;
                case "=": tokens.add(new Token(TokenCategory.ASSIGNMENT, token)); continue;
                case "(": tokens.add(new Token(TokenCategory.BRACKET_OPEN, token)); continue;
                case ")": tokens.add(new Token(TokenCategory.BRACKET_CLOSE, token)); continue;
                default:
                    try {
                        Double d = Double.parseDouble(token);
                        tokens.add(new Token(TokenCategory.VALUE, d));
                    } catch (NumberFormatException e) {
                        tokens.add(new Token(TokenCategory.IDENTIFIER, token));
                    }
            }
        }
        return tokens;
    }

    private static class Token {
        private final TokenCategory tokenCategory;
        private final Object object;

        private Token(TokenCategory tokenCategory, Object object) {
            this.tokenCategory = tokenCategory;
            this.object = object;
        }

        @Override
        public String toString() {
            return "(" + tokenCategory  + ", " + object + ")";
        }
    }

    private enum TokenCategory {
        VALUE,
        OPERATOR,
        OPERATOR_PRIO_2,
        ASSIGNMENT,
        BRACKET_OPEN,
        BRACKET_CLOSE,
        IDENTIFIER;
    }
}

________________________________________________________
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Interpreter {

    private final Map<String, Double> varMap = new HashMap<>();

    private enum Associativity {
        RIGHT, LEFT
    }

    private enum Operator {
        BIN_OP, VAR, CONST
    }

    private interface Ast {
        Operator op();
    }

    private static final class BinOp implements Ast {
        private final String op;
        private final Ast a;
        private final Ast b;

        public BinOp(String op, Ast a, Ast b) {
            this.op = op;
            this.a = a;
            this.b = b;
        }

        @Override
        public Operator op() {
            return Operator.BIN_OP;
        }
    }

    private static final class Var implements Ast {
        private final String identifier;

        public Var(String identifier) {
            this.identifier = identifier;
        }

        @Override
        public Operator op() {
            return Operator.VAR;
        }
    }

    private static final class Const implements Ast {
        private final double n;

        public Const(double n) {
            this.n = n;
        }

        @Override
        public Operator op() {
            return Operator.CONST;
        }
    }

    public Double input(String input) {
        List<String> tokens = tokenize(input);
        if (tokens.size() == 0) return null;
        Double result = null;
        try {
            Ast ast = parse(tokens);
            if (ast != null) result = eval(ast);
        } catch (Exception e) {
            System.out.println("ERROR: " + e.getMessage());
            throw new RuntimeException(e);
        }

        return result;
    }

    private static List<String> tokenize(String input) {
        List<String> tokens = new ArrayList<>();
        Pattern pattern = Pattern.compile("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
        Matcher m = pattern.matcher(input);
        while (m.find())
            tokens.add(m.group());
        return tokens;
    }

    private Associativity getAssociativity(String operator) {
        return operator.equals("=") ? Associativity.RIGHT : Associativity.LEFT;
    }

    private int getPrecedence(String operator) {
        switch (operator) {
            case "*":
            case "/":
            case "%": return 3;
            case "-":
            case "+": return 2;
            case "=": return 1;
            default: return 0;
        }
    }

    private void addBinOp(Stack<Ast> astStack, String operator) {
        Ast right = astStack.pop();
        Ast left = astStack.pop();
        astStack.push(new BinOp(operator, left, right));
    }

    private Ast parse(List<String> tokens) throws Exception {
        Stack<String> operatorStack = new Stack<>();
        Stack<Ast> astStack = new Stack<>();

        for (String token : tokens) {
            switch (token) {
                case "(":
                    operatorStack.push(token);
                    continue;
                case ")":
                    while (!operatorStack.isEmpty()) {
                        String popped = operatorStack.pop();
                        if (popped.equals("(")) break;
                        else addBinOp(astStack, popped);
                    }
                    continue;
                case "+":
                case "-":
                case "*":
                case "/":
                case "%":
                case "=":
                    while (!operatorStack.isEmpty()) {
                        String popped = operatorStack.peek();
                        if (!popped.equals("(")
                                && getAssociativity(token) != Associativity.RIGHT
                                && getPrecedence(popped) - getPrecedence(token) >= 0) {
                            operatorStack.pop();
                            addBinOp(astStack, popped);
                        } else {
                            break;
                        }
                    }
                    operatorStack.push(token);
                    continue;
                default:
                    break;
            }

            if (Character.isAlphabetic(token.charAt(0)))
                astStack.push(new Var(token));
            else if (Character.isDigit(token.charAt(0)))
                astStack.push(new Const(Double.parseDouble(token)));
        }

        while (!operatorStack.isEmpty())
            addBinOp(astStack, operatorStack.pop());

        if (astStack.size() > 1) throw new Exception();
        return astStack.pop();
    }

    private double eval(final Ast ast) throws Exception {
        if (ast == null) return 0;

        if (ast.op() == Operator.BIN_OP) {
            BinOp binOp = (BinOp) ast;
            switch (binOp.op) {
                case "+": return eval(binOp.a) + eval(binOp.b);
                case "-": return eval(binOp.a) - eval(binOp.b);
                case "*": return eval(binOp.a) * eval(binOp.b);
                case "/": return eval(binOp.a) / eval(binOp.b);
                case "%": return eval(binOp.a) % eval(binOp.b);
                case "=":
                    double result = eval(binOp.b);
                    varMap.put(((Var) binOp.a).identifier, result);
                    return result;
                default: return 0;
            }
        } else if (ast.op() == Operator.VAR) {
            Var var = (Var) ast;
            Double varValue = varMap.get(var.identifier);
            if (varValue == null)
                throw new Exception("Invalid identifier. No variable with name '"
                        + var.identifier + "' was found.");
            return varValue;
        } else {
            return ((Const) ast).n;
        }
    }
}

________________________________________________________
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Interpreter {

  HashMap<String,Double> reg = new HashMap<>();  
  String cReg = "",cmd = "";
  boolean dirty = false;
  
  public Double input(String input) {
    if(input.trim().isEmpty()) return null;
    Deque<String> tokens = tokenize(input);
    reg.put("ans", 0d);
    cReg = cmd = "";
    dirty = false;
 
   while(tokens.contains("(")){
      int ob = input.indexOf('(');
      int cb = getCloseBracketIndex(input, ob);
      input = input.substring(0, ob) + input(input.substring(ob + 1, cb)) + input.substring(cb + 1);
      tokens = tokenize(input);
    }
   
    if (tokens.size() == 5) {
      if (tokens.contains("=")) {
        cReg = tokens.getFirst();
        cmd = "asg";
        tokens.removeFirst();
        tokens.removeFirst(); 
        dirty = true;
      }else {
        cReg = tokens.getFirst();
        tokens.removeFirst();
        if(tokens.getFirst().equals("+")) { 
          cmd = "add"; 
          tokens.removeFirst(); 
        }else if(tokens.getFirst().equals("-")) { 
          cmd = "sub"; 
          tokens.removeFirst(); 
        }else{
          input = input(input.substring(0, 5)) + input.substring(5);
          tokens = tokenize(input);
        }
      }
      dirty = true;
    }
    if (tokens.size() == 3) {
        if(!dirty) dirty = !tokens.contains("=");
        
             if (tokens.contains("+")) reg.put((dirty) ? "ans" : tokens.getFirst(), getNum(tokens.getFirst()) + Double.valueOf(tokens.getLast()));
        else if (tokens.contains("-")) reg.put((dirty) ? "ans" : tokens.getFirst(), getNum(tokens.getFirst()) - Double.valueOf(tokens.getLast()));
        else if (tokens.contains("*")) reg.put((dirty) ? "ans" : tokens.getFirst(), getNum(tokens.getFirst()) * Double.valueOf(tokens.getLast()));
        else if (tokens.contains("/")) reg.put((dirty) ? "ans" : tokens.getFirst(), getNum(tokens.getFirst()) / Double.valueOf(tokens.getLast()));
        else if (tokens.contains("%")) reg.put((dirty) ? "ans" : tokens.getFirst(), getNum(tokens.getFirst()) % Double.valueOf(tokens.getLast()));
        else if (tokens.contains("=")) {
          reg.put(tokens.getFirst(), Double.valueOf(tokens.getLast()));
          reg.put("ans", reg.get(tokens.getFirst()));
        }
        
        if (!dirty) reg.put("ans", reg.get(tokens.getFirst()));
    } else if (tokens.size() == 1) {
      if (reg.containsKey(tokens.getFirst())) {
        return reg.get(tokens.getFirst());
      } else {
        try{ 
          reg.put("ans", Double.valueOf(tokens.getFirst())); 
        }catch(NumberFormatException e){ 
          throw new IllegalArgumentException("ERROR: Invalid identifier. No variable with name '"+ tokens.getFirst() +"' was found."); 
        }
      }
    }else{
      throw new IllegalArgumentException();
    }
    
    if(dirty && cReg != ""){
      if (cmd == "asg")
        reg.put(cReg, reg.get("ans"));
      else{
        if (cmd == "add") reg.put("ans", reg.get("ans") + getNum(cReg));
        else if(cmd == "sub") reg.put("ans", reg.get("ans") - getNum(cReg));
      }
    }    
    return reg.get("ans");
  }

  private static Deque<String> tokenize(String input) {
    Deque<String> tokens = new LinkedList<>();
    Pattern pattern = Pattern.compile("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
    Matcher m = pattern.matcher(input);
    while (m.find()) {
      tokens.add(m.group());
    }
    return tokens;
  }
    public static int getCloseBracketIndex(String expression, int indexOfOpenBracket) {
    int internalBracket = 0;
    if (indexOfOpenBracket > expression.length() || indexOfOpenBracket < 0) {
      throw new StringIndexOutOfBoundsException(indexOfOpenBracket);
    }
    for (int i = indexOfOpenBracket + 1; i < expression.length(); i++) {
      if (expression.charAt(i) == '(') {
        internalBracket++;
      }
      if (expression.charAt(i) == ')') {
        if (internalBracket == 0) {
          return i;
        }
        internalBracket--;
      }
    }
    return -1;
  }

  public Double getNum(String first) {
    try {
      return Double.valueOf(first);
    } catch (NumberFormatException e) {
      return reg.get(first);
    }
  }

}

________________________________________________________
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Interpreter {
  private static final String IDENTIFIER = "IDENTIFIER";
    private static final String NUMBER = "NUMBER";
    private static final String REGEX_IDENTIFIER = "[A-Za-z_][A-Za-z0-9_]*";
    private static final String REGEX_NUMBER = "[0-9]*(\\.?[0-9]+)";
    private static final Pattern pattern = Pattern.compile(
            "=>|[-+*/%=\\(\\)]|" + REGEX_IDENTIFIER + "|" + REGEX_NUMBER);
    private static final Pattern patternIdentifier = Pattern.compile(REGEX_IDENTIFIER);
    private static final Pattern patternNumber = Pattern.compile(REGEX_NUMBER);

    private Map<String, Double> variables = new HashMap<>();

    /** Topmost current token. */
    private String curToken;
    /** Next token from the input */
    private String nextToken;
    private Deque<String> tokens;

    public Double input(String input) {
        tokens = tokenize(input);
        if (tokens.isEmpty()) return null;
        advance();
        double res = exprOrAssign();
        if (nextToken != null || !tokens.isEmpty())
            throw new RuntimeException("Expected eof but found: " + nextToken);
        return res;
    }

    private static Deque<String> tokenize(String input) {
        Deque<String> tokens = new LinkedList<>();
        Matcher m = pattern.matcher(input);
        while (m.find()) {
            tokens.add(m.group());
        }
        return tokens;
    }

    /** Advances to the next token. */
    private void advance() {
        curToken = nextToken;
        nextToken = tokens.poll();
    }

    /** Checks and consumes the one token if it matches. */
    private boolean accept(String token) {
        if (nextToken != null) {
            if (checkToken(token, nextToken)) {
                advance();
                return true;
            }
        }
        return false;
    }

    private static boolean checkToken(String expected, String token) {
        switch (expected) {
            case IDENTIFIER:
                return patternIdentifier.matcher(token).matches();
            case NUMBER:
                return patternNumber.matcher(token).matches();
            default:
                return expected.equals(token);
        }
    }

    /** Checks and consumes the one token. Throws an Exception if the wrong token was found. */
    private void expect(String token) {
        if (!accept(token))
            throw new RuntimeException("Expected token " + token + " but found: " + nextToken);
    }

    /* Grammar Original:
     * expression      ::= factor | expression operator expression
     * factor          ::= number | identifier | assignment | '(' expression ')'
     * assignment      ::= identifier '=' expression
     *
     * operator        ::= '+' | '-' | '*' | '/' | '%'
     *
     * identifier      ::= letter | '_' { identifier-char }
     * identifier-char ::= '_' | letter | digit
     *
     * number          ::= { digit } [ '.' digit { digit } ]
     *
     * letter          ::= 'a' | 'b' | ... | 'y' | 'z' | 'A' | 'B' | ... | 'Y' | 'Z'
     * digit           ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
     *
     * =================
     * Grammar Modified:
     * expression split into expressionAdd and expressionMul
     * expressionAdd ::= expressionMul ({ '+' expressionMul } | { '-' expressionMul })
     * expressionMul ::= factor ({ '*' factor } | { '/' factor } | { '%' factor })
     */

    private double exprOrAssign() {
        if (checkToken(IDENTIFIER, nextToken) && checkToken("=", tokens.peek())) {
            return assignmentOrVariable();
        } else {
            return expression();
        }
    }

    private double expression() {
        double val = expressionMul();
        while (accept("+") || accept("-")) {
            String op = curToken;
            double right = expressionMul();
            if (op.equals("+")) {
                val += right;
            } else {
                val -= right;
            }
        }
        return val;
    }

    private double expressionMul() {
        double val = factor();
        while (accept("*") || accept("/") || accept("%")) {
            String op = curToken;
            double right = factor();
            if (op.equals("*")) {
                val *= right;
            } else if (op.equals("/")) {
                val /= right;
            } else {
                val %= right;
            }
        }
        return val;
    }

    private double factor() {
        if (accept(NUMBER)) {
            return Double.parseDouble(curToken);
        } else if (accept("(")) {
            double expression = expression();
            expect(")");
            return expression;
        } else {
            return assignmentOrVariable();
        }
    }

    private double assignmentOrVariable() {
        accept(IDENTIFIER);
        String var = curToken;
        if (accept("=")) {
            variables.put(var, expression());
        }
        return variables.get(var);
    }

    private String debugTokens() {
        return String.format("tokens[cur=%s, next=%s, rest=%s]",
                             curToken, nextToken, String.join(", ", tokens));
    }
}
