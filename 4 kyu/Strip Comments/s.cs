51c8e37cee245da6b40000bd


using System;
using System.Linq;
using System.Text.RegularExpressions;
public class StripCommentsSolution
{
    public static string StripComments(string text, string[] commentSymbols)
    {
        string[] lines = text.Split(new [] { "\n" }, StringSplitOptions.None);
        lines = lines.Select(x => x.Split(commentSymbols, StringSplitOptions.None).First().TrimEnd()).ToArray();
        return string.Join("\n", lines);
    }
}
__________________________________
using System;
using System.Linq;
using System.Collections.Generic;

public class StripCommentsSolution
{
    public static string StripComments(string text, string[] commentSymbols)
    {
      return string
        .Join("\n", text.Split("\n")
        .Select(x => x.Split(commentSymbols, StringSplitOptions.None)[0]
        .TrimEnd(' ')));
    }
}
__________________________________
using System;
using NUnit.Framework;
using System.Linq;
using System.Collections.Generic;
using System.Text;

public class StripCommentsSolution
{
        public static string StripComments(string text, string[] commentSymbols)
        {
           return String.Join('\n', text.Split('\n').Select(str => str.Split(commentSymbols, 0)[0].TrimEnd()));
        }
}
__________________________________
using System.Linq;
using System.Text.RegularExpressions;

public class StripCommentsSolution
{
    public static string StripComments(string text, string[] commentSymbols)
    { // [ \t]*([#].*|$)
      string regex = @"[ \t]*(["+ string.Join("",commentSymbols)+ @"].*|$)";
      return Regex.Replace(
         text,regex,"", RegexOptions.Multiline);
    }
}
