5470c635304c127cad000f0d


using System;

public class RegExpParser {
  public static Reg.Exp parse (string input) {
    int pos = 0;
    try {
      return parse(input + "\0", ref pos);
    } catch (InvalidOperationException) {
      return null;
    }
  }
  
  private static Reg.Exp parse(string input, ref int pos) {
    var lhs = parseStr(input, ref pos);
    while (pos < input.Length-1 && input[pos] == '|') {
      ++pos;
      var rhs = parseStr(input, ref pos);
      lhs = Reg.or(lhs, rhs);
    }
    return lhs;
  }
  
  private static Reg.Exp parseStr(string input, ref int pos) {
    Reg.Exp exp = parseFac(input, ref pos);
    if (pos < input.Length-1 && "|)".IndexOf(input[pos]) < 0) {
      exp = Reg.str(exp);
      do {
        exp = Reg.add((Reg.Str)exp, parseFac(input, ref pos));
      } while (pos < input.Length-1 && "|)".IndexOf(input[pos]) < 0);
    }
    return exp;
  }
  
  private static Reg.Exp parseFac(string input, ref int pos) {
    Reg.Exp exp;
    if (input[pos] == '(') {
      ++pos;
      exp = parse(input, ref pos);
      ++pos;
    } else if (input[pos] == '.') {
      exp = Reg.any();
      ++pos;
    } else if ("()*|.\0".IndexOf(input[pos]) < 0) {
      exp = Reg.normal(input[pos++]);
    } else {
      throw new InvalidOperationException($"{input[pos]} unexpected");
    }
  
    if (pos < input.Length - 1 && input[pos] == '*') {
      exp = Reg.zeroOrMore(exp);
      ++pos;
    }
    
    return exp;
  }
}
___________________________________________
using System;
using System.Collections.Generic;
public class RegExpParser {
  public static Reg.Exp parse (string s) {
    var i = 0;
    try {
      var ast = parseOr();
      if (i != s.Length) throw new Exception("Invalid");
      return ast;
    } catch {
      return null;
    }
    Reg.Exp parseNormal() => @"*|()".Contains(s[i]) ? null : Reg.normal(s[i++]);
    Reg.Exp parseAny() {
      if (s[i] == '.') { i++; return Reg.any(); }
      return parseNormal();
    }
    Reg.Exp parseGroup() {
      if (s[i] == '(') {
        i++;
        var next = parseOr();
        if (s[i++] != ')') throw new Exception("Unbalanced parens");
        return next;
      } else {
        return parseAny();
      }
    }
    Reg.Exp parseZeroOrMore() {
      if (i >= s.Length) return null;
      var next = parseGroup();
      if (i >= s.Length || next == null) return next;
      if (s[i] == '*') {
        i++;
        return Reg.zeroOrMore(next);
      }
      return next;
    }
    Reg.Exp parseStr() {
      var set = new List<Reg.Exp>();
      Reg.Exp r = null;
      while ((r = parseZeroOrMore()) != null) set.Add(r);
      if (set.Count == 0) return null;
      return (set.Count == 1) ? set[0] : parseSeq(set);
    }
    Reg.Exp parseOr() {
      var next = parseStr();
      if (i >= s.Length) return next;
      if (s[i] == '|') {
        i++;
        return Reg.or(next, parseStr());
      } else {
        return next;
      }
    }
    Reg.Exp parseSeq(List<Reg.Exp> seq) {
      Reg.Str next = null;
      foreach (var exp in seq) {
        if (next == null) next = Reg.str(exp);
        else next = Reg.add(next, exp);
      }
      return next;
    }
  }
}
___________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class RegExpParser {
  public static Reg.Exp parse (string input) {
    var scanner = new Scanner(input);
    var tokens = scanner.ScanTokens();
    var parser = new Parser(tokens);

    try
    {
        var expr = parser.Parse();
        return expr;
    }
    catch (Exception ex)
    {
        return null;
    }
  }
}


    public class Parser
    {
        private readonly List<Token> tokens;

        private int current = 0;

        private Token Peek => tokens[current];
        private Token Previous => tokens[current - 1];
        private bool AtEnd => Peek.Type == TokenType.EOF;

        public Parser(List<Token> tokens)
        {
            this.tokens = tokens;
        }

        public Reg.Exp Parse()
        {
            if (AtEnd)
            {
                return null;
            }

            Reg.Exp expr = Expression();

            while(!AtEnd)
            {
                expr = Reg.add(Reg.str(expr), Expression());
            }

            return expr;
        }

        private Reg.Exp Expression()
        {
            return AltExpression();
        }

        private Reg.Exp AltExpression()
        {
            var expr = ContatenationExpression();

            if (Match(TokenType.PIPE))
            {
                var expr2 = ContatenationExpression();
                expr = Reg.or(expr, expr2);
            }

            return expr;
        }

        private Reg.Exp StarExpression()
        {
            var expr = Primary();

            if (Match(TokenType.STAR))
            {
                expr = Reg.zeroOrMore(expr);
            }

            return expr;
        }

        private Reg.Exp ContatenationExpression()
        {
            bool first = false;
            Reg.Exp star = null;

            while (!AtEnd 
                && Peek.Type != TokenType.RIGHT_PAREN 
                && Peek.Type != TokenType.PIPE)
            {
                var next = StarExpression();
                if (star is null)
                {
                    star = next;
                    first = true;
                } else
                {
                    if (first)
                    {
                        star = Reg.add(Reg.str(star), next);
                    } else
                    {
                        star = Reg.add(star as Reg.Str, next);
                    }
                    first = false;
                }
            }

            if (star is null)
            {
                throw new Exception("Invalid");
            }

            return star;
        }

        private Reg.Exp Primary()
        {
            if (Match(TokenType.LEFT_PAREN))
            {
                if (Match(TokenType.RIGHT_PAREN))
                {
                    throw new Exception($"Unknown {Peek}");
                }

                Reg.Exp expr = Expression();

                while (!Match(TokenType.RIGHT_PAREN))
                {
                    expr = Reg.add(Reg.str(expr), Expression());
                }
                return expr;
            } else if (Match(TokenType.CHAR))
            {
                var expr = Reg.normal(Previous.Lexeme[0]);
                //while (Match(TokenType.CHAR))
                //{
                //    expr = Reg.add(Reg.str(expr), Expression());
                //}

                return expr;
            } else if (Match(TokenType.DOT))
            {
                return Reg.any();
            }
            else
            {
                throw new Exception($"Unknown {Peek}");
            }
        }

        private Token Consume(TokenType type, string errorMessage)
        {
            if (Check(type))
            {
                return Advance();
            }
            else
            {
                throw new Exception($"{Peek}, {errorMessage}");
            }
        }

        private bool Match(params TokenType[] types)
        {
            foreach (var type in types)
            {
                if (Check(type))
                {
                    Advance();
                    return true;
                }
            }

            return false;
        }

        private bool Check(TokenType type)
        {
            return AtEnd ? false : Peek.Type == type;
        }

        private Token Advance()
        {
            if (!AtEnd)
            {
                current++;
            }

            return Previous;
        }
    }

