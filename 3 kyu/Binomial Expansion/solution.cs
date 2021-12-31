using System;
using System.Collections.Generic;

public class KataSolution
{
  

  public static string Expand(string expr)
            {
                clsExponCalc2 oEC = new clsExponCalc2();
                int aNumber, bNumber, n;
                string aLettter, aNumberTemp = "", bNumberTemp = "", nTemp = "";

                int i = 1;
                if (!Char.IsLetter(expr[i]))
                    while (i < expr.Length && !Char.IsLetter(expr[i]))
                    {
                        aNumberTemp = aNumberTemp + expr[i];
                        i++;
                    }
                else
                    aNumberTemp = "1";
                aLettter = expr[i].ToString();
                i++;
                if (aNumberTemp == "-")
                    aNumber = -1;
                else
                    aNumber = Int32.Parse(aNumberTemp);

                while (i < expr.Length && i != expr.IndexOf(')'))
                {
                    bNumberTemp = bNumberTemp + expr[i];
                    i++;
                }
                bNumber = Int32.Parse(bNumberTemp);
                i += 2;

                while (i < expr.Length)
                {
                    nTemp += expr[i];
                    i++;
                }
                n = Int32.Parse(nTemp);

                return oEC.MainCalc(n, aLettter, bNumber, aNumber);


            }
}


class clsExponCalc2
    {
        public string MainCalc(int n, string a, int b, int an)
        {
            if (n == 0)
            {
                return "1";
            }
            else if (n < 0)
            {
                return "1/(" + calculation(n * (-1), a, b, an) + ")";
            }
            else
            {
                return calculation(n, a, b, an);
            }
        }

        public string calculation(int n, string a, int b, int an)
        {
            if (b == 0)
            {
                if (an != 1 && an != 0 && an != -1)
                {
                    return (Math.Pow(an,n) + a + "^" + n);
                }
                else if(an == 1)
                {
                    return (a + "^" + n);
                }
                else if (an == 0)
                {
                    return ("0");
                }
                else if (an == -1)
                {
                    return ("-" + a + "^" + n);
                }
            }

            List<string> Evaluation = new List<string>();
            List<int> lstRes = new List<int>();
            lstRes.Add(1);
            lstRes.Add(1);

            ListFill(lstRes, n);
            Evaluation = VarSet(lstRes, b, a, an);

            return ToString(Evaluation);
        }



        public List<int> ListFill (List<int> lst, int n)
        {
            int iTmp1 = 0, iTmp2 = 0;

            for (int i = 1; i < n; i++)
            {
                for (int j = 0; j < lst.Count; j++)
                {
                    if (j != 0)
                    {
                        iTmp1 = lst[j];
                        lst[j] = lst[j] + iTmp2;
                        iTmp2 = iTmp1;
                    }
                    else
                    {
                        iTmp2 = lst[j];
                    }
                }
                lst.Add(1);
            }

            return lst;
        }

        public List<string> VarSet(List<int> lst, int b, string a, int an)
        {
            List<string> lEval = new List<string>();
            for (int i = 0; i < lst.Count; i++)
            {
                if (lst.Count != 2)
                {
                    if (lst[i] != 1)
                    {
                        if (i != lst.Count - 1 && i != lst.Count - 2)
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i) * Math.Pow(an, lst.Count - i - 1)).ToString() + a + "^" + (lst.Count - i - 1));
                        }
                        else if (i == lst.Count - 2)
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i) * an).ToString() + a);
                        }
                    }
                    else if (lst[i] == 1)
                    {
                        if (i == 0)
                        {
                            if (Math.Pow(an, lst.Count - i - 1) != 1 && Math.Pow(an, lst.Count - i - 1) != (-1))
                            {
                                lEval.Add(Math.Pow(an, lst.Count - i - 1) + a + "^" + (lst.Count - 1));
                            }
                            else if (Math.Pow(an, lst.Count - i - 1) == 1)
                            {
                                lEval.Add(a + "^" + (lst.Count - 1));
                            }
                            else
                            {
                                lEval.Add("-" + a + "^" + (lst.Count - 1));
                            }
                        }
                        else
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i)).ToString());
                        }
                    }
                }
                else
                {
                    if (lst[i] != 1)
                    {
                        if (i != lst.Count - 1 && i != lst.Count - 2)
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i) * Math.Pow(an, lst.Count - i - 1)).ToString() + a);
                        }
                        else if (i == lst.Count - 2)
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i) * an).ToString() + a);
                        }
                    }
                    else if (lst[i] == 1)
                    {
                        if (i == 0)
                        {
                            if (Math.Pow(an, lst.Count - i - 1) != 1)
                            {
                                lEval.Add(Math.Pow(an, lst.Count - i - 1) + a);
                            }
                            else
                            {
                                lEval.Add(a);
                            }
                        }
                        else
                        {
                            lEval.Add((lst[i] * Math.Pow(b, i)).ToString());
                        }
                    }
                }              
            }

            return lEval;
        }


        public string ToString(List<string> lst)
        {
            string temp = "";

            for (int i = 0; i < lst.Count; i++)
            {
                if (i != 0)
                {
                    temp = temp + "+" + lst[i].ToString();
                }
                else
                {
                    temp = lst[i].ToString();
                }
            }
            temp = temp.Replace("+-", "-");
            return temp;
        }

    }
    
