import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

// Class required
class PrefixDiff {
    
    final private static String  OPS_2_TERMS = "[+*/^-]";
    final private static String  OPS_1_TERM  = String.join("|", Arrays.asList("cos", "sin", "tan", "exp", "ln"));
    final private static String  VARS        = "[a-zA-Z]+";
    final private static String  NUMS        = "-?\\d+";
    final private static String  MISC        = "[(]";
    
    final private static Pattern TOKENIZER   = Pattern.compile(String.join("|",  Arrays.asList(VARS, NUMS, MISC, OPS_1_TERM, OPS_2_TERMS)));
    
    
    public String diff(String expr)  {
        return PrefixDiff.parseExpr(TOKENIZER.matcher(expr), 0)
                         .diff()
                         .simplify()
                         .toString()
                         .replaceAll("\\.0",  ""); 
    }

    private static Expr parseExpr(Matcher m, int i) {
        i++;
        while (m.find()) {
            String tok = m.group();
            
            switch(tok) {
                case "(":   return parseExpr(m, i);
                case "+":   return new Add(parseExpr(m, i), parseExpr(m, i));
                case "-":   return new Sub(parseExpr(m, i), parseExpr(m, i));
                case "*":   return new Mul(parseExpr(m, i), parseExpr(m, i));
                case "/":   return new Div(parseExpr(m, i), parseExpr(m, i));
                case "^":   return new Pow(parseExpr(m, i), parseExpr(m, i));
                case "exp": return new Exp(parseExpr(m, i));
                case "ln":  return new Ln(parseExpr(m, i));
                case "cos": return new Cos(parseExpr(m, i));
                case "sin": return new Sin(parseExpr(m, i));
                case "tan": return new Tan(parseExpr(m, i));
            }
            if (tok.matches(NUMS)) return new Num(tok);
            if (tok.matches(VARS)) return new Var(tok);
        }
        return null;
    }
    
}



interface Expr {
    
    static Expr zero = new Num("0"), one  = new Num("1"), two  = new Num("2");
    
    static Map<String, String> SYMBOL = new HashMap<String,String>() {{
        put("Add", "+");    put("Sub", "-");    put("Mul", "*");    put("Div", "/");    put("Pow", "^");    
        put("Exp", "exp");  put("Ln",  "ln");   put("Neg",  "-");
        put("Cos", "cos");  put("Sin", "sin");  put("Tan", "tan");  
    }};
    
    default String getSymbol()        { return SYMBOL.get(this.getClass().getName());    }
    default Expr throwOverrideError() { throw new RuntimeException(getTrace()); }
    default String getTrace ()        { return String.format("Override lacking in the subclass %s.", this.getClass().getName()); }
    
    default boolean isNum()           { return this instanceof Num; }
    
    default boolean isZero()          {  
        if (!this.isNum()) return false;
        double d = Double.parseDouble(this.toString());
        return Math.abs(d) < 1e-8;
    }
    default boolean isOne()          {  
        if (!this.isNum()) return false;
        double d = Double.parseDouble(this.toString());
        return Math.abs(d-1) < 1e-8;
    }
    
    @Override public String toString();
    Expr diff();
    Expr simplify();
    
}


class Term implements Expr {
    protected String var;
    protected Term(String s) { var = s; }
    @Override public String toString() { return var;  }
    @Override public Expr   simplify() { return this; }
    @Override public Expr   diff()     { return throwOverrideError(); }
}

class Num extends Term {
    public Num(String s)         { super(s); }
    @Override public Expr diff() { return zero; }
}

class Var extends Term {
    public Var(String s)         { super(s); }
    @Override public Expr diff() { return one; }
}




class NonTerm2 implements Expr {
    protected Expr left, right;
    protected NonTerm2(Expr l, Expr r)  { left = l; right = r; }
    
    @Override public String toString()  { return String.format("(%s %s %s)", getSymbol(), left.toString(), right.toString()); }
    @Override public Expr   diff()      { return throwOverrideError(); }
    @Override public Expr   simplify()  { return throwOverrideError(); }
    
    protected Expr eval(Expr l, Expr r) {
        double a = Double.parseDouble(l.toString()),
               b = Double.parseDouble(r.toString()),
               ab = 0;
        switch (this.getClass().getName()) {
            case "Add": ab = a + b;             break;
            case "Sub": ab = a - b;             break;
            case "Mul": ab = a * b;             break;
            case "Div": ab = a / b;             break;
            case "Pow": ab = Math.pow(a, b);    break;
        }
        return new Num(""+ab); 
    }
}

