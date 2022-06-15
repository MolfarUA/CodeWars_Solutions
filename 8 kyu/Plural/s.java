public class Plural{
  public static boolean isPlural(float f){
   return (f != 1 );
  }
}
__________________
public class Plural{
  public static boolean isPlural(float f){
    boolean asw = false;
    if (f == 0){
      asw = true;
    } 
    if (f == 1f){
      asw = false;
    }
    if (f >= 0.1 && f < 1f){
      asw = true;
    }
    if (f > 1f) {
      asw = true;
      }
    if (f < 0){
      asw = false;
    }
    
     return asw;
  }
}
__________________
public class Plural{
  public static boolean isPlural(float f){
    
    if(f > 1 || f==0 || f<1 && f>0){
      return true;
    }
    return false; 
  }
}
__________________
public class Plural{
  public static boolean isPlural(float f){
    boolean a = true;
    if (f==1) {
  a = false; } 
    else  {
      a = true;
    }
    return a;
  }
}
__________________
public class Plural {
  
  public static boolean isPlural (float f) {
    if (f < 0) {
      return false;
    }
    
    if (f == 1){
      return false;
    }
    
    return true;    
    
  }
}
