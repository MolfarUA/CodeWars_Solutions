namespace CompilerKata
{
    using System;
    using System.Linq;
    using System.Text.RegularExpressions;
    using System.Collections.Generic;

    public class Compiler
    {
        public class Source
        {
            private readonly Dictionary<string, int> _args = new Dictionary<string, int>();
            private readonly IReadOnlyList<string> _tokens;
            private int _pos;
            
            public Source(IReadOnlyList<string> tokens)
            {
                _tokens = tokens;
                _pos = tokens.Count - 1;

                for (var idx = 1; _tokens[idx] != "]"; ++idx) _args[_tokens[idx]] = _args.Count;
            }

            public string Next() => _tokens[_pos--];

            public string Current => _tokens[_pos];

            public int GetArg(string name) => _args[name];
        }

        public Ast Factor(Source source)
        {
            var value = source.Next();
            if (value == ")")
            {
                var result = Expression(source);
                source.Next();
                return result;
            }
            return int.TryParse(value, out var number) ?new UnOp("imm", number) : new UnOp("arg", source.GetArg(value));
        }

        public Ast Term(Source source)
        {
            var factor = Factor(source);
            return "*/".Contains(source.Current) ? new BinOp(source.Next(), Term(source), factor) : factor;
        }

        public Ast Expression(Source source)
        {
            var term = Term(source);
            return "+-".Contains(source.Current) ? new BinOp(source.Next(), Expression(source), term) : term;
        }

        private void Pop(List<string> code)
        {
            if (code.Last() == "PU") code.RemoveAt(code.Count - 1); else code.Add("PO");
        }

        private void GenerateAsm(Ast ast, List<string> code)
        {
            if(ast is UnOp unOp)
            {
                switch(unOp.op())
                {
                    case "imm": code.Add($"IM {unOp.n()}"); break;
                    case "arg": code.Add($"AR {unOp.n()}"); break;
                }

                code.Add("PU");
            }
            else if (ast is BinOp binOp)
            {
                GenerateAsm(binOp.a(), code);
                GenerateAsm(binOp.b(), code);

                Pop(code);
                code.Add("SW");
                Pop(code);
                switch (binOp.op())
                {
                    case "+": code.Add("AD"); break;
                    case "-": code.Add("SU"); break;
                    case "*": code.Add("MU"); break;
                    case "/": code.Add("DI"); break;
                }

                code.Add("PU");
            }
        }

        public Ast pass1(string prog) => Expression(new Source(tokenize(prog)));

        public Ast pass2(Ast ast)
        {
            if (ast is BinOp binOp)
            {
                var a = pass2(binOp.a());
                var b = pass2(binOp.b());

                if(a is UnOp uOp1 && b is UnOp uOp2 && a.op() == "imm" && b.op() == "imm")
                {
                    switch(binOp.op())
                    {
                        case "*": return new UnOp("imm", uOp1.n() * uOp2.n());
                        case "/": return new UnOp("imm", uOp1.n() / uOp2.n());
                        case "+": return new UnOp("imm", uOp1.n() + uOp2.n());
                        case "-": return new UnOp("imm", uOp1.n() - uOp2.n());
                    }
                }

                return new BinOp(binOp.op(), a, b);
            }

            return ast;
        }

        public List<string> pass3(Ast ast)
        {
            var result = new List<string>();
            GenerateAsm(ast, result);
            Pop(result);
            return result;
        }

        private List<string> tokenize(string input)
        {
            var tokens = new List<string>();
            var rgxMain = new Regex("\\[|\\]|[-+*/=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            var matches = rgxMain.Matches(input);
            foreach (Match m in matches) tokens.Add(m.Groups[0].Value);
            return tokens;
        }
    }
}
  
#######################
namespace CompilerKata
 {
   using System;
   using System.Text.RegularExpressions;
   using System.Collections.Generic;
   using System.Linq;
      
   public class Compiler
   {
   class Token
    {
        public enum Type
        {
            Number,
            Variable,
            Operator,
            Block
        }

        public Type type;
        public List<Token> tokens;
        public string value;

        public Token(Type type, string value)
        {
            this.type = type;
            this.value = value;
        }

        public static bool IsOperator(char smb) => smb == '+' || smb == '-' || smb == '*' || smb == '/';
        public static bool IsNumber(string val)
        {
            int tmp;
            return int.TryParse(val, out tmp);
        }
    }
    
    class Block
    {
        public static bool IsSimple(Ast ast) => !IsOp(ast._a._op);
        public static bool IsComplex(Ast ast) => IsOp(ast._a._op) && IsOp(ast._b._op);
        public static bool NeedInversion(string op) => op == "/" || op == "-";

        public static string TokenToASM(Ast ast)
        {
            if (ast._op == "arg")
                return $"AR {ast._n}";

            return $"IM {ast._n}";
        }
        
        public static string OperatorToASM(string op)
        {
          switch(op)
          {
              case "+": return "AD";
              case "-": return "SU";
              case "*": return "MU";
              case "/": return "DI";
          }
          return null;
        }
    }
    
    private string[] arguments;
    private Token expression;
    private List<string> ExpASM;
    
    private int GetVariableIndex(string name)
        {
            for (int now = 0; now < arguments.Length; ++now)
                if (arguments[now] == name)
                    return now;
            return -1;
        }
    
     public Ast pass1(string prog)
     {
        Match match = Regex.Match(prog, @"^\[ (?<arguments>[a-zA-Z ]+) \] (?<expression>.*)$", RegexOptions.IgnoreCase);
        arguments = match.Groups["arguments"].Value.Split();
        string exp = match.Groups["expression"].Value;

        expression = new Token(Token.Type.Block, null);
        expression.tokens = GenerateTokens(exp + ' ');
        
        GenerateActionTree(expression);
        
        return GenAst(expression);
     }
     
     private Ast GenAst(Token ex)
     {
       Ast left, right;
       
       if ( ex.tokens[0].type == Token.Type.Block )
         left = GenAst( ex.tokens[0] );
       else if ( ex.tokens[0].type == Token.Type.Variable )
         left = new UnOp("arg", int.Parse( ex.tokens[0].value ) );
       else
         left = new UnOp("imm", int.Parse( ex.tokens[0].value ) );
       
       if ( ex.tokens[2].type == Token.Type.Block )
         right = GenAst( ex.tokens[2] );
       else if ( ex.tokens[2].type == Token.Type.Variable )
         right = new UnOp("arg", int.Parse( ex.tokens[2].value ) );
       else
         right = new UnOp("imm", int.Parse( ex.tokens[2].value ) );
         
       return new BinOp( ex.tokens[1].value, left, right );
     }
     
     private void GenerateActionTree(Token token)
        {
            for (int now = 0; now < token.tokens.Count; ++now)
                if (token.tokens[now].type == Token.Type.Block)
                    GenerateActionTree(token.tokens[now]);

            for (int now = 1; now < token.tokens.Count - 1;)
            {
                if(token.tokens.Count == 3) break;

                var val = token.tokens[now].value;
                if(val == "*" || val == "/")
                {
                    var block = new Token(Token.Type.Block, null);
                    block.tokens = new List<Token>(3);
                    block.tokens.Add(token.tokens[now - 1]);
                    block.tokens.Add(token.tokens[now]);
                    block.tokens.Add(token.tokens[now + 1]);

                    token.tokens[now - 1] = block;

                    token.tokens.RemoveAt(now);
                    token.tokens.RemoveAt(now);
                }
                else now += 2;
            }

            for (int now = 1; now < token.tokens.Count - 1;)
            {
                if(token.tokens.Count == 3) break;

                var val = token.tokens[now].value;
                if(val == "+" || val == "-")
                {
                    var block = new Token(Token.Type.Block, null);
                    block.tokens = new List<Token>(3);
                    block.tokens.Add(token.tokens[now - 1]);
                    block.tokens.Add(token.tokens[now]);
                    block.tokens.Add(token.tokens[now + 1]);

                    token.tokens[now - 1] = block;

                    token.tokens.RemoveAt(now);
                    token.tokens.RemoveAt(now);
                }
                else now += 2;
            }
        }
     
     public Ast pass2(Ast ast)
     {
       RecSmp(ast);
       return new BinOp( ast._op, ast._a, ast._b);
     }
     
     private Ast RecSmp(Ast ast)
     {
       if ( IsOp(ast._a._op) ) ast._a = RecSmp(ast._a);
       if ( IsOp(ast._b._op) ) ast._b = RecSmp(ast._b);
       
       ast = new BinOp(ast._op, ast._a, ast._b);
       
       if ( ast._a._op == "imm" && ast._b._op == "imm" )
       {
         switch( ast._op ) {
           case "+": ast = new UnOp( "imm", ast._a._n + ast._b._n ); break;
           case "-": ast = new UnOp( "imm", ast._a._n - ast._b._n ); break;
           case "*": ast = new UnOp( "imm", ast._a._n * ast._b._n ); break;
           case "/": ast = new UnOp( "imm", ast._a._n / ast._b._n ); break;
         }
       }
       return ast;
     }
     
     private static bool IsOp(string op) => op != "imm" && op != "arg";
     
     
     public List<string> pass3(Ast ast)
     {
       ExpASM = new List<string>(50);
       ParseTree(ast);
       return ExpASM;
     }
     
     private void ParseTree(Ast ast)
        {
            if (Block.IsSimple(ast))
            {
                if( IsOp(ast._b._op) )
                {
                    ParseTree(ast._b);
                }
                else
                {
                    ExpASM.Add(Block.TokenToASM(ast._b));
                    ExpASM.Add("SW");
                    ExpASM.Add(Block.TokenToASM(ast._a));
                }
            }
            else if(Block.IsComplex(ast))
            {
                ParseTree(ast._a);
                ExpASM.Add("PUSH");
                ParseTree(ast._b);
                ExpASM.Add("SW");
                ExpASM.Add("POP");
            }
            else
            {
                ParseTree(ast._a);
                ExpASM.Add("SW");
                ExpASM.Add(Block.TokenToASM(ast._b));
                if(Block.NeedInversion(ast._op))
                    ExpASM.Add("SW");
            }

            ExpASM.Add(Block.OperatorToASM(ast._op));
        }
     
     private List<Token> GenerateTokens(string exp)
     {
       var list = new List<Token>(100);

        string buffer = "";
        int level = 0;
        bool parse;
  
        char smb, nextSmb;
  
        for (int now = 0; now < exp.Length - 1; ++now)
        {
            parse = false;
  
            smb = exp[now];
            nextSmb = now == exp.Length - 2 ? (char)0 : exp[now + 1];
  
            if (smb == ' ' && level == 0) continue;
            buffer += smb;
  
            if (nextSmb == (char)0) parse = true;
            if (nextSmb == '(' || nextSmb == ')') parse = true;
            if (nextSmb == ' ') parse = true;
            if (Token.IsOperator(nextSmb)) parse = true;
  
            if (smb == '(')
            {
                if (level == 0) buffer = "";
                ++level;
            }
            else if (smb == ')')
            {
                --level;
                if (level == -1) throw new Exception("Unexpected closing bracket ')'");
  
                if (level == 0)
                {
                    var token = new Token(Token.Type.Block, null);
                    token.tokens = GenerateTokens(buffer);
                    list.Add(token);
                    buffer = "";
                    continue;
                }
            }
  
            if (level != 0) continue;
  
            if (Token.IsOperator(smb))
            {
                list.Add(new Token(Token.Type.Operator, smb.ToString()));
                buffer = "";
                continue;
            }
  
            if (parse && buffer != "")
            {
                if (Token.IsNumber(buffer))
                    list.Add(new Token(Token.Type.Number, buffer));
                else
                    list.Add(new Token(Token.Type.Variable, GetVariableIndex(buffer).ToString()));
                buffer = "";
            }
        }
  
        return list;
     }
   }
 }
 
####################
namespace CompilerKata
{
    using System;
    using System.Text.RegularExpressions;
    using System.Collections.Generic;
    using System.Linq;

    public class Compiler
    {
        public Ast pass1(string prog)
        {
            var tokens = tokenize(prog);
            var args = new List<string>();
            int idx = 0; 

            if (tokens[0] == "[")
            {
                args.AddRange(tokens.Skip(1).TakeWhile(tk => tk != "]").ToList());
                idx = args.Count + 2;
            }

            var outputQueue = new Queue<string>();
            var operatorStack = new Stack<string>();

            foreach (var token in tokens.Skip(idx))
            {
                switch (token)
                {
                    case "+":
                    case "-":
                        while (operatorStack.Count != 0 &&
                               operatorStack.Peek() != "(")
                            outputQueue.Enqueue(operatorStack.Pop());
                        operatorStack.Push(token);
                        break;
                    case "*":
                    case "/":
                        while (operatorStack.Count != 0 &&
                               (operatorStack.Peek() == "*" || operatorStack.Peek() == "/") &&
                               operatorStack.Peek() != "(")
                            outputQueue.Enqueue(operatorStack.Pop());
                        operatorStack.Push(token);
                        break;
                    case "(":
                        operatorStack.Push(token);
                        break;
                    case ")":
                        while (operatorStack.Peek() != "(")
                            outputQueue.Enqueue(operatorStack.Pop());
                        operatorStack.Pop();
                        break;
                    default:
                        outputQueue.Enqueue(token);
                        break;
                }
            }

            while (operatorStack.Count != 0)
                outputQueue.Enqueue(operatorStack.Pop());

            var stack = new Stack<Ast>();

            while (outputQueue.Count != 0)
            {
                var token = outputQueue.Dequeue();
                switch (token)
                {
                    case "+":
                    case "-":
                    case "*":
                    case "/":
                        var b = stack.Pop();
                        var a = stack.Pop();
                        stack.Push(new BinOp(token, a, b));
                        break;
                    default:
                        if (args.Contains(token))
                            stack.Push(new UnOp("arg", args.FindIndex(tk => tk == token)));
                        else
                            stack.Push(new UnOp("imm", int.Parse(token)));
                        break;
                }
            }

            return stack.Pop();
        }

        public Ast pass2(Ast ast)
        {
            switch (ast.op())
            {
                case "imm":
                case "arg":
                    return ast;

                default:
                    var binOp = (BinOp)ast;
                    var a = pass2(binOp.a());
                    var b = pass2(binOp.b());
                    if (a.op() == "imm" && b.op() == "imm")
                        switch (binOp.op())
                        {
                            case "+": return new UnOp("imm", ((UnOp)a).n() + ((UnOp)b).n());
                            case "-": return new UnOp("imm", ((UnOp)a).n() - ((UnOp)b).n());
                            case "*": return new UnOp("imm", ((UnOp)a).n() * ((UnOp)b).n());
                            case "/": return new UnOp("imm", ((UnOp)a).n() / ((UnOp)b).n());
                            default: return null;
                        }
                    else
                        return new BinOp(binOp.op(), a, b);
            }
        }

        public List<string> pass3(Ast ast)
        {
            var instructions = new List<string>();
            switch (ast.op())
            {
                case "arg": instructions.Add(string.Format("AR {0}", ((UnOp)ast).n())); break;
                case "imm": instructions.Add(string.Format("IM {0}", ((UnOp)ast).n())); break;
                default:
                    var binOp = (BinOp)ast;
                    bool aDoesntUseStack = binOp.a().op() == "imm" || binOp.a().op() == "arg";
                    bool bDoesntUseStack = binOp.b().op() == "imm" || binOp.b().op() == "arg";
                    if (aDoesntUseStack)
                    {
                        instructions.AddRange(pass3(binOp.b()));
                        instructions.Add("SW");
                        instructions.AddRange(pass3(binOp.a()));
                    }
                    else if (bDoesntUseStack)
                    {
                        instructions.AddRange(pass3(binOp.a()));
                        instructions.Add("SW");
                        instructions.AddRange(pass3(binOp.b()));
                        instructions.Add("SW");
                    }
                    else
                    {
                        instructions.AddRange(pass3(binOp.a()));
                        instructions.Add("PU");
                        instructions.AddRange(pass3(binOp.b()));
                        instructions.Add("SW");
                        instructions.Add("PO");
                    }
                    switch (binOp.op())
                    {
                        case "+": instructions.Add("AD"); break;
                        case "-": instructions.Add("SU"); break;
                        case "*": instructions.Add("MU"); break;
                        case "/": instructions.Add("DI"); break;
                    }
                    break;
            }
            return instructions;
        }

        private List<string> tokenize(string input)
        {
            List<string> tokens = new List<string>();
            Regex rgxMain = new Regex("\\[|\\]|[-+*/=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            MatchCollection matches = rgxMain.Matches(input);
            foreach (Match m in matches) tokens.Add(m.Groups[0].Value);
            return tokens;
        }
    }
}
  
######################
 namespace CompilerKata
 {
   using System;
   using System.Text.RegularExpressions;
   using System.Collections.Generic;
   using static CompilerKata.AstFunc;
      
   public partial class Compiler
    {
        public Ast pass1(string prog)
        {
            List<string> tokens = tokenize(prog);
            var index = tokens.IndexOf("]") + 1;
            return Expression.Expr(tokens.GetRange(index, tokens.Count - index), tokens.GetRange(1, tokens.IndexOf("]") - 1));
        }

        public Ast pass2(Ast ast)
            => CombineImm.Combine(ast);

        public List<string> pass3(Ast ast)
            => new List<string>(Assembly.Convert(ast, new Queue<string>()));

        private List<string> tokenize(string input)
        {
            List<string> tokens = new List<string>();
            Regex rgxMain = new Regex("\\[|\\]|[-+*/=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            MatchCollection matches = rgxMain.Matches(input);
            foreach (Match m in matches) tokens.Add(m.Groups[0].Value);
            return tokens;
        }
    }
    
   class Assembly
   {
       public static Queue<string> Convert(Ast ast, Queue<string> codes)
       {
           if (ast is UnOp)
               codes.Enqueue((ast.op() == "imm" ? "IM" : "AR") + (ast as UnOp).n().ToString(), "PU");
           else
           {
               Convert((ast as BinOp).a(), codes);
               Convert((ast as BinOp).b(), codes);
               codes.Enqueue("PO", "SW", "PO");
               switch ((Compiler.Token)ast.op()[0])
               {
                   case Compiler.Token.PLUS:
                       codes.Enqueue("AD");
                       break;
                   case Compiler.Token.MINUS:
                       codes.Enqueue("SU");
                       break;
                   case Compiler.Token.MUL:
                       codes.Enqueue("MU");
                       break;
                   case Compiler.Token.DIV:
                       codes.Enqueue("DI");
                       break;
               }
               codes.Enqueue("PU");
           }
           return codes;
       }
   }
   
    public class AstFunc
    {
        public static Ast Plus(Ast a, Ast b)
            => new BinOp("+", a, b);
        public static Ast Minus(Ast a, Ast b)
            => new BinOp("-", a, b);
        public static Ast Mul(Ast a, Ast b)
            => new BinOp("*", a, b);
        public static Ast Div(Ast a, Ast b)
            => new BinOp("/", a, b);
        public static Ast Arg(List<string> args, string arg)
            => new UnOp("arg", args.IndexOf(arg));
        public static Ast Imm(int i)
            => new UnOp("imm", i);
    }
    
    /*
    internal class BinOp : Ast
    {
        public Ast A;
        public Ast B;

        public Ast a() => A;
        public Ast b() => B;

        public BinOp(string op, Ast a, Ast b)
        {
            this.Op = op;
            this.A = a;
            this.B = b;
        }
    }
    */
    
    class CombineImm
    {
        public static Ast Combine(Ast ast)
        {
            if (ast is UnOp)
                return ast;
            var binAst = ast as BinOp;
            if (binAst.a() is BinOp)
                ast = new BinOp(ast.op(),Combine(binAst.a()),binAst.b());
                binAst = ast as BinOp;
            if (binAst.b() is BinOp)
                ast = new BinOp(ast.op(),binAst.a(),Combine(binAst.b()));
                binAst = ast as BinOp;
            if (binAst.a() is UnOp && binAst.b() is UnOp && (binAst.a() as UnOp).op() == "imm" && (binAst.b() as UnOp).op()=="imm")
            {
                switch ((Compiler.Token)binAst.op()[0])
                {
                    case Compiler.Token.PLUS:
                        ast = new UnOp("imm", (binAst.a() as UnOp).n() + (binAst.b() as UnOp).n());
                        break;
                    case Compiler.Token.MINUS:
                        ast = new UnOp("imm", (binAst.a() as UnOp).n() - (binAst.b() as UnOp).n());
                        break;
                    case Compiler.Token.MUL:
                        ast = new UnOp("imm", (binAst.a() as UnOp).n() * (binAst.b() as UnOp).n());
                        break;
                    case Compiler.Token.DIV:
                        ast = new UnOp("imm", (binAst.a() as UnOp).n() / (binAst.b() as UnOp).n());
                        break;
                    default:
                        break;
                }
            }
            return ast;
        }
    }
    
        class Expression
    {
        public static Ast Expr(List<string> tokens, List<string> args)
        {
            var left = Term(tokens,args);
            while (true)
            {
                var token = tokens.TakeToken();
                switch (token.Token)
                {
                    case Compiler.Token.PLUS:
                        left = Plus(left, Term(tokens,args));
                        break;
                    case Compiler.Token.MINUS:
                        left = Minus(left, Term(tokens,args));
                        break;
                    default:
                        return left;
                }
            }
        }

        private static Ast Term(List<String> tokens,List<string> args)
        {
            var left = Prim(tokens,args);
            while (true)
            {
                var token = tokens.TakeToken();
                switch (token.Token)
                {
                    case Compiler.Token.MUL:
                        left = Mul(left, Prim(tokens,args));
                        break;
                    case Compiler.Token.DIV:
                        var r = Prim(tokens,args);
                        // if (r.Op == "imm" && (r as UnOp).N == 0) { };
                        left = Div(left, r);
                        break;
                    case Compiler.Token.END:
                        return left;
                    default:
                        tokens.Insert(0, token.Val);
                        return left;
                }
            }
        }

        private static Ast Prim(List<String> tokens,List<string> args)
        {
            var token = tokens.TakeToken();
            switch (token.Token)
            {
                case Compiler.Token.NAME:
                    return Arg(args, token.Val);
                case Compiler.Token.NUMBER:
                    return Imm(int.Parse(token.Val));
                case Compiler.Token.LP:
                    return Expr(tokens, args);
                case Compiler.Token.END:
                    return null;
                default:
                    tokens.Insert(0, token.Val);
                    return null;
            }
        }
    }
    
        public static class ListEx
    {
        public static TokenInfo TakeToken(this List<string> list)
        {
            if (list.Count == 0)
                return new TokenInfo { Token = Compiler.Token.END, Val = "" };
            var str = list[0];
            list.RemoveAt(0);
            switch (str[0])
            {
                case '+':
                case '-':
                case '*':
                case '/':
                case '(':
                case ')':
                    return new TokenInfo { Token = (Compiler.Token)str[0], Val = str };
                default:
                    if (char.IsNumber(str[0]))
                        return new TokenInfo { Token = Compiler.Token.NUMBER, Val = str };
                    if (char.IsLetter(str[0]) || str[0] == '_')
                        return new TokenInfo { Token = Compiler.Token.NAME, Val = str };
                    return new TokenInfo { Token = Compiler.Token.END, Val = str };
            }
        }
    }
    
    public static class QueueEx
    {
        public static Queue<T> Enqueue<T>(this Queue<T> queue, params T[] items)
        {
            foreach (var item in items)
                queue.Enqueue(item);
            return queue;
        }
    }
    
    public partial class Compiler
    {
        public enum Token
        {
            NAME,NUMBER,END,
            PLUS='+', MINUS='-', MUL='*', DIV='/',
            LP='(', RP=')',
        }
    }
    
    /*
    internal class UnOp : Ast
    {
        public int N { get; set; }
        public int n() => N;

        public UnOp(string op, int n)
        {
            this.Op = op;
            this.N = n;
        }
    }
    */
    
    public class TokenInfo
    {
        public Compiler.Token Token;
        public string Val;
    }
 }
 
########################
namespace CompilerKata
{
    using System.Text.RegularExpressions;
    using System.Collections.Generic;
    using System;
    using System.Linq;

    public class Compiler
    {
        public class Source
        {
            private readonly Dictionary<string, int> _args = new Dictionary<string, int>();
            private readonly IReadOnlyList<string> _tokens;
            private int _pos;
            
            public Source(IReadOnlyList<string> tokens)
            {
                _tokens = tokens;
                _pos = tokens.Count - 1;

                for (var idx = 1; _tokens[idx] != "]"; ++idx) _args[_tokens[idx]] = _args.Count;
            }

            public string Next() => _tokens[_pos--];

            public string Current => _tokens[_pos];

            public int GetArg(string name) => _args[name];
        }

        public Ast Factor(Source source)
        {
            var value = source.Next();
            if (value == ")")
            {
                var result = Expression(source);
                source.Next();
                return result;
            }
            return int.TryParse(value, out var number) ?new UnOp("imm", number) : new UnOp("arg", source.GetArg(value));
        }

       

        private void Pop(List<string> code)
        {
            if (code.Last() == "PU") code.RemoveAt(code.Count - 1); else code.Add("PO");
        }
        //////////////////////////////////////////  
      public Ast Term(Source source)
        {
            var factor = Factor(source);
            return "*/".Contains(source.Current) ? new BinOp(source.Next(), Term(source), factor) : factor;
        }

        public Ast Expression(Source source)
        {
            var term = Term(source);
            return "+-".Contains(source.Current) ? new BinOp(source.Next(), Expression(source), term) : term;
        }
        private void GenerateAsm(Ast ast, List<string> code)
        {
            if(ast is UnOp unOp)
            {
                switch(unOp.op())
                {
                    case "imm": code.Add($"IM {unOp.n()}"); break;
                    case "arg": code.Add($"AR {unOp.n()}"); break;
                }

                code.Add("PU");
            }
            else if (ast is BinOp binOp)
            {
                GenerateAsm(binOp.a(), code);
                GenerateAsm(binOp.b(), code);

                Pop(code);
                code.Add("SW");
                Pop(code);
                switch (binOp.op())
                {
                    case "+": code.Add("AD"); break;
                    case "-": code.Add("SU"); break;
                    case "*": code.Add("MU"); break;
                    case "/": code.Add("DI"); break;
                }

                code.Add("PU");
            }
        }

        public Ast pass1(string prog) => Expression(new Source(tokenize(prog)));

        public Ast pass2(Ast ast)
        {
            if (ast is BinOp binOp)
            {
                var a = pass2(binOp.a());
                var b = pass2(binOp.b());

                if(a is UnOp uOp1 && b is UnOp uOp2 && a.op() == "imm" && b.op() == "imm")
                {
                    switch(binOp.op())
                    {
                        case "*": return new UnOp("imm", uOp1.n() * uOp2.n());
                        case "/": return new UnOp("imm", uOp1.n() / uOp2.n());
                        case "+": return new UnOp("imm", uOp1.n() + uOp2.n());
                        case "-": return new UnOp("imm", uOp1.n() - uOp2.n());
                    }
                }

                return new BinOp(binOp.op(), a, b);
            }

            return ast;
        }

        public List<string> pass3(Ast ast)
        {
            var result = new List<string>();
            GenerateAsm(ast, result);
            Pop(result);
            return result;
        }

        private List<string> tokenize(string input)
        {
            var tokens = new List<string>();
            var rgxMain = new Regex("\\[|\\]|[-+*/=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            var matches = rgxMain.Matches(input);
            foreach (Match m in matches) tokens.Add(m.Groups[0].Value);
            return tokens;
        }
    }
}
    
###############
  namespace CompilerKata
 {
   using System;
   using System.Text.RegularExpressions;
   using System.Collections.Generic;
   using Newtonsoft.Json;  
      
    public class Compiler
    {
        List<string> var = new List<string>();
        Stack<String> stkOp = new Stack<string>();
        Stack<String> stkOps = new Stack<string>();
        Stack<Ast> stkAst = new Stack<Ast>();

        Action<string, Stack<Ast>> CompileOps = delegate(string Op, Stack<Ast> stk)  
        {
            var b = stk.Pop();
            var a = stk.Pop(); 
            stk.Push(new BinOp(Op, a, b)); 
        }; 

        Ast RecursiveDescent(Ast node)
        {
            Ast ret;

            if(node.GetType() == typeof(BinOp))
            {
                if(node._a.GetType() == typeof(BinOp))
                {
                    node._a = RecursiveDescent(node._a);
                }                         
                
                if(node._b.GetType() == typeof(BinOp))
                {
                    node._b = RecursiveDescent(node._b);
                }
                
                if(node._a.GetType() == typeof(UnOp) && 
                    node._a._op == "imm"  && 
                    node._b.GetType() == typeof(UnOp) &&
                    node._b._op == "imm") 
                {
                    switch (node._op)
                    {
                        case "+":   return new UnOp("imm", 
                                    node._a._n +  
                                    node._b._n);
                        
                        case "-":   return new UnOp("imm", 
                                    node._a._n -  
                                    node._b._n);
                        
                        case "*":   return new UnOp("imm", 
                                    node._a._n *  
                                    node._b._n);
                        
                        case "/":   return new UnOp("imm", 
                                    node._a._n /  
                                    node._b._n);
                        
                        default: throw new FormatException();                    
                    }                          
                }

                ret = new BinOp(node._op, node._a, node._b);
                 
            } else 
            {
                ret = new UnOp(node._op, node._n);               
            }
                       
            return ret;
        }
        void RecursiveDescent(Ast node, List<string> code)
        {
            if (node.GetType() == typeof(BinOp))
            {
                RecursiveDescent(node._a, code);
                RecursiveDescent(node._b, code);

                switch (node._op)
                {

                    case "-":
                        {
                            code.Add($"PO");
                            code.Add($"SW");
                            code.Add($"PO");
                            code.Add($"SU");
                            code.Add($"PU"); break;
                        }
                    case "+":
                        {
                            code.Add($"PO");
                            code.Add($"SW");
                            code.Add($"PO");
                            code.Add($"AD"); 
                            code.Add($"PU"); break;
                        }
                    case "/":
                        {
                            code.Add($"PO");
                            code.Add($"SW");
                            code.Add($"PO");
                            code.Add($"DI"); 
                            code.Add($"PU"); break;
                        }
                    case "*":
                        {   
                            code.Add($"PO");
                            code.Add($"SW");
                            code.Add($"PO");
                            code.Add($"MU"); 
                            code.Add($"PU"); break;
                        }
                    default: throw new FormatException();
                }

            }
            else
            {
                switch (node._op)
                {
                    case "imm":
                        {
                            code.Add($"IM {node._n}"); break; 
                            
                        }
                    case "arg":
                        {
                            code.Add($"AR {node._n}"); break;
                        }
                    default: throw new FormatException();
                }

                code.Add($"PU");
            }

        }
      
        public Ast pass1(string prog)
        {
            List<string> tokens = tokenize(prog);

            var OpsTmpl = @"\+|\-|\/|\*|\(|\)";
            var OpTmpl = "[a-zA-Z]|[0-9]";
            var OpsOrder = new Dictionary<string, int> { { "(", -1 }, { ")", -1 }, { "+", 1 }, { "-", 1 }, { "/", 1 }, { "*", 2 } };

            foreach (string token in tokens)
            {
                if (token == "[")
                    stkOps.Push(token);
                else if (token == "]")
                    stkOps.Pop();
                else if (stkOps.Count > 0 && "[" == stkOps.Peek())
                    var.Add(token);
                else if (Regex.IsMatch(token, OpsTmpl))
                {
                    if (stkOps.Count == 0)
                        stkOps.Push(token);
                    else if (token == "(")
                        stkOps.Push(token);
                    else if (token == ")")
                    {
                        while (stkOps.Count > 0  && stkOps.Peek() != "(")
                        {
                            var PopOps = stkOps.Pop();
                            CompileOps(PopOps, stkAst);
                        }

                        stkOps.Pop();
                    }
                    else if (OpsOrder[token] <= OpsOrder[stkOps.Peek()])
                    {
                        while (stkOps.Count > 0  && stkOps.Peek() != "(")
                        {
                            var PopOps = stkOps.Pop();
                            CompileOps(PopOps, stkAst);
                        }
                        stkOps.Push(token);
                    }
                    else
                    {
                        stkOps.Push(token);
                    }
                }
                else if (Regex.IsMatch(token, OpTmpl))
                {
                    stkOp.Push(token);
                    if (Regex.IsMatch(token, "[0-9]"))
                        stkAst.Push(new UnOp("imm", int.Parse(token)));
                    else
                        stkAst.Push(new UnOp("arg", var.IndexOf(token)));
                }
                else
                {
                    throw new FormatException();
                }
            }

            while (stkOps.Count > 0)
            {
                var PopOps = stkOps.Pop();
                CompileOps(PopOps, stkAst);
            }

            return stkAst.Pop();
        }
        public Ast pass2(Ast ast)
        {
            return RecursiveDescent(ast);
        } 
        
        public List<string> pass3(Ast ast)
        {
            List<String> code = new List<string>();
            RecursiveDescent(ast, code);
            code.Add($"PO");
            return code;
        }
      
        private List<string> tokenize(string input)
        {
            List<string> tokens = new List<string>();
            Regex rgxMain = new Regex("\\[|\\]|[-+*/=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            MatchCollection matches = rgxMain.Matches(input);
            foreach (Match m in matches) tokens.Add(m.Groups[0].Value);
            return tokens;
        }
    }
  
}
