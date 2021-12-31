public class HumanTimeFormat{
  public static string formatDuration(int seconds){
    //Enter Code here
            string s = "";
            int sec = seconds;
            int[] divArr = { 60 * 60 * 24 * 365, 60 * 60 * 24, 60 * 60, 60, 1 };
            string[] nameArr = {"year","day","hour","minute","second"};

            if (seconds == 0)
            {
                s = "now";
            }

            for (int i = 0; i< divArr.Length; i++)
            {
                int k = sec / divArr[i];
                sec = sec % divArr[i];
                if (k != 0)
                {
                    string pref = "";
                    if (s != "")
                    {
                        if (sec == 0)
                        {
                            pref = " and ";    
                        }
                        else
                        {
                            pref = ", ";
                        }
                    }
                    s = s + pref + k.ToString() + " " + nameArr[i];
                    s += k > 1 ? "s" : "";
                }
            }
            return s;
  }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class HumanTimeFormat{
  public static string formatDuration(int seconds){
    if (seconds == 0){
      return "now";
    }
    
    var time = TimeSpan.FromSeconds(seconds);
    var timesList = new string[]{
      MultipleFormat("year", time.Days / 365),
      MultipleFormat("day", time.Days % 365),
      MultipleFormat("hour", time.Hours),
      MultipleFormat("minute", time.Minutes),
      MultipleFormat("second", time.Seconds)
    };
    var list = timesList.Where(x => x != string.Empty).ToList();
    
    if (list.Count == 1){
      return list.First();
    }
    
    var firstPart = string.Join(", ", list.Take(list.Count - 1));
    
    return $"{firstPart} and {list.Last()}";
  }
  
  private static string MultipleFormat(string measure, double count){
    var c = (int)count;
    if (measure == string.Empty || c == 0){
      return string.Empty;
    }
    if (c != 1){
      measure = measure + "s";
    }
    return $"{c} {measure}";
  }
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public static class HumanTimeFormat
{
  public static string formatDuration(int seconds)
  {
    if(seconds == 0)
      return "now";
      
    var timeSpan = TimeSpan.FromSeconds(seconds);
    
    var timeFormatters = new List<ITimeFormatter>{new YearFormatter(), new DayFormatter(), new HourFormatter(), new MinuteFormatter(), new SecondFormatter() };
    
    var timeStrings = timeFormatters.Where(x => x.CanFormat(timeSpan)).Select(x => x.Format(timeSpan)).ToList();
    
    if(timeStrings.Count == 1)
    {
      return timeStrings[0];
    }
    
    return string.Join(", ", timeStrings.Take(timeStrings.Count - 1)) + " and " + timeStrings.Last();
  }
}

public interface ITimeFormatter
{
  bool CanFormat(TimeSpan time);
  string Format(TimeSpan time);
}

public static class PluralHelper
{
  public static string AppendWord(int number, string value)
  {
    return $"{number} {value}{(number > 1 ? "s" : "")}";
  }
}

public class YearFormatter : ITimeFormatter
{
  public bool CanFormat(TimeSpan time) => time.Days >= 365;
  public string Format(TimeSpan time) => PluralHelper.AppendWord(((int)Math.Floor(time.Days / 365d)),"year");
}

public class DayFormatter : ITimeFormatter
{
  public bool CanFormat(TimeSpan time) => time.Days % 365 > 0;
  public string Format(TimeSpan time) => PluralHelper.AppendWord(time.Days % 365, "day");
}

public class HourFormatter : ITimeFormatter
{
  public bool CanFormat(TimeSpan time) => time.Hours > 0;
  public string Format(TimeSpan time) => PluralHelper.AppendWord(time.Hours, "hour");
}

public class MinuteFormatter : ITimeFormatter
{
  public bool CanFormat(TimeSpan time) => time.Minutes > 0;
  public string Format(TimeSpan time) => PluralHelper.AppendWord(time.Minutes, "minute");
}

public class SecondFormatter : ITimeFormatter
{
  public bool CanFormat(TimeSpan time) => time.Seconds > 0;
  public string Format(TimeSpan time) => PluralHelper.AppendWord(time.Seconds, "second");
}

___________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class HumanTimeFormat{
  public static string formatDuration(int seconds){
      if (seconds == 0)
      {
          return "now";
      }
            
      var values = new Dictionary<string, int>()
      {
          { "year", seconds / (60 * 60 * 24 * 365) },
          { "day", seconds / (60 * 60 * 24) % 365 },
          { "hour", seconds / (60 * 60) % 24 },
          { "minute", seconds / 60 % 60 },
          { "second", seconds % 60 },
      };

      var formattedValues =
          values.Where(x => x.Value > 0)
          .Select(x => string.Format("{0} {1}{2}", x.Value, x.Key, x.Value > 1 ? "s" : ""))
          .ToArray();

      if (formattedValues.Length == 1)
      {
          return formattedValues.First();
      }
            
      var joinedValues =
          String.Join(", ", formattedValues, 0, formattedValues.Length - 1)
          + (formattedValues.Length > 1
          ? " and " + formattedValues.LastOrDefault()
          : "");

      return joinedValues;
  }
}
