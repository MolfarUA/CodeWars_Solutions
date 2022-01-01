public static class TimeFormat
{
    public static string GetReadableTime(int seconds)
    {
        return string.Format("{0:d2}:{1:d2}:{2:d2}", seconds / 3600, seconds / 60 % 60, seconds % 60);
    }
}

_____________________________________
using System;

public static class TimeFormat
{
    public static string GetReadableTime(int seconds)
    {
        var t = TimeSpan.FromSeconds(seconds);
        return string.Format("{0:00}:{1:00}:{2:00}", (int)t.TotalHours, t.Minutes, t.Seconds);
    }
}

_____________________________________
using System;

public static class TimeFormat
{
    public static string GetReadableTime(int seconds)
    {
      int sec = (seconds % 60);
      int min = ((seconds-sec)/60)%60;
      int hour = (seconds-sec-(60*min))/(60*60);
      
      return (hour.ToString("00")+":"+min.ToString("00")+":"+sec.ToString("00"));
    }
}

_____________________________________
using System;
public static class TimeFormat
{
    public static string GetReadableTime(int s) => String.Format("{0:D2}:{1:D2}:{2:D2}", s / 3600, s / 60 % 60, s % 60);
}

_____________________________________
using System;

public static class TimeFormat
{
    public static string GetReadableTime(int seconds)
    {
        var span = TimeSpan.FromSeconds(seconds);
        return String.Format("{0}:{1}:{2}",
            Math.Floor(span.TotalHours).ToString("00"),
            span.Minutes.ToString("00"),
            span.Seconds.ToString("00"));
    }
}