class Add extends NonTerm2 {
    public Add(Expr l, Expr r)   { super(l,r); }
    
    @Override public Expr diff() { return new Add(left.diff(), right.diff()); }
    
    @Override public Expr simplify() {
        Expr sl = left.simplify(), sr = right.simplify();
        return sl.isZero()              ? sr
             : sr.isZero()              ? sl
             : sl.isNum() && sr.isNum() ? eval(sl, sr)
                                        : new Add(sl, sr); 
    }
}

class Sub extends NonTerm2 {
    public Sub(Expr l, Expr r)   { super(l,r); }
    @Override public Expr diff() { return new Sub(left.diff(), right.diff()); }
    
    @Override public Expr simplify() {
        Expr sl = left.simplify(), sr = right.simplify();
        return sl.isZero()              ? sr
             : sr.isZero()              ? new Neg(sl).simplify()
             : sl.isNum() && sr.isNum() ? eval(sl, sr)
                                        : new Add(sl, sr); 
    }
}

class Mul extends NonTerm2 {
    public Mul(Expr l, Expr r)   { super(l,r); }
    @Override public Expr diff() { return new Add(new Mul(left, right.diff()), new Mul(left.diff(), right)); }
    
    @Override public Expr simplify() {
        Expr sl = left.simplify(), sr = right.simplify();
        return sl.isZero() || sr.isZero() ? zero
             : sl.isOne()                 ? sr
             : sr.isOne()                 ? sl
             : sl.isNum() && sr.isNum()   ? eval(sl, sr)
                                          : new Mul(sl, sr);
    }
}

class Div extends NonTerm2 {
    public Div(Expr l, Expr r)   { super(l,r); }
    @Override public Expr diff() { return new Div(new Sub(new Mul(left,        right.diff()),
                                                          new Mul(left.diff(), right)),
                                                  new Pow(right, two)); }
    @Override public Expr simplify() {
        Expr sl = left.simplify(), sr = right.simplify();
        return sl.isZero()              ? zero
             : sr.isOne()               ? sl 
             : sl.isNum() && sr.isNum() ? eval(sl, sr)
                                        : new Div(sl, sr);
    }
}

class Pow extends NonTerm2 {
    public Pow(Expr l, Expr r)   { super(l,r); }
    @Override public Expr diff() { return new Mul(right, new Pow(left, new Sub(right, one))); }
    
    @Override public Expr simplify() {
        Expr sl = left.simplify(), sr = right.simplify();
        return sr.isZero()              ? one
             : sl.isZero()              ? zero
             : sr.isOne()               ? sl
             : sl.isNum() && sr.isNum() ? eval(sl, sr)
                                        : new Pow(sl, sr);
    }
}

class NonTerm1 implements Expr {
    protected Expr val;
    public NonTerm1(Expr e) { val = e; }
    @Override public String toString() { return String.format("(%s %s)", getSymbol(), val.toString()); }
    @Override public Expr   diff()     { return throwOverrideError(); }
    @Override public Expr   simplify() { return throwOverrideError(); }
}

class Tan extends NonTerm1 {
    public Tan(Expr e)                 { super(e); }
    @Override public Expr diff()       { return new Mul(val.diff(), new Add(one, new Pow(new Tan(val), two))); }
    @Override public Expr simplify()   { return new Tan(val.simplify()); }
}

class Sin extends NonTerm1 {
    public Sin(Expr e)                 { super(e); }
    @Override public Expr diff()       { return new Mul(val.diff(), new Cos(val)); }
    @Override public Expr simplify()   { return new Sin(val.simplify()); }
}

class Cos extends NonTerm1 {
    public Cos(Expr e)                 { super(e); }
    @Override public Expr diff()       { return new Mul(new Mul(new Num("-1"), val.diff()), new Sin(val)); }
    @Override public Expr simplify()   { return new Cos(val.simplify()); }
}

class Exp extends NonTerm1 {
    public Exp(Expr e)                 { super(e); }
    @Override public Expr diff()       { return new Mul(val.diff(), new Exp(val)); }
    @Override public Expr simplify()   { return new Exp(val.simplify()); }
}

class Ln extends NonTerm1 {
    public Ln(Expr e)                  { super(e); }
    @Override public Expr diff()       { return new Mul(val.diff(), new Div(one, val)); }
    @Override public Expr simplify()   { return new Ln(val.simplify()); }
}

