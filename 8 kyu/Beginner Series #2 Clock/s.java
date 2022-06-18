55f9bca8ecaa9eac7100004a


public class Clock
{
  public static int Past(int h, int m, int s) 
  {
    return h * 3600000 + m * 60000 + s * 1000;
  }
}
__________________________
import java.time.Duration;

public class Clock {
  public static int Past(int h, int m, int s) {
    return (int)Duration.ofHours(h).plusMinutes(m).plusSeconds(s).toMillis();
  }
}
__________________________
public class Clock
{
  public static int Past(int h, int m, int s) 
  {
    return 1000*(s+60*(m+60*h));
  }
}
__________________________
public class Clock
{
  public static int Past(int h, int m, int s) 
  {
    return ((h*60 + m)*60 + s)*1000;
  }
}
__________________________
public class Clock
{
  public static int Past(int h, int m, int s) 
  {
    return (h*3600+m*60+s)*1000;
  }
}