___________________________________________________
using System;
using System.Collections.Generic;

    public class KataSolution
    {
        public class itemT
        {
            public string variable { get; set; }
            public int order { get; set; }
            public long coeff { get; set; }
        }

        static List<itemT> calc(List<itemT> lhs, List<itemT> rhs)
        {
            Dictionary<int, List<itemT>> dic = new Dictionary<int, List<itemT>>();

            for (int i = 0; i < lhs.Count; ++i)
            {
                for (int j = 0; j < rhs.Count; ++j)
                {
                    itemT i0 = lhs[i];
                    itemT i1 = rhs[j];

                    itemT newItem = new itemT { coeff = i0.coeff * i1.coeff, order = i0.order + i1.order };
                    if (i0.variable != null)
                        newItem.variable = i0.variable;
                    else if (i1.variable != null)
                        newItem.variable = i1.variable;

                    if (dic.ContainsKey(newItem.order) == false)
                        dic.Add(newItem.order, new List<itemT>());

                    dic[newItem.order].Add(newItem);
                }
            }

            List<itemT> ret = new List<itemT>();

            foreach (var item in dic)
            {
                if (item.Value.Count == 0)
                    continue;

                if (item.Value.Count > 1)
                {
                    for (int i = 1; i < item.Value.Count; ++i)
                    {
                        item.Value[0].coeff += item.Value[i].coeff;
                    }
                }

                ret.Add(item.Value[0]);
            }

            return ret;
        }

        private static List<itemT> convert(string str)
        {
            List<itemT> ret = new List<itemT>();

            str = str.Substring(1, str.Length - 2);

            string sub = null;
            for (int i = 0; i < str.Length; ++i)
            {
                if (str[i] == '+' || str[i] == '-')
                    sub += str[i];
                else
                {
                    int n = 0;
                    if (int.TryParse(str[i].ToString(), out n))
                        sub += str[i];
                    else
                    {
                        itemT it = new itemT { variable = str[i].ToString(), order = 1 };

                        if (sub == null)
                            it.coeff = 1;
                        else if (sub == "-")
                            it.coeff = -1;
                        else
                            it.coeff = int.Parse(sub);

                        if (it.coeff != 0)
                            ret.Add(it);

                        sub = null;
                    }
                }
            }

            if (sub != null)
            {
                itemT it = new itemT { coeff = int.Parse(sub), variable = null, order = 0 };
                if (it.coeff != 0)
                    ret.Add(it);
            }

            return ret;
        }

        public static string Expand(string expr)
        {
            Console.WriteLine(expr);

            string[] fields = expr.Split('^');
            string itemStr = fields[0];
            int p = int.Parse(fields[1]);

            if (p == 0)
                return "1";

            var aas = convert(itemStr);

            List<itemT> start = aas;
            for (int i = 1; i < p; ++i)
            {
                start = calc(start, aas);
            }

            string ret = null;
            foreach (var item in start)
            {
                if (item.variable != null)
                {
                    if (item.order == 1)
                        ret += string.Format("{0}{1}{2}", item.coeff > 0 ? "+" : "", item.coeff == 1 ? "" : item.coeff == -1 ? "-" : item.coeff.ToString(), item.variable);
                    else
                        ret += string.Format("{0}{1}{2}^{3}", item.coeff > 0 ? "+" : "", item.coeff == 1 ? "" : item.coeff == -1 ? "-" : item.coeff.ToString(), item.variable, item.order);
                }
                else
                    ret += string.Format("{0}{1}", item.coeff > 0 ? "+" : "", item.coeff);
            }

            if (ret[0] == '+')
                ret = ret.Substring(1, ret.Length - 1);

            return ret;
        }
    }
    
