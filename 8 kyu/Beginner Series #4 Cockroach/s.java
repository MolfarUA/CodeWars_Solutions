55fab1ffda3e2e44f00000c6


public class Cockroach{
  public int cockroachSpeed(double kph){
    int secondsInHour = 3600;
    int cmInKm = 100000;
    int centimetresPerSecond = (int) (kph * cmInKm / secondsInHour);
    return centimetresPerSecond;
  }
}
__________________________
public class Cockroach{
  public int cockroachSpeed(double x){
    return (int)(x / 0.036);
  }
}
__________________________
public class Cockroach{
  public int cockroachSpeed(double x){
    return (int) (x * 100000)/3600;
  }
}
__________________________
public class Cockroach{
  public int cockroachSpeed(double x){
    x = x * 1000 / 36;
    x = Math.floor(x);
    return (int) x;
  }
}
__________________________
class Cockroach {
  static int cockroachSpeed(double x) {
    return (int) (27.7778 * x);
  }
}
__________________________
public class Cockroach{
  public int cockroachSpeed(double x){
   return (int) Math.floor((x*100000)/3600);
  }
}
