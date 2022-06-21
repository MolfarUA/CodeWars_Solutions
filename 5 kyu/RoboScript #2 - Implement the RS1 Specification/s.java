5870fa11aa0428da750000da


import java.util.*;
import java.util.regex.*;
import java.util.stream.*;
import java.awt.Point;


public class RoboScript {
    
    final static private int     INF       = Integer.MAX_VALUE-1;
    final static private Point[] DIRS      = {new Point(0,1), new Point(1,0), new Point(0,-1), new Point(-1,0)};
    final static private Pattern TOKENIZER = Pattern.compile("(R+|F+|L+)(\\d*)");
                                 
    
    public static String execute(String code) {
        
        Point      pos   = new Point(0,0);
        int        iDir  = 0;
        Set<Point> seens = new HashSet<>(Arrays.asList(new Point(0,0)));
        Matcher    m     = TOKENIZER.matcher(code);
        
        while (m.find()) {
        
            String cmd = m.group(1);
            char   c   = cmd.charAt(0);
            int    n   = Integer.parseInt(m.group(2).isEmpty() ? "1" : m.group(2)) + cmd.length()-1;
            
            if (c=='F') {
                Point move = DIRS[iDir];
                IntStream.range(1,n+1)
                         .mapToObj( i -> new Point(pos.x+i*move.x, pos.y+i*move.y) )
                         .forEach(seens::add);
                pos.x = pos.x + n*move.x;
                pos.y = pos.y + n*move.y;
                
            } else {
                iDir = (iDir + DIRS.length + n % DIRS.length * (c=='L' ? -1:1)) % DIRS.length;
            }
        }
        return formatOutput(seens);
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
}
__________________________
import java.util.Arrays;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class RoboScript {
    private enum CardinalPoint {
        EAST(1, 1), SOUTH(0, 1), WEST(1, -1), NORTH(0, -1);

        final int axis; // 0 for the ordinate, 1 for the abscissa
        final int change;
        CardinalPoint left;
        CardinalPoint right;

        CardinalPoint(int axis, int change) {
            this.axis = axis;
            this.change = change;
        }

        static {
            for (CardinalPoint cp : values()) {
                int n = cp.ordinal();
                cp.left = values()[(n + 3) % 4];
                cp.right = values()[(n + 1) % 4];
            }
        }
    }

    private final String code;
    private final int[] minPos = new int[2];
    private final int[] maxPos = new int[2];
    private char[][] trace;
    private static final Pattern REPEATING_COMMAND = Pattern.compile("(([FLR])\\2*)(\\d+)?");

    private RoboScript(String code) {
        this.code = code;
    }

    private void follow() {
        int[] pos = new int[2];
        if (trace != null)
            trace[pos[0] = -minPos[0]][pos[1] = -minPos[1]] = '*';
        CardinalPoint direction = CardinalPoint.EAST;
        Matcher m = REPEATING_COMMAND.matcher(code);
        while (m.find()) {
            String sequence = m.group(1);
            int r = sequence.length();
            String repeat = m.group(3);
            if (repeat != null)
                r += Integer.parseInt(repeat) - 1;
            switch (sequence.charAt(0)) {
                case 'F':
                    int axis = direction.axis;
                    int change = direction.change;
                    if (trace == null) {
                        int coord = pos[axis];
                        if (change > 0) {
                            coord += r;
                            if (coord > maxPos[axis])
                                maxPos[axis] = coord;
                        } else {
                            coord -= r;
                            if (coord < minPos[axis])
                                minPos[axis] = coord;
                        }
                        pos[axis] = coord;
                    } else
                        for (int i = 0; i < r; i++) {
                            pos[axis] += change;
                            trace[pos[0]][pos[1]] = '*';
                        }
                    break;
                case 'L':
                    for (int i = 0; i < r; i++)
                        direction = direction.left;
                    break;
                case 'R':
                    for (int i = 0; i < r; i++)
                        direction = direction.right;
                    break;
            }
        }
    }

    private String judgment() {
        follow();
        trace = new char[maxPos[0] - minPos[0] + 1][maxPos[1] - minPos[1] + 1];
        for (char[] row : trace)
            Arrays.fill(row, ' ');
        follow();
        StringBuilder sb = new StringBuilder();
        for (char[] row : trace)
            sb.append(row).append("\r\n");
        sb.delete(sb.length() - 2, sb.length());
        return sb.toString();
    }

    public static String execute(String code) {
        return new RoboScript(code).judgment();
    }
}
__________________________
import java.util.*;

public class RoboScript {
     public static String execute(String code) {
        Tokenizer tokenizer = new Tokenizer(code);
        Executor executor = new Executor();
        Token token;

        while ((token = tokenizer.getNextToken()) != null) {
            executor.execute(token);
        }

        return executor.render();
    }

