52ffcfa4aff455b3c2000750


using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text.RegularExpressions;


public class Interpreter
{
    #region Operators
    private readonly Dictionary<string, int> OperatorPriority = new Dictionary<string, int>
    {
        {"=", 0},
        {"(", 0},
        {")", 0},
        {"+", 1},
        {"-", 1},
        {"*", 2},
        {"/", 2},
        {"%", 2},
        {"~", 3}
    };

    private readonly HashSet<string> Operators = new HashSet<string>
    {
        "+",
        "-",
        "*",
        "/",
        "~",
        "=",
        "%"
    };
    #endregion

    #region Storages
    private readonly Dictionary<string, double> Variables = new Dictionary<string, double>();
    private readonly Dictionary<string, int> FuncDecls = new Dictionary<string, int>();
    private readonly Dictionary<string, Func<string[], double?>> FuncBodies =
        new Dictionary<string, Func<string[], double?>>();
    #endregion

    #region Regexes
    private readonly Regex FuncDeclRegex = new Regex(@"^fn[ ]([a-zA-Z_][a-zA-Z0-9_]*[ ])+=>.+$");
    private readonly Regex TokenRegex = new Regex(@"[a-zA-Z_][a-zA-Z0-9_]*|[0-9]+(\.[0-9]+)?|[-+*\/()~=%]");
    private readonly Regex VariableRegex = new Regex(@"[a-zA-Z_][a-zA-Z0-9_]*");
    private readonly Regex NumericRegex = new Regex(@"[0-9]+(\.[0-9]+)?");
    #endregion

    #region Main
    public double? input(string expression)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(expression))
                return null;
            var funcDecl = IsFuncDecl(expression);
            if (funcDecl)
            {
                AddFuncDecl(expression);
                return null;
            }
            else
            {
                var tokens = ParseExpression(expression);
                var result = EvaluateExpression(tokens);
                return result;
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
            return null;
        }
    }
    
    private string ConvertToReversePolishNotation(List<string> tokens)
    {
        var notation = new List<object>();
        var operators = new Stack<string>();
        foreach (var token in tokens)
        {
            double d;
            var isNumber = TryParseDouble(token, out d);
            if (isNumber)
                notation.Add(token);
            else if (VariableRegex.IsMatch(token))
                notation.Add(token);
            else
            {
                if (token == "(")
                    operators.Push(token);
                else if (token == ")")
                {
                    while (operators.Peek() != "(")
                        notation.Add(operators.Pop());
                    operators.Pop();
                }
                else
                {
                    if (token == "~" || token == "=")
                        while (operators.Count != 0 && OperatorPriority[token] < OperatorPriority[operators.Peek()])
                            notation.Add(operators.Pop());

                    else
                        while (operators.Count != 0 && OperatorPriority[token] <= OperatorPriority[operators.Peek()])
                            notation.Add(operators.Pop());
                    operators.Push(token);
                }
            }
        }
        while (operators.Count > 0)
            notation.Add(operators.Pop());
        return string.Join(" ", notation);
    }

    private double CalculateNotation(string notation)
    {
        var tokens = notation.Split(' ');
        var stack = new Stack<object>();
        foreach (var token in tokens)
        {
            if (!Operators.Contains(token))
                stack.Push(token);
            else
            {
                var operands = new List<object>();
                var result = 0.0;
                if (token == "~")
                {
                    operands.Add(stack.Pop());
                    result = ParseDouble(operands.Last().ToString())*-1;
                }
                else
                {
                    operands.Insert(0, stack.Pop());
                    operands.Insert(0, stack.Pop());
                    if (Variables.ContainsKey(operands[0].ToString()) && token != "=")
                        operands[0] = Variables[operands[0].ToString()];
                    if (Variables.ContainsKey(operands[1].ToString()))
                        operands[1] = Variables[operands[1].ToString()];

                    if (!NumericRegex.IsMatch(operands[0].ToString()) && token != "=")
                        throw new InvalidOperationException("ERROR: Invalid identifier. No variable with name '" +
                                                            operands[0] + "' was found.");
                    if (!NumericRegex.IsMatch(operands[1].ToString()))
                        throw new InvalidOperationException("ERROR: Invalid identifier. No variable with name '" +
                                                            operands[1] + "' was found.");
                    switch (token)
                    {
                        case "+":
                            result = operands.Aggregate(0.0, (l, r) => Calc(l, ParseDouble(r.ToString()), token));
                            break;
                        case "*":
                            result = operands.Aggregate(1.0, (l, r) => Calc(l, ParseDouble(r.ToString()), token));
                            break;
                        case "-":
                        case "/":
                        case "%":
                            result = operands.Skip(1)
                                .Aggregate(ParseDouble(operands.First().ToString()),
                                    (l, r) => Calc(l, ParseDouble(r.ToString()), token));
                            break;
                        case "=":
                            var val = ParseDouble(operands[1].ToString());
                            var variableName = operands[0].ToString();
                            DefineVariable(variableName, val);
                            result = val;
                            break;
                        case "~":
                        default:
                            throw new ArgumentException("Invalid operator");
                    }
                }
                stack.Push(result);
            }
        }
        var res = stack.Pop();
        if (Variables.ContainsKey(res.ToString().Replace(',', '.')))
            res = ParseDouble(Variables[res.ToString()].ToString(CultureInfo.InvariantCulture));
        if (!NumericRegex.IsMatch(res.ToString()))
            throw new InvalidOperationException("ERROR: Invalid identifier. No variable with name '" + res +
                                                "' was found.");
        return ParseDouble(res.ToString());
    }

    private void DefineVariable(string variableName, double val)
    {
        if (FuncDecls.ContainsKey(variableName))
            throw new InvalidOperationException("A variable with the same name was already introduced: " +
                                                variableName);
        if (!VariableRegex.IsMatch(variableName))
            throw new InvalidOperationException("The left-hand side of an assignment must be a variable");
        Variables[variableName] = val;
    }

    private void DefineFunction(string funcName, int argsCount, List<string> args, string body)
    {
        if (Variables.ContainsKey(funcName))
            throw new InvalidOperationException("A variable with the same name was already introduced: " + funcName);
        FuncDecls[funcName] = argsCount;
        FuncBodies[funcName] = _args =>
        {
            if (_args.Length != args.Count)
                throw new InvalidOperationException("Arguments count mismatch");
            var b = body;
            var counter = 0;
            foreach (var arg in args)
            {
                b = Regex.Replace(b, @"\b" + arg + @"\b", _args[counter++]);
            }
            return input(b);
        };
    }
    #endregion

    #region Private

    private bool IsFuncDecl(string expression)
    {
        return FuncDeclRegex.IsMatch(expression);
    }

    private void AddFuncDecl(string declaration)
    {
        var baseSplit = declaration.Split(new[] { "=>" }, StringSplitOptions.RemoveEmptyEntries);
        var signature = baseSplit[0];
        var signatureSplit = signature.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries);
        var body = baseSplit[1];

        var funcName = signatureSplit[1];
        var args = signatureSplit.Skip(2).ToList();
        var argsCount = args.Count;

        var localVariables = VariableRegex.Matches(body).Cast<Match>().Select(m => m.Value).ToList();
        var isConsistent = args.SequenceEqual(localVariables);
        if (!isConsistent)
            throw new InvalidOperationException("Unknown local variables found in function declaration");
        DefineFunction(funcName, argsCount, args, body);
    }

    private List<string> ParseExpression(string exp)
    {
        var expression = OptimizeExpression(exp);
        var tokens = TokenRegex.Matches(expression).Cast<Match>().Select(m => m.Value).ToList();
        return tokens;
    }

    private double EvaluateExpression(List<string> tokens)
    {
        var notation = ConvertToReversePolishNotation(tokens);
        var result = CalculateNotation(notation);
        return result;
    }

    private double Calc(double l, double r, string token)
    {
        switch (token)
        {
            case "+":
                return l + r;
            case "-":
                return l - r;
            case "*":
                return l*r;
            case "/":
                return l/r;
            case "%":
                return l%r;
            case "~":
            case "=":
            default:
                throw new ArgumentException("Invalid operator");
        }
    }

    private string OptimizeExpression(string exp)
    {
        var expression = exp;

        var regexes = new List<Regex>();
        foreach (var fnDecl in FuncDecls)
        {
            var pattern = string.Format(@"{0}[ ]([a-zA-Z0-9_]+([ ])){{{1}}}", fnDecl.Key, fnDecl.Value);
            regexes.Add(new Regex(pattern, RegexOptions.RightToLeft));
        }
        expression += " ";
        while (true)
        {
            var regexSkipped = false;
            foreach (var rgx in regexes)
            {
                while (true)
                {
                    var matches = rgx.Matches(expression).Cast<Match>().Select(m => m.Value).ToList();
                    if (matches.Count == 0) break;
                    foreach (var match in matches)
                    {
                        var split = match.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries);
                        var funcName = split[0];
                        var args = split.Skip(1).ToArray();
                        var hasFunctionCallInArgs = args.Any(arg => FuncDecls.ContainsKey(arg));
                        if (hasFunctionCallInArgs)
                        {
                            regexSkipped = true;
                            break;
                        }
                        var func = FuncBodies[funcName];
                        if (func == null)
                            throw new InvalidOperationException("Unknown function: " + funcName);
                        var callResult = func(args);
                        expression = expression.Replace(match.Trim(), callResult.ToString().Replace(",", "."));
                    }
                    if (regexSkipped)
                        break;
                }
            }
            if (!regexSkipped)
                break;
        }

        var tokenCount = TokenRegex.Matches(expression).Cast<Match>().Select(m => m.Value).Count();
        expression = expression.Replace(" ", "");
        tokenCount -= TokenRegex.Matches(expression).Cast<Match>().Select(m => m.Value).Count();
        if (tokenCount != 0)
            throw new InvalidOperationException("Syntax error");
        expression = Regex.Replace(expression, @"(?<![)0-9])-", "~");
        return expression;
    }

    private static bool TryParseDouble(string token, out double d)
    {
        return double.TryParse(token.Replace(',', '.'),
            NumberStyles.AllowLeadingSign | NumberStyles.AllowDecimalPoint,
            new NumberFormatInfo {NegativeSign = "-"}, out d);
    }

    private static double ParseDouble(string token)
    {
        return double.Parse(token.Replace(',', '.'), NumberStyles.AllowLeadingSign | NumberStyles.AllowDecimalPoint,
            new NumberFormatInfo {NegativeSign = "-"});
    }

    #endregion
}

