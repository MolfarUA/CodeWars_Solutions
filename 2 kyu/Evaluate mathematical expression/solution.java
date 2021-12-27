import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MathEvaluator {

  private final Pattern parens = Pattern.compile("(-?)\\(([^()]+)\\)");
  private final Pattern divMul = Pattern.compile("(-?[0-9.]+)\\s*(/|\\*)\\s*(-?[0-9.]+)");
  private final Pattern addSub = Pattern.compile("(-?[0-9.]+)\\s*(\\+|-)\\s*(-?[0-9.]+)");

  public double calculate(String expression) {
    Matcher m;
    while ((m = parens.matcher(expression)).find()) {
      String eval = evaluate(m.group(2));
      if (!m.group(1).isEmpty())
        eval = eval.startsWith("-") ? eval.substring(1) : "-" + eval;
      expression = expression.substring(0, m.start()) + eval + expression.substring(m.end());
    }
    return Double.parseDouble(evaluate(expression));
  }
  
  private String evaluate(String expression) {
    Matcher m;
    while ((m = divMul.matcher(expression)).find()) {
      double x = Double.parseDouble(m.group(1));
      double y = Double.parseDouble(m.group(3));
      double v = m.group(2).equals("*") ? x * y : x / y;
      expression = expression.substring(0, m.start()) + v + expression.substring(m.end());
    }
    while ((m = addSub.matcher(expression)).find()) {
      double x = Double.parseDouble(m.group(1));
      double y = Double.parseDouble(m.group(3));
      double v = m.group(2).equals("+") ? x + y : x - y;
      expression = expression.substring(0, m.start()) + v + expression.substring(m.end());
    }
    return expression;
  }

}
____________________________________________________
/*
expr   -> term {+ term}*
        | term {- term}*

term   -> factor {* factor}*
        | factor {/ factor}*

factor -> -pfactor
        | pfactor

pfactor -> digits
         | (expr)
*/

import java.util.*;

enum TokenType {
    NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN
}

class Token {
    final TokenType type;
    final String value;

    Token(TokenType type) {
        this.type = type;
        this.value = "";
    }

    Token(TokenType type, String value) {
        this.type = type;
        this.value = value;
    }
}

class MathEvaluator {

    private Iterator<Token> tokenIter;
    private Token curToken;
    private Token nextToken;

    private void scan(String input) {
        ArrayList<Token> tokens = new ArrayList<>();
        for (int i = 0; i < input.length(); ++i) {
            char c = input.charAt(i);
            if (c == '+') { tokens.add(new Token(TokenType.PLUS)); }
            else if (c == '-') { tokens.add(new Token(TokenType.MINUS)); }
            else if (c == '*') { tokens.add(new Token(TokenType.TIMES)); }
            else if (c == '/') { tokens.add(new Token(TokenType.DIVIDE)); }
            else if (c == '(') { tokens.add(new Token(TokenType.LPAREN)); }
            else if (c == ')') { tokens.add(new Token(TokenType.RPAREN)); }
            else if (Character.isDigit(c) || c == '.') {
                int j = i+1;
                while (j < input.length() && (Character.isDigit(input.charAt(j)) || input.charAt(j) == '.')) ++j;
                tokens.add(new Token(TokenType.NUM, input.substring(i, j)));
                i = j - 1;
            } else if (!Character.isWhitespace(c)) {
                throw new Error(String.format("Unknown token at position %d: %c", i, c));
            }
        }

        tokenIter = tokens.iterator();
    }

    private void advance() {
        curToken = nextToken;
        nextToken = tokenIter.hasNext() ? tokenIter.next() : null;
    }

    private boolean accept(TokenType tk) {
        if (nextToken != null && nextToken.type == tk) {
            advance();
            return true;
        }
        return false;
    }

    private void expect(TokenType tk) {
        if (!accept(tk)) {
            throw new Error(String.format("Expected token type: %s, but token <%s, %s> occurred",
                    tk, nextToken.type, nextToken.value));
        }
    }

    private double expr() {
        double val = term();
        while (accept(TokenType.PLUS) || accept(TokenType.MINUS)) {
            TokenType type = curToken.type;
            double rhs = term();
            if (type == TokenType.PLUS) val += rhs;
            else val -= rhs;
        }
        return val;
    }

    private double term() {
        double val = factor();
        while (accept(TokenType.TIMES) || accept(TokenType.DIVIDE)) {
            TokenType type = curToken.type;
            double rhs = factor();
            if (type == TokenType.TIMES) val *= rhs;
            else val /= rhs;
        }
        return val;
    }

    private double factor() {
        if (accept(TokenType.MINUS)) {
            return -pfactor();
        } else {
            return pfactor();
        }
    }

    private double pfactor() {
        if (accept(TokenType.NUM)) {
            return Double.valueOf(curToken.value);
        } else if (accept(TokenType.LPAREN)) {
            double val = expr();
            expect(TokenType.RPAREN);
            return val;
        } else {
            throw new Error(String.format("Expected NUM or LPAREN, but token <%s, %s> occurred",
                    nextToken.type, nextToken.value));
        }
    }

    public double calculate(String expression) {
        scan(expression);
        advance();
        return expr();
    }
}
_____________________________________________________
import java.util.*;

public class MathEvaluator {

  private char[] stream;
  private int ptr;

