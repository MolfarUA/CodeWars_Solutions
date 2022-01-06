using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

public class TreeNode {
  public string val;
  public TreeNode left, right;
  public TreeNode(string val = "", TreeNode left = null, TreeNode right = null) {
    this.val = val; this.left = left; this.right = right;
  }
  public TreeNode(string val, string left, string right) {
    this.val = val; this.left = left != "" ? new TreeNode(left) : null; this.right = right != "" ? new TreeNode(right) : null;
  }
}

class PrefixDiff {
  public static List<string> Tokenize(string s) {
    var res = new List<string>();
    string ns = "", vs = "", t = s + " ";
    for (int i = 0; i < t.Length; i++) {
      var c = t[i];
      if (c == '.' || c >= '0' && c <= '9') {
        ns += c;
      } else if (c >= 'a' && c <= 'z') {
        vs += c;
      } else {
        if (ns != "") res.Add(ns);
        if (vs != "") res.Add(vs);
        ns = vs = "";
        if (c == '-') {
          if (i > 0 && t[i - 1] == ' ') ns = "-";
          else res.Add(c.ToString());
        } else if ("+*/^()".Contains(c)) {
          res.Add(c.ToString());
        }
      }
    }
    return res;
  }
  (TreeNode, int) BuildTree(List<string> tokens, int cur) {
    if (cur >= tokens.Count) return ((TreeNode) null, cur);
    if (tokens[cur] == "(") {
      var val = tokens[cur + 1];
      var node = new TreeNode(val);
      if (val == "cos" || val == "sin" || val == "tan" || val == "ln" || val == "exp") {
        var c1 = BuildTree(tokens, cur + 2);
        node.left = c1.Item1;
        return (node, c1.Item2 + 1);
      } else {
        var c1 = BuildTree(tokens, cur + 2);
        var c2 = BuildTree(tokens, c1.Item2);
        node.left = c1.Item1;
        node.right = c2.Item1;
        return (node, c2.Item2 + 1);
      }
    } else {
      return (new TreeNode(tokens[cur]), cur + 1);
    }
  }
  string ToString(TreeNode node) {
    if (node == null) return "";
    if (node.left == null) return node.val;
    string c1 = ToString(node.left), c2 = ToString(node.right);
    return $"({node.val} " + c1 + (node.right == null ? "" : " " + c2) + ")";
  }
  double ToNumber(string s) { return double.Parse(s); }
  double ToNumber(TreeNode node) { return double.Parse(node.val); }
  bool IsNumber(string s) { return (s[0] >= '0' && s[0] <= '9') || (s.Length >= 2 && s[0] == '-' && s[1] >= '0' && s[1] <= '9'); }
  bool IsNumber(TreeNode node) { return node != null && IsNumber(node.val); }
  TreeNode Simplify(TreeNode node) {
    if (node == null || node.left == null) return node;
    node.left = Simplify(node.left);
    node.right = Simplify(node.right);
    if (node.val == "*" && (IsNumber(node.left) || IsNumber(node.right))) {
      if (node.left.val == "*" && IsNumber(node.left.left)) {
        node.left.left.val = (ToNumber(node.left.left) * ToNumber(node.right)).ToString();
        return node.left;
      } else if (node.left.val == "*" && IsNumber(node.left.right)) {
        node.left.right.val = (ToNumber(node.left.right) * ToNumber(node.right)).ToString();
        return node.left;
      } else if (node.right.val == "*" && IsNumber(node.right.left)) {
        node.right.left.val = (ToNumber(node.right.left) * ToNumber(node.left)).ToString();
        return node.right;
      } else if (node.right.val == "*" && IsNumber(node.right.left)) {
        node.right.right.val = (ToNumber(node.right.right) * ToNumber(node.left)).ToString();
        return node.right;
      }
    }
    if ((node.val == "*" && node.right.val == "1") ||
        ((node.val == "+" || node.val == "-") && node.right.val == "0")) {
      var tmp = node.left;
      node.val = tmp.val;
      node.left = tmp.left;
      node.right = tmp.right;
    } else if (IsNumber(node.left.val)) {
      if (node.left.val == "0") {
        if (node.val == "+")  {
          node.val = node.right.val;
          node.left = node.right.left;
          node.right = node.right.right;
        } else if (node.val == "-")  {
          node.val = (ToNumber(node.right) * -1).ToString();
          node.left = node.right.left;
          node.right = node.right.right;
        } else if (node.val == "*" || node.val == "/" || node.val == "^") {
          node.val = "0";
          node.left = node.right = null;
        }
      } else if (node.left.val == "1" && "*^".Contains(node.val)) {
        if (node.val == "*")  {
          node.val = node.right.val;
          node.left = node.right.left;
          node.right = node.right.right;
        } else if (node.val == "^") {
          node.val = "1";
          node.left = node.right = null;
        }
      } else if (IsNumber(node.right)) {
        if (node.val == "+") {
          node.val = (ToNumber(node.left) + ToNumber(node.right)).ToString();
          node.left = node.right = null;
        } else if (node.val == "-") {
          node.val = (ToNumber(node.left) - ToNumber(node.right)).ToString();
          node.left = node.right = null;
        } else if (node.val == "*") {
          node.val = (ToNumber(node.left) * ToNumber(node.right)).ToString();
          node.left = node.right = null;
        } else if (node.val == "/") {
          node.val = (ToNumber(node.left) / ToNumber(node.right)).ToString();
          node.left = node.right = null;
        } else if (node.val == "^") {
          double x = ToNumber(node.left), y = ToNumber(node.right);
          node.val = Math.Pow(x, y).ToString();
          node.left = node.right = null;
        }
      } else if (node.right != null && node.right.val == "x") {
      } else if (node.right != null && node.right.val == "*") {
        if (IsNumber(node.right.left.val)) {
          node.left.val = (ToNumber(node.left.val) * ToNumber(node.right.left.val)).ToString();
          node.right = node.right.right;
        } else if (IsNumber(node.right.right.val)) {
          node.left.val = (ToNumber(node.left.val) * ToNumber(node.right.right.val)).ToString();
          node.right = node.right.left;
        }
      }
    } else if (node.left.val == "x") {
      if (node.right != null && IsNumber(node.right.val)) {
        if (node.val == "^" && node.right.val == "0") {
          node.val = "1";
          node.left = node.right = null;
        } else if (node.val == "^" && node.right.val == "1") {
          node.val = "x";
          node.left = node.right = null;
        }
      } else if (node.right != null && node.right.val == "x") {
        if (node.val == "+") {
          node.val = "*";
          node.left.val = "2";
        } else if (node.val == "-") {
          node.val = "0";
          node.left = node.right = null;
        } else if (node.val == "*") {
          node.val = "^";
          node.right.val = "2";
        } else if (node.val == "/") {
          node.val = "1";
          node.left = node.right = null;
        }
      }
    }
    return node;
  }
  TreeNode Copy(TreeNode node) {
    if (node == null) return null;
    return new TreeNode(node.val, Copy(node.left), Copy(node.right));
  }
  TreeNode Diff(TreeNode node) {
    if (node == null) return node;
    if (node.left == null) {
      if (node.val == "x") node.val = "1";
      else node.val = "0";
    } else if (node.val == "+" || node.val == "-") {
      Diff(node.left);
      Diff(node.right);
    } else if (node.val == "*") {
      if (!IsNumber(node.left.val)) Diff(node.left);
      if (!IsNumber(node.right.val)) Diff(node.right);
    } else if (node.val == "^") {
      if (node.left.val == "x" && IsNumber(node.right.val)) {
        double a = ToNumber(node.right.val);
        node.val = "*";
        node.left.val = a.ToString();
        node.right.val = "^";
        node.right.left = new TreeNode("x");
        node.right.right = new TreeNode((a - 1).ToString());
      } else if (IsNumber(node.left.val) && node.right.val == "x") {
        double a = ToNumber(node.left.val);
        node.val = "*";
        node.left.val = "^";
        node.left.left = new TreeNode(a.ToString());
        node.left.right = new TreeNode("x");
        node.right = new TreeNode("ln", new TreeNode("x"));
      }
    } else if (node.val == "/") {
      if (IsNumber(node.left.val) && IsNumber(node.right.val)) {
        node.val = "0";
        node.left = node.right = null;
      } else if (IsNumber(node.left.val) && node.right.val == "x") {
        node.left.val = (ToNumber(node.left.val) * -1).ToString();
        node.right = new TreeNode("^", new TreeNode("x"), new TreeNode("2"));
      } else if (node.left.val == "x" && IsNumber(node.right.val)) {
        node.left.val = "1";
      } else {
        TreeNode f = Copy(node.left), ff = Diff(Copy(node.left));
        TreeNode g = Copy(node.right), gg = Diff(Copy(node.right));
        node.left = new TreeNode("-", new TreeNode("*", ff, g), new TreeNode("*", f, gg));
        node.right = new TreeNode("^", Copy(node.right), new TreeNode("2"));
      }
    } else if (node.val == "sin") {
      if (node.left.val == "x") {
        node.val = "cos";
      } else if (!IsNumber(node.left.val)) {
        var tmp = Copy(node.left);
        node.val = "*";
        node.right = new TreeNode("cos", node.left);
        node.left = tmp;
        Diff(node.left);
      }
    } else if (node.val == "cos") {
      if (node.left.val == "x") {
        node.val = "*";
        node.left.val = "-1";
        node.right = new TreeNode("sin", new TreeNode("x"));
      } else if (!IsNumber(node.left.val)) {
        var tmp = Copy(node.left);
        node.val = "*";
        node.left = new TreeNode("*", new TreeNode("-1"), new TreeNode("sin", node.left));
        node.right = tmp;
        Diff(node.right);
      }
    } else if (node.val == "tan") {
      if (node.left.val == "x") {
        node.val = "^";
        node.left = new TreeNode("cos", new TreeNode("x"));
        node.right = new TreeNode("-2");
      } else if (!IsNumber(node.left)) {
        TreeNode f = Diff(Copy(node.left)), g = Copy(node);
        node.val = "/";
        node.left = f;
        g.val = "cos";
        node.right = new TreeNode("^", g, new TreeNode("2"));
      }
    } else if (node.val == "ln") {
      if (node.left.val == "x") {
        node.val = "/";
        node.left = new TreeNode("1");
        node.right = new TreeNode("x");
      }
    } else if (node.val == "exp") {
      TreeNode f = Diff(Copy(node.left)), g = Copy(node);
      node.val = "*";
      node.left = f;
      node.right = g;
    }
    return node;
  }
  public string Diff(string expr) {
    var tokens = Tokenize(expr);
    var ret = BuildTree(tokens, 0);
    return ToString(Simplify(Diff(Simplify(ret.Item1))));
  }
}
______________________________________________
using System;
using System.Linq;
using System.Text.RegularExpressions;
class PrefixDiff // Class name required
{
    public string Diff(string expr)
    {
      if (Regex.IsMatch(expr, @"^-?[0-9.x]+$"))
          return (expr == "x") ? "1" : "0";
      string[] com = Regex.Matches(expr.Substring(1, expr.Length - 2), @"\((?>\((?<DEPTH>)|\)(?<-DEPTH>)|[^()]+)*\)|[^() ]+").Cast<Match>().Select(w => w.Groups[0].Value).ToArray();
      string a = Diff(com[1]);
      string b = "";
      if (com.Length == 3)
          b = Diff(com[2]);
      switch (com[0])
      {
          case "-":
          case "+": return clean(com[0], a, b);
          case "*": return clean("+", clean("*", a, com[2]), clean("*", com[1], b));
          case "/": return clean("+", clean("/", a, com[2]), clean("/", clean("*", clean("*", "-1", com[1]), b), $"(^ {com[2]} 2)"));
          case "^": return clean("*", com[2], clean("*", a, clean("^", com[1], (int.Parse(com[2]) - 1).ToString())));
          case "sin": return clean("*", a, $"(cos {com[1]})");
          case "cos": return clean("*", a, $"(* -1 (sin {com[1]}))");
          case "tan": return $"(/ {a} (^ (cos {com[1]}) 2))";
          case "ln": return $"(/ {a} {com[1]})";
          case "exp": return clean("*", a, $"(exp {com[1]})");
      }
      return "";
    }
  