public enum TokenType
{
    LEFT_PAREN, RIGHT_PAREN,
    DOT,
    STAR,
    CHAR,
    PIPE,
    EOF,
}

public class Token
{
    public TokenType Type { get; }
    public string Lexeme { get; }
    public object? Literal { get; }

    internal Token(TokenType type, string lexeme, object? literal)
    {
        Type = type;
        Lexeme = lexeme;
        Literal = literal;
    }

    public override string? ToString()
    {
        return $"{Type} {Lexeme} {Literal}";
    }
}

    public class Scanner
    {
        private readonly string source;


        private readonly List<Token> tokens = new();

        private int start = 0;
        private int current = 0;
        public bool AtEnd => current >= source.Length;

        public Scanner(string source)
        {
            this.source = source;
        }

        public List<Token> ScanTokens()
        {
            while (!AtEnd)
            {
                start = current;
                ScanToken();
            }
            tokens.Add(new Token(TokenType.EOF, "", null));

            return tokens;
        }

        private void ScanToken()
        {
            var c = Advance();
            switch(c)
            {
                case '(':
                    AddToken(TokenType.LEFT_PAREN);
                    break;

                case ')':
                    AddToken(TokenType.RIGHT_PAREN);
                    break;

                case '*':
                    AddToken(TokenType.STAR);
                    break;

                case '.':
                    AddToken(TokenType.DOT);
                    break;

                case '|':
                    AddToken(TokenType.PIPE);
                    break;

                default:
                    AddToken(TokenType.CHAR, c.ToString());
                    break;
            }
        }

        private char Advance()
        {
            return source[current++];
        }

        private void AddToken(TokenType tokenType, object? literal = null)
        {
            string text = source.Substring(start, current - start);
            tokens.Add(new Token(tokenType, text, literal));
        }
    }