class Neg extends NonTerm1 {
    public Neg(Expr e)                 { super(e); }
    @Override public Expr diff()       { return new Neg(val.diff()); }
    @Override public Expr simplify()   {
        val = val.simplify();
        return !(val instanceof Num) ? val : new Num("-"+val.toString());
    }
}
______________________________________________
public class PrefixDiff {
    private abstract static class Expression {
        boolean isConst() {
            return this instanceof Constant;
        }

        boolean isConst(int c) {
            return isConst() && asConst() == c;
        }

        double asConst() {
            return ((Constant)this).c;
        }

        Expression multiply(Expression multiplier) {
            return new BinaryFunction(BinaryOp.MULTIPLICATION, this, multiplier);
        }

        Expression add(Expression addend) {
            return new BinaryFunction(BinaryOp.ADDITION, this, addend);
        }

        Expression subtract(Expression subtrahend) {
            return new BinaryFunction(BinaryOp.SUBTRACTION, this, subtrahend);
        }

        Expression divide(Expression divisor) {
            return new BinaryFunction(BinaryOp.DIVISION, this, divisor);
        }

        Expression raise(Expression power) {
            return new BinaryFunction(BinaryOp.POWER, this, power);
        }

        abstract Expression derivative();

        Expression simplify() {
            return this;
        }
    }

    private static Constant cnst(double c) {
        return new Constant(c);
    }

    private static class Constant extends Expression {
        final double c;

        Constant(double c) {
            this.c = c;
        }

        @Override
        Expression derivative() {
            return cnst(0);
        }

        @Override
        public String toString() {
            int ic = (int)c;
            return c == ic ? Integer.toString(ic) : Double.toString(c);
        }
    }

    private static class Variable extends Expression {
        @Override
        Expression derivative() {
            return cnst(1);
        }

        @Override
        public String toString() {
            return "x";
        }
    }

    private enum UnaryOp {
        SIN("sin"), COS("cos"), TAN("tan"), EXP("exp"), LN("ln");

        final String str;

        UnaryOp(String str) {
            this.str = str;
        }

        @Override
        public String toString() {
            return str;
        }
    }

    private static class UnaryFunction extends Expression {
        final UnaryOp op;
        final Expression arg;

        UnaryFunction(UnaryOp op, Expression arg) {
            this.op = op;
            this.arg = arg;
        }

        @Override
        Expression derivative() {
            Expression opDer;
            switch (op) {
                case SIN:
                    opDer = new UnaryFunction(UnaryOp.COS, arg);
                    break;
                case COS:
                    opDer = cnst(-1).multiply(new UnaryFunction(UnaryOp.SIN, arg));
                    break;
                case TAN:
                    opDer = cnst(1).divide(new UnaryFunction(UnaryOp.COS, arg).raise(cnst(2)));
                    break;
                case EXP:
                    opDer = this;
                    break;
                case LN:
                    opDer = cnst(1).divide(arg);
                    break;
                default:
                    return null;
            }
            return arg.derivative().multiply(opDer);
        }

        @Override
        Expression simplify() {
            Expression sarg = arg.simplify();
            return sarg == arg ? this : new UnaryFunction(op, sarg);
        }

        @Override
        public String toString() {
            return "(" + op + " " + arg + ")";
        }
    }

    private enum BinaryOp {
        ADDITION("+"), SUBTRACTION("-"), MULTIPLICATION("*"), DIVISION("/"), POWER("^");

        final String str;

        BinaryOp(String str) {
            this.str = str;
        }

        @Override
        public String toString() {
            return str;
        }
    }

    private static class BinaryFunction extends Expression {
        final BinaryOp op;
        final Expression arg1;
        final Expression arg2;

        BinaryFunction(BinaryOp op, Expression arg1, Expression arg2) {
            this.op = op;
            this.arg1 = arg1;
            this.arg2 = arg2;
        }

        @Override
        Expression derivative() {
            switch (op) {
                case ADDITION:
                    return arg1.derivative().add(arg2.derivative());
                case SUBTRACTION:
                    return arg1.derivative().subtract(arg2.derivative());
                case MULTIPLICATION:
                    return arg1.derivative().multiply(arg2).add(arg1.multiply(arg2.derivative()));
                case DIVISION:
                    return arg1.derivative().multiply(arg2).subtract(arg1.multiply(arg2.derivative()))
                        .divide(arg2.raise(cnst(2)));
                case POWER:
                    return arg1.derivative().multiply(arg2).multiply(arg1.raise(arg2.subtract(cnst(1))))
                        .add(arg2.derivative().multiply(new UnaryFunction(UnaryOp.LN, arg1).multiply(this)));
                default:
                    return null;
            }
        }