    public string clean(string op, string p1, string p2)
    {
      switch (op)
      {
          case "-":
          case "+": if (p1 == "0")
                  return (op == "+") ? p2 : clean("*", "-1", p2);
              if (p2 == "0")
                  return p1;
              if (Regex.IsMatch(p1, "^-?[0-9.]+$") && Regex.IsMatch(p2, "^-?[0-9.]+$"))
                  return (float.Parse(p1) + (op == "+" ? float.Parse(p2) : -float.Parse(p2))).ToString();
              break;
          case "*": if (p1 == "1")
                  return p2;
              if (p2 == "1")
                  return p1;
              if (p1 == "0" || p2 == "0")
                  return "0";
              if (Regex.IsMatch(p1, "^-?[0-9.]+$") && Regex.IsMatch(p2, "^-?[0-9.]+$"))
                  return (float.Parse(p1) * float.Parse(p2)).ToString();
              break;
          case "/": if (p2 == "1")
                  return p1;
              if (p1 == "0")
                  return "0";
              if (Regex.IsMatch(p1, "^-?[0-9.]+$") && Regex.IsMatch(p2, "^-?[0-9.]+$"))
                  return (float.Parse(p1) / float.Parse(p2)).ToString();
              break;
          case "^": if (p2 == "1")
                  return p1;
              if (p2 == "0")
                  return "1";
              if (Regex.IsMatch(p1, "^-?[0-9.]+$") && Regex.IsMatch(p2, "^-?[0-9.]+$"))
                  return (Math.Pow(float.Parse(p1), float.Parse(p2))).ToString();
              break;
      }
      return $"({op} {p1} {p2})";
    }
}
______________________________________________
using System;
using System.Linq;

