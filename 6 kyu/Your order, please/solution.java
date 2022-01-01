import java.util.Arrays;
import java.util.Comparator;

public class Order {
  public static String order(String words) {
    return Arrays.stream(words.split(" "))
      .sorted(Comparator.comparing(s -> Integer.valueOf(s.replaceAll("\\D", ""))))
      .reduce((a, b) -> a + " " + b).get();
  }
}

_____________________________________________
public class Order {
   public static String order(String words) {
        String[] arr = words.split(" ");
        StringBuilder result = new StringBuilder("");
        for (int i = 0; i < 10; i++) {
            for (String s : arr) {
                if (s.contains(String.valueOf(i))) {
                    result.append(s + " ");
                }
            }
        }
        return result.toString().trim();
    }
}

_____________________________________________
public class Order {
   public static String order(String words) {
        if (words.length() == 0) return "";
        String[] newWordsArray = words.split(" ");
        int num1 = 0;
        String newStr = "";

        for (int i = 0; i < newWordsArray.length; i++) {//go on words
            for (int j = 0; j < newWordsArray[i].length(); j++) {//go on symbols in a word

                num1 = tempNum(newWordsArray, i, j);// 57(9)-48(0) get number from string[]

                if (num1 > 0 && num1 < 10) {
                    newWordsArray = sortBubble(newWordsArray, i, j);
                    break;
                }
            }
        }
         for (int i = 0; i < newWordsArray.length; i++) {
            if (i == newWordsArray.length - 1) newStr += newWordsArray[i];
            else newStr += newWordsArray[i] + " ";
        }

        return newStr;
    }

    private static int indexJNext(int j, String[] newWordsArray) {
        int num2 = 0, index = 0;
        for (int i = 0; i < newWordsArray[j].length(); i++) {//go on symbols in a word
            num2 = tempNum(newWordsArray, j, i);// 57(9)-48(0)

            if (num2 > 0 && num2 < 10) {
                index = i;
                break;
            } else continue;
        }
        return index;
    }

    private static int tempNum(String[] newWordsArray, int i, int j) {
        return newWordsArray[i].charAt(j) - '0';
    }

    public static String[] sortBubble(String[] newWordsArray, int indexI, int indexJ) {
        for (int j = indexI + 1; j < newWordsArray.length; j++) {

            if (newWordsArray[indexI].charAt(indexJ) > newWordsArray[j].charAt(indexJNext(j, newWordsArray))) {
                String temp = newWordsArray[indexI];
                newWordsArray[indexI] = newWordsArray[j];
                newWordsArray[j] = temp;
                indexJ = indexJNext(indexI, newWordsArray);
            } else continue;
        }
        return newWordsArray;
    }
}

_____________________________________________
public class Order {
  public static String order(String words) {
    // ...
    String[] w = words.split(" ");
    String result = "";
    for (int i = 1; i <= w.length; i++) {
      for (String word : w) {
        if (word.contains(i+"")) {
          result+=word;
          if (i != w.length) result+=" ";
          break;
        }
      }
    }
    return result;
  }
}

_____________________________________________
public class Order {
  public static String order(String words) {
    if(words.equals("")){
      return words;
    }
    String[] wordsArr = words.split(" ");
    String[] finalArr = new String[wordsArr.length];
    
    for(int i=0; i<=wordsArr.length-1;i++){
      String temp = wordsArr[i].replaceAll("[^\\d.]", "");
      int tempIndex = Integer.valueOf(temp);
      finalArr[tempIndex-1] = wordsArr[i];
    }
    
    return String.join(" ", finalArr);
    
  }
}
