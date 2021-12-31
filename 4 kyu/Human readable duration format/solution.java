import java.util.Arrays;
import java.util.stream.*;
public class TimeFormatter {    
    public static String formatDuration(int seconds) {            
        return seconds == 0 ? "now" : 
                Arrays.stream(
                  new String[]{
                       formatTime("year",  (seconds / 31536000)),
                       formatTime("day",   (seconds / 86400)%365),
                       formatTime("hour",  (seconds / 3600)%24),
                       formatTime("minute",(seconds / 60)%60),
                       formatTime("second",(seconds%3600)%60)})
                      .filter(e->e!="")
                      .collect(Collectors.joining(", "))
                      .replaceAll(", (?!.+,)", " and ");
    }
    public static String formatTime(String s, int time){
      return time==0 ? "" : Integer.toString(time)+ " " + s + (time==1?"" : "s");
    }
}

__________________________________________________
public class TimeFormatter {
    
  private static int S_PER_MIN = 60;
  private static int S_PER_HR  = 60 * S_PER_MIN;
  private static int S_PER_DAY = 24 * S_PER_HR;
  private static int S_PER_YR =  365 * S_PER_DAY;
  
  private static String unit(int n, String kind) {
    return n == 0 ? "" : String.format("%d %s%s, ", n, kind, n == 1 ? "" : "s");
  }
  
  public static String formatDuration(int s) {
  
    if (s == 0) return "now";
    
    int y, d, h, m;
    
    s -= (y = s / S_PER_YR)  * S_PER_YR;
    s -= (d = s / S_PER_DAY) * S_PER_DAY;
    s -= (h = s / S_PER_HR)  * S_PER_HR;
    s -= (m = s / S_PER_MIN) * S_PER_MIN;
    
    String ret = unit(y,"year") + unit(d,"day") + unit(h,"hour") + unit(m,"minute") + unit(s,"second");  
    ret = ret.substring(0, ret.length()-2); // remove trailing ', '
    return ret.lastIndexOf(",") == -1 ? ret : ret.replaceAll("(.+), (.+?)$", "$1 and $2"); // replace last , with "and"
  }
  
}

__________________________________________________
import java.util.Arrays;
import java.util.EnumMap;
import java.util.Map;
import java.util.Map.Entry;

public class TimeFormatter {

    public static String formatDuration(int seconds) {
       System.out.println(seconds);  

        if (seconds == 0) {
            return "now";
        }

        Map<TimePeriod, Integer> timePeriodsOccurrence = new EnumMap<>(TimePeriod.class);
        TimePeriod currentTimePeriod;

        while (seconds > 0) {

            currentTimePeriod = TimePeriod.of(seconds);
            if (timePeriodsOccurrence.containsKey(currentTimePeriod)) {
                Integer integer = timePeriodsOccurrence.get(currentTimePeriod);
                timePeriodsOccurrence.put(currentTimePeriod, integer + 1);
            } else {
                timePeriodsOccurrence.put(currentTimePeriod, 1);
            }
            seconds -= currentTimePeriod.valueInSeconds;
        }
        return buildAnswer(timePeriodsOccurrence);
    }

    private static String buildAnswer(Map<TimePeriod, Integer> timePeriodsOccurrence) {
        StringBuilder stringBuilder = new StringBuilder();
        int index = 0;
        for (Entry<TimePeriod, Integer> timePeriodIntegerEntry : timePeriodsOccurrence.entrySet()) {

            Integer valueInSeconds = timePeriodIntegerEntry.getValue();
            stringBuilder.append(valueInSeconds);
            stringBuilder.append(" ");

            TimePeriod timePeriod = timePeriodIntegerEntry.getKey();
            String formattedName = timePeriod.getFormattedName(valueInSeconds);
            stringBuilder.append(formattedName);
            if (index == timePeriodsOccurrence.entrySet().size() - 2) {
                stringBuilder.append(" and ");
            } else if (index < timePeriodsOccurrence.entrySet().size() - 1) {
                stringBuilder.append(", ");
            }
            index++;
        }

        return stringBuilder.toString().trim();
    }