    enum Direction {
        NORTH(0, 1),
        EAST(1, 0),
        SOUTH(0, -1),
        WEST(-1, 0);

        private final int dx;
        private final int dy;

        Direction(int dx, int dy) {
            this.dx = dx;
            this.dy = dy;
        }
    }
    static class Executor {
        private int minX = 0;
        private int maxX = 0;
        private int minY = 0;
        private int maxY = 0;

        private Direction direction = Direction.EAST;
        private int x = 0;
        private int y = 0;
        private final List<Point> path;

        public Executor() {
            path = new ArrayList<>();
            path.add(new Point(0, 0));
        }

        public void execute(Token token) {
            for (int i = 0; i < token.repeat; i++) {
                switch (token.type) {
                    case 'F' -> moveForward();
                    case 'L' -> turnLeft();
                    case 'R' -> turnRight();
                }
            }
        }

        public String render() {
            int x0 = Math.abs(minX);
            int y0 = Math.abs(minY);
            int w = x0 + maxX + 1;
            int h = y0 + maxY + 1;
            boolean[][] field = new boolean[w][h];

            for (Point point : path) {
                field[x0 + point.x][h - (y0 + point.y) - 1] = true;
            }

            StringBuilder buffer = new StringBuilder();

            for (int j = 0; j < h; j++) {
                for (int i = 0; i < w; i++) {
                    buffer.append(field[i][j] ? '*' : ' ');
                }
                if (j < h - 1) {
                    buffer.append("\r\n");
                }
            }

            return buffer.toString();
        }

        private void moveForward() {
            x += direction.dx;
            y += direction.dy;
            path.add(new Point(x, y));
            if (x > maxX) maxX = x;
            if (x < minX) minX = x;
            if (y > maxY) maxY = y;
            if (y < minY) minY = y;
        }

        private void turnLeft() {
            direction = switch (direction) {
                case NORTH -> Direction.WEST;
                case WEST -> Direction.SOUTH;
                case SOUTH -> Direction.EAST;
                case EAST -> Direction.NORTH;
            };
        }

        private void turnRight() {
            direction = switch (direction) {
                case NORTH -> Direction.EAST;
                case EAST -> Direction.SOUTH;
                case SOUTH -> Direction.WEST;
                case WEST -> Direction.NORTH;
            };
        }
    }

    record Point(int x, int y) {
    }

    static class Tokenizer {
        private final String code;
        private int pos;
        private char currentSymbol;

        public Tokenizer(String code) {
            this.code = code;
            this.pos = 0;
            this.currentSymbol = pos < code.length() ? code.charAt(pos) : 0;
        }

        public Token getNextToken() {
            Token token = tryExtractToken('F');

            if (token == null) {
                token = tryExtractToken('L');
            }

            if (token == null) {
                token = tryExtractToken('R');
            }

            return token;
        }

        private Token tryExtractToken(char type) {
            if (currentSymbol != type) {
                return null;
            }

            int count = 0;
            while (currentSymbol == type) {
                count++;
                next();
            }

            if (Character.isDigit(currentSymbol)) {
                StringBuilder buffer = new StringBuilder();
                while (Character.isDigit(currentSymbol)) {
                    buffer.append(currentSymbol);
                    next();
                }
                count += Integer.parseInt(buffer.toString()) - 1;
            }

            return new Token(type, count);
        }

        private void next() {
            if (pos < code.length() - 1) {
                currentSymbol = code.charAt(++pos);
            } else {
                currentSymbol = 0;
            }
        }
    }

    record Token(char type, int repeat) {
    }
}