        @Override
        Expression simplify() {
            Expression sarg1 = arg1.simplify();
            Expression sarg2 = arg2.simplify();
            boolean bothConst = sarg1.isConst() && sarg2.isConst();
            switch (op) {
                case ADDITION:
                    if (sarg1.isConst(0))
                        return sarg2;
                    if (sarg2.isConst(0))
                        return sarg1;
                    if (bothConst)
                        return cnst(sarg1.asConst() + sarg2.asConst());
                    break;
                case SUBTRACTION:
                    if (sarg1.isConst(0))
                        return cnst(-1).multiply(sarg2).simplify();
                    if (sarg2.isConst(0))
                        return sarg1;
                    if (bothConst)
                        return cnst(sarg1.asConst() - sarg2.asConst());
                    break;
                case MULTIPLICATION:
                    if (sarg1.isConst(0) || sarg2.isConst(0))
                        return cnst(0);
                    if (sarg1.isConst(1))
                        return sarg2;
                    if (sarg2.isConst(1))
                        return sarg1;
                    if (bothConst)
                        return cnst(sarg1.asConst() * sarg2.asConst());
                    if (sarg1.isConst() && sarg2 instanceof BinaryFunction) {
                        double c = sarg1.asConst();
                        BinaryFunction bf = (BinaryFunction)sarg2;
                        if (bf.op == BinaryOp.MULTIPLICATION) {
                            if (bf.arg1.isConst())
                                return cnst(c * bf.arg1.asConst()).multiply(bf.arg2);
                            if (bf.arg2.isConst())
                                return cnst(c * bf.arg2.asConst()).multiply(bf.arg1);
                        } else if (bf.op == BinaryOp.DIVISION) {
                            if (bf.arg1.isConst())
                                return cnst(c * bf.arg1.asConst()).divide(bf.arg2);
                            if (bf.arg2.isConst())
                                return cnst(c / bf.arg2.asConst()).multiply(bf.arg1);
                        }
                    }
                    break;
                case DIVISION:
                    if (sarg1.isConst(0))
                        return cnst(0);
                    if (sarg2.isConst(1))
                        return sarg1;
                    if (bothConst)
                        return cnst(sarg1.asConst() / sarg2.asConst());
                    break;
                case POWER:
                    if (sarg2.isConst(0))
                        return cnst(1);
                    if (sarg2.isConst(1))
                        return sarg1;
                    if (bothConst)
                        return cnst(Math.pow(sarg1.asConst(), sarg2.asConst()));
                    break;
                default:
                    break;
            }
            return sarg1 == arg1 && sarg2 == arg2 ? this : new BinaryFunction(op, sarg1, sarg2);
        }

        @Override
        public String toString() {
            return "(" + op + " " + arg1 + " " + arg2 + ")";
        }
    }

    private static class Parser {
        final String s;
        final int end;
        int i;

        Parser(String s) {
            this.s = s;
            end = s.length();
        }

        void error() {
            throw new IllegalArgumentException("Wrong expression: " + s);
        }

        void checkChar(char c) {
            if (i == end || s.charAt(i) != c)
                error();
            i++;
        }

        Expression parseArg() {
            if (i == end)
                error();
            char ch = s.charAt(i++);
            if (ch == '(') {
                for (UnaryOp op : UnaryOp.values())
                    if (s.startsWith(op.str, i)) {
                        i += op.str.length();
                        checkChar(' ');
                        Expression arg = parseArg();
                        checkChar(')');
                        return new UnaryFunction(op, arg);
                    }
                for (BinaryOp op : BinaryOp.values())
                    if (s.startsWith(op.str, i)) {
                        i += op.str.length();
                        checkChar(' ');
                        Expression arg1 = parseArg();
                        checkChar(' ');
                        Expression arg2 = parseArg();
                        checkChar(')');
                        return new BinaryFunction(op, arg1, arg2);
                    }
                error();
                return null;
            } else if (ch == 'x')
                return new Variable();
            else {
                int j = i;
                while (j < end) {
                    ch = s.charAt(j);
                    if (ch == ' ' || ch == ')')
                        break;
                    j++;
                }
                double c = 0;
                try {
                    c = Double.parseDouble(s.substring(i - 1, j));
                } catch (NumberFormatException e) {
                    error();
                }
                i = j;
                return cnst(c);
            }
        }

