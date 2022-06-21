5263c6999e0f40dee200059d


import java.util.*;

public class ObservedPin {

    private static final Map<Character,String> ADJACENTS = new HashMap<Character,String>() {{
        put('1', "124");
        put('2', "2135");
        put('3', "326");
        put('4', "4157");
        put('5', "54268");
        put('6', "6953");
        put('7', "748");
        put('8', "87590");
        put('9', "986");
        put('0', "08");
    }};

    public static List<String> getPINs(String observed) {
        
        List<String> ans = Arrays.asList("");
        
        for (char c: observed.toCharArray()) {
            
            List<String> tmp = new ArrayList<String>();
            for (char cc: ADJACENTS.get(c).toCharArray()) {
                for (String s: ans) tmp.add(s+cc);
            }
            ans = tmp;
        }
        return ans;
    }

}
______________________________
import java.util.*;


public class ObservedPin {
   List<String> list=new ArrayList<>();
    char ar[][]={{'0','8'},
                  {'1','2','4'},
                  {'1','2','3','5'},
                  {'2','3','6'},
                  {'1','4','5','7'},
                  {'2','4','5','6','8'},
                  {'3','5','6','9'},
                  {'4','7','8'},
                  {'0','5','7','8','9'},
                  {'6','8','9'}};
  
  public void solve(String s, String pre){
    int d=Integer.parseInt(s.charAt(0)+"");
    if(s.length()==1){
      for(int x=0;x<ar[d].length;x++){
        list.add(pre+ar[d][x]);
      }
    }
    else{
      for(int x=0;x<ar[d].length;x++){
        solve(s.substring(1),pre+ar[d][x]);
      }
    }
  }
  
  public static List<String> getPINs(String observed) {
    ObservedPin ob=new ObservedPin();
    ob.solve(observed,"");
    //list.add(observed);
    return ob.list;
    
    } // getPINs

} // ObservedPin
______________________________
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class ObservedPin {

    public static List<String> getPINs(String observed) {
    HashMap<String, String[]> adjacents = new HashMap<>();
        adjacents.put("1", new String[]{"1", "2", "4"});
        adjacents.put("2", new String[]{"1", "2", "3", "5"});
        adjacents.put("3", new String[]{"2", "3", "6"});
        adjacents.put("4", new String[]{"1", "4", "5", "7"});
        adjacents.put("5", new String[]{"2", "4", "5", "6", "8"});
        adjacents.put("6", new String[]{"3", "5", "6", "9"});
        adjacents.put("7", new String[]{"4", "7", "8"});
        adjacents.put("8", new String[]{"5", "7", "8", "9", "0"});
        adjacents.put("9", new String[]{"6", "8", "9"});
        adjacents.put("0", new String[]{"0", "8"});

        StringBuilder pinBuilder = new StringBuilder(observed);

        char[] observedPin = observed.toCharArray();

        String[] firstPositionValues = adjacents.get(String.valueOf(observedPin[0]));

        List<String> pins = new ArrayList<>();

        for (String value : firstPositionValues) {


            pinBuilder.setCharAt(0, value.charAt(0));

            int currentDigit = 1; 
            int[] currentPermutation = new int[observedPin.length]; 

            if (observedPin.length > 1) {

               
                while (currentDigit != observedPin.length && currentDigit > 0) {

                    
                    String[] values = adjacents.get(String.valueOf(observedPin[currentDigit]));

                    if (currentDigit == observedPin.length - 1) {

                       
                        if (currentPermutation[currentDigit] < values.length) {

                            for (String val : values) {

                                pinBuilder.setCharAt(currentDigit, val.charAt(0));

                                if (currentPermutation[currentDigit] < values.length) {
                                    currentPermutation[currentDigit]++;
                                }

                                
                                if (pins.indexOf(pinBuilder.toString()) == -1) {
                                    pins.add(pinBuilder.toString());
                                }

                            }
                        } else {
                            currentPermutation[currentDigit] = 0;
                            currentDigit = currentDigit - 1;
                        }


                    } else {

                        if (currentPermutation[currentDigit] < values.length) {
                            pinBuilder.setCharAt(currentDigit, values[currentPermutation[currentDigit]].charAt(0));
                            currentPermutation[currentDigit]++;
                            currentDigit++;
                        }
                        else {
                            currentPermutation[currentDigit] = 0;
                            currentDigit = currentDigit - 1;
                        }
                    }
                }
            }

            if (pins.indexOf(pinBuilder.toString()) == -1) {
                pins.add(pinBuilder.toString());
            }
        }

        System.out.println("There are : " + pins.size()+  " possible pins");
        return pins;
    } // getPINs

} 
