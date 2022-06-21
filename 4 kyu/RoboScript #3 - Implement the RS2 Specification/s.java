58738d518ec3b4bf95000192


import java.util.*;
import java.util.regex.*;
import java.util.stream.*;
import java.awt.Point;


public class RoboScript {
    
    final static private int     INF       = Integer.MAX_VALUE-1;
    final static private Point[] DIRS      = {new Point(0,1), new Point(1,0), new Point(0,-1), new Point(-1,0)};
    final static private Pattern TOKENIZER = Pattern.compile("(R+|F+|L+|[()])(\\d*)");
                                 
    
    public static String execute(String code) {
        
        Point      pos    = new Point(0,0);
        int        iDir   = 0;
        Set<Point> seens  = new HashSet<>(Arrays.asList(new Point(0,0)));
        
        for (Cmd cmd: convertToInstructions(code)) {
            if (cmd.c=='F') {
                Point move = DIRS[iDir];
                IntStream.range(1,cmd.n+1)
                         .mapToObj( n -> new Point(pos.x+n*move.x, pos.y+n*move.y) )
                         .forEach(seens::add);
                pos.x = pos.x + cmd.n*move.x;
                pos.y = pos.y + cmd.n*move.y;
                
            } else {
                iDir = (iDir + DIRS.length + cmd.n % DIRS.length * (cmd.c=='L' ? -1:1)) % DIRS.length;
            }
        }
        return formatOutput(seens);
    }
    
    
    private static List<Cmd> convertToInstructions(String code) {
    
        Stack<List<Cmd>> stk = new Stack<>();
        stk.push(new ArrayList<Cmd>());
        
        Matcher m = TOKENIZER.matcher(code);
        while (m.find()) {
            String cmd = m.group(1);
            char   c   = cmd.charAt(0);
            int    n   = Integer.parseInt(m.group(2).isEmpty() ? "1" : m.group(2));
            switch (c) {
            case '(': stk.push(new ArrayList<Cmd>()); break;
            case ')': enqueueLast(stk, n);            break;
            default:  stk.peek().add( new Cmd(c, n+cmd.length()-1) );
            }
        }
        return stk.peek();
    }
    
    private static void enqueueLast(Stack<List<Cmd>> stk, int nTimes) {
        List<Cmd> lst = stk.pop();
        for (int i=0 ; i<nTimes ; i++) stk.peek().addAll(lst);
    }
    
    
    private static String formatOutput(Set<Point> seens) {
        
        int miX = INF, maX = -INF, miY = INF, maY = -INF;
        for (Point p: seens) {
            if (p.x < miX) miX = p.x;
            if (p.y < miY) miY = p.y;
            if (p.x > maX) maX = p.x;
            if (p.y > maY) maY = p.y;
        }
        final int minX = miX, minY = miY, maxX = maX, maxY = maY;
        return IntStream.range(minX,maxX+1)
                        .mapToObj( x -> IntStream.range(minY, maxY+1)
                                                 .mapToObj( y -> seens.contains(new Point(x,y)) ? "*" : " " )
                                                 .collect(Collectors.joining()) )
                        .collect(Collectors.joining("\r\n"));
    }
    
    //--------------------------
    
    private static class Cmd {
        protected char c;
        protected int  n;
        protected Cmd(char cmd, int i)     { c=cmd; n=i; }
        @Override public String toString() { return String.format("Cmd(%s,%d)", c,n); }
    }
}
__________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class RoboScript {
    
    public static final String INSTRUCTION = "(?<command>[FLR])(?<count>\\d+)?";
  public static final Pattern INSTRUCTION_PATTERN = Pattern.compile(INSTRUCTION);
  public static final Pattern BRACED_PATTERN = Pattern.compile(
      "\\((?<instruction>(" + INSTRUCTION + ")+)\\)(?<repeat>\\d*)");

  enum Heading {
    UP, RIGHT, DOWN, LEFT;

    Heading turn(String turn, int count) {
      count = count % Heading.values().length;
      return switch (turn) {
        case "L" -> getHeading(ordinal() - count);
        case "R" -> getHeading(ordinal() + count);
        default -> throw new IllegalArgumentException("Unknown value: " + turn);
      };
    }

    private Heading getHeading(int ordinal) {
      return Heading.values()[(ordinal + Heading.values().length) % Heading.values().length];
    }
  }

  record Position(int x, int y) {
    Position move(Heading heading) {
      return switch (heading) {
        case UP -> new Position(this.x() - 1, this.y());
        case RIGHT -> new Position(this.x(), this.y() + 1);
        case DOWN -> new Position(this.x() + 1, this.y());
        case LEFT -> new Position(this.x(), this.y() - 1);
      };
    }
  }


  public static String execute(String code) {
    code = replaceBraces(code);

    Position startPosition = new Position(0, 0);
    Heading heading = Heading.RIGHT;


    List<Position> path = executeCode(code, startPosition, heading);

    return drawToMap(path);
  }

  private static String replaceBraces(String code) {
    while (true) {
      Matcher matcher = BRACED_PATTERN.matcher(code);
      if (!matcher.find()) return code;
      String instruction = matcher.group("instruction");
      String repeatString = matcher.group("repeat");
      int count = repeatString.isEmpty() ? 1 : Integer.parseInt(repeatString);
      String replacement = IntStream.range(0, count).mapToObj(i -> instruction).collect(Collectors.joining());
      code = matcher.replaceFirst(replacement);
    }
  }

  private static String drawToMap(List<Position> path) {
    List<Position> shiftedPath = shiftToPositiveCoordinates(path);
    char[][] map = prepareBlankMap(shiftedPath);
    drawPath(map, shiftedPath);
    return toString(map);
  }

  private static String toString(char[][] map) {
    return Stream.of(map).map(String::valueOf).collect(Collectors.joining("\r\n"));
  }

  private static void drawPath(char[][] map, List<Position> path) {
    for (Position pos : path) {
      map[pos.x()][pos.y()] = '*';
    }
  }

  private static char[][] prepareBlankMap(List<Position> path) {
    int rows = path.stream().mapToInt(Position::x).max().orElseThrow() + 1;
    int columns = path.stream().mapToInt(Position::y).max().orElseThrow() + 1;

    char[][] map = new char[rows][columns];
    for (char[] row : map) {
      Arrays.fill(row, ' ');
    }
    return map;
  }

  private static List<Position> shiftToPositiveCoordinates(List<Position> path) {
    int xMin = path.stream().mapToInt(Position::x).min().orElseThrow();
    int yMin = path.stream().mapToInt(Position::y).min().orElseThrow();
    return path.stream().map(pos -> new Position(pos.x() - xMin, pos.y() - yMin)).toList();
  }

  private static List<Position> executeCode(String code, Position currentPosition, Heading heading) {
    List<Position> path = new ArrayList<>();
    path.add(currentPosition);


    Matcher matcher = INSTRUCTION_PATTERN.matcher(code);
    while (matcher.find()) {
      String command = matcher.group("command");
      String countString = matcher.group("count");
      int count = Objects.isNull(countString) ? 1 : Integer.parseInt(countString);
      switch (command) {
        case "L", "R" -> heading = heading.turn(command, count);
        case "F" -> currentPosition = moveAndAddToPath(currentPosition, heading, count, path);
      }
    }
    return path;
  }

  private static Position moveAndAddToPath(Position currentPosition, Heading heading, int count,
                                           List<Position> path) {
    for (int i = 0; i < count; i++) {
      currentPosition = currentPosition.move(heading);
      path.add(currentPosition);
    }
    return currentPosition;
  }
}
__________________________
import java.util.*;
import java.util.stream.*;
import java.util.Map.Entry;

