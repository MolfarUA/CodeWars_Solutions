public class FakeBinary {
    public static String fakeBin(String numberString) {
        return numberString.replaceAll("[0-4]", "0").replaceAll("[5-9]", "1");
    }
}
__________________________________
public class FakeBinary {
    public static String fakeBin(String numberString) {
        final char c[] = numberString.toCharArray();
        for (int i = 0; i < c.length; i++)
          c[i] = c[i] < '5' ? '0' : '1';
        return new String(c);
    }
}
__________________________________
public class FakeBinary {
    public static String fakeBin(String s) {
        return s.replaceAll("[1-4]","0").replaceAll("[^0]","1");
    }
}
__________________________________
public class FakeBinary {
    public static String fakeBin(String numberString) {
      String[] strArray = numberString.split("");  
      
      for(int i=0; i<strArray.length; i++){
        if(Integer.parseInt(strArray[i])<5){
          strArray[i] = strArray[i].replace(strArray[i], "0");
        } else{
          strArray[i] = strArray[i].replace(strArray[i], "1");
        }
      }
      return String.join("", strArray);
     
    
    }
}
__________________________________
public class FakeBinary {
    public static String fakeBin(String numberString) {
      String res = ""; 
      for (char ch: numberString.toCharArray()) {
        if (Integer.parseInt(String.valueOf(ch)) < 5) {
          res+= "0";
        } else {
          res += "1";
        }
       } 
      return res;
    }
}
