public class HumanReadableTime {
  public static String makeReadable(int seconds) {
    return String.format("%02d:%02d:%02d", seconds / 3600, (seconds / 60) % 60, seconds % 60);
  }
}

_____________________________________
public class HumanReadableTime {
    public static String makeReadable(int seconds) {
        int h = seconds/60/60;
        int min = seconds/60%60;
        int sec = seconds%60;
        return String.format("%02d:%02d:%02d",h,min,sec);
    }
}

_____________________________________
public class HumanReadableTime {
  public static String makeReadable(int seconds) {
    return String.format("%02d:%02d:%02d", seconds/3600, seconds%3600/60, seconds%60);
  }
}

_____________________________________
public class HumanReadableTime {
  public static String makeReadable(int seconds) {

    int h = seconds / 3600;
    int m = seconds % 3600 / 60;
    int s = seconds % 60;

    return (h > 9 ? "" : "0") + h + ":" + (m > 9 ? "" : "0") + m + ":" + (s > 9 ? "" : "0") + s;
  }
}

_____________________________________
public class HumanReadableTime {
  public static String makeReadable(int seconds) {
    int timeHours = seconds / 3600;
    int timeMinutes = (seconds % 3600) / 60;
    int timeSeconds = seconds % 60;
    String timeString = String.format("%02d:%02d:%02d", timeHours, timeMinutes, timeSeconds);
    //thanks Bigtoes for help!
    return timeString;
  }
}