public class PrefixDiff
{
    public string Diff(string expr)
    {
        Console.WriteLine(expr);

        var parseTree = TreeBuilder.Build(expr);
        var processedTree = TreeProcessing.Process(parseTree);
        var optimizedTree = TreeOptimization.Optimize(processedTree);

        return optimizedTree.BuildString();
    }
}

public static class TreeBuilder
{
    public static TreeNode Build(string expr)
    {
        var parts = expr.Split(new[] { ' ', '(', ')' }, StringSplitOptions.RemoveEmptyEntries);

        var root = new TreeNode();
        var currentNode = root;

        foreach (var part in parts)
        {
            var id = Array.IndexOf(new[] { '+', '-', '*', '/', '^' }, part[0]);
            if (id >= 0)
            {
                currentNode.Type = id switch
                {
                    0 => TreeNode.NodeType.Plus,
                    1 => TreeNode.NodeType.Minus,
                    2 => TreeNode.NodeType.Multiplication,
                    3 => TreeNode.NodeType.Division,
                    4 => TreeNode.NodeType.Power,
                    _ => throw null
                };

                currentNode.Left = new TreeNode();
                currentNode = currentNode.Left;
                continue;
            }

            id = Array.IndexOf(new[] { "exp", "cos", "sin", "tan", "log", "ln" }, part);
            if (id >= 0)
            {
                currentNode.Type = id switch
                {
                    0 => TreeNode.NodeType.Exp,
                    1 => TreeNode.NodeType.Cos,
                    2 => TreeNode.NodeType.Sin,
                    3 => TreeNode.NodeType.Tan,
                    4 => TreeNode.NodeType.Log,
                    5 => TreeNode.NodeType.Ln,
                    _ => throw null
                };

                currentNode.Left = new TreeNode();
                currentNode = currentNode.Left;
                continue;
            }

            if (int.TryParse(part, out int value))
            {
                currentNode.Type = TreeNode.NodeType.Value;
                currentNode.Value = value;

                currentNode = FromLeaf(currentNode);
            }
            else if (char.IsLetter(part[0]))
            {
                currentNode.Type = TreeNode.NodeType.Variable;

                currentNode = FromLeaf(currentNode);
            }
        }
        return root;
    }