___________________________________________________
using System.Text.RegularExpressions;
using System;

public class KataSolution
{
    public static string Expand(string expr)
    {
        Console.WriteLine(expr);
        var match = Regex.Match(expr, "^\\((-?[0-9]*)([a-z])([+-])([0-9]*)\\)\\^([0-9]*)$");
        string pre = match.Groups[1].Value == "" ? "1" : match.Groups[1].Value == "-" ? "-1" : match.Groups[1].Value;
        string variable = match.Groups[2].Value;
        string op = match.Groups[3].Value;
        string num = match.Groups[4].Value;
        string pow = match.Groups[5].Value;

        if (pow == "0")
        {
            return "1";
        }

        string result = "";
        for (int i = 0; i <= Convert.ToDouble(pow); i++)
        {
            result += (op == "-" && i % 2 == 1 ? "-" : "+") + PascalTriangle(Convert.ToInt32(pow), i)
                            * Math.Pow(Convert.ToInt32(pre), Convert.ToInt32(pow) - i) * Math.Pow(Convert.ToInt32(num), i) + variable + "^" + (Convert.ToInt32(pow) - i);
        }
        result = result.Replace("+-", "-").Replace(variable + "^0", "").Replace("-1"+variable, "-"+variable).Replace("--", "+").Trim('+');

        MatchEvaluator evaluator = new MatchEvaluator(OperatorAndVariable);
        result = Regex.Replace(result, "(^|[^0-9])1" + variable, evaluator);

        evaluator = new MatchEvaluator(VariableAndOperator);
        result = Regex.Replace(result, variable + "\\^1([^0-9]|$)", evaluator);
        result = Regex.Replace(result, "(\\+|-)0" + variable + "?(\\^[0-9]*)?", "");

        return result;
    }

    public static string VariableAndOperator(Match match)
    {
        return match.Value[0].ToString() + match.Value[match.Value.Length-1].ToString();
    }

    public static string OperatorAndVariable(Match match)
    {
        return match.Value[0] == '-' ? "-" + match.Value[match.Value.Length-1] : match.Value[match.Value.Length-1].ToString();
    }

