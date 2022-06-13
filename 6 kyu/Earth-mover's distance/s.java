import java.util.Comparator;
import java.util.stream.IntStream;

/**
 * Solution for 'Earth-mover's distance'.
 *
 * @author Johnny Lim
 */
public class Earth_Movers_Distance {

  public static double earth_movers_distance(double[] x, double[] px, double[] y, double[] py) {
    Bucket[] xBuckets = createBuckets(x, px);
    Bucket[] yBuckets = createBuckets(y, py);

    double distance = 0d;
    double xValue = 0;
    double xProbability = 0;
    int xIndex = 0;
    for (int i = 0; i < yBuckets.length; i++) {
      Bucket yBucket = yBuckets[i];
      double yValue = yBucket.value;
      double yProbability = yBucket.probability;

      distance += (yValue - xValue) * xProbability;
      xValue = yValue;
      while (xIndex < xBuckets.length) {
        Bucket xBucket = xBuckets[xIndex];
        if (xBucket.value > yValue) {
          break;
        }

        distance += (yValue - xBucket.value) * xBucket.probability;
        xProbability += xBucket.probability;
        xIndex++;
      }

      while (xProbability < yProbability) {
        Bucket xBucket = xBuckets[xIndex];
        double xProbabilitySum = xProbability + xBucket.probability;
        if (xProbabilitySum > yProbability) {
          double xLeftProbability = xProbabilitySum - yProbability;
          double xProbabilityToMove = xBucket.probability - xLeftProbability;
          xBucket.probability = xLeftProbability;
          distance += (xBucket.value - yValue) * xProbabilityToMove;
          xProbability += xProbabilityToMove;
        }
        else {
          distance += (xBucket.value - yValue) * xBucket.probability;
          xProbability += xBucket.probability;
          xIndex++;
        }
      }
      xProbability -= yProbability;
    }
    return distance;
  }

  private static Bucket[] createBuckets(double[] values, double[] probabilities) {
    return IntStream.range(0, values.length).mapToObj((i) -> new Bucket(values[i], probabilities[i]))
        .sorted(Comparator.comparingDouble((bucket) -> bucket.value)).toArray(Bucket[]::new);
  }

  static class Bucket {

    double value;

    double probability;

    Bucket(double value, double probability) {
      this.value = value;
      this.probability = probability;
    }

    @Override
    public String toString() {
      return "Bucket{" + "value=" + value + ", probability=" + probability + '}';
    }

  }

}
_________________________________________________
import java.util.Map.Entry;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.stream.IntStream;
public class Earth_Movers_Distance {
  public static double earth_movers_distance(double x[], double px[], double y[], double py[]) {
    SortedMap<Double, Double> diffs = new TreeMap<>();
    for(int i=0; i<x.length; ++i) diffs.put(x[i], px[i]);
    for(int i=0; i<y.length; ++i) diffs.merge(y[i], -py[i], (a,b)->a+b);
    
    double work = 0.;
    double pushcart = 0.;
    double last = diffs.firstKey();
    for(Entry<Double, Double> e : diffs.entrySet()) {
      double current = e.getKey();
      work += Math.abs(pushcart) * (current - last);
      pushcart += e.getValue();
      last = current;
    }
    return work;
  }
}
_________________________________________________
import java.util.*;

public class Earth_Movers_Distance
{
  
// A possible value and its probability:
private static class Atom
{
 public double x,p;
 public Atom(double ax, double ap) { x = ax;  p = ap; }
}
  
// Compare possible values, disregarding their associated probabilities:
private static class Atom_Comparator implements Comparator<Atom> 
{ 
 public int compare(Atom a, Atom b) { return a.x < b.x ? -1 : a.x == b.x ? 0 : 1; } 
} 
  
// Calculate the earth-mover's distance between two probability distributions:
public static double earth_movers_distance(double x[], double px[], double y[], double py[])
{
 Atom d[] = new Atom[x.length + y.length];   
 for(int i=0; i != x.length; i++)
   d[i] = new Atom(x[i], px[i]);
 for(int i=0; i != y.length; i++)
   d[i + x.length] = new Atom(y[i], -py[i]);
  
 Arrays.sort(d, new Atom_Comparator());
  
 double f = 0.0, sum = 0.0, last = 0.0;
 for( Atom a : d )
 {
   sum += Math.abs(f) * (a.x - last);
   f += a.p;
   last = a.x;
 }
   
 return sum;
}
  
}  // end class Earth_Movers_Distance