  // Implementation using a simple LL(1) parser
  public double calculate(String expression) {
    // X  ::= F [[+ | -] F]*
    // F  ::= S [[* | /] S]*
    // S  ::= - S
    //        ( X )
    //        L
    // L  ::= [DIGIT]+ [. [DIGIT]+]?
    
    stream = expression.replaceAll("\\s", "").toCharArray();
    return rdExpression();
  }
  
  private double rdExpression() {
    double acc = rdFactor();
    while (lookahead() == '+' || lookahead() == '-') {
      char op = consume();
      if (op == '+') {
        acc += rdFactor();
      } else {
        acc -= rdFactor();
      }
    }
    return acc;
  }
  
  private double rdFactor() {
    double acc = rdPrimary();
    while (lookahead() == '*' || lookahead() == '/') {
      char op = consume();
      if (op == '*') {
        acc *= rdPrimary();
      } else {
        acc /= rdPrimary();
      }
    }
    return acc;
  }
  
  private double rdPrimary() {
    if (lookahead() == '-') {
      consume(); // -
      return -rdPrimary();
    } else if (lookahead() == '(') {
      consume(); // (
      double tmp = rdExpression();
      consume(); // )
      return tmp;
    } else {
      return rdLiteral();
    }
  }
  
  private double rdLiteral() {
    StringBuilder sb = new StringBuilder();
    while (lookahead() >= '0' && lookahead() <= '9') {
      sb.append(consume());
    }
    if (lookahead() == '.') {
      sb.append(consume());
      while (lookahead() >= '0' && lookahead() <= '9') {
        sb.append(consume());
      }
    }
    return Double.parseDouble(sb.toString());
  }
  
  private char consume() {
    assert ptr < stream.length;
    return stream[ptr++];
  }
  
  private char lookahead() {
    if (ptr >= stream.length) {
      return (char) 0;
    }
    return stream[ptr];
  }

}
___________________________________________________
import java.util.*;

public class MathEvaluator {
   private Character[] operations = {'/','*','-','+'};
   
   public double calculate(String expression) {
      expression = expression.replace(" ", "");
      return Double.parseDouble(simplifyExpression(expression));
   }

   private String simplifyExpression(String expression) {
      String trailingExpression = "";
      ArrayList<Character> opList = new ArrayList<Character>();
      
      //removeBrackets
      for (int i = 0; i < expression.length(); i++) {
         if (expression.charAt(i) == '(') {
            expression = expression.substring(0, i) + simplifyExpression(expression.substring(i+1));
         } else if (expression.charAt(i) == ')') {
            trailingExpression = expression.substring(i+1);
            expression = expression.substring(0, i);
         }
      }

      //extract operation order
      for (char c : expression.toCharArray()) {
         if (Arrays.asList(operations).contains(c)) opList.add(c);
      }

      //split on operations and handle -- etc
      String[] numbers = expression.split("[-+*/]");
      ArrayList<Double> numList = new ArrayList<Double>();
      int diff = 0, sign = 1;
      for (int n = 0; n < numbers.length; n++) {
         if (!numbers[n].isEmpty()) {
            numList.add(sign*Double.parseDouble(numbers[n]));
            sign = 1;
         } else {
            switch (opList.get(n-diff)) {
               case '+': opList.remove(n-diff++); break;
               case '-': opList.remove(n-diff++); sign *= -1; break;
            }
         }
      }

      //perform operations in order
      for (Character op : operations) {
         int i = 0;
         while (i < opList.size()) {
            if (opList.get(i) == op) {
               double a = numList.get(i), b = numList.get(i+1);
               switch (op) {
                  case '/': numList.set(i, a/b); numList.remove(i+1); break;
                  case '*': numList.set(i, a*b); numList.remove(i+1); break;
                  case '+': numList.set(i, a+b); numList.remove(i+1); break;
                  case '-': numList.set(i, a-b); numList.remove(i+1); break;
               }                                                                             
               opList.remove(i);
            } else {
               i++;
            }
         }
      }

      return numList.get(0) + trailingExpression;
   }
}
________________________________________________________________________
import java.util.regex.Pattern;
import java.util.Scanner;

public class MathEvaluator {
    public double calculate(String expression) {
        expression = expression.replaceAll(" ", "");
        while (expression.contains("(")) 
            expression = Pattern.compile("\\(([^()]*)\\)").matcher(expression)
                                .replaceAll(mr -> String.valueOf(simpleCalculate(mr.group(1))))
                                .replaceAll("(?<=[\\-\\+\\*/])--",""); //to simplify 1 + -(-1)
        return simpleCalculate(expression);
    }
    
    private double simpleCalculate(String expression) {
        Scanner sc = new Scanner(expression);
        Calculator calc = new Calculator(Double.valueOf(sc.findInLine("-?[0-9.]+"))); //set 1 number
        sc.findAll("([\\-\\+\\*/])?(-?[0-9.]+)").forEachOrdered(
                    mr -> calc.append(mr.group(1), Double.valueOf(mr.group(2))));
        return calc.calculate();
    }
}

class Calculator {
    private double result = 0, prev;
    private String prevOper = "+";
    Calculator (double firstOperator) {prev = firstOperator;}
    
    public double calculate() {
        return "+".equals(prevOper) ? result + prev : result - prev;
    }
    
    public void append (String operation, double operand) {
        switch (operation) {
            case "/": prev /= operand; break;
            case "*": prev *= operand; break;
            case "+": 
            case "-": result = calculate(); prevOper = operation; prev = operand;
        }
    }
}