    public static int PascalTriangle(int line, int spot)
    {
        int result = 1;
        for (int i = 1; i <= spot; i++)
        {
            result *= line - (spot - i);
            result /= i;
        }
        return result;
    }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public class KataSolution
{
  public static string Expand(string expr)  
  {
    char[] components = expr.ToCharArray();
    int i = 1;
    string _coefficient = "";
    string variable = "";
    string _constant = "";
    string _power = "";
    while (!Char.IsLetter(components[i])){_coefficient += components[i];i++;}
    if (_coefficient == ""){_coefficient = "1";}
    else if (_coefficient == "-"){_coefficient = "-1";}
    variable = Convert.ToString(components[i]); i++;
    while (components[i] != ')'){
      _constant += components[i];
      i++;
    } i+=2;
    for(int j = i; j<components.Length; j++){_power += components[j];}
    
    double coefficient = Convert.ToDouble(_coefficient);
    double constant = Convert.ToDouble(_constant);
    double power = Convert.ToDouble(_power);
    double? tpower = 0;
    double antipower = 0;
    double? scoefficient = 0;
    
    string final = "";
    
    if(power == 0){
      return "1";  
    }
    
    if(constant == 0){
      if (scoefficient == 1){
        scoefficient = null;
      }
      if (scoefficient == -1){scoefficient = null; final += "-";}
      return final+$"{Math.Pow(coefficient,power)}{variable}^{power}";  
    }
    
    for(int j = 0; j<Convert.ToInt32(_power); j++){
      double nfact = Factorial(Convert.ToDouble(_power));
      double antifact = Factorial(antipower);
      double remfact = Factorial(Convert.ToDouble(_power)-antipower);
      double choose = (double)(nfact/(antifact*remfact));
      double? tempco = Math.Pow(coefficient,power)*choose*Math.Pow(constant,antipower);
      string? tothe = "^";
      tpower = power;
      if (tempco == 1){tempco = null;}
      if (tempco == -1){tempco = null; final += "-";}
      if (tpower == 1){tpower = null; tothe = null;}
            
      if (final.Length > 0){
        if (tempco < 0 && final[^1] == '+'){
          final = final[..^1];
        }  
      }
            
      final += $"{tempco}{variable}{tothe}{tpower}+";
      
      power--;
      antipower++;
    }
    
    if (constant < 0 && final[^1] == '+' && antipower%2 == 1){
      final = final[..^1];
      }  
    
    final += $"{Math.Pow(constant,antipower)}";
    
    return final;
  }
  
  public static double Factorial(double num){
    double n = 0;n = num;
    if(n == 0){return 1;}
    for (double i = n - 1; i > 0; i--){n *= i;}
    return n;
  }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

public class KataSolution
{
  

  public static string Expand(string expr)  
  {
 
    char[] components = expr.ToCharArray();
    int i = 1;
    string _coefficient = "";
    string variable = "";
    string _constant = "";
    string _power = "";
    while (!Char.IsLetter(components[i])){_coefficient += components[i];i++;}
    if (_coefficient == ""){_coefficient = "1";}
    else if (_coefficient == "-"){_coefficient = "-1";}
    variable = Convert.ToString(components[i]); i++;
    while (components[i] != ')'){
      _constant += components[i];
      i++;
    } i+=2;
    for(int j = i; j<components.Length; j++){_power += components[j];}
    
    double coefficient = Convert.ToDouble(_coefficient);
    double constant = Convert.ToDouble(_constant);
    double power = Convert.ToDouble(_power);
    double? tpower = 0;
    double antipower = 0;
    
    string final = "";
    
    if(power == 0){
      return "1";  
    }
    
    if(constant == 0){
      return $"{Math.Pow(coefficient,power)}{variable}^{power}";  
    }
    
    //issues with powers
    for(int j = 0; j<Convert.ToInt32(_power); j++){
      double nfact = Factorial(Convert.ToDouble(_power));
      double antifact = Factorial(antipower);
      double remfact = Factorial(Convert.ToDouble(_power)-antipower);
      double choose = (double)(nfact/(antifact*remfact));
      double? tempco = Math.Pow(coefficient,power)*choose*Math.Pow(constant,antipower);
      Console.WriteLine($"j={j}");
      Console.WriteLine($"{tempco} {nfact} {antifact} {remfact} {choose} {power}");
      string? tothe = "^";
      tpower = power;
      if (tempco == 1){tempco = null;}
      if (tempco == -1){tempco = null; final += "-";}
      if (tpower == 1){tpower = null; tothe = null;}
      
      Console.WriteLine(final);
      
      if (final.Length > 0){
        if (tempco < 0 && final[^1] == '+'){
          final = final[..^1];
        }  
      }
      
      Console.WriteLine(final);
      
      final += $"{tempco}{variable}{tothe}{tpower}+";
      
      power--;
      antipower++;
    }
    
    if (constant < 0 && final[^1] == '+' && antipower%2 == 1){
      final = final[..^1];
      }  
    
    final += $"{Math.Pow(constant,antipower)}";
    
    return final;
  }
  
  public static double Factorial(double num){
    double n = 0;n = num;
    if(n == 0){return 1;}
    for (double i = n - 1; i > 0; i--){n *= i;}
    Console.WriteLine("Factorial of {0}! = {1}\n", num, n);
    return n;
  }
}

___________________________________________________
using System;
using System.Text.RegularExpressions;

public class KataSolution
{
    public static string Expand(string expr)
    {
        Console.WriteLine(expr);
        var s = Regex.Match(expr, @"[a-z]").Value;
        var a = Convert.ToInt32(Regex.Match(Regex.Replace(expr, $@"\(([\-]?){s}", m => "(" + m.Groups[1].Value + $"1{s}"), $@"\((.*){s}").Groups[1].Value);
        var b = Convert.ToInt32(Regex.Match(expr, $@"{s}(.*)\)").Groups[1].Value);
        var power = Convert.ToInt32(Regex.Match(expr, @"\^(.*)$").Groups[1].Value);

        var str = "";

        var pascal_line = new int[power + 1];
        pascal_line[0] = pascal_line[^1] = 1;

        for (int i = 1; i <= (power + 1) / 2; i++)
            pascal_line[^(i + 1)] = pascal_line[i] = pascal_line[i - 1] * (power - i + 1) / i;

        for (int i = power; i > 0 ; i--)
            str += (pascal_line[i] * (long)Math.Pow(a, i) * (long)Math.Pow(b, power - i)).ToString("+0;-#") + $"{s}^{i}";

        str += ((long)Math.Pow(b, power)).ToString("+0;-#");

        str = Regex.Replace(str, $@"([\-+])1{s}", m => m.Groups[1].Value + s);
        str = Regex.Replace(str, $@"[+\-]0(?:{s}\^[\d]*)?", "");
        str = Regex.Replace(str, $@"\b\^1\b", "");

        if (str[0] == '+') 
            str = str.Remove(0, 1);

        return str;
    }
}

___________________________________________________
using System;
using System.Text.RegularExpressions;

public class KataSolution
{
  private const string LEADING_SIGN = @"^\+";
  private const string ONE_COEF = @"(\D)1([a-z])";
  private const string INPUT = @"\((?<firstCoef>((\+|-)?\d*))(?<firstVar>[a-z]*)(?<secondCoef>((\+|-)?\d*))(?<secondVar>[a-z]*)\)\^(?<power>\d+)";
  
  public static string Expand(string expr)  
  {
    Console.WriteLine(expr);
    var match = Regex.Match(expr, INPUT);
    if (!match.Success)
    {
      return string.Empty;
    }
    
    var firstCoef = ToInt(match.Groups["firstCoef"].Value);
    var firstVar = match.Groups["firstVar"].Value;
    
    var secondCoef = ToInt(match.Groups["secondCoef"].Value);
    var secondVar = match.Groups["secondVar"].Value;
    
    var power = ToInt(match.Groups["power"].Value);
    
    var result = string.Empty;
    for (var i = 0; i < power + 1; i++)
    {
      var coef = (long)(BinomialCoefficient(power, i)
                       * Math.Pow(firstCoef, Math.Max(0, power - i))
                       * Math.Pow(secondCoef, Math.Min(power, i)));
      if (coef == 0)
      {
        continue;  
      }
      
      result += ToString(coef);
      if (!string.IsNullOrEmpty(firstVar) && i < power)
      {
        result += firstVar;
        result += power - i > 1 ? $"^{power - i}" : string.Empty;
      }
      
      if (!string.IsNullOrEmpty(secondVar) && i > 0)
      {
        result += secondVar;
        result += i - 1 > 1 ? $"^{i - 1}" : string.Empty;
      }
    }
    
    var withoutOneCoef = Regex.Replace(result, ONE_COEF, "$1$2");
    
    return Regex.Replace(withoutOneCoef, LEADING_SIGN, string.Empty);
  }
  
  private static long BinomialCoefficient(int n, int k)
  {
    return Factorial(n) / (Factorial(k) * Factorial(n - k));
  }
  
  private static long Factorial(int number)
  {
    var result = 1L;
    for (var i = number; i > 1; i--)
    {
        result *= i;
    }
    
    return result;
  }
  
  private static int ToInt(string coefficient)
  {
    return coefficient switch 
    {
      "" => 1,
      "-" => -1,
      "+" => 1,
      _ => int.Parse(coefficient)
    };
  }
  
  private static string ToString(long coefficient)
  {
    return coefficient switch
    {
      long x when (x > 0) => $"+{coefficient}",
      _ => coefficient.ToString()
    };
  }
}
