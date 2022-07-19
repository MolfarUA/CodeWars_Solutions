55225023e1be1ec8bc000390


public class Greeter {
  public static String greet(String name) {
    if (!name.isEmpty()) {
      if (name.equals("Johnny"))
        return "Hello, my love!";
      else
        return String.format("Hello, %s!", name);
    }
    return "name is null";
  }
}
__________________________________
public class Greeter {
  public static String greet(String name) {
    return "Hello, " + (name == "Johnny" ?  "my love" : name) + "!";
  }
}
__________________________________
public class Greeter {
  public static String greet(String name) {
    
    if(name.equals("Johnny")){
      return "Hello, my love!";
    }

    return String.format("Hello, %s!", name);
  }
}
__________________________________
public class Greeter {
  public static String greet(String name) {
    if(!"Johnny".equals(name)) {
      return String.format("Hello, %s!", name);
    } else {
      return "Hello, my love!";
    }
  }
}
