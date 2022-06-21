58708934a44cfccca60000c4


using System.Text.RegularExpressions;

public class Syntax
{
  public static string Highlight(string code)
  {
    code = new Regex("(F+)").Replace(code, "<span style=\"color: pink\">$1</span>");
    code = new Regex("(L+)").Replace(code, "<span style=\"color: red\">$1</span>");
    code = new Regex("(R+)").Replace(code, "<span style=\"color: green\">$1</span>");
    code = new Regex(@"(\d+)").Replace(code, "<span style=\"color: orange\">$1</span>");
    return code;
  }
}
__________________________
using System.Text.RegularExpressions;

public class Syntax
{
  public static string Highlight(string code)
  {
    code = Regex.Replace(code, "F+", "<span style=\"color: pink\">$0</span>");
    code = Regex.Replace(code, "L+", "<span style=\"color: red\">$0</span>");
    code = Regex.Replace(code, "R+", "<span style=\"color: green\">$0</span>");
    code = Regex.Replace(code, "[0123456789]+", "<span style=\"color: orange\">$0</span>");
    return code;
  }
}
__________________________
using System.Text.RegularExpressions;

public class Syntax
{
  public static string Highlight(string code)
  {
    string CreateReplacement(string color) { return $"<span style=\"color: {color}\">$1</span>"; }
            
    return Regex.Replace(Regex.Replace(Regex.Replace(Regex.Replace(code, 
                    @"(\d+)", CreateReplacement("orange")), 
                    @"(F+)", CreateReplacement("pink")), 
                    @"(L+)", CreateReplacement("red")), 
                    @"(R+)", CreateReplacement("green"));
  }
}
