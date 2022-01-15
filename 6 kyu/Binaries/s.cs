using System;
using System.Linq;

public class CodeDecode
{
    public static string Code(string strng)
    {
        return string.Concat(strng.Select(n => Convert.ToString(n-'0', 2)).Select(b => "1".PadLeft(b.Length, '0') + b));
    }
    public static string Decode(string s)
    {
        var i = s.IndexOf('1') + 1;  
        return (i > 0) ? Convert.ToInt32(s.Substring(i,i), 2) + Decode(s.Substring(i+i)) : "";
    }
}
__________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
public class CodeDecode
{
    private static Dictionary<int, string> codeMap = new Dictionary<int, string>
    {
        [0] = "10",
        [1] = "11",
        [2] = "0110",
        [3] = "0111",
        [4] = "001100",
        [5] = "001101",
        [6] = "001110",
        [7] = "001111",
        [8] = "00011000",
        [9] = "00011001"
    };
    public static string Code(string strng) => string.Concat(strng.Select(x => codeMap[x - '0']));
    public static string Decode(string str) => string.Concat(Regex.Matches(str, $"{string.Join("|", codeMap.Select(x => x.Value).Reverse())}").Select(x => codeMap.First(y => y.Value == x.Value).Key));
}
__________________________
using System;

public class CodeDecode
{

    private static string dec2Bin(string s)
    {
        string[] dict = new string[] {"10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
        return dict[int.Parse(s)];
    }
    public static string Code(string strng)
    {
        int lg = strng.Length;
        string ret = "";
        for (int start = 0; start < lg; start += 1)
            ret += dec2Bin(Convert.ToString(strng[start]));
        return ret;
    }
    public static string Decode(string str)
    {
        string ret = "";
        int i = 0;
        int lg = str.Length;
        while (i < lg)
        {
            int zero_i = i;
            while ((zero_i < lg) && (str[zero_i] != '1'))
            {
                zero_i++;
            }
            int l = zero_i - i + 2;
            string ss = str.Substring(zero_i + 1, (zero_i + l) - (zero_i + 1));
            ret += Convert.ToString(Convert.ToInt32(ss, 2), 10);
            i = zero_i + l;
        }
        return ret;
    }
}
__________________________
using System;
using System.Text;

public class CodeDecode
{
    private static string[] codes = new string[10] { "10", "11", "0110", "0111", "001100", "001101", "001110", "001111", "00011000", "00011001"};
    public static string Code(string strng)
    {
        if (strng.Length == 0) return strng;
        var sb = new StringBuilder();
        for (int i = 0; i < strng.Length; i++) {
          sb.Append(codes[strng[i] - '0']);
        }
        return sb.ToString();
    }
    public static string Decode(string str)
    {
        if (str.Length == 0) return str;
        int ind = 0;
        var sb = new StringBuilder();
        var cnt = 0;
        while (ind < str.Length) {
          while (str[ind] == '0') {
            cnt++;
            ind++;
          }
          cnt++;
          ind++;
          sb.Append(Array.IndexOf(codes, str.Substring(ind - cnt, 2 * cnt)));
          ind+=cnt;
          cnt = 0;
        }
        return sb.ToString();
    }
}
__________________________
using System;
using System.Linq;

public class CodeDecode
{
    public static string Code(string s) => string.Concat(s.Select(n => "1".PadLeft(n>55?4:n>51?3:n&2, '0') + Convert.ToString(n-48, 2)));
  
    public static string Decode(string s)
    {
        var i = s.IndexOf('1') + 1;  
        return (i > 0) ? Convert.ToInt32(s.Substring(i,i), 2) + Decode(s.Substring(i+i)) : "";
    }

}