    private static TreeNode FromLeaf(TreeNode node)
    {
        if (node?.Parent is null)
            return node;

        if (new[] { TreeNode.NodeType.Plus, TreeNode.NodeType.Minus, TreeNode.NodeType.Multiplication, TreeNode.NodeType.Division, TreeNode.NodeType.Power }
            .Contains(node.Parent.Type))
        {
            if (node.Parent.Left is null)
            {
                node.Parent.Left = new TreeNode();
                return node.Parent.Left;
            }

            if (node.Parent.Right is null)
            {
                node.Parent.Right = new TreeNode();
                return node.Parent.Right;
            }
        }

        return FromLeaf(node.Parent);
    }
}

public static class TreeProcessing
{
    public static TreeNode Process(TreeNode parseTree)
    {
        return parseTree.Type switch
        {
            TreeNode.NodeType.Cos => DiffCos(parseTree),
            TreeNode.NodeType.Sin => DiffSin(parseTree),
            TreeNode.NodeType.Plus => DiffPlus(parseTree),
            TreeNode.NodeType.Minus => DiffMinus(parseTree),
            TreeNode.NodeType.Exp => DiffExp(parseTree),
            TreeNode.NodeType.Tan => DiffTan(parseTree),
            TreeNode.NodeType.Ln => DiffLn(parseTree),
            TreeNode.NodeType.Multiplication => DiffMultiplication(parseTree),
            TreeNode.NodeType.Division => DiffDivision(parseTree),
            TreeNode.NodeType.Power => DiffPower(parseTree),
            TreeNode.NodeType.Value => DiffValue(parseTree),
            TreeNode.NodeType.Variable => DiffVariable(parseTree),
            _ => throw new NotImplementedException()
        };
    }

