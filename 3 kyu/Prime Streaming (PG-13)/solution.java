import java.util.stream.IntStream;

public class Primes {
  public static IntStream stream() {
    return IntStream.rangeClosed(2, Integer.MAX_VALUE).filter(Primes::isPrime);
  }
  
  public static boolean isPrime(int number) {
    for (int i = 2; i < (int) Math.sqrt(number) + 1; i++)
      if (number % i == 0) return false;
  
    return true;
  }
}
___________________________________________________________
import java.util.stream.IntStream;
import java.util.function.IntSupplier;
public class Primes {
  
  public static IntStream stream() {
    return IntStream.generate(
      new IntSupplier(){
      int lastSeen = 1;
      public int getAsInt(){
      int i = lastSeen;
      while(!isPrime(++i)){}
      lastSeen = i;
      return i;
    }});
  }
  public static boolean isPrime(int i){
    if(i==1) return false;
    if(i==2 || i==3 || i==5 || i==7 || i==11 || i==13 || i==17 || i==19) return true; // edge cases
    if(i%2==0 || i%3==0) return false; // edge cases
    int endp = (int)Math.ceil(Math.sqrt(i)/6.0)+2;
    for(int m = 1; m <= endp; m++){
      if(i%(6*m+1)==0 || i%(6*m-1)==0) return false;
    }
    return true;
  }
  
}
___________________________________________________________
import java.util.stream.IntStream;

public class Primes {
  private static final int N = 20000000;
  private static final boolean[] SIEVE = new boolean[N + 1];
  static {
    for (int i = 2; i * i <= N; i++) {
      if (!SIEVE[i]) {
        for (int j = i; i * j <= N; j++) {
          SIEVE[i * j] = true;
        }
      }
    }
  }

  public static IntStream stream() {
    return IntStream.range(2, N).filter(x -> !SIEVE[x]);
  }
}
___________________________________________________________
import java.util.stream.IntStream;

public class Primes {
  public static IntStream stream() {
        return IntStream.concat(
                IntStream.of(2),
                IntStream.iterate(3, n -> n + 2).filter(Primes::isPrime)
        );
    }

    private static boolean isPrime(int n) {
        return IntStream.iterate(3, x -> x <= (int) Math.sqrt(n), x -> x + 2)
                .allMatch(i -> n % i != 0);
    }
}
