import java.util.ArrayList;

class Metro {

  public static int countPassengers(ArrayList<int[]> stops) {
    return stops.stream()
                .mapToInt(x -> x[0] - x[1])
                .sum();
  }
}
_____________________________________
import java.util.ArrayList;
class Metro {
  public static int countPassengers(ArrayList<int[]> stops) {
    int res = 0;
    for(int[] onOff : stops) res += onOff[0] - onOff[1];
    return res;
  }
}
_____________________________________
import java.util.ArrayList;

class Metro {
  public static int countPassengers(ArrayList<int[]> stops) {
      int total = 0;
      for (int[] i : stops) {
          total += i[0];
          total -= i[1];
      }
      return total;
  }
}
_____________________________________
import java.util.ArrayList;

class Metro {

  public static int countPassengers(ArrayList<int[]> stops) {
    int peopleIn = 0;
    int peopleOut = 0;
    int peopleInBus = 0;
    for(int[] element: stops){
      peopleIn = peopleIn + element[0];
      peopleOut = peopleOut + element[1]; 
    }
    peopleInBus = peopleIn - peopleOut;
    return peopleInBus;
  }
}
