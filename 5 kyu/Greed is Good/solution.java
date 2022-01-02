public class Greed {

  public static int greedy(int[] dice) {
    int n[] = new int[7];
    for (int d : dice) n[d]++;
    return n[1]/3*1000 + n[1]%3*100 + n[2]/3*200 + n[3]/3*300 + n[4]/3*400 + n[5]/3*500 + n[5]%3*50 + n[6]/3*600;
  }
  
}
_____________________________________________
public class Greed{
  public static int greedy(int[] dice){
        int res = 0;
        int[] count = new int[]{0, 0, 0, 0, 0, 0};
        int[] weight = new int[]{100, 0, 0, 0, 50, 0};
        int[] weight3 = new int[]{1000, 200, 300, 400, 500, 600};

        for (int die : dice) count[die-1]++;

        for (int i = 0; i < count.length; i++) res+=(count[i]/3*weight3[i]) + (count[i]%3 * weight[i]);

        return res;
  }
}
_____________________________________________
import java.util.HashMap;
public class Greed{
  public static int greedy(int[] dice){
        int sum = 0;
        HashMap<Integer, Integer> c = new HashMap<Integer, Integer>();
        for(int i = 0; i < dice.length; i++) {
            if(c.containsKey(dice[i]) && c.get(dice[i]) != null) {
                c.put(dice[i], c.get(dice[i])+1);
            } else {
                c.put(dice[i], 1);
            }
        }
        for(int i = 1; i < 7; i++) {
            if(c.get(i) != null) {
                int tmp = c.get(i);
                sum += score(i, (tmp-tmp%3)/3, tmp%3);
            }
        }
        return sum;
    }

    public static int score (int n, int three, int one) {
        int result = 0;

        switch (n) {
            case 1: result = three * 1000 + one * 100; break;
            case 2: result = three *200; break;
            case 3: result = three *300; break;
            case 4: result = three *400; break;
            case 5: result = three *500 + one *50; break;
            case 6: result = three *600; break;
            default: break;
        }
        return result;
    }
}
_____________________________________________
import java.util.Arrays;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Greed{
  public static int greedy(int[] dice){
    Map<Integer, Long> collect = Arrays.stream(dice).boxed().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
    int score = 0;
    for (Map.Entry<Integer, Long> e : collect.entrySet()) {
      switch (e.getKey()) {
        case 1: score += ( ( e.getValue() >= 3) ? 1000 : 0) + (e.getValue() % 3) * 100; break;
        case 2: score += ( ( e.getValue() >= 3) ? 200 : 0); break;
        case 3: score += ( ( e.getValue() >= 3) ? 300 : 0); break;
        case 4: score += ( ( e.getValue() >= 3) ? 400 : 0); break;
        case 5: score += ( ( e.getValue() >= 3) ? 500 : 0) + (e.getValue() % 3) * 50; break;
        case 6: score += ( ( e.getValue() >= 3) ? 600 : 0); break;
      }
    }
    return score;
  }
}