___________________________________________________________________________
namespace InterpreterKata
{
  using System;
  using System.Linq;
  using System.Collections.Generic;
  using System.Text.RegularExpressions;

  public class Interpreter
  {
      public static Interpreter Current { get; private set; }

      private Tokenizer<LexicalToken> _lexer;
      private Parser _evaluator;
      private SemanticAnalyzer _semanticAnalyzer;

      internal Dictionary<string, Expression> SymbolTable = new Dictionary<string, Expression>();

      public Interpreter()
      {
          Current = this;

          _lexer = new Tokenizer<LexicalToken>()
                              .AddToken(@"fn", LexicalToken.FunctionKeyword)
                              .AddToken(@"=>", LexicalToken.FunctionOperator)
                              .AddToken(@"[A-z]+", LexicalToken.Identifier)
                              .AddToken(@"\+", LexicalToken.Plus)
                              .AddToken(@"\*", LexicalToken.Mul)
                              .AddToken(@"/", LexicalToken.Div)
                              .AddToken(@"-", LexicalToken.Sub)
                              .AddToken(@"%", LexicalToken.Mod)
                              .AddToken(@"[0-9]+\.?[0-9]*", LexicalToken.Number)
                              .AddToken(@"\s", LexicalToken.Whitespace)
                              .AddToken(@"\(", LexicalToken.LParen)
                              .AddToken(@"\)", LexicalToken.RParen)
                              .AddToken(@"=", LexicalToken.Assignment)
                              .IgnoreToken(LexicalToken.Whitespace);
          _evaluator = new Parser(_lexer);
          _semanticAnalyzer = new SemanticAnalyzer();
      }

      public double? input(string input)
      {
          _lexer.Text = input;
          var ast = _evaluator.Parse(input);
          _semanticAnalyzer.Analyse(ast);
          return ast.Interpret();
      }
  }

  enum LexicalToken
  {
      Plus,
      Sub,
      Div,
      Mul,
      Mod,
      Identifier,
      Assignment,
      FunctionKeyword,
      FunctionOperator,
      Number,
      Whitespace,
      LParen,
      RParen
  }
  
  class Tokenizer<TTokenType>
  {
      private string _text;
      public string Text
      {
          get => _text;
          set
          {
              _text = value;
              _currentPosition = 0;
          }
      }

      private int _currentPosition;
      private List<ITokenParser<TTokenType>> _tokenParsers = new List<ITokenParser<TTokenType>>();
      private List<TTokenType> _ignore = new List<TTokenType>();

      public Tokenizer(string code = "")
      {
          Text = code;
      }

      public Token<TTokenType> NextToken()
      {
          if (_currentPosition >= Text.Length) return null;

          foreach (var parser in _tokenParsers)
          {
              Token<TTokenType> token;
              if ((token = parser.Parse(Text, _currentPosition)) != null)
              {
                  _currentPosition += token.Value.Length;
                  if (!_ignore.Contains(token.TokenType))
                  {
                      return token;
                  }
                  else
                  {
                      return NextToken();
                  }
              }
          }

          throw new Exception($"Invalid symbol: {Text[_currentPosition]}");
      }