___________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

#nullable enable
public sealed class RegExpParser
{
  public static Reg.Exp? parse(string input)
  {
    try
    {
      return new RegExpParser().Parse(input);
    }
    catch (Exception ex)
    {
      Console.WriteLine(ex);
      return null;
    }
  }
  
  public Reg.Exp Parse(string input)
  {
    if (input == "")
      throw new ArgumentException("input is empty");
    foreach (var letter in input)
      expressions.Add(ParseCharacter(letter));
    if (rememberGroupPositions.Count > 0)
      throw new ClosingBracketMissing();
    return GetAndMergeLastExpressions();
  }

  public class ClosingBracketMissing : Exception { }
  private readonly List<Reg.Exp> expressions = new();
  private readonly Stack<int> rememberGroupPositions = new();

  private Reg.Exp ParseCharacter(char letter)
  {
    switch (letter)
    {
    case '*' when expressions.Count > 0 && expressions[^1] is not Reg.ZeroOrMore:
      return new Reg.ZeroOrMore(GetAndMergeLastExpressions(true));
    case '|' when expressions.Count > 0:
      return new Reg.Or(GetAndMergeLastExpressions(), null!);
    case '.':
      return new Reg.Any();
    case '(':
      rememberGroupPositions.Push(expressions.Count + 1);
      return new StartSequence();
    case ')':
      var currentGroupStartPosition = rememberGroupPositions.Pop();
      var group = AddExpressions(expressions.Skip(currentGroupStartPosition).ToList());
      expressions.RemoveRange(currentGroupStartPosition - 1, expressions.Count - currentGroupStartPosition + 1);
      return group;
    default:
      if (letter != '*' || letter == '|')
        return new Reg.Normal(letter);
      throw new UnsupportedCharacterCannotParse(letter);
    }
  }

  private Reg.Exp GetAndMergeLastExpressions(bool onlyLastOne = false)
  {
    Reg.Exp lastOrMergedExpression;
    if (onlyLastOne || expressions.Count - (rememberGroupPositions.Count == 0
        ? 0
        : rememberGroupPositions.Peek()) == 1)
    {
      lastOrMergedExpression = expressions[^1];
      expressions.Remove(lastOrMergedExpression);
    }
    else
    {
      lastOrMergedExpression = AddExpressions(expressions);
      expressions.Clear();
    }
    return lastOrMergedExpression;
  }

  public sealed class UnsupportedCharacterCannotParse : Exception
  {
    public UnsupportedCharacterCannotParse(char letter) : base(letter.ToString()) { }
  }

  private static Reg.Exp AddExpressions(IReadOnlyList<Reg.Exp> expressions)
  {
    if (expressions[0] is Reg.Or or)
    {
      var field = or.GetType().GetField("right", System.Reflection.BindingFlags.NonPublic
    | System.Reflection.BindingFlags.Instance)!;
      if (field.GetValue(or) == null)
      {
        var right = expressions.Count > 2
          ? AddExpressions(expressions.Skip(1).ToList())
          : expressions.Count == 1
            ? null!
            : expressions[1];
        field.SetValue(or, right);
        return or;
      }
    }
    if (expressions.Count == 1)
      return expressions[0];
    Reg.Exp sequence = new Reg.Str(expressions.ToList());
    return sequence;
  }
}
public class StartSequence : Reg.Exp{}
