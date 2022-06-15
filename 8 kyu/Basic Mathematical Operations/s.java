public class BasicOperations
{
  public static Integer basicMath(String op, int v1, int v2)
  {
  switch (op) {
    case "-":
      return v1 - v2;
    case "+":
      return v1 + v2;
    case "*":
      return v1 * v2;
    case "/": {
      if (v2 == 0)
        throw new IllegalArgumentException("Division by zero");
      return v1 / v2;
    }
    default:
      throw new IllegalArgumentException("Unknown operation: " + op);
    }
  }
}
________________________________
public class BasicOperations {
    public static Integer basicMath(String op, int v1, int v2) {
      int num = 0;
        if(op == "+") {
          num = v1 + v2;
        };
        if(op == "-") {
          num = v1 - v2;
        };
        if(op == "*") {
          num = v1 * v2;
        };
        if(op == "/") {
          num = v1 / v2;
        };
      return num;
    }
}
________________________________
public class BasicOperations
{
  public static Integer basicMath(String op, int v1, int v2)
  {
    switch(op) {
      case "-":
        return v1 - v2;
      case "+":
        return v1 + v2;
      case "/":
        return v1 / v2;
      default:
        return v1 * v2;
    }
  }
}
________________________________
public class BasicOperations
{
  public static Integer basicMath(String op, int v1, int v2)
  {
    if (op.equals("*") == true) {
      return v1 * v2;
    }
    if (op.equals("+") == true) {
      return v1 + v2;
    }
    if (op.equals("/") == true) {
      return v1 / v2;
    }
    else {
      return v1 - v2;
    }
  }
}
________________________________
public class BasicOperations
{
  public static Integer basicMath(String op, int v1, int v2)
  {
    int result = 0;
    char x = op.charAt(0);
    if (x == '+')
      result = v1 + v2;
    else if (x == '-')
      result = v1 - v2;
    else if (x == '*')
      result = v1 * v2;
    else
      result = v1 / v2;
    return result;
  }
}