      public IEnumerable<Token<TTokenType>> Tokenize()
      {
          Token<TTokenType> token;
          while ((token = NextToken()) != null)
          {
              yield return token;
          }
      }

      public Tokenizer<TTokenType> AddToken(string regex, TTokenType tokenType)
      {
          _tokenParsers.Add(new RegExParser<TTokenType>(regex, tokenType));
          return this;
      }

      public Tokenizer<TTokenType> IgnoreToken(TTokenType tokenType)
      {
          _ignore.Add(tokenType);
          return this;
      }
  }

  interface ITokenParser<TTokenType>
  {
      Token<TTokenType> Parse(string expression, int startAt);
  }

  class RegExParser<TTokenType> : ITokenParser<TTokenType>
  {
      private Regex _regex;
      private TTokenType _tokenType;

      public RegExParser(string regex, TTokenType tokenType)
      {
          _regex = new Regex("\\G" + regex);
          _tokenType = tokenType;
      }

      public Token<TTokenType> Parse(string expression, int startAt)
      {
          Match match = _regex.Match(expression, startAt);

          if (match.Value == string.Empty) return null;
          else return new Token<TTokenType>(match.Value, _tokenType);
      }
  }

  class Parser
  {
      private Token<LexicalToken> _current;
      private Token<LexicalToken> _next;
      private Tokenizer<LexicalToken> _lexer;

      public Parser(Tokenizer<LexicalToken> tokenizer)
      {
          _lexer = tokenizer;
      }

      public Expression Parse(string code)
      {
          _lexer.Text = code;
          _current = _lexer.NextToken();
          _next = _lexer.NextToken();
          var statement = Statement();
          if(_current != null) throw new Exception();
          return statement;
      }

      private void Eat(LexicalToken tokenType)
      {
          if (_current.TokenType == tokenType)
          {
              _current = _next;
              _next = _lexer.NextToken();
          }
          else
          {
              throw new Exception();
          }
      }

      private Expression Statement()
      {
          Expression result;

          if(Match(_current, LexicalToken.FunctionKeyword))
          {
              result = FunctionDeclaration();
          }
          else
          {
              result = Expression();
          }

          return result;
      }

      private Expression FunctionDeclaration()
      {
          FunctionDeclaration result = null;

          if(Match(_current, LexicalToken.FunctionKeyword))
          {
              Eat(LexicalToken.FunctionKeyword);
              result = new FunctionDeclaration()
              {
                  Token = _current
              };
              Eat(LexicalToken.Identifier);

              while(Match(_current, LexicalToken.Identifier))
              {
                  result.Parameters.Add(new Variable()
                  {
                      Token = _current
                  });
                  Eat(LexicalToken.Identifier);
              }
              Eat(LexicalToken.FunctionOperator);

              result.Body = Statement();
          }

          return result;
      }

      private Expression FunctionCall()
      {
          FunctionCall result = new FunctionCall();

          result.Token = _current;
          Eat(LexicalToken.Identifier);
          var parameterDeclarations = 
              (Interpreter.Current.SymbolTable[result.FunctionName] as FunctionDeclaration).Parameters;

          for (int i = 0; i < parameterDeclarations.Count; i++)
          {
              result.Parameters.Add(parameterDeclarations[i].Name, Expression());
          }

          return result;
      }

      private Expression Expression()
      {
          Expression result = Term();

          while (Match(_current, LexicalToken.Plus, LexicalToken.Sub))
          {
              result = new BinaryOperation()
              {
                  Left = result,
                  Token = Operator(),
                  Right = Statement()
              };
          }

          return result;
      }

      private Expression Term()
      {
          Expression result = Factor();
          while (Match(_current, LexicalToken.Mul, LexicalToken.Div, LexicalToken.Mod))
          {
              result = new BinaryOperation()
              {
                  Left = result,
                  Token = Operator(),
                  Right = Factor()
              };
          }

          return result;
      }

      private Expression Assignment()
      {
          Expression result = null;

          result = new Variable()
          {
              Token = _current
          };
          Eat(LexicalToken.Identifier);

          var token = _current;
          Eat(LexicalToken.Assignment);
          result = new Assignment()
          {
              Left = result,
              Token = token,
              Right = Statement()
          };

          return result;
      }

      private Expression Factor()
      {
          Expression result = null;

          if(Match(_current, LexicalToken.Identifier))
          {
              if(Match(_next, LexicalToken.Assignment))
              {
                  result = Assignment();
              }
              else if(Interpreter.Current.SymbolTable.ContainsKey(_current.Value) &&
                      Interpreter.Current.SymbolTable[_current.Value] is FunctionDeclaration)
              {
                  result = FunctionCall();
              }
              else
              {
                  result = new Variable()
                  {
                      Token = _current
                  };
                  Eat(LexicalToken.Identifier);
              }
          }
          else if(Match(_current, LexicalToken.Number))
          {
              result = new Number()
              {
                  Token = _current
              };
              Eat(LexicalToken.Number);
          }
          else if (Match(_current, LexicalToken.LParen))
          {
              Eat(LexicalToken.LParen);
              result = Expression();
              Eat(LexicalToken.RParen);
          }

          return result;
      }

      private Token<LexicalToken> Operator()
      {
          Token<LexicalToken> result = null;

          if(Match(_current, LexicalToken.Plus,
                             LexicalToken.Sub,
                             LexicalToken.Mul,
                             LexicalToken.Div,
                             LexicalToken.Mod))
          {
              result = _current;
              Eat(_current.TokenType);
          }

          return result;
      }

      private bool Match(Token<LexicalToken> token, params LexicalToken[] tokenTypes)
      {
          return token == null ? false : tokenTypes.Contains(token.TokenType);
      }
  }

  abstract class Expression
  {
      public Token<LexicalToken> Token { get; set; }

      public abstract dynamic Interpret();
  }

  class BinaryOperation : Expression
  {
      public Expression Left { get; set; }

      public Expression Right { get; set; }

      public override dynamic Interpret()
      {
          switch (Token.TokenType)
          {
              case LexicalToken.Plus:
                  return Left.Interpret() + Right.Interpret();
              case LexicalToken.Sub:
                  return Left.Interpret() - Right.Interpret();
              case LexicalToken.Div:
                  return Left.Interpret() / Right.Interpret();
              case LexicalToken.Mul:
                  return Left.Interpret() * Right.Interpret();
              case LexicalToken.Mod:
                  return Left.Interpret() % Right.Interpret();
          }

          throw new Exception($"Unknown operation {Token}");
      }

      public override string ToString()
      {
          return Token.Value;
      }
  }