public class RoboScript {
    
  public static String execute(String code) {
    Map<Integer, Set<Integer>> map = new HashMap<>();
    Set<Integer> initial = new HashSet<>();
    initial.add(0);
    map.put(0, initial);

    IntPair pos = new IntPair(0, 0);
    IntPair dir = new IntPair(1, 0);

    Step step = parse(code);
    step.run(pos, dir, map);

    // Render
    int min = map.values().stream().flatMapToInt(val -> val.stream().mapToInt(i -> i)).min().orElse(0);
    int max = map.values().stream().flatMapToInt(val -> val.stream().mapToInt(i -> i)).max().orElse(0);
    int dist = max - min + 1;
    return map.entrySet().stream().sorted(Comparator.comparing(ent -> -ent.getKey())).map(Entry::getValue).map(line -> renderLine(min, dist, line)).collect(Collectors.joining("\r\n"));
  }
  
  public static String renderLine(int offset, int length, Set<Integer> entries) {
    StringBuilder builder = new StringBuilder(length);
    for (int i = 0; i < length; i++) {
      builder.append(entries.contains(offset + i) ? '*' : ' ');
    }
    return builder.toString();
  }

  static ActionGroup parse(String code) {
    ActionGroup root = new ActionGroup(1);
    
    int i = 0;
    while (i < code.length()) {
      char c = code.charAt(i++);

      Step step;
      if (c == '(') {
        int brackets = 1;
        int end = i;
        while (brackets > 0) {
            if (code.charAt(end) == '(') brackets++;
            else if (code.charAt(end) == ')') brackets--;
            ++end;
        }
        step = parse(code.substring(i, end - 1));
        i = end;
      } else {
        step = new Action(1, c);
      }
      char numChar;
//       String repStr = code.drop(i).takeWhile{it.isDigit()}
      String repStr = "";
      while (i < code.length() && Character.isDigit(numChar = code.charAt(i))) {
        repStr += numChar;
        i++;
      }
      if (!repStr.isEmpty()) step.repetitions = Integer.parseInt(repStr);
      root.steps.add(step);
    }
    
    return root;
  }

  static class IntPair {

    int first;
    int second;

    IntPair(int first, int second) {
      this.first = first;
      this.second = second;
    }

    void add(IntPair other) {
        first += other.first;
        second += other.second;
    }
  }

  static abstract class Step {
    
    int repetitions;
    
    Step(int repetitions) {
      this.repetitions = repetitions;
    }
    
    void run(IntPair pos, IntPair dir, Map<Integer, Set<Integer>> map) {
      for (int i = 0; i < repetitions; i++) {
        go(pos, dir, map);
      }
    }
    protected abstract void go(IntPair pos, IntPair dir, Map<Integer, Set<Integer>> map);
  }

  static class Action extends Step {
    
    char action;
    
    Action(int repetitions, char action) {
      super(repetitions);
      this.action = action;
    }
    
    protected void go(IntPair pos, IntPair dir, Map<Integer, Set<Integer>> map) {
      switch (action) {
        case 'F':
          pos.add(dir);
          map.computeIfAbsent(pos.second, k -> new HashSet<>()).add(pos.first);
          break;
        case 'L':
          int first = dir.first;
          dir.first = -dir.second;
          dir.second = first;
          break;
        case 'R':
          first = dir.first;
          dir.first = dir.second;
          dir.second = -first;
          break;
      }
    }
  }

  static class ActionGroup extends Step {
    
    ActionGroup(int repetitions) {
      super(repetitions);
    }
    
    List<Step> steps = new ArrayList<>();

    protected void go(IntPair pos, IntPair dir, Map<Integer, Set<Integer>> map) {
      for (Step step : steps) {
        step.run(pos, dir, map);
      }
    }
  }
}
