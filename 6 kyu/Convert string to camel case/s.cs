using System;
using System.Text.RegularExpressions;

public class Kata
{
  public static string ToCamelCase(string str)
  {
    return Regex.Replace(str, @"[_-](\w)", m => m.Groups[1].Value.ToUpper());
  }
}
________________________
using System;
using System.Text;

public class Kata
{
  public static string ToCamelCase(string str)
  {
     
    var answerStr = new StringBuilder();
    
    bool flag = false;
     for(int i = 0; i < str.Length; i++){
       
      if(str[i] != '-' && str[i] != '_'){
        if (flag){
          string capLetter = str[i].ToString().ToUpper();
          answerStr.Append(capLetter);
          flag = false;
        }else{
          answerStr.Append(str[i]);
        }
        
      }
 
      else{
        flag = true;
      }
    }
   // Console.WriteLine(answerStr.ToString());
    return answerStr.ToString();
  }
}
________________________
using System;

public class Kata
{
  public static string ToCamelCase(string str)
  {
    while (str.IndexOf('_') != -1)
    {
        str = str.Insert(str.IndexOf('_'), char.ToUpper(str[str.IndexOf('_') + 1]).ToString());
        str = str.Remove(str.IndexOf('_'), 2);
    }
    while (str.IndexOf('-') != -1)
    {
        str = str.Insert(str.IndexOf('-'), char.ToUpper(str[str.IndexOf('-') + 1]).ToString());
        str = str.Remove(str.IndexOf('-'), 2);
    }
    return str;
  }
}
________________________
using System;

public class Kata
{
  public static string ToCamelCase(string str)
  {
     int flag=0;
                string result="";
               foreach (char c in str)
                {
                    if(flag == 0)
                    {
                        flag=1;
                        if (Char.IsLower(c))
                        {
                            result = c.ToString();
                        }
                        result = c.ToString();
                        continue;
                    }

                    if(flag == 2)
                    {
                        result=result+c.ToString().ToUpper();
                        flag = 1;
                        continue;
                    }

                    if (c == '_' || c == '-')
                    {
                        flag = 2;
                        continue;
                    }

                    result = result + c.ToString();

                } 
                
                return result;
  }
}