  class Number : Expression
  {
      public virtual double Value => double.Parse(Token.Value);

      public override dynamic Interpret()
      {
          return Value;
      }

      public override string ToString()
      {
          return Value.ToString();
      }
  }

  class Variable : Expression
  {
      public string Name => Token.Value;

      public override dynamic Interpret()
      {
          return Interpreter.Current.SymbolTable[Name].Interpret();
      }
  }

  class Assignment : BinaryOperation
  {
      public override dynamic Interpret()
      {
          var result = Right.Interpret();
          Interpreter.Current.SymbolTable[Left.Token.Value] = new Number()
          {
              Token = new Token<LexicalToken>(result.ToString(), LexicalToken.Number)
          };
          return result;
      }
  }

  class FunctionDeclaration : Expression
  {
      public string FunctionName => Token.Value;

      public Expression Body { get; set; }

      public List<Variable> Parameters { get; set; } = new List<Variable>();

      public override dynamic Interpret()
      {
          Interpreter.Current.SymbolTable[FunctionName] = this;
          return null;
      }
  }

  class FunctionCall : Expression
  {
      public string FunctionName => Token.Value;

      public Dictionary<string, Expression> Parameters { get; set; } = new Dictionary<string, Expression>();

      public override dynamic Interpret()
      {
          FunctionDeclaration functionDeclaration = Interpreter.Current.SymbolTable[FunctionName] as FunctionDeclaration;
      
          foreach (var key in Parameters.Keys.ToArray())
          {
              Parameters[key] = new Number()
              {
                  Token = new Token<LexicalToken>(Parameters[key].Interpret().ToString(), LexicalToken.Number)
              };
          }
          var globalScope = Interpreter.Current.SymbolTable;
          var body = (Interpreter.Current.SymbolTable[FunctionName] as FunctionDeclaration).Body;
          Interpreter.Current.SymbolTable = Parameters;
          var result = body.Interpret();
          Interpreter.Current.SymbolTable = globalScope;
          return result;
      }
  }

  class FunctionParameter : Expression
  {
      public FunctionCall FunctionCall { get; set; }

      public override dynamic Interpret()
      {
          return FunctionCall.Parameters[Token.Value];
      }
  }

  class Token<TTokenType>
  {
      public TTokenType TokenType { get; set; }

      public string Value { get; set; }

      public Token(string value, TTokenType tokenType)
      {
          TokenType = tokenType;
          Value = value;
      }

      public override string ToString()
      {
          return $"{{{TokenType}, {Value}}}";
      }
  }
  
  class SemanticAnalyzer
  {
      private List<Variable> _variables = null;
      private List<FunctionDeclaration> _functionDeclarations = null; 

      public void Analyse(Expression ast)
      {
          Init();

          Visit(ast);
      }

      private void Visit(Expression ast)
      {
          if (ast is BinaryOperation binop)
          {
              VisitBinaryOperation(binop);
          }
      }

      private void VisitBinaryOperation(BinaryOperation binaryOperation)
      {
          if (binaryOperation is Assignment assignment)
          {
              VisitAssignment(assignment);
          }
          else
          {
              Visit(binaryOperation.Left);
              Visit(binaryOperation.Right);
          }
      }

      private void VisitAssignment(Assignment assignment)
      {
          if(assignment.Left is Variable variable)
          {
              var isFunction = _functionDeclarations.Any(fd => fd.FunctionName == variable.Name);

              if (isFunction)
              {
                  throw new Exception("Cant assign value to function");
              }
          }

          Visit(assignment.Right);
      }

      private void Init()
      {
          _variables = new List<Variable>();
          _functionDeclarations = new List<FunctionDeclaration>();

          LoadSymbolTable();
      }

      private void LoadSymbolTable()
      {
          _variables.AddRange(Interpreter.Current.SymbolTable.Where(i => i.Value is Variable).Select(i => i.Value as Variable));
          _functionDeclarations.AddRange(Interpreter.Current.SymbolTable.Where(i => i.Value is FunctionDeclaration).Select(i => i.Value as FunctionDeclaration));
      }
  }
}

