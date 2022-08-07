576986639772456f6f00030c


import java.util.Arrays;
import java.util.EnumSet;
import java.util.HashSet;
import java.util.Set;
import java.util.stream.Stream;

public class Finder {

    private final int n;
    private final int[][] hills;

    static int pathFinder(final String area) {
        final Finder finder = new Finder(area);
        return finder.climbRounds(new Position(0,0), new Position(finder.n - 1, finder.n - 1));
    }

    public Finder(final String area) {
        n = Math.max(area.indexOf('\n'), 1);
        hills = parse(area);
    }

    private int[][] parse(final String area) {
        final int[][] field = new int[n][n];
        final String[] rows = area.split("\n");
        for (int y = 0; y < n; y++) {
            final String row = rows[y];
            for (int x = 0; x < n; x++) {
                field[y][x] = Character.getNumericValue(row.charAt(x));
            }
        }
        return field;
    }

    int climbRounds(final Position s, final Position t) {
        final int[][] climbRounds = initSquareArea(n, Integer.MAX_VALUE);
        climbRounds[s.y][s.x] = 0;
        final Set<Position> nextVisits = new HashSet<>();
        nextVisits.add(s);
        while (!nextVisits.isEmpty()) {
            final Set<Position> lastVisits = new HashSet<>(nextVisits);
            nextVisits.clear();
            for (final Position source : lastVisits) {
                mooreNeighborsInArea(source).forEach(target -> {
                    final int newTotalClimbRounds = climbRounds[source.y][source.x] + Math.abs(hills[source.y][source.x] - hills[target.y][target.x]);
                    if (newTotalClimbRounds < climbRounds[target.y][target.x]) {
                        climbRounds[target.y][target.x] = newTotalClimbRounds;
                        nextVisits.add(target);
                    }
                });
            }
        }
        return climbRounds[t.y][t.x];
    }

    private static int[][] initSquareArea(final int size, final int value) {
        final int[][] area = new int[size][size];
        for (final int[] row : area) {
            Arrays.fill(row, value);
        }
        return area;
    }

    public Stream<Position> mooreNeighborsInArea(final Position position) {
        return Direction.all().map(position::toDirection).filter(pos -> pos.isInBounds(n, n));
    }

    public enum Direction {

        N(0, -1), E(1, 0), S(0, 1), W(-1, 0);

        private final int dx;
        private final int dy;

        Direction(final int dx, final int dy) {
            this.dx = dx;
            this.dy = dy;
        }

        public Position of(final Position position) {
            return new Position(position.x + dx, position.y + dy);
        }

        public static Stream<Direction> all() {
            return EnumSet.allOf(Direction.class).stream();
        }
    }

    public static class Position {

        public int x;
        public int y;

        public Position(final int x, final int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(final Object o) {
            return this == o || (o instanceof Position && x == ((Position) o).x && y == ((Position) o).y);
        }

        @Override
        public int hashCode() {
            int result = x;
            result = 31 * result + y;
            return result;
        }

        public Position toDirection(final Direction direction) {
            return direction.of(this);
        }

        public boolean isInBounds(final int width, final int height) {
            return x >= 0 && y >= 0 && x < width && y < height;
        }

        @Override
        public String toString() {
            return "[" + x + "," + y + "]";
        }
    }
}
_____________________________
import java.awt.*;
import java.util.LinkedList;

public class Finder {
    private static int[][] costs, fillMap;
    private static LinkedList<Point> buffer;

    public static int pathFinder(String maze) {
        init(maze);
        while (buffer.size() > 0){
            Point point = buffer.pollFirst();
            if (point.x > 0)
                push(new Point(point.x-1, point.y), fillMap[point.x][point.y] + Math.abs(costs[point.x][point.y] - costs[point.x-1][point.y]));
            if (point.x < fillMap.length-1)
                push(new Point(point.x+1, point.y), fillMap[point.x][point.y] + Math.abs(costs[point.x][point.y] - costs[point.x+1][point.y]));
            if (point.y > 0)
                push(new Point(point.x, point.y-1), fillMap[point.x][point.y] + Math.abs(costs[point.x][point.y] - costs[point.x][point.y-1]));
            if (point.y < fillMap.length-1)
                push(new Point(point.x, point.y+1), fillMap[point.x][point.y] + Math.abs(costs[point.x][point.y] - costs[point.x][point.y+1]));
        }
        return fillMap[costs.length - 1][costs.length - 1];
    }

    private static void init(String maze){
        String[] lines = maze.split("\n");
        costs = new int[lines.length][lines.length];
        fillMap = new int[lines.length][lines.length];
        for(int i=0; i<lines.length; i++)
            for(int j=0; j<lines.length; j++) {
                costs[i][j] = Integer.parseInt(lines[i].substring(j, j+1));
                fillMap[i][j] = Integer.MAX_VALUE;
            }
        buffer = new LinkedList<>();
        push(new Point(0, 0), 0);
    }

    private static void push(Point point,int n) {
        if (fillMap[point.x][point.y] <= n)
            return;
        fillMap[point.x][point.y] = n;
        buffer.add(point);
    }
}
_____________________________
import java.util.Comparator;
import java.util.PriorityQueue;

public class Finder {

  static int pathFinder(String str) {
    char[][] maze;
    int n;
    PriorityQueue<int[]> queue = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
    String[] strings = str.split("\n");
    n = strings.length;
    maze = new char[n][n];
    int[][] weights = new int[n][n];
    for (int i = 0; i < n; i++) {
      maze[i] = strings[i].toCharArray();
      for (int j = 0; j < n; j++)   weights[i][j] = Integer.MAX_VALUE;
    }
    weights[0][0] = 0;
    int[] tmp = {0, 0, 0};
    queue.add(tmp);
    int i, j, w;
    while (true) {
      tmp = queue.poll();
      w = tmp[0]; i = tmp[1]; j = tmp[2];
      if (i == n - 1 && j == n - 1) return w;
      for (int ii = 1; ii >= -1; ii--)
        for (int jj = 1; jj >= -1; jj--) {
          if (ii * jj != 0) continue; //without diagonals
          int ni = i + ii, nj = j + jj;
          if (ni < 0 || ni >= n || nj < 0 || nj >= n) continue; //borders
          if (ii == 0 && jj == 0) continue;
          int nw = w + Math.abs(maze[i][j] - maze[ni][nj]);
          if (nw < weights[ni][nj]) {
            int[] tmp1 = new int[3];
            weights[ni][nj] = nw;
            tmp1[0] = nw;
            tmp1[1] = ni;
            tmp1[2] = nj;
            queue.add(tmp1);
          }
        }
    }
  }
}
