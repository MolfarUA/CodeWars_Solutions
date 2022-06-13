import java.util.Arrays;

public class MontyHall {

    public int montyHallCase(int correctDoorNumber, int[] participantGuesses) {
        long winners = Arrays.stream(participantGuesses)
                .filter(door -> door != correctDoorNumber)
                .count();
        return (int) Math.round(100.0 * winners / participantGuesses.length);
    }

}
_________________________________________________
public class MontyHall {
  public int montyHallCase(int c, int[] guesses) {
    int wins = 0;
    for(int guess : guesses) if(guess != c) wins++;
    return (int) Math.round(1.0 * wins / guesses.length * 100);
  }
}
_________________________________________________
public class MontyHall {

  public int montyHallCase(int correctDoorNumber, int[] participantGuesses) {
  
    int sum = participantGuesses.length;
    int partici = participantGuesses.length;
    
    for(int x : participantGuesses){
      if(x == correctDoorNumber) {
        sum--;
      }
    }
    return (int) Math.round((sum*100.0)/partici);
  }

}
_________________________________________________
import static java.util.stream.IntStream.of;

class MontyHall {
  static int montyHallCase(int correctDoorNumber, int[] participantGuesses) {
    return Math.round(100f * of(participantGuesses).filter(g -> g != correctDoorNumber).count() / participantGuesses.length);
  }
}