___________________________________________________________________________
namespace InterpreterKata
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text.RegularExpressions;

    public class Interpreter
    {
        private class Function
        {
            private readonly string[] _arguments;
            private readonly string[] _expressionParts;

            private static readonly string[] _allowedTokens = { "+", "-", "*", "/", "%", "=", "(", ")" };

            public Function(string str, Dictionary<string, Function> knownFunctions)
            {
                string[] parts = str.Split("=>", StringSplitOptions.None);
                _arguments = parts[0].Split(' ', StringSplitOptions.RemoveEmptyEntries);
                _expressionParts = Tokenize(parts[1]);
                foreach (string part in _expressionParts)
                {
                    if (!_allowedTokens.Contains(part) && !double.TryParse(part, out _) && !_arguments.Contains(part) && !knownFunctions.ContainsKey(part))
                        throw new ArgumentException($"ERROR: Invalid identifier '{part}' in function body.");
                }
            }

            public int ArgumentsCount => _arguments.Length;

            public double Execute(double[] argValues, Dictionary<string, Function> knownFunctions) =>
                ExecuteExpression(_expressionParts, _arguments.Zip(argValues).ToDictionary(x => x.First, x => x.Second), knownFunctions);
        }

        Dictionary<string, Function> _functions = new Dictionary<string, Function>();
        Dictionary<string, double> _globalVariables = new Dictionary<string, double>();

        public double? input(string input)
        {
            if (input.StartsWith("fn "))
            {
                int functionBodyStartIndex = input.IndexOf(' ', 3) + 1;
                string functionName = input.Substring(3, functionBodyStartIndex - 4);

                if (_globalVariables.ContainsKey(functionName))
                    return null;

                try
                {
                    _functions[functionName] = new Function(input.Substring(functionBodyStartIndex), _functions);
                }
                catch { }

                return null;
            }

            try
            {
                return ExecuteExpression(Tokenize(input), _globalVariables, _functions);
            }
            catch
            {
                return null;
            }

        }

        private static double ExecuteExpression(string[] parts, Dictionary<string, double> availableVariables, Dictionary<string, Function> knownFunctions)
        {
            const int maxDepth = 10;
            int depth = 0;
            double? currentValue = null;
            Stack<(string, double)>[] multiplicativeStack = Enumerable.Range(1, maxDepth).Select(x => new Stack<(string, double)>()).ToArray();
            Stack<(string, double)>[] additiveStack = Enumerable.Range(1, maxDepth).Select(x => new Stack<(string, double)>()).ToArray();
            Stack<double> collectedFunctionArguments = new Stack<double>();

            for (int i = parts.Length - 1; i >= 0; i--)
            {
                switch (parts[i])
                {
                    case "*":
                    case "/":
                    case "%":
                        multiplicativeStack[depth].Push((parts[i], currentValue.Value));
                        currentValue = null;
                        break;
                    case "+":
                    case "-":
                        currentValue = ApplyMultiplicativeOperations(currentValue, multiplicativeStack[depth]);
                        additiveStack[depth].Push((parts[i], currentValue.Value));
                        currentValue = null;
                        break;
                    case ")":
                        if (currentValue.HasValue)
                        {
                            FinalizeAndSaveFunctionArgument(collectedFunctionArguments, currentValue, multiplicativeStack[depth], additiveStack[depth]);
                        }
                        currentValue = null;
                        depth++;
                        break;
                    case "(":
                        currentValue = ApplyMultiplicativeOperations(currentValue, multiplicativeStack[depth]);
                        currentValue = ApplyAdditiveOperations(currentValue, additiveStack[depth]);
                        depth--;
                        break;
                    case "=":
                        if (knownFunctions.ContainsKey(parts[i - 1]))
                            throw new ArgumentException();

                        currentValue = ApplyMultiplicativeOperations(currentValue, multiplicativeStack[depth]);
                        currentValue = ApplyAdditiveOperations(currentValue, additiveStack[depth]);
                        availableVariables[parts[i - 1]] = currentValue.Value;
                        i--;
                        break;
                    default:
                        if (double.TryParse(parts[i], out double scalar))
                        {
                            if (currentValue.HasValue)
                            {
                                FinalizeAndSaveFunctionArgument(collectedFunctionArguments, currentValue, multiplicativeStack[depth], additiveStack[depth]);
                            }
                            currentValue = scalar;
                        }
                        else if (availableVariables.ContainsKey(parts[i]))
                        {
                            if (currentValue.HasValue)
                            {
                                FinalizeAndSaveFunctionArgument(collectedFunctionArguments, currentValue, multiplicativeStack[depth], additiveStack[depth]);
                            }
                            currentValue = availableVariables[parts[i]];
                        }
                        else if (knownFunctions.ContainsKey(parts[i]))
                        {
                            if (currentValue.HasValue)
                            {
                                FinalizeAndSaveFunctionArgument(collectedFunctionArguments, currentValue, multiplicativeStack[depth], additiveStack[depth]);
                            }

                            if (collectedFunctionArguments.Count < knownFunctions[parts[i]].ArgumentsCount)
                                throw new ArgumentException();

                            double[] arguments = new byte[knownFunctions[parts[i]].ArgumentsCount].Select(x => collectedFunctionArguments.Pop()).ToArray();
                            currentValue = knownFunctions[parts[i]].Execute(arguments, knownFunctions);
                        }
                        else
                        {
                            throw new ArgumentException();
                        }
                        break;
                }
            }

            if (collectedFunctionArguments.Count > 0)
                throw new ArgumentException();

            currentValue = ApplyMultiplicativeOperations(currentValue, multiplicativeStack[depth]);
            currentValue = ApplyAdditiveOperations(currentValue, additiveStack[depth]);
            return currentValue.Value;
        }

        private static double? ApplyAdditiveOperations(double? currentValue, Stack<(string, double)> additiveStack)
        {
            while (additiveStack.Count > 0)
            {
                (string operation, double value) = additiveStack.Pop();
                currentValue = operation == "+" ? currentValue + value : currentValue - value;
            }

            return currentValue;
        }

        private static double? ApplyMultiplicativeOperations(double? currentValue, Stack<(string, double)> multiplicativeStack)
        {
            while (multiplicativeStack.Count > 0)
            {
                (string operation, double value) = multiplicativeStack.Pop();
                currentValue = operation switch
                {
                    "*" => currentValue * value,
                    "/" => currentValue / value,
                    "%" => currentValue % value
                };
            }

            return currentValue;
        }

        private static void FinalizeAndSaveFunctionArgument(Stack<double> collectedFunctionArguments, double? currentValue, Stack<(string, double)> multiplicativeStack, Stack<(string, double)> additiveStack)
        {
            currentValue = ApplyMultiplicativeOperations(currentValue, multiplicativeStack);
            currentValue = ApplyAdditiveOperations(currentValue, additiveStack);
            collectedFunctionArguments.Push(currentValue.Value);
        }

        private static string[] Tokenize(string input)
        {
            List<string> tokens = new List<string>();
            Regex rgxMain = new Regex("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            MatchCollection matches = rgxMain.Matches(input);
            return matches.Select(x => x.Groups[0].Value).ToArray();
        }
    }
}

___________________________________________________________________________
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;

namespace MPerlInterpreter
{
    public class Function
    {
        public string name;
        public string[] parameters;
        public string data;
        public string error = null;

        public Function(string name, string parameters, string data)
        {
            this.name = name;
            if (parameters != "")
                this.parameters = parameters.Split();
            else
                this.parameters = new string[0];
            this.data = data;
        }

        public string Execute(string[] args)
        {
            Console.WriteLine("Debug: " + name + " [ " + string.Join(" ", args) + " ]");

            try
            {
                string expression = data;
                for (int now = 0; now < parameters.Length; ++now)
                    expression = expression.Replace(parameters[now], args[now]);

                return Interpreter.eval(expression);
            }
            catch (Exception ex)
            {
                Console.WriteLine("ERROR: " + ex.Message);
            }

            return null;
        }

        internal bool Test()
        {
            int lv = 0;
            char[] ops = { '+', '-', '*', '/', '%' };
            for (int now = 0; now < data.Length; ++now)
            {
                var smb = data[now];
                if (smb == '(')
                    ++lv;
                else if (smb == ')')
                    --lv;

                if (lv == -1)
                {
                    error = "ERROR: Unexpected using of ) at " + (now + 1);
                    return false;
                }
            }

            bool lastOp = true;
            string variable = "";
            bool number = false;
            bool nuller = false;
            int val;

            for (int now = 0; now < data.Length; ++now)
            {
                if (data[now] == ' ')
                    nuller = true;

                if (ops.Contains(data[now]))
                {
                    if (lastOp)
                    {
                        error = "ERROR: Unexpected operator " + data[now];
                        return false;
                    }
                    lastOp = true;
                }

                if (char.IsNumber(data[now]))
                {
                    if (number || variable == "")
                    {
                        number = true;
                        variable += data[now];
                    }
                    else
                    {
                        error = "ERROR: " + data[now] + " is not a digit";
                        return false;
                    }

                    lastOp = false;
                }
                else if (char.IsLetter(data[now]))
                {
                    if ((!number || variable == ""))
                    {
                        variable += data[now];
                        number = false;
                    }
                    else
                    {
                        error = "ERROR: " + data[now] + " is not a letter";
                        return false;
                    }
                    lastOp = false;
                }
                else
                {
                    nuller = true;
                }

                if (now == data.Length - 1)
                    nuller = true;

                if (!string.IsNullOrEmpty(variable) && nuller)
                {
                    if (!int.TryParse(variable, out val))
                    {
                        if (!parameters.Contains(variable))
                        {
                            error = "ERROR: Invalid identifier. No variable with name '" + variable + "' was found.";
                            return false;
                        }
                    }
                }

                if (nuller)
                {
                    lastOp = false;
                    nuller = false;
                    variable = "";
                }
            }

            return true;
        }
    }
    public class Variable
    {
        public string name;
        public string value;