        Expression parse() {
            Expression e = parseArg();
            if (i != end)
                error();
            return e;
        }
    }

    public static String diff(String expr) {
        return new Parser(expr).parse().derivative().simplify().toString();
    }
}
______________________________________________
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.function.BiFunction;


class PrefixDiff {

    interface MathOp{
        MathOp differentiate();
        MathOp simplify();
        @Override
        String toString();
    }

    private static Pattern tokens = Pattern.compile("\\(([*/^+\\-]) (\\(.+\\)|[\\-0-9.x]+) (\\(.+\\)|[\\-0-9.x]+)|((sin|cos|tan|exp|ln) (\\(.+\\)|[\\-0-9.x]+))\\)");
    private final Argument MINUSONE= new Argument("-1");
    private final Argument ZERO = new Argument("0");
    private final Argument ONE = new Argument("1");
    private final Argument TWO = new Argument("2");
    private final Argument VAR = new Argument("x");

    private enum Operator {
        MULTIPLICATION("*",((l, r) -> l * r)),
        ADDITION("+", ((l, r) -> l + r)),
        SUBTRACTION("-", ((l, r) -> l - r)),
        DIVISION("/", ((l, r) -> l / r)),
        POWER("^", (Math::pow));

        private String desc;
        private BiFunction<Double, Double, Double> func;

        Operator(String text, BiFunction<Double, Double, Double> func) {
            this.desc = text;
            this.func = func;
        }

        public String getDesc(){
            return this.desc;
        }

        public Double applyFunc(double x, double y){
            return this.func.apply(x, y);
        }

        public static Operator fromString(String text) {
            for (Operator oper : Operator.values()) {
                if (oper.getDesc().equalsIgnoreCase(text)) {
                    return oper;
                }
            }
            return null;
        }
    }

    private enum Func {
        SIN("sin"),
        COS("cos"),
        TAN("tan"),
        LN("ln"),
        EXP("exp");

        private String desc;

        Func(String text) {
            this.desc = text;
        }

        public String getDesc(){
            return this.desc;
        }

        public static Func fromString(String text) {
            for (Func fun : Func.values()) {
                if (fun.getDesc().equalsIgnoreCase(text)) {
                    return fun;
                }
            }
            return null;
        }
    }

    class Operation implements MathOp{
        private Operator operator;
        private MathOp op1;
        private MathOp op2;

        public Operation(Operator operator, MathOp op1, MathOp op2){
            this.operator = operator;
            this.op1 = op1;
            this.op2 = op2;
        }

        @Override
        public MathOp differentiate() {
            switch(this.operator){
                case MULTIPLICATION:
                    return new Operation(Operator.ADDITION,
                            new Operation(Operator.MULTIPLICATION, this.op1.differentiate(), this.op2),
                            new Operation(Operator.MULTIPLICATION, this.op1, this.op2.differentiate()));
                case ADDITION:
                    return new Operation(Operator.ADDITION, this.op1.differentiate(), this.op2.differentiate());
                case SUBTRACTION:
                    return new Operation(Operator.SUBTRACTION, this.op1.differentiate(), this.op2.differentiate());
                case DIVISION:
                    return new Operation(Operator.DIVISION, new Operation(Operator.SUBTRACTION,
                        new Operation(Operator.MULTIPLICATION, this.op1.differentiate(), this.op2),
                        new Operation(Operator.MULTIPLICATION, this.op1, this.op2.differentiate())),
                            new Operation(Operator.POWER, this.op2, TWO));
                case POWER:
                    return new Operation(Operator.MULTIPLICATION, this.op2, new Operation(Operator.POWER, this.op1,
                                    new Argument(String.valueOf(Integer.parseInt(((Argument) this.op2).getArg()) - 1))));
            }

            return null;
        }