    private static TreeNode DiffCos(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Multiplication,
            Left = new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = -1
            },
            Right = new TreeNode
            {
                Type = TreeNode.NodeType.Multiplication,
                Left = new TreeNode
                {
                    Type = TreeNode.NodeType.Sin,
                    Left = node.Left
                },
                Right = Process(node.Left)
            }
        };
    }
    private static TreeNode DiffSin(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Multiplication,
            Left = Process(node.Left),
            Right = new TreeNode
            {
                Type = TreeNode.NodeType.Cos,
                Left = node.Left
            }
        };
    }
    private static TreeNode DiffMinus(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Minus,
            Left = Process(node.Left),
            Right = Process(node.Right)
        };
    }
    private static TreeNode DiffPlus(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Plus,
            Left = Process(node.Left),
            Right = Process(node.Right)
        };
    }
    private static TreeNode DiffValue(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Value,
            Value = 0
        };
    }
    private static TreeNode DiffVariable(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Value,
            Value = 1
        };
    }
    private static TreeNode DiffTan(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Multiplication,
            Left = Process(node.Left),
            Right = new TreeNode
            {
                Type = TreeNode.NodeType.Power,
                Left = new TreeNode
                {
                    Type = TreeNode.NodeType.Cos,
                    Left = node.Left
                },
                Right = new TreeNode
                {
                    Type = TreeNode.NodeType.Value,
                    Value = -2
                }
            }
        };
    }
    private static TreeNode DiffLn(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Multiplication,
            Left = new TreeNode
            {
                Type = TreeNode.NodeType.Division,
                Left = new TreeNode
                {
                    Type = TreeNode.NodeType.Value,
                    Value = 1
                },
                Right = node.Left
            },
            Right = Process(node.Left)
        };
    }
    private static TreeNode DiffExp(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Multiplication,
            Left = Process(node.Left),
            Right = node,
        };
    }
    private static TreeNode DiffDivision(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Division,
            Left = new TreeNode
            {
                Type = TreeNode.NodeType.Minus,
                Left = new TreeNode
                {
                    Type = TreeNode.NodeType.Multiplication,
                    Left = Process(node.Left),
                    Right = node.Right
                },
                Right = new TreeNode
                {
                    Type = TreeNode.NodeType.Multiplication,
                    Left = node.Left,
                    Right = Process(node.Right)
                }
            },
            Right = new TreeNode
            {
                Type = TreeNode.NodeType.Power,
                Left = node.Right,
                Right = new TreeNode
                {
                    Type = TreeNode.NodeType.Value,
                    Value = 2
                }
            }
        };
    }
    private static TreeNode DiffMultiplication(TreeNode node)
    {
        return new TreeNode
        {
            Type = TreeNode.NodeType.Plus,
            Left = new TreeNode
            {
                Type = TreeNode.NodeType.Multiplication,
                Left = Process(node.Left),
                Right = node.Right
            },
            Right = new TreeNode
            {
                Type = TreeNode.NodeType.Multiplication,
                Left = node.Left,
                Right = Process(node.Right)
            }
        };
    }
    private static TreeNode DiffPower(TreeNode node)
    {
        if (node.Left.Type == TreeNode.NodeType.Variable && node.Right.Type == TreeNode.NodeType.Value)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Multiplication,
                Left = new TreeNode
                {
                    Type = TreeNode.NodeType.Value,
                    Value = node.Right.Value
                },
                Right = new TreeNode
                {
                    Type = TreeNode.NodeType.Power,
                    Left = node.Left,
                    Right = new TreeNode
                    {
                        Type = TreeNode.NodeType.Value,
                        Value = node.Right.Value - 1
                    }
                }
            };
        }

        if (node.Left.Type == TreeNode.NodeType.Value && node.Right.Type == TreeNode.NodeType.Variable)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Multiplication,
                Left = node,
                Right = new TreeNode
                {
                    Type = TreeNode.NodeType.Ln,
                    Left = new TreeNode
                    {
                        Type = TreeNode.NodeType.Value,
                        Value = node.Left.Value
                    }
                }
            };
        }

        if (node.Left.Type == TreeNode.NodeType.Value && node.Right.Type == TreeNode.NodeType.Value)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = 0
            };
        }

        throw new NotImplementedException("you have no power here!");
    }
}

