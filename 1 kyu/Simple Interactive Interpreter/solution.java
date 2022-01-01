import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Interpreter {
    private static final Map<String, BiFunction<Double, Double, Double>> MAP_OPERATOR = initOpMap();
    private final Map<String, Deque<Token>> mapFunctionDefinition = new HashMap<>();
    private final Map<String, Deque<Token>> mapFunctionParameterDef = new HashMap<>();
    private final Map<String, Double> mapVariableStore = new HashMap<>();

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

        if (TokenCategory.FUNCTION.equals(token.tokenCategory)) {
            parseFunctionDefinition(tokens);
            return null;
        }

        if (TokenCategory.BRACKET_OPEN.equals(token.tokenCategory)) {
            final Token checkToken = tokens.getFirst();
            if (Objects.nonNull(checkToken) && TokenCategory.FUNCTION.equals(checkToken.tokenCategory)) {
                throw new RuntimeException("ERROR: Braces not allowed before function declaration");
            }
            return parse(tokens);
        }

        if (TokenCategory.IDENTIFIER.equals(token.tokenCategory) &&
                mapFunctionDefinition.containsKey(token.object.toString())) {
            tokens.addFirst(new Token(TokenCategory.VALUE, getIdentifierValue(token, tokens)));
            return parse(tokens);
        }

        final Token nextToken = tokens.pollFirst();
        if (TokenCategory.IDENTIFIER.equals(token.tokenCategory) &&
                Objects.nonNull(nextToken) &&
                TokenCategory.ASSIGNMENT.equals(nextToken.tokenCategory)) {
            if (mapFunctionDefinition.containsKey(Objects.toString(token.object))) {
                throw new RuntimeException("ERROR: variable name is already declared as function");
            }
            final Double value = parse(tokens);
            mapVariableStore.put(Objects.toString(token.object), value);
            return value;
        } else if (TokenCategory.IDENTIFIER.equals(token.tokenCategory) &&
                (Objects.isNull(nextToken) || TokenCategory.BRACKET_CLOSE.equals(nextToken.tokenCategory))) {
            return getIdentifierValue(token, tokens);
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
            final Double op1 = TokenCategory.VALUE.equals(token.tokenCategory) ? (Double)token.object : getIdentifierValue(token, tokens);
            final BiFunction<Double, Double, Double> operator = (BiFunction<Double, Double, Double>) nextToken.object;
            final Token op2Token = tokens.pollFirst();
            if (Objects.isNull(op2Token) || (!TokenCategory.VALUE.equals(op2Token.tokenCategory)
                    && !TokenCategory.IDENTIFIER.equals(op2Token.tokenCategory)
                    && !TokenCategory.BRACKET_OPEN.equals(op2Token.tokenCategory))) {
                throw new RuntimeException("ERROR: Invalid syntax. Identifier or Value expected, found: " + (Objects.isNull(op2Token) ? "null" : op2Token.tokenCategory));
            }
            final Double op2 = TokenCategory.BRACKET_OPEN.equals(op2Token.tokenCategory) ? parse(tokens) : getIdentifierValue(op2Token, tokens);
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
            final Double op1 = TokenCategory.VALUE.equals(token.tokenCategory) ? (Double)token.object : getIdentifierValue(token, tokens);
            final BiFunction<Double, Double, Double> operator = (BiFunction<Double, Double, Double>) nextToken.object;
            final Double op2 = parse(tokens);
            tokens.addFirst(new Token(TokenCategory.VALUE, operator.apply(op1, op2)));
            return parse(tokens);
        }

        throw new RuntimeException("ERROR: Invalid Syntax");
    }

    private Double getIdentifierValue(final Token token, final Deque<Token> tokens) {
        if (TokenCategory.VALUE.equals(token.tokenCategory)) {
            return (Double)token.object;
        }

        if (mapVariableStore.containsKey(token.object.toString())) {
            return mapVariableStore.get(token.object.toString());
        } else if (mapFunctionDefinition.containsKey(token.object.toString())) {
            final Deque<Token> functionDefTokens = mapFunctionDefinition.get(token.object.toString());
            final Deque<Token> functionParamTokens = mapFunctionParameterDef.get(token.object.toString());
            return parse(replaceDefParams(functionDefTokens, new LinkedList<>(functionParamTokens), tokens));
        }

        throw new RuntimeException("ERROR: Invalid identifier. No variable with name '" + token + "' was found.");
    }

    private Deque<Token> replaceDefParams(final Deque<Token> functionDefTokens,
                                          final Deque<Token> functionParamTokens,
                                          final Deque<Token> tokens) {
        final Deque<Token> result = new LinkedList<>();
        for (final Token funcToken: functionDefTokens) {
            if (!functionParamTokens.contains(funcToken)) {
                result.add(funcToken);
                continue;
            }

            if (tokens.isEmpty()) {
                throw new RuntimeException("ERROR: Given arguments do not match parameter list of the function called");
            }

            Token tokenToReplace = tokens.pollFirst();
            if (Objects.nonNull(tokenToReplace) && TokenCategory.IDENTIFIER.equals(tokenToReplace.tokenCategory)) {
                tokenToReplace = new Token(TokenCategory.VALUE, getIdentifierValue(tokenToReplace, tokens));
            }

            functionParamTokens.removeFirst();
            result.add(tokenToReplace);
        }

        return result;
    }

    private void parseFunctionDefinition(final Deque<Token> tokens ) {
        final Token token = tokens.pollFirst();
        if (Objects.isNull(token)) {
            return;
        }

        if (!TokenCategory.IDENTIFIER.equals(token.tokenCategory)) {
            throw new RuntimeException("Invalid Function name");
        }

        if (mapVariableStore.containsKey(token.object.toString())) {
            throw new RuntimeException("ERROR: Conflict function name with given variable name");
        }

        final Deque<Token> parameterList = new LinkedList<>();
        mapFunctionParameterDef.put(token.object.toString(), parameterList);
        mapFunctionDefinition.put(token.object.toString(), tokens);

        Token nextToken = tokens.pollFirst();
        while (Objects.nonNull(nextToken) && !TokenCategory.FUNCTION_OP.equals(nextToken.tokenCategory)) {
            if (!TokenCategory.IDENTIFIER.equals(nextToken.tokenCategory)) {
                throw new RuntimeException("ERROR: Invalid token found. Identifier expected, found: " + nextToken);
            }
            parameterList.add(nextToken);
            nextToken = tokens.pollFirst();
        }
        if (Objects.isNull(nextToken)) {
            throw new RuntimeException("ERROR: Function operator \"=>\" is missing.");
        }

        final Long aLong = parameterList.stream()
                .map(Token::toString)
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))
                .values()
                .stream()
                .filter(i -> i > 1)
                .findAny()
                .orElse(0L);
        if (aLong > 0) {
            throw new RuntimeException("ERROR: Parameter name not unique");
        }

        for (final Token paramneter : parameterList) {
            if (!tokens.contains(paramneter)) {
                throw new RuntimeException("ERROR: Parameter list does not match with function definition.");
            }
        }
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
                case "fn": tokens.add(new Token(TokenCategory.FUNCTION, token)); continue;
                case "=>": tokens.add(new Token(TokenCategory.FUNCTION_OP, token)); continue;
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
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Token token = (Token) o;
            return tokenCategory == token.tokenCategory && Objects.equals(object, token.object);
        }

        @Override
        public int hashCode() {
            return Objects.hash(tokenCategory, object);
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
        IDENTIFIER,
        FUNCTION,
        FUNCTION_OP;
    }
}