        @Override
        public MathOp simplify() {
            this.op1 = this.op1.simplify();
            this.op2 = this.op2.simplify();
            Argument tmp1, tmp2;
            if (isArgument(this.op1)){
                tmp1 = (Argument) this.op1;
                if (tmp1.isZero() && (this.operator.equals(Operator.POWER) ||
                        this.operator.equals(Operator.DIVISION) || this.operator.equals(Operator.MULTIPLICATION)))
                    return ZERO;
                if(tmp1.isOne() && this.operator.equals(Operator.MULTIPLICATION) ||
                        tmp1.isZero() && this.operator.equals(Operator.ADDITION))
                    return this.op2;
                if(tmp1.isOne() && this.operator.equals(Operator.POWER))
                    return ONE;
            }
            if (isArgument(this.op2)) {
                tmp2 = (Argument) this.op2;
                if (tmp2.isZero() && this.operator.equals(Operator.MULTIPLICATION))
                    return ZERO;
                if (tmp2.isOne() && (this.operator.equals(Operator.MULTIPLICATION) || this.operator.equals(Operator.POWER)) ||
                        tmp2.isZero() && (this.operator.equals(Operator.ADDITION) || this.operator.equals(Operator.SUBTRACTION)))
                    return this.op1;
                if((tmp2.isZero()) && this.operator.equals(Operator.POWER))
                    return ONE;
            }
            if (isArgument(this.op1) && isArgument(this.op2)){
                tmp1 = (Argument) this.op1;
                tmp2 = (Argument) this.op2;
                if (tmp1.isConstant() && tmp2.isConstant()) {
                    return tmp1.reduce2args(tmp2, this.operator);
                }
            }
            return this;
        }

        @Override
        public String toString(){
            return String.format("(%s %s %s)", this.operator.getDesc(), this.op1.toString(), this.op2.toString());
        }
    }

    class Function implements MathOp{
        private Func function;
        private MathOp op;

        public Function(Func function, MathOp op){
            this.function = function;
            this.op = op;
        }

        @Override
        public MathOp differentiate() {
            switch(this.function) {
                case SIN:
                    return new Operation(Operator.MULTIPLICATION, this.op.differentiate(), new Function(Func.COS, this.op));
                case COS:
                    return new Operation(Operator.MULTIPLICATION, this.op.differentiate(),
                            new Operation(Operator.MULTIPLICATION, MINUSONE, new Function(Func.SIN, this.op)));
                case TAN:
                    return new Operation(Operator.MULTIPLICATION, this.op.differentiate(), new Operation(Operator.ADDITION, ONE,
                            new Operation(Operator.POWER, new Function(Func.TAN, this.op), TWO)));
                case LN:
                    return new Operation(Operator.MULTIPLICATION, this.op.differentiate(), new Operation(Operator.DIVISION, ONE, this.op));
                case EXP:
                    return new Operation(Operator.MULTIPLICATION, this.op.differentiate(), this);
            }
            return null;
        }

        @Override
        public MathOp simplify() {
            this.op = this.op.simplify();
            return this;
        }

        @Override
        public String toString(){
            return String.format("(%s %s)", this.function.getDesc(), this.op.toString());
        }
    }

    class Argument implements MathOp{
        private String arg;

        public Argument(String arg){
            this.arg = arg;
        }

        @Override
        public MathOp differentiate() {
            if(this.equals(VAR))
                return ONE;
            else
                return ZERO;
        }

        @Override
        public MathOp simplify() {
            return this;
        }

        @Override
        public String toString(){
            return this.arg;
        }

        public Argument reduce2args(Argument arg2, Operator opearation){
            double d = opearation.applyFunc(Double.parseDouble(this.arg), Double.parseDouble(arg2.getArg()));
            if((d % 1) == 0)
                return new Argument(String.valueOf((int) d));
            else
                return new Argument(String.valueOf(d));
        }

        public boolean isZero(){
            return this.equals(ZERO);
        }

        public boolean isOne(){
            return this.equals(ONE);
        }

        public boolean isConstant(){
            return !this.equals(VAR);
        }

        public String getArg(){
            return this.arg;
        }

        public boolean equals(Argument other) {
            return this.arg.equals(other.getArg());
        }
    }

    private boolean isArgument(MathOp mop){
        return mop.getClass() == Argument.class;
    }

    public MathOp parse(String expr) {
        Matcher m = tokens.matcher(expr);
        if (m.find()){
            if(m.group(1) != null){
                return new Operation(Operator.fromString(m.group(1)), parse(m.group(2)), parse(m.group(3)));
            }else if(m.group(4) != null){
                return new Function(Func.fromString(m.group(5)), parse(m.group(6)));
            }
        }
        return new Argument(expr);
    }

    public String diff(String expr) {
        MathOp res = parse(expr).differentiate();
        res = res.simplify();
        return res.toString();
    }
}