public class TreeNode
{
    public enum NodeType { Value, Variable, Exp, Cos, Sin, Tan, Ln, Log, Plus, Minus, Multiplication, Division, Power }

    private TreeNode _left;
    private TreeNode _right;

    public TreeNode Left
    {
        get => _left;
        set
        {
            _left = value;
            _left.Parent = this;
        }
    }

    public TreeNode Right
    {
        get => _right;
        set
        {
            _right = value;
            _right.Parent = this;
        }
    }

    public TreeNode Parent { get; private set; }

    public double Value { get; set; }
    public NodeType Type { get; set; }
}
public static class TreeOptimization
{
    public static TreeNode Optimize(TreeNode diffTree)
    {
        return OptimizeBinary(diffTree);
    }

    private static TreeNode OptimizeBinary(TreeNode node)
    {
        if (!(node.Left is null) && node.Left.Type != TreeNode.NodeType.Value
                                 && node.Left.Type != TreeNode.NodeType.Variable)
        {
            node.Left = Optimize(node.Left);
        }
        if (!(node.Right is null) && node.Right?.Type != TreeNode.NodeType.Value
                                  && node.Right?.Type != TreeNode.NodeType.Variable)
        {
            node.Right = Optimize(node.Right);
        }

        return node.Type switch
        {
            TreeNode.NodeType.Plus => OptimizePlus(node),
            TreeNode.NodeType.Minus => OptimizeMinus(node),
            TreeNode.NodeType.Multiplication => OptimizeMultiplication(node),
            TreeNode.NodeType.Division => OptimizeDivision(node),
            TreeNode.NodeType.Power => OptimizePower(node),
            _ => node
        };
    }

