public class Hello{
  public String sayHello(String[] name, String city, String state){
    return String.format("Hello, %s! Welcome to %s, %s!",String.join(" ", name),city,state);
  }
}
_______________________________________
import java.util.Arrays;

public class Hello {

  /**
   * Greets a person with the given name into the given City
   *
   * @param name array of names forming a full name
   * @param city the city
   * @param state the state that the city is in
   * @return the greeting
   */
  public String sayHello(String[] name, String city, String state) {
    if (name == null) {
      throw new IllegalArgumentException("Provided name must be non-null array");
    } else if (Arrays.asList(name).contains(null)) {
      throw new IllegalArgumentException("Name array must not contain null, was: " + Arrays.toString(name));
    } else if (city == null) {
      throw new IllegalArgumentException("City must not be null");
    } else if (state == null) {
      throw new IllegalArgumentException("State must not be null");
    }
    return String.format("Hello, %s! Welcome to %s, %s!", String.join(" ", name), city, state);
  }
}
_______________________________________
public class Hello{
  public String sayHello(String [] name, String city, String state){
    String fullName = "";
    for (String nam : name){
        fullName += " " + nam;
    }
    return String.format("Hello,%s! Welcome to %s, %s!", fullName, city, state);
  }
}
_______________________________________
public class Hello{
  public String sayHello(String [] name, String city, String state){
    String fullName = String.join(" ", name);
    return String.format("Hello, %s! Welcome to %s, %s!", fullName, city, state);
  }
}