    enum TimePeriod {

        YEAR("year", 31536000),
        DAY("day", 86400),
        HOUR("hour", 3600),
        MINUTE("minute", 60),
        SECOND("second", 1);

        final private String name;
        final private int valueInSeconds;

        TimePeriod(String name, int valueInSeconds) {

            this.name = name;
            this.valueInSeconds = valueInSeconds;
        }

        static TimePeriod of(int seconds) {

            return Arrays.stream(values())
                    .filter(v -> seconds >= v.valueInSeconds)
                    .findFirst()
                    .orElse(null);
        }

        String getFormattedName(int value) {
            return value == 1 ? name : name + "s";
        }
    }
}

__________________________________________________
import java.util.ArrayList;

public class TimeFormatter {

  public static String formatDuration(int seconds) {
    if (seconds == 0) {
      return "now";
    }
    ArrayList<String> resultParts = new ArrayList<>();

    final int years = seconds / (60 * 60 * 24 * 365);
    // case: years
    if (years > 0) {
      resultParts.add(years + " year" + (years > 1 ? "s" : ""));
      seconds = seconds % (60 * 60 * 24 * 365);
    }

    // case: days
    final int days = seconds / (60 * 60 * 24);
    if (days > 0) {
      resultParts.add(days + " day" + (days > 1 ? "s" : ""));
      seconds = seconds % (60 * 60 * 24);
    }

    // case: hours
    final int hours = seconds / (60 * 60);
    if (hours > 0) {
      resultParts.add(hours + " hour" + (hours > 1 ? "s" : ""));
      seconds = seconds % (60 * 60);
    }

    // case: minutes
    final int minutes = seconds / 60;
    if (minutes > 0) {
      resultParts.add(minutes + " minute" + (minutes > 1 ? "s" : ""));
      seconds = seconds % 60;
    }

    // case: seconds
    if (seconds > 0) {
      resultParts.add(seconds + " second" + (seconds> 1 ? "s" : ""));
    }

    StringBuilder output = new StringBuilder();
    for (int i = 0; i < resultParts.size(); i++) {
      output.append(resultParts.get(i));
      if (i < resultParts.size() - 2) {
        output.append(", ");
      } else if (resultParts.size() > 1 && i < resultParts.size() - 1) {
        output.append(" and ");
      }

    }

    return output.toString();
  }
}

__________________________________________________
import java.util.*;
import java.util.stream.Collectors;

public class TimeFormatter {

    public enum TIME_UNIT {
        SECOND(1),
        MINUTE(60),
        HOUR(MINUTE.numberOfSeconds * 60),
        DAY(HOUR.numberOfSeconds * 24),
        YEAR(DAY.numberOfSeconds * 365);

        private int numberOfSeconds;

        TIME_UNIT(int numberOfSeconds) {
            this.numberOfSeconds = numberOfSeconds;
        }

        public int getNumberOfSeconds() {
            return numberOfSeconds;
        }
    }

    public static String formatDuration(int seconds) {
        if(seconds == 0) {
            return "now";
        }

        var list = new ArrayList<String>();
        var units = TIME_UNIT.values();
        Arrays.sort(units, Comparator.reverseOrder());

        for (TIME_UNIT unit : units) {
            var numberOfUnits = seconds / unit.getNumberOfSeconds();
            seconds %= unit.getNumberOfSeconds();
            if(numberOfUnits > 0) {
                list.add(numberOfUnits + " " + unit.name().toLowerCase() + (numberOfUnits > 1 ? "s" : ""));
            }
        }
        var result = list.stream().collect(Collectors.joining(", "));
        return result.replaceFirst(",(?!.*,)", " and");
    }
}