        public Variable(string name, string value)
        {
            this.name = name;
            this.value = value;
        }
    }

    class Operator
    {
        public char symbol;
        public int priority;
        public Func<Token, Token, string> execute;


        public Operator(char symbol, int priority, Func<Token, Token, string> execute)
        {
            if (symbol == 0) throw new Exception("Symbol can not be empty");
            if (execute == null) throw new Exception("Function need to be passed as 3'rd argument");

            this.symbol = symbol;
            this.priority = priority;
            this.execute = execute;
        }
    }

    class Token
    {
        public enum Type
        {
            Number,
            Operator,
            Function,
            Variable
        }

        public Type type;
        public string value;

        public Token(Type type, string value)
        {
            this.type = type;
            this.value = value;
        }

        public Token(string value)
        {
            this.type = Type.Number;
            this.value = value;
        }
    }

    class Interpreter
    {
        private static List<Function> functions;
        private static List<Variable> variables;

        private static Operator[] operators = new Operator[]
        {
            new Operator ( '*', 2, ( f, s ) => (double.Parse( f.value ) * double.Parse( s.value )).ToString() ),
            new Operator ( '/', 2, ( f, s ) => (double.Parse( f.value ) / double.Parse( s.value )).ToString() ),
            new Operator ( '%', 2, ( f, s ) => (double.Parse( f.value ) % double.Parse( s.value )).ToString() ),
            new Operator ( '+', 1, ( f, s ) => (double.Parse( f.value ) + double.Parse( s.value )).ToString() ),
            new Operator ( '-', 1, ( f, s ) => (double.Parse( f.value ) - double.Parse( s.value )).ToString() ),
            new Operator ( '=', 0, ( f, s ) => ( f.value = s.value ).ToString() )
        };

        static Interpreter()
        {
            if (functions == null)
                functions = new List<Function>(10);
            if (variables == null)
                variables = new List<Variable>(10);
        }

        public static void Reset()
        {
            functions = new List<Function>(10);
            variables = new List<Variable>(10);
        }

        public static string eval(string command)
        {
            var data = command.Split();
            if (data[0] == "fn")
                return addFunction(data);
            try
            {
                return Execute(command, 0);
            }
            catch (Exception ex)
            {
                return ex.Message;
            }
        }

        private static bool isOperator(char symbol)
        {
            foreach (Operator op in operators)
                if (op.symbol == symbol)
                    return true;
            return false;
        }

        private static bool isNumber(string value)
        {
            double tmp;
            return double.TryParse(value, out tmp);
        }

        private static void LogToken(Token token, int depth)
        {
            for(int now = 0; now < depth; now++)
                Console.Write("   ");
            Console.WriteLine("Added token {0}( {1} )", token.type.ToString(), token.value);
        }

        private static string Execute(string data, int depth)
        {
            if (string.IsNullOrWhiteSpace(data)) return null;

            var tokens = new List<Token>(100);

            string buffer = "";
            bool clear = false;
            bool capture = false;
            int level = 0;

            for (int now = 0; now <= data.Length; ++now )
            {
                char smb = (char) 0;
                if ( now == data.Length) clear = true;
                if (!clear)
                {
                    smb = data[now];
                    if (isOperator(smb)) clear = true;
                    if (buffer.Length == 1 && isOperator(buffer[0])) clear = true;
                    if (smb == ' ') clear = true;
                }
                
                if (smb == '(' && !capture)
                {
                    level = 1;
                    buffer = "";
                    capture = true;
                    continue;
                }
                
                if(capture)
                {
                    clear = false;

                    if(smb == '(')
                        level++;
                    else if (smb == ')')
                        level--;

                    if(level == 0)
                    {
                        tokens.Add(new Token(Token.Type.Number, Execute(buffer, depth + 1)));
                        LogToken(tokens[tokens.Count - 1], depth);
                        buffer = "";
                        capture = false;
                        
                        continue;
                    }
                    buffer += smb;
                    continue;
                }

                if (clear && buffer.Length != 0)
                {
                    if (isOperator(buffer[0]))
                    {
                        tokens.Add(new Token(Token.Type.Operator, buffer));
                        if (buffer[0] == '=' && (tokens.Count < 2 || tokens[tokens.Count - 2].type != Token.Type.Variable))
                            throw new Exception("ERROR: Invalid input");
                    }
                    else if (IsFunction(buffer))
                        tokens.Add(new Token(Token.Type.Function, buffer));
                    else if (isNumber(buffer))
                        tokens.Add(new Token(Token.Type.Number, buffer));
                    else
                        tokens.Add(new Token(Token.Type.Variable, buffer));
                    
                    LogToken(tokens[tokens.Count - 1], depth);

                    buffer = "";
                    clear = false;
                }
                if (smb != ' ' && smb != 0) buffer += smb;
                else clear = false;
            }

            for (int now = tokens.Count - 1; now >= 0; --now)
            {
                if (tokens[now].type == Token.Type.Function)
                {
                    Function func = GetFunction(tokens[now].value);
                    if (func.parameters.Length == 0)
                        tokens[now] = new Token(Token.Type.Number, func.Execute(new string[0]));
                }
            }

            while (tokens.Count > 1)
            {
                bool changed = false;
                // PARSE SIMPLE MATH EXPRESSION
                bool waitingNumber = true;
                bool isToo = false;
                int startTokenIndex = tokens.Count - 1;
                for (int now = tokens.Count - 1; now >= 0; --now)
                {
                    if (now == 0 || (tokens[now - 1].type != Token.Type.Number && tokens[now - 1].type == Token.Type.Function)) isToo = true;
                    
                    if (tokens[now].type == Token.Type.Variable)
                    {
                        if (now == tokens.Count - 1 || tokens[now + 1].value != "=")
                        {
                            Variable var = GetVariable(tokens[now].value);
                            if (var == null)
                                throw new Exception("ERROR Invalid identifier. No variable with name '" + tokens[now].value + "' was found.");
                            tokens[now] = new Token(Token.Type.Number, var.value);
                            changed = true;
                        }
                        else
                        {
                            isToo = true;
                        }
                    }

                    if (tokens[now].type == Token.Type.Number || tokens[now].type == Token.Type.Operator)
                    {
                        if ((tokens[now].type == Token.Type.Number && !waitingNumber) || (tokens[now].type == Token.Type.Operator && waitingNumber))
                        {
                            startTokenIndex = now + 1;
                            isToo = false;
                            waitingNumber = false;
                            continue;
                        }
                        else
                        {
                            if(tokens[now].value == "=")
                                isToo = true;
                            else
                                waitingNumber = !waitingNumber;
                        }
                    }

                    if (isToo)
                    {
                        isToo = false;

                        if(tokens[now].value == "=" && startTokenIndex == now + 1)
                        {
                            changed = true;
                            SetVariable(tokens[now - 1].value, tokens[now + 1].value);
                            tokens[now - 1] = new Token(Token.Type.Number, tokens[now + 1].value);
                            tokens.RemoveAt(now);
                            tokens.RemoveAt(now);
                            waitingNumber = true;
                            startTokenIndex = now - 1;

                            if(tokens.Count == 1)
                                break;

                            continue;
                        }

                        if(tokens[now].type == Token.Type.Function && waitingNumber)
                        {
                            waitingNumber = true;
                            startTokenIndex = now - 2;
                            now -= 2;
                            continue;
                        }
                        waitingNumber = true;

                        if(tokens[now].type != Token.Type.Number)
                            now++;

                        for (int priority = 3; priority >= 0; --priority)
                        {
                            for (int i = now; i < startTokenIndex; ++i)
                            {
                                if (tokens[i].type == Token.Type.Operator)
                                {
                                    var op = GetOperator(tokens[i].value[0]);
                                    if (op.priority == priority)
                                    {
                                        tokens[i - 1].value = op.execute(tokens[i - 1], tokens[i + 1]);
                                        tokens.RemoveAt(i);
                                        tokens.RemoveAt(i);
                                        i -= 2;
                                        startTokenIndex -= 2;
                                        changed = true;
                                    }
                                }
                            }
                        }

                        if(tokens[now].type != Token.Type.Number)
                            now--;

                        if (now > 1 && (tokens[now - 2].type == Token.Type.Variable || tokens[now - 2].type == Token.Type.Function) && tokens[now - 1].value == "=")
                        {
                            int index = 0;
                            foreach(Function func in functions)
                            {
                                if(func.name == tokens[now - 2].value)
                                    throw new Exception("ERROR: function with same name already exist");
                                index++;
                            }
                            SetVariable(tokens[now - 2].value, tokens[now].value);
                            tokens[now - 2] = new Token(Token.Type.Number, tokens[now].value);
                            tokens.RemoveAt(now - 1);
                            tokens.RemoveAt(now - 1);
                            now -= 2;
                            changed = true;
                        }
                    }
                }

                // EXECUTE FUNCTIONS
                for (int now = tokens.Count - 1; now >= 0; --now)
                {
                    if (tokens[now].type == Token.Type.Function)
                    {
                        Function func = GetFunction(tokens[now].value);

                        string[] args = new string[func.parameters.Length];
                        for (int i = 0; i < args.Length; ++i)
                            args[i] = tokens[now + i + 1].value;

                        tokens[now] = new Token(Token.Type.Number, func.Execute(args));
                        for (int i = 0; i < args.Length; i++) tokens.RemoveAt(now + 1);
                        changed = true;
                    }
                }

                if(!changed)
                    throw new Exception("ERROR: Invalid input");
            }
            
            if(tokens[0].type == Token.Type.Variable)
                return GetVariable(tokens[0].value)?.value;

            return tokens[0]?.value;
        }