    private static TreeNode OptimizePlus(TreeNode node)
    {
        if (node.Right.Type == TreeNode.NodeType.Value
            && node.Right.Type == node.Left.Type)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = node.Left.Value + node.Right.Value
            };
        }
        if (node.Left.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Left.Value) < 0.01)
        {
            return node.Right;
        }
        if (node.Right.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Right.Value) < 0.01)
        {
            return node.Left;
        }

        return node;
    }
    private static TreeNode OptimizeMinus(TreeNode node)
    {
        if (node.Right.Type == TreeNode.NodeType.Value
            && node.Right.Type == node.Left.Type)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = node.Left.Value - node.Right.Value
            };
        }

        if (node.Left.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Left.Value) < 0.01)
        {
            return node.Right;
        }
        if (node.Right.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Right.Value) < 0.01)
        {
            return node.Left;
        }

        return node;
    }
    private static TreeNode OptimizeMultiplication(TreeNode node)
    {
        if (node.Right.Type == TreeNode.NodeType.Value
            && node.Right.Type == node.Left.Type)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = node.Left.Value * node.Right.Value
            };
        }

        if (node.Left.Type == TreeNode.NodeType.Value)
        {
            if (Math.Abs(node.Left.Value - 1) < 0.01)
            {
                return node.Right;
            }
            if (Math.Abs(node.Left.Value) < 0.01)
            {
                return node.Left;
            }
        }
        if (node.Right.Type == TreeNode.NodeType.Value)
        {
            if (Math.Abs(node.Right.Value - 1) < 0.01)
            {
                return node.Left;
            }
            if (Math.Abs(node.Right.Value) < 0.01)
            {
                return node.Right;
            }
        }

        if (node.Type == node.Right.Type)
        {
            if (node.Left.Type == TreeNode.NodeType.Value)
            {
                if (node.Right.Left.Type == TreeNode.NodeType.Value)
                {
                    node.Left.Value *= node.Right.Left.Value;
                    node.Right = node.Right.Right;
                }
                else if (node.Right.Right.Type == TreeNode.NodeType.Value)
                {
                    node.Left.Value *= node.Right.Right.Value;
                    node.Right = node.Right.Left;
                }
            }
            else if (node.Right.Type == TreeNode.NodeType.Value)
            {
                if (node.Left.Left.Type == TreeNode.NodeType.Value)
                {
                    node.Right.Value *= node.Left.Left.Value;
                    node.Left = node.Left.Right;
                }
                else if (node.Left.Right.Type == TreeNode.NodeType.Value)
                {
                    node.Right.Value *= node.Left.Right.Value;
                    node.Left = node.Left.Left;
                }
            }
        }

        return node;
    }

    private static TreeNode OptimizeDivision(TreeNode node)
    {
        if (node.Right.Type == TreeNode.NodeType.Value
            && node.Right.Type == node.Left.Type)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = node.Left.Value / node.Right.Value
            };
        }

        if (node.Left.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Left.Value) < 0.01)
        {
            return node.Left;
        }
        if (node.Right.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Right.Value - 1) < 0.01)
        {
            return node.Left;
        }

        return node;
    }

    private static TreeNode OptimizePower(TreeNode node)
    {
        if (node.Right.Type == TreeNode.NodeType.Value
            && node.Right.Type == node.Left.Type)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = Math.Pow(node.Left.Value, node.Right.Value)
            };
        }
        if (node.Left.Type == TreeNode.NodeType.Value
            && Math.Abs(node.Left.Value - 1) < 0.01)
        {
            return new TreeNode
            {
                Type = TreeNode.NodeType.Value,
                Value = 1
            };
        }
        if (node.Right.Type == TreeNode.NodeType.Value)
        {
            if (Math.Abs(node.Right.Value) < 0.01)
            {
                return new TreeNode
                {
                    Type = TreeNode.NodeType.Value,
                    Value = 1
                };
            }
            if (Math.Abs(node.Right.Value - 1) < 0.01)
            {
                return node.Left;
            }
        }

        return node;
    }
}

public static class TreeNodeUtils
{
    public static void PrintTree(this TreeNode node, int level = 0)
    {
        if (node is null) return;

        Console.Write(new string('-', level));
        Console.Write(node.Type);

        if (node.Type == TreeNode.NodeType.Value)
            Console.Write($": {node.Value}");
        Console.WriteLine();

        if (!(node.Left is null))
        {
            Console.Write(new string('-', level));
            Console.WriteLine("Left:");
            PrintTree(node.Left, level + 1);
        }
        if (!(node.Right is null))
        {
            Console.Write(new string('-', level));
            Console.WriteLine("Right:");
            PrintTree(node.Right, level + 1);
        }
    }

    public static string BuildString(this TreeNode node)
    {
        if (node is null) throw new NullReferenceException();

        string value = null;
        switch (node.Type)
        {
            case TreeNode.NodeType.Value:
                value = $"{node.Value:0.##}";
                break;
            case TreeNode.NodeType.Variable:
                value = "x";
                break;
            case TreeNode.NodeType.Exp:
                value = $"(exp {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Tan:
                value = $"(tan {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Ln:
                value = $"(ln {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Log:
                value = $"(log {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Cos:
                value = $"(cos {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Sin:
                value = $"(sin {BuildString(node.Left)})";
                break;
            case TreeNode.NodeType.Plus:
                value = $"(+ {BuildString(node.Left)} {BuildString(node.Right)})";
                break;
            case TreeNode.NodeType.Minus:
                value = $"(- {BuildString(node.Left)} {BuildString(node.Right)})";
                break;
            case TreeNode.NodeType.Multiplication:
                value = $"(* {BuildString(node.Left)} {BuildString(node.Right)})";
                break;
            case TreeNode.NodeType.Division:
                value = $"(/ {BuildString(node.Left)} {BuildString(node.Right)})";
                break;
            case TreeNode.NodeType.Power:
                value = $"(^ {BuildString(node.Left)} {BuildString(node.Right)})";
                break;
        }

        return value;
    }
}
