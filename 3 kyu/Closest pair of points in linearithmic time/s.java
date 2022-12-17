5376b901424ed4f8c20002b7


import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class Kata {
    public static List<Point> closestPair(final List<Point> points) {
        points.sort((a, b) -> Double.compare(a.x, b.x) == 0 ? Double.compare(a.y, b.y) : Double.compare(a.x, b.x));

        return find((points));
    }

    private static List<Point> find(final List<Point> points) {
        if (points.size() <= 3) {
            return bruteForce(points);
        }

        final int mid = points.size() / 2;
        final List<Point> pointsLeft = find(points.subList(0, mid));
        final List<Point> pointsRight = find(points.subList(mid, points.size()));

        final double distanceL = calcDistance(pointsLeft.get(0), pointsLeft.get(1));
        final double distanceR = calcDistance(pointsRight.get(0), pointsRight.get(1));
        final double delta = Math.min(distanceL, distanceR);
        final List<Point> stripPoints = stripPoint(points, delta, mid);

        if (stripPoints.isEmpty()) {
            return distanceL < distanceR ? pointsLeft : pointsRight;
        }

        return stripPoints;
    }

    private static List<Point> stripPoint(final List<Point> points, final double delta, final int mid) {
        final List<Point> strips = points.stream()
                .filter(p -> Math.abs(p.x - points.get(mid).x) < delta)
                .sorted(Comparator.comparing(p -> p.y))
                .collect(Collectors.toList());

        double min = delta;
        Point p1 = null;
        Point p2 = null;
        for (int i = 0; i < strips.size(); ++i) {
            for (int j = i + 1; j < strips.size() && (strips.get(j).y - strips.get(i).y) < min; ++j) {
                final double dist = calcDistance(strips.get(i), strips.get(j));
                if (dist < min) {
                    min = dist;
                    p1 = strips.get(i);
                    p2 = strips.get(j);
                }
            }
        }

        if (Objects.nonNull(p1)) {
            return Arrays.asList(p1, p2);
        }

        return Collections.emptyList();
    }

    private static double calcDistance(final Point point1, final Point point2) {
        return Math.sqrt(Math.pow(point1.x - point2.x, 2) + Math.pow(point1.y - point2.y, 2));
    }

    private static List<Point> bruteForce(final List<Point> points) {
        Point p1 = null;
        Point p2 = null;
        double min = Double.MAX_VALUE;
        for (int i = 0; i < points.size(); i++) {
            for (int j = i + 1; j < points.size(); j++) {
                final double dist = calcDistance(points.get(i), points.get(j));

                if (dist < min) {
                    min = dist;
                    p1 = points.get(i);
                    p2 = points.get(j);
                }
            }
        }

        return Arrays.asList(p1, p2);
    }
}
______________________________________
import java.util.Arrays;
import java.util.List;
import java.util.TreeSet;

public class Kata {

    public static double distance(Point p1, Point p2) {
        return Math.sqrt( Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2) );
    }

    public static List<Point> closestPair(List<Point> l) {
        Point [] points = l.toArray(new Point[]{});
        Arrays.sort(points, ( p1, p2) -> {
            if ( p1.x < p2.x ) return -1;
            if ( p1.x > p2.x ) return 1;
            return Double.compare(p1.y, p2.y);
        });

        TreeSet<Point> candidates = new TreeSet<>( ( p1, p2) -> {
            if ( p1.y < p2.y ) return -1;
            if ( p1.y > p2.y ) return 1;
            return Double.compare(p1.x, p2.x);
        });
        double min = Double.POSITIVE_INFINITY;
        Point[] closest = new Point[2];
        //index in points: left border for all points on the left with: current.x - x < currentMin
        int i = 0;
        for ( Point p : points ) {
            while ( p.x - points[i].x > min ) {
                candidates.remove(points[i]);
                i += 1;
            }
            Point from = new Point(p.x, p.y - min);
            Point to = new Point(p.x, p.y + min);
            for ( Point c : candidates.subSet(from, to) ) {
                double d = distance(p, c);
                if ( d < min ) {
                    min = d;
                    closest[0] = c;
                    closest[1] = p;
                }
            }
            candidates.add(p);
        }
        return Arrays.asList(closest);
    }

}
______________________________________
import java.util.*;
import java.lang.*;

public class Kata
{
	public static List<Point> closestPair(List<Point> points) 
  {
      final List<Point> pair = new ArrayList<Point>();
      final List<Point> arr = new ArrayList<>(points);
      arr.sort((a, b) -> Double.valueOf(a.x).compareTo(Double.valueOf(b.x)));
      final int n = points.size();
      double l = Double.valueOf(Integer.MAX_VALUE);
      double tolerance = Math.sqrt(l);
      int a = 0, b = 0;
      for (int i = 0; i + 1 < n; i++) 
      {
          for (int j = i + 1; j < n; j++) 
          {
              if (arr.get(j).x >= arr.get(i).x + tolerance) break;
              final double ls = Math.pow(arr.get(i).x - arr.get(j).x, 2) + Math.pow(arr.get(i).y - arr.get(j).y, 2);
              if (ls < l) 
              {
                  l = ls;
                  tolerance = Math.sqrt(l);
                  a = i;
                  b = j;
              }
          }
      }
      pair.add(arr.get(a));
      pair.add(arr.get(b));
		  return pair;
	}
}