        private static Operator GetOperator(char symbol)
        {
            foreach (Operator o in operators)
                if (o.symbol == symbol)
                    return o;
            return null;
        }
        private static Variable GetVariable(string name)
        {
            foreach (Variable v in variables)
                if (v.name == name)
                    return v;
            return null;
        }
        private static Function GetFunction(string name)
        {
            foreach (Function f in functions)
                if (f.name == name)
                    return f;
            return null;
        }

        private static string addFunction(string[] data)
        {
            string name = data[1];
            string parameters = "";
            string body = "";
            bool isBody = false;
            for (int now = 2; now < data.Length; ++now)
            {
                if (data[now] == "=>") { isBody = true; continue; }
                if (isBody) body += data[now] + " ";
                else parameters += data[now] + " ";
            }

            var func = new Function(name, parameters.TrimEnd(), body.TrimEnd());
            if (func.Test())
            {
                int index = 0;
                foreach (Function f in functions)
                {
                    if (f.name == name)
                    {
                        functions[index] = func;
                        break;
                    }
                    index++;
                }
                if (index == functions.Count)
                    functions.Add(func);
            }
            else return func.error;

            return null;
        }
        private static string SetVariable(string name, string value)
        {
            Variable var = GetVariable(name);

            if ( var == null) variables.Add(new Variable(name, value));
            else var.value = value;

            return value;
        }

        private static bool IsFunction(string name)
        {
            foreach (Function f in functions)
                if (f.name == name)
                    return true;
            return false;
        }
        private static bool isVariable(string name)
        {
            foreach (Variable f in variables)
                if (f.name == name)
                    return true;
            return false;
        }
    }
}
namespace InterpreterKata
{
  public class Interpreter 
  {
      public Interpreter()
      {
        MPerlInterpreter.Interpreter.Reset();
      }
      
      public double? input(string input)
      {
          Console.WriteLine("I : " + input);
          string data = MPerlInterpreter.Interpreter.eval(input);
          Console.WriteLine(data);
          try {
            return double.Parse(data);
          } catch ( Exception ex) {
            Console.WriteLine(ex.Message + " : " + input + " : " + data);
            return null;
          }
      }
  }
}

___________________________________________________________________________
using System.Linq;
using System.Linq.Expressions;
using System.Runtime.InteropServices.WindowsRuntime;

namespace InterpreterKata
{
    using System;
    using System.Collections.Generic;
    using System.Text.RegularExpressions;

    public class Interpreter
    {
        private readonly Dictionary<string, LambdaExpression> _functions = new Dictionary<string, LambdaExpression>();
        private readonly Dictionary<ParameterExpression, Expression> _variables = new Dictionary<ParameterExpression, Expression>();
        private readonly Dictionary<string, ParameterExpression> _localVariables = new Dictionary<string, ParameterExpression>();

        private static readonly Regex ConstantRegex = new Regex(@"[0-9]*(\.?[0-9]+)");
        private static readonly Regex LeftAssociativeOperatorRegex = new Regex(@"[-+*/%]{1}");
        private static readonly Regex RightAssociativeOperatorRegex = new Regex(@"(=|=>)");
        private static readonly Regex VariableRegex = new Regex(@"[A-Za-z_][A-Za-z0-9_]*");

