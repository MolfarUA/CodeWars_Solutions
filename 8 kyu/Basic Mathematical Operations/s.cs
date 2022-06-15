namespace Solution
{
  public static class Program
  {
    public static double basicOp(char op, double val1, double val2)
    {
      switch(op){
        case '+': return val1+val2;
        case '-': return val1-val2;
        case '*': return val1*val2;
        case '/': return val1/val2;
        default:
           throw new System.ArgumentException("Unknown operation!", op.ToString());
      }
    }
  }
}
________________________________
using System;
using System.Data;

public static class Program
{
  public static double basicOp(char op, double a, double b)
  {
    return Convert.ToDouble(new DataTable().Compute($"{a}{op}{b}", ""));
  }
}
________________________________
using System;

public static class Program
{
  public static double basicOp(char op, double a, double b)
  {
    return op switch
    {
        '+' => a + b,
        '-' => a - b,
        '*' => a * b,
        '/' => a / b,
        _ => throw new ArgumentException("Unknown operation", $"{op}")
    };
  }
}
________________________________
namespace Solution
{
  public static class Program
  {
    public static double basicOp(char op, double val1, double val2)
    {
      switch (op)
      {
        case '+': return val1+val2;
        case '-': return val1-val2;
        case '*': return val1*val2;
        case '/': return val1/val2;
      }
      return 0;
    }
  }
}
________________________________
namespace Solution
{
  public static class Program
  {
    public static double basicOp(char op, double val1, double val2)
    {
        double result;
        switch(op)
        {        
          case '+': 
            result = val1 + val2;
            break;
            
          case '-':
            result = val1-val2;
            break;
          
          case '*':
            result = val1*val2;
            break;
          
          case '/':
            result = val1/val2;
            break;
          
          default:
            result = 0;
            break;      
        }
        return result;   
      
    }
  }
}