___________________________________________________________________________
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Interpreter {
    private final Map<String, FuncCall> funcMap = new HashMap<>();
    private final Map<String, Double> varMap = new HashMap<>();

    private static class Pair {
        private int parsedArgs;
        private final int funcArgs;

        public Pair(int parsedArgs, int funcArgs) {
            this.parsedArgs = parsedArgs;
            this.funcArgs = funcArgs;
        }
    }

    private enum Associativity {
        RIGHT, LEFT
    }

    private enum Operator {
        BIN_OP, VAR, CONST
    }

    private interface Ast {
        default Operator op() { return null; }
        default Ast a() { return null; }
        default Ast b() { return null; }
        default Ast copy() { return null; }
    }

    private static final class BinOp implements Ast {
        private final String op;
        private Ast a;
        private Ast b;

        public BinOp(String op, Ast a, Ast b) {
            this.op = op;
            this.a = a;
            this.b = b;
        }

        @Override
        public Operator op() {
            return Operator.BIN_OP;
        }

        @Override
        public Ast a() {
            return a;
        }

        @Override
        public Ast b() {
            return b;
        }

        @Override
        public Ast copy() {
            return new BinOp(op, a.copy(), b.copy());
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

        @Override
        public Ast copy() {
            return new Var(identifier);
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

        @Override
        public Ast copy() {
            return new Const(n);
        }
    }

    private static final class FuncCall implements Ast {
        private final int numArgs;
        private final Map<Integer, String> args;
        private Ast functionRoot;

        public FuncCall(int numArgs, Map<Integer, String> args, Ast functionRoot) {
            this.numArgs = numArgs;
            this.args = args;
            this.functionRoot = functionRoot;
        }

        public FuncCall(FuncCall funcCall) {
            this(funcCall.numArgs, funcCall.args, funcCall.functionRoot.copy());
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
        Pattern pattern = Pattern.compile("=>|[-+*/%=()]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
        Matcher m = pattern.matcher(input);
        while (m.find())
            tokens.add(m.group());
        return tokens;
    }

    private Associativity getAssociativity(String operator) {
        return operator.startsWith("$") || operator.equals("=") ? Associativity.RIGHT : Associativity.LEFT;
    }

    private int getPrecedence(String operator) {
        switch (operator) {
            case "*":
            case "/":
            case "%": return 4;
            case "-":
            case "+": return 3;
            case "=": return 2;
            case "$": return 1;
            default: return 0;
        }
    }

    private Ast substituteVars(Ast node, Map<String, Ast> substitution) {
        if (node == null) return null;
        substituteVars(node.a(), substitution);
        substituteVars(node.b(), substitution);

        if (node.a() != null && node.b() != null) {
            if (node.a().op() == Operator.VAR && substitution.containsKey(((Var) node.a()).identifier))
                ((BinOp) node).a = substitution.get(((Var) node.a()).identifier);
            if (node.b().op() == Operator.VAR && substitution.containsKey(((Var) node.b()).identifier))
                ((BinOp) node).b = substitution.get(((Var) node.b()).identifier);
        } else if (node.op() == Operator.VAR) {
            return substitution.get(((Var) node).identifier);
        }

        return node;
    }

    private void checkDefinedness(Ast node, HashSet<String> args) throws Exception {
        if (node == null) return;
        checkDefinedness(node.a(), args);
        checkDefinedness(node.b(), args);

        if (node.op() == Operator.VAR && !args.contains(((Var) node).identifier))
            throw new Exception("Unknown identifier '" + ((Var) node).identifier + "'");
    }

    private void addFuncCall(Stack<Ast> astStack, String identifier) {
        FuncCall funcCall = funcMap.get(identifier.substring(1));
        Map<String, Ast> funcArgs = new HashMap<>();
        for (int i = funcCall.numArgs - 1; i >= 0; i--)
            funcArgs.put(funcCall.args.get(i), astStack.pop());

        FuncCall funcCallCopy = new FuncCall(funcCall);
        funcCallCopy.functionRoot = substituteVars(funcCallCopy.functionRoot, funcArgs);
        astStack.push(funcCallCopy.functionRoot);
    }

    private void addBinOp(Stack<Ast> astStack, String operator) {
        Ast right = astStack.pop();
        Ast left = astStack.pop();
        astStack.push(new BinOp(operator, left, right));
    }

    private void updateFuncStack(Stack<Pair> funcStack) {
        if (!funcStack.isEmpty()) {
            Pair temp = funcStack.pop();
            temp.parsedArgs += 1;
            funcStack.push(temp);
        }
    }

    private void parseFunc(List<String> tokens, int i) throws Exception {
        if (i > 0) throw new Exception("Function declaration have to start with 'fn'.");
        int j = i + 2;
        Map<Integer, String> args = new HashMap<>();
        for (; !tokens.get(j).equals("=>"); j++) {
            if (args.containsValue(tokens.get(j))) {
                throw new Exception("Invalid argument name. Argument with name '"
                        + tokens.get(j) + "' already exists.");
            }
            args.put(j - (i + 2), tokens.get(j));
        }
        String funcId = tokens.get(i + 1);
        if (varMap.containsKey(funcId))
            throw new Exception("Invalid identifier. Variable with name '"
                    + funcId + "' already exists.");
        
        Ast functionBody = parse(tokens.subList(j + 1, tokens.size()));
        checkDefinedness(functionBody, new HashSet<>(args.values()));
        FuncCall funcCall = new FuncCall(j - (i + 2), args, functionBody);
        funcMap.put(funcId, funcCall);
    }

    private Ast parse(List<String> tokens) throws Exception {
        Stack<String> operatorStack = new Stack<>();
        Stack<Ast> astStack = new Stack<>();
        Stack<Pair> funcStack = new Stack<>();
        boolean complexExpr = false;

        for (int i = 0, tokensSize = tokens.size(); i < tokensSize; i++) {
            if (!funcStack.isEmpty() && funcStack.peek().parsedArgs == funcStack.peek().funcArgs) {
                funcStack.pop();
                addFuncCall(astStack, operatorStack.pop());
            }

            String token = tokens.get(i);
            switch (token) {
                case "fn":
                    parseFunc(tokens, i);
                    return null;
                case "(":
                    operatorStack.push(token);
                    complexExpr = true;
                    continue;
                case ")":
                    while (!operatorStack.isEmpty()) {
                        String popped = operatorStack.pop();
                        if (popped.equals("(")) break;
                        else addBinOp(astStack, popped);
                    }
                    complexExpr = false;
                    updateFuncStack(funcStack);
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
                            if(!complexExpr) updateFuncStack(funcStack);
                        } else {
                            break;
                        }
                    }
                    operatorStack.push(token);
                    continue;
                default: break;
            }

            if (Character.isAlphabetic(token.charAt(0))) {
                if (funcMap.containsKey(token)) {
                    operatorStack.push("$" + token);
                    funcStack.push(new Pair(0, funcMap.get(token).numArgs));
                } else {
                    astStack.push(new Var(token));
                    if(!complexExpr) updateFuncStack(funcStack);
                }
            } else if (Character.isDigit(token.charAt(0))) {
                astStack.push(new Const(Double.parseDouble(token)));
                if(!complexExpr) updateFuncStack(funcStack);
            }
        }

        while (!operatorStack.isEmpty()) {
            if (!funcStack.isEmpty()) {
                addFuncCall(astStack, operatorStack.pop());
                funcStack.pop();
            } else {
                addBinOp(astStack, operatorStack.pop());
            }
        }

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
            else if (funcMap.containsKey(var.identifier))
                throw new Exception("Invalid identifier. Function with name '"
                        + var.identifier + "' already exists.");
            return varValue;
        } else {
            return ((Const) ast).n;
        }
    }
}