        public double? input(string input)
        {
            Console.WriteLine(DateTime.Now.ToString("O") + " - input: " + input);
            try
            {
                var tokens = this.Tokenize(input);
                var orderedTokens = this.ReorderTokensWithOperatorPrecedence(tokens.ToList());
                var expression = this.BuildExpressionTree(orderedTokens);

                var resultBlock = new List<Expression>(this._variables.Select(x => x.Value));
                resultBlock.Add(expression);

                var le = Expression.Lambda<Func<double>>(Expression.Block(this._variables.Keys, resultBlock));
                var compiledExpression = le.Compile();
                return compiledExpression();
            }
            catch
            {
                return null;
            }
        }

        private Queue<string> ReorderTokensWithOperatorPrecedence(IList<string> tokens)
        {
            var operatorStack = new Stack<string>();
            var orderedTokens = new Queue<string>();
            for (var i = 0; i < tokens.Count(); i++)
            {
                if (tokens[i] == "fn")
                {
                    orderedTokens.Enqueue(tokens[i]);
                    i++;
                    var funcName = tokens[i];
                    orderedTokens.Enqueue(funcName);
                    this._functions.Remove(funcName);
                }
                else if (this._functions.ContainsKey(tokens[i]) || RightAssociativeOperatorRegex.IsMatch(tokens[i]))
                {
                    // Function are like operators, BUT are right associative
                    var tokenPrecedence = this.PrecedenceLevel(tokens[i]);
                    while (operatorStack.Count > 0
                           && operatorStack.Peek() != "("
                           && tokenPrecedence < this.PrecedenceLevel(operatorStack.Peek()))
                    {
                        var op = operatorStack.Pop();
                        orderedTokens.Enqueue(op);
                    }

                    operatorStack.Push(tokens[i]);
                }
                else if (ConstantRegex.IsMatch(tokens[i]) || VariableRegex.IsMatch(tokens[i]))
                {
                    orderedTokens.Enqueue(tokens[i]);
                }
                else if (LeftAssociativeOperatorRegex.IsMatch(tokens[i]))
                {
                    var tokenPrecedence = this.PrecedenceLevel(tokens[i]);
                    while (operatorStack.Count > 0
                           && operatorStack.Peek() != "("
                           && tokenPrecedence <= this.PrecedenceLevel(operatorStack.Peek()))
                    {
                        var op = operatorStack.Pop();
                        orderedTokens.Enqueue(op);
                    }

                    operatorStack.Push(tokens[i]);
                }
                else if (tokens[i] == "(")
                {
                    operatorStack.Push(tokens[i]);
                }
                else if (tokens[i] == ")")
                {
                    string op;
                    do
                    {
                        op = operatorStack.Pop();
                        if (op != "(")
                        {
                            orderedTokens.Enqueue(op);
                        }
                    }
                    while (op != "(");
                }
            }

            // Add remaining operators to the output.
            while (operatorStack.Count > 0)
            {
                orderedTokens.Enqueue(operatorStack.Pop());
            }

            return orderedTokens;
        }

        private Expression BuildExpressionTree(Queue<string> orderedTokens)
        {
            var outputStack = new Stack<Expression>();
            while (orderedTokens.Count > 0)
            {
                var token = orderedTokens.Dequeue();

                if (LeftAssociativeOperatorRegex.IsMatch(token) || RightAssociativeOperatorRegex.IsMatch(token))
                {
                    outputStack.Push(this.OperatorToExpression(token, outputStack));
                }
                else if (this._functions.ContainsKey(token))
                {
                    var func = this._functions[token];
                    var funcParams = new Stack<Expression>();
                    for (var i = 0; i < func.Parameters.Count; i++)
                    {
                        funcParams.Push(outputStack.Pop());
                    }

                    outputStack.Push(Expression.Invoke(this._functions[token], funcParams));
                }
                else if (ConstantRegex.IsMatch(token))
                {
                    outputStack.Push(Expression.Constant(double.Parse(token)));
                }

                else if (VariableRegex.IsMatch(token))
                {
                    var parameterExpression = this._variables.Keys.FirstOrDefault(x => x.Name == token);
                    if (this._localVariables.ContainsKey(token))
                    {
                        parameterExpression = this._localVariables[token];
                    }
                    else if (parameterExpression == null)
                    {
                        parameterExpression = Expression.Variable(typeof(double), token);
                    }

                    this._localVariables[token] = parameterExpression;
                    outputStack.Push(parameterExpression);
                }
            }

            if (outputStack.Count > 1)
            {
                throw new InvalidOperationException("Too many operand with not enough operators");
            }

            return outputStack.Pop();
        }

        private Expression OperatorToExpression(string op, Stack<Expression> outputStack)
        {
            Expression e = null;
            var right = outputStack.Pop();
            var left = outputStack.Pop();
            switch (op)
            {
                case "+":
                    e = Expression.Add(left, right);
                    break;
                case "-":
                    e = Expression.Subtract(left, right);
                    break;
                case "*":
                    e = Expression.Multiply(left, right);
                    break;
                case "/":
                    e = Expression.Divide(left, right);
                    break;
                case "%":
                    e = Expression.Modulo(left, right);
                    break;
                case "=":
                    e = Expression.Assign(left, right);
                    var variable = (ParameterExpression)left;
                    if (this._functions.ContainsKey(variable.Name))
                    {
                        throw new InvalidOperationException("There's already a function define with that name");
                    }

                    this._variables[variable] = e;
                    break;
                case "=>":
                    var funcName = left as ParameterExpression;
                    var funcKeyWord = outputStack.Pop() as ParameterExpression;
                    var funcParams = new Stack<ParameterExpression>();
                    while (funcKeyWord != null && funcKeyWord.Name != "fn")
                    {
                        funcParams.Push(funcName);
                        funcName = funcKeyWord;
                        funcKeyWord = outputStack.Pop() as ParameterExpression;
                    }

                    if (this._variables.Any(x => x.Key.Name == funcName.Name))
                    {
                        throw new InvalidOperationException("There's already a function define with that name");
                    }

                    var func = Expression.Lambda(right, funcName.Name, funcParams);
                    this._functions[funcName.Name] = func;
                    e = func;
                    break;
            }

            return e;
        }

        private IEnumerable<string> Tokenize(string input)
        {
            var rgxMain = new Regex("=>|[-+*/%=\\(\\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*(\\.?[0-9]+)");
            var matches = rgxMain.Matches(input);
            return (from Match m in matches select m.Groups[0].Value);
        }

        public int PrecedenceLevel(string str)
        {
            switch (str)
            {
                case "*":
                case "/":
                case "%":
                    return 4;
                case "+":
                case "-":
                    return 3;
                case "=":
                    return 2;
                case "=>":
                    return 1;
                default:
                    // Everything else should be functions
                    return 0;
            }
        }
    }
}
