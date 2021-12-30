import java.util.*;

public class Go {
    private static class Move {
        // All integers correspond to indices of the board array (see below).
        final int placed;
        final List<Integer> captured;

        Move(int placed, List<Integer> captured) {
            this.placed = placed;
            this.captured = captured;
        }
    }

    private final int height;
    private final int width;
    // Board is indexed from top to bottom row and from left to right point in each row.
    // Values is this array are 0, 1, 2 (see constants below).
    private final int[] board;
    private static final int EMPTY_POINT = 0;
    private static final int BLACK_STONE = 1;
    private static final int WHITE_STONE = 2;
    private final int[][] adjacent;
    private boolean handicapPlaced;
    private boolean whiteTurn;
    private final Stack<Move> history = new Stack<>();

    public Go(int size) {
        this(size, size);
    }

    public Go(int height, int width) {
        if (height <= 0)
            throw new IllegalArgumentException("Wrong height: " + height);
        this.height = height;
        if (width <= 0 || width > 25)
            throw new IllegalArgumentException("Wrong width: " + width);
        this.width = width;
        int area = height * width;
        board = new int[area];
        adjacent = new int[area][];
        int i = 0;
        int[] adj = new int[4];
        for (int y = 0; y < height; y++)
            for (int x = 0; x < width; x++) {
                int k = 0;
                if (y > 0)
                    adj[k++] = i - width;
                if (y < height - 1)
                    adj[k++] = i + width;
                if (x > 0)
                    adj[k++] = i - 1;
                if (x < width - 1)
                    adj[k++] = i + 1;
                adjacent[i++] = Arrays.copyOf(adj, k);
            }
    }

    private static final Map<Integer, int[]> HANDICAPS = new HashMap<>();
    static {
        int[] sizes = { 9, 13, 19 };
        int[][][] coordinates = { { { 2, 6 }, { 6, 2 }, { 6, 6 }, { 2, 2 }, { 4, 4 } },
            { { 3, 9 }, { 9, 3 }, { 9, 9 }, { 3, 3 }, { 6, 6 }, { 6, 3 }, { 6, 9 }, { 3, 6 }, { 9, 6 } },
            { { 3, 15 }, { 15, 3 }, { 15, 15 }, { 3, 3 }, { 9, 9 }, { 9, 3 }, { 9, 15 }, { 3, 9 }, { 15, 9 } } };
        for (int i = 0; i < sizes.length; i++) {
            int size = sizes[i];
            int[][] hCoords = coordinates[i];
            int hCount = hCoords.length;
            int[] hStones = new int[hCount];
            for (int j = 0; j < hCount; j++)
                hStones[j] = hCoords[j][0] * size + hCoords[j][1];
            HANDICAPS.put(size, hStones);
        }
    }

    public void handicapStones(int count) {
        if (handicapPlaced || !history.isEmpty())
            throw new IllegalArgumentException(
                    "Handicap has already been placed or some moves have been made");
        int[] hStones = HANDICAPS.get(height);
        if (height != width || hStones == null)
            throw new IllegalArgumentException("Handicap is unavailable for this board");
        if (count <= 0 || count > hStones.length)
            throw new IllegalArgumentException("Wrong number of handicap stones: " + count);
        for (int i = 0; i < count; i++)
            board[hStones[i]] = BLACK_STONE;
        handicapPlaced = true;
    }

    public Map<String, Integer> getSize() {
        Map<String, Integer> result = new HashMap<>(2);
        result.put("height", height);
        result.put("width", width);
        return result;
    }

    private static final char[] STONE_CHARS = { '.', 'x', 'o' };

    public char[][] getBoard() {
        char[][] result = new char[height][width];
        int i = 0;
        for (char[] row : result)
            for (int j = 0; j < width; j++)
                row[j] = STONE_CHARS[board[i++]];
        return result;
    }

    private int strPointToInt(String point) {
        int n = point.length() - 1;
        if (n < 1)
            return -1;
        int y;
        try {
            y = height - Integer.parseInt(point.substring(0, n));
        } catch (NumberFormatException e) {
            return -1;
        }
        char c = point.charAt(n);
        int x = c - 'A';
        if (c > 'I')
            x--;
        return (c == 'I' || x < 0 || x >= width || y < 0 || y >= height) ? -1 : y * width + x;
    }

    public String getPosition(String point) {
        int index = strPointToInt(point);
        if (index < 0)
            throw new IllegalArgumentException("Invalid point: " + point);
        return Character.toString(STONE_CHARS[board[index]]);
    }

    public String getTurn() {
        return whiteTurn ? "white" : "black";
    }

    private List<Integer> getCaptured(int color, boolean removeFromBoard) {
        int area = board.length;
        int[] libBoard = board.clone();
        Queue<Integer> queue = new ArrayDeque<>(area);
        List<Integer> innerColored = new ArrayList<>(area);
        for (int i = 0; i < area; i++)
            if (board[i] == color) {
                boolean liberated = false;
                for (int a : adjacent[i])
                    if (libBoard[a] == EMPTY_POINT) {
                        liberated = true;
                        break;
                    }
                if (liberated) {
                    libBoard[i] = EMPTY_POINT;
                    queue.add(i);
                } else
                    innerColored.add(i);
            }
        int captured = innerColored.size();
        while (captured > 0) {
            Integer i = queue.poll();
            if (i == null)
                break;
            for (int a : adjacent[i])
                if (libBoard[a] == color) {
                    libBoard[a] = EMPTY_POINT;
                    queue.add(a);
                    captured--;
                }
        }
        List<Integer> result = new ArrayList<>(captured);
        if (captured > 0) {
            for (int i : innerColored)
                if (libBoard[i] != EMPTY_POINT)
                    result.add(i);
            if (removeFromBoard)
                for (int point : result)
                    board[point] = EMPTY_POINT;
        }
        return result;
    }

    private static boolean cancelOut(int placed, List<Integer> captured) {
        return captured.size() == 1 && placed == captured.get(0);
    }

    private void move(String point) {
        int placed = strPointToInt(point);
        if (placed < 0 || board[placed] != EMPTY_POINT)
            throw new IllegalArgumentException(
                    (placed < 0 ? "Invalid" : "Already occupied") + " point: " + point);
        int playerStone = whiteTurn ? WHITE_STONE : BLACK_STONE;
        int opponentStone = whiteTurn ? BLACK_STONE : WHITE_STONE;
        board[placed] = playerStone;
        List<Integer> captured = getCaptured(opponentStone, true);
        Move prevMove = history.isEmpty() ? null : history.peek();
        history.add(new Move(placed, captured));
        whiteTurn ^= true;
        if (captured.isEmpty()) {
            if (!getCaptured(playerStone, false).isEmpty()) {
                rollBack();
                throw new IllegalArgumentException("Suicide is illegal");
            }
        } else if (prevMove != null && cancelOut(placed, prevMove.captured)
                && cancelOut(prevMove.placed, captured)) {
            rollBack();
            throw new IllegalArgumentException("Ko!");
        }
    }

    public void move(String... moves) {
        for (String point : moves)
            move(point);
    }

    public void passTurn() {
        history.push(null);
        whiteTurn ^= true;
    }

    private void rollBack() {
        whiteTurn ^= true;
        Move move = history.pop();
        if (move != null) {
            int opponentStone = whiteTurn ? BLACK_STONE : WHITE_STONE;
            for (int pos : move.captured)
                board[pos] = opponentStone;
            board[move.placed] = EMPTY_POINT;
        }
    }

    public void rollBack(int turns) {
        if (turns <= 0 || turns > history.size())
            throw new IllegalArgumentException("Wrong number of turns to roll back: " + turns);
        do
            rollBack();
        while (--turns > 0);
    }

    public void reset() {
        Arrays.fill(board, EMPTY_POINT);
        handicapPlaced = false;
        whiteTurn = false;
        history.clear();
    }
}

____________________________________________________________
import java.util.*;
import java.util.stream.*;
import java.awt.Point;

public class Go {
        
    final private static Point[] MOVES   = {new Point(1,0), new Point(-1,0), new Point(0,1), new Point(0,-1)};
    final private static char[]  SYMBOLS = {'x', 'o'};
    
    final private static Map<Point,String[]> HANDICAP = new HashMap<Point,String[]>() {{
        put(new Point( 9, 9), new String[] {"7G",  "3C", "3G", "7C",  "5E"});
        put(new Point(13,13), new String[] {"10K", "4D", "4K", "10D", "7G",  "7D",  "7K",  "10G", "4G"});
        put(new Point(19,19), new String[] {"16Q", "4D", "4Q", "16D", "10K", "10D", "10Q", "16K", "4K"});
    }};
    
    private int lenX, lenY, p;
    private char[][] board;
    private Map<String,Point> posConverter;
    private Stack<char[][]> archive;
    private boolean hasHandi;
    
    
    public Go(int... size) {
        if (Arrays.stream(size).anyMatch( s -> s<0 || s>25 )) throw new IllegalArgumentException("Wrong size of Board: "+lenX+", "+lenY);
        
        lenX = size[0];
        lenY = size.length ==2 ? size[1] : lenX;
        posConverter  = new HashMap<String,Point>() {{
            for (int i = 1 ; i < lenX+1 ; i++) for (int j = 0 ; j < lenY ; j++) 
                put(""+i + (char) (65+j + (j>7 ? 1:0)), new Point(lenX-i, j) );
        }};
        initializer(this, lenX, lenY);
    }
    
    public Map<String,Integer> getSize()      { return new HashMap<String,Integer>() {{ put("height", lenX);  put("width", lenY); }}; }
    public String              getTurn()      { return p == 0 ? "black" : "white"; }
    public char[][]            getBoard()     { return board; }
    public void                reset()        { initializer(this, lenX, lenY); }
    
    public char getPosition(String pos) { 
        if (!posConverter.containsKey(pos)) throw new IllegalArgumentException("Invalid position");
        Point pt = posConverter.get(pos);
        return board[pt.x][pt.y];
    }
    
    public void passTurn() {
        archiveBoard();
        updatePlayer();
    }
    
    public void rollBack(int n) {
        for (int i = 0 ; i < n ; i++) {
            board = archive.pop();
            updatePlayer();
        }
    }
    
    public void handicapStones(int n) {
        if (archive.size() != 0 || p != 0 || hasHandi)
            throw new IllegalArgumentException("Cannot initiate handicap stones if not at the beginning of the game");
        
        hasHandi = true;
        Point key = new Point(lenX,lenY);
        if (!HANDICAP.containsKey(key) || n < 1 || n > HANDICAP.get(key).length)
            throw new IllegalArgumentException("Cannot initiate handicap stones: wrong size of the board or wrong number of stones asked for");
        
        int i = 0;
        for (String posStr: HANDICAP.get(key)) { i++;
            Point pt = posConverter.get(posStr);
            board[pt.x][pt.y] = SYMBOLS[p];
            if (i == n) break;
        }
    }
    
    
    public void move(String... moves) {
        
        for (String m: moves) {
            if (!posConverter.containsKey(m)) throw new IllegalArgumentException("Invalid move: " + m);
            
            final Point pt     = posConverter.get(m);
            final char  player = SYMBOLS[p],
                        opp    = SYMBOLS[p^1];
            
            if (board[pt.x][pt.y] != '.')     throw new IllegalArgumentException("Invalid move: " + m + ". Stone already present at this position.");
            

            archiveBoard();
            board[pt.x][pt.y] = player;
            
            List<Point> seedAround = Arrays.stream(MOVES)
                                           .map( dp -> new Point(pt.x+dp.x, pt.y+dp.y) )
                                           .filter( neigh ->    0 <= neigh.x && neigh.x < lenX
                                                             && 0 <= neigh.y && neigh.y < lenY
                                                             && board[neigh.x][neigh.y] != '.'  )
                                           .collect(Collectors.toList());
            seedAround.add(pt);
            
            Map<Character, Stack<Set<Point>>> grpsAround = new HashMap<Character, Stack<Set<Point>>>();
            Map<Character, Stack<Integer>>    libsAround = new HashMap<Character, Stack<Integer>>();
            for (char c: SYMBOLS) {
                grpsAround.put(c, new Stack<Set<Point>>());
                libsAround.put(c, new Stack<Integer>());
            }
            
            for (Point seed: seedAround) {
                final char c = board[seed.x][seed.y];
                if (grpsAround.get(c).stream().allMatch( grp -> !grp.contains(seed) )) {
                    grpsAround.get(c).push(new HashSet<Point>());
                    floodLib(seed, c, grpsAround.get(c).peek(), libsAround.get(c));
                }
            }
            
            boolean isSuicidal  = libsAround.get(player).peek() == 0,
                    isCapturing = libsAround.get(opp).stream().anyMatch(lib -> lib == 0 );
            if (isSuicidal && !isCapturing) {
                rollInvalidMove_Raise("Invalid move: suicide!");
            }
            
            while (!libsAround.get(opp).empty()) {
                Set<Point> grp = grpsAround.get(opp).pop();
                int        lib = libsAround.get(opp).pop();
                
                if (lib == 0) {
                    grp.forEach( g -> board[g.x][g.y] = '.');
                    if (grp.size() == 1
                            && archive.size() > 2
                            && Arrays.deepEquals(board, archive.get(archive.size()-2))) {
                        rollInvalidMove_Raise("Invalid move: ko rule!");
                    }   
                }
            }
            
            updatePlayer();
        }
    }

    
    private void updatePlayer() { p ^= 1; }

    private static void initializer(Go obj, int lenX, int lenY) {
        obj.p        = 0;
        obj.board    = new char[lenX][lenY];
        obj.archive  = new Stack<char[][]>();
        obj.hasHandi = false;
        for (int x = 0 ; x < lenX ; x++) for (int y = 0 ; y < lenY ; y++) obj.board[x][y] = '.';
        //obj.archiveBoard();
    }
    
    private void archiveBoard() {
        archive.push(Arrays.stream(board)
                           .map( line -> Arrays.copyOf(line, lenY) )
                           .toArray(char[][]::new));
    }
    
    private void rollInvalidMove_Raise(String msg) {
        rollBack(1);
        updatePlayer();
        throw new IllegalArgumentException(msg);
    }


    private void floodLib(Point seed, final char c, Set<Point> grpSet, Stack<Integer> libStk) {         // WARNING: mutate grpSet and libStk during the executions
        
        Set<Point> seens = new HashSet<Point>() {{ add(seed); }},
                   q     = new HashSet<Point>() {{ add(seed); }};
        
        grpSet.add(seed);
        int[] lib = {0};
        
        while (!q.isEmpty()) {
            
            Point pt = q.stream().findAny().get();
            q.remove(pt);
            
            Arrays.stream(MOVES)
                  .map(    dp    -> new Point(pt.x+dp.x, pt.y+dp.y) )
                  .filter( neigh ->   0 <= neigh.x && neigh.x < lenX
                                   && 0 <= neigh.y && neigh.y < lenY
                                   && !seens.contains(neigh) )
                  .forEach(neigh -> { if      (board[neigh.x][neigh.y] == '.')   lib[0] += 1;
                                      else if (board[neigh.x][neigh.y] ==  c ) { grpSet.add(neigh); q.add(neigh); }
                                      seens.add(neigh);
                                    });
        }
        libStk.push(lib[0]);
    }
}

____________________________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Go {

    private static final char EMPTY_SQUARE = '.';
    private static final char BLACK_STONE = 'x';
    private static final char WHITE_STONE = 'o';
    private static final char OUTSIDE_SQUARE = ' ';
    private static final Pattern COORDS = Pattern.compile("(\\d+)([A-Za-z]+)");
    private static final String COLUMN_LABELS = "ABCDEFGHJKLMNOPQRSTUVWXYZ";
    private static final String[] STONE_NAMES = {"black", "white"};
    private static final int[][] DIRS = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    final int width;
    final int height;
    final long[] black;
    final long[] white;
    final long[][] both;
    final long[][][] lastTwo = new long[2][][]; // for KO checking
    final List<String> journal;
    int turn;

    public Go(int width) {
        this(width, width);
    }

    public Go(int height, int width) {
        this.width = width;
        this.height = height;
        if (width < 1 || height < 1 || width > COLUMN_LABELS.length() || height > 31) {
            throw new IllegalArgumentException("invalid board size " + width + "x" + height);
        }
        black = new long[height];
        white = new long[height];
        both = new long[][]{black, white};
        journal = new ArrayList<>();
    }

    public Map<String, Integer> getSize() {
        return new HashMap<String, Integer>() {{
            put("height", height);
            put("width", width);
        }};
    }

    private static int[][] handicapCoords(int width) {
        switch (width) {
            case 9:
                return new int[][]{{6, 6}, {2, 2}, {6, 2}, {2, 6}, {4, 4}};
            case 13:
                return new int[][]{{9, 9}, {3, 3}, {9, 3}, {3, 9}, {6, 6}, {3, 6}, {9, 6}, {6, 9}, {6, 3}};
            case 19:
                return new int[][]{{15, 15}, {3, 3}, {15, 3}, {3, 15}, {9, 9}, {3, 9}, {15, 9}, {9, 15}, {9, 3}};
            default:
                throw new IllegalArgumentException("handicaps not permitted for board dimension " + width + "x" + width);
        }
    }

    public void reset() {
        Arrays.fill(white, 0);
        Arrays.fill(black, 0);
        Arrays.fill(lastTwo, new long[0][0]);
        turn = 0;
        journal.clear();
    }

    public String getTurn() {
        return STONE_NAMES[turn % 2];
    }

    public void handicapStones(int handicaps) {
        if (handicaps == 0) {
            return;
        } else if (width != height) {
            throw new IllegalArgumentException("handicaps not permitted for non-square-boards");
        } else if (turn != 0) {
            throw new IllegalArgumentException("handicaps not permitted after game has started");
        }
        int[][] hpts = handicapCoords(width);
        if (handicaps < 0 || handicaps > hpts.length) {
            throw new IllegalArgumentException("handicaps=" + handicaps + ", allowed=0.." + hpts.length);
        }
        for (int h = 0; h < hpts.length && h < handicaps; ++h) {
            int[] hpt = hpts[h];
            turn = 0;
            move(hpt[0], hpt[1]);
        }
        journal.add("H" + handicaps);
    }

    private long toIdx(int column, int row) {
        return row * width + column;
    }

    private boolean hasLiberties(int column, int row) {
        char t = getAtPos(column, row);
        if (t == EMPTY_SQUARE) {
            return true;
        } else {
            return hasLiberties(t, column, row, new HashSet<>());
        }
    }

    private boolean hasLiberties(char t, int column, int row, Set<Long> checked) {
        if (!checked.add(toIdx(column, row))) {
            return false;
        }
        for (int[] d : DIRS) {
            char neib = getAtPos(column + d[0], row + d[1]);
            if (neib == EMPTY_SQUARE
                    || neib == t && hasLiberties(t, column + d[0], row + d[1], checked)) {
                return true;
            }
        }
        return false;
    }

    private void clearGroup(Set<Long> found, int column, int row) {
        for (Long idx : found) {
            int r = (int) (idx / width);
            int c = (int) (idx % width);
            long bsel = 1L << c;
            black[r] &= ~bsel;
            white[r] &= ~bsel;
        }
        if (Arrays.equals(black, lastTwo[0][0]) && Arrays.equals(white, lastTwo[0][1])) {
            undoCurrent();
            throw new IllegalArgumentException("KO detected in attempted move-"
                    + (journal.size() + 1) + " at " + toCoords(column, row));
        }
    }

    private void findCaptureGroup(int column, int row, Set<Long> found) {
        char t = getAtPos(column, row);
        findGroup(t, column, row, found);
    }

    private void findGroup(char t, int column, int row, Set<Long> found) {
        if (found.add(toIdx(column, row))) {
            for (int[] d : DIRS) {
                char neib = getAtPos(column + d[0], row + d[1]);
                if (neib == t) {
                    findGroup(t, column + d[0], row + d[1], found);
                }
            }
        }
    }

    public void passTurn() {
        ++turn;
        journal.add("-");
    }

    private boolean onBoard(int column, int row) {
        return column >= 0 && column < width && row >= 0 && row < height;
    }

    private boolean move(int column, int row) {
        if (!onBoard(column, row)) {
            throw new IllegalArgumentException("position " + toCoords(column, row)
                    + " out of bounds for " + width + "x" + height + " board");
        }
        long bsel = 1L << column;
        if (((black[row] | white[row]) & bsel) != 0) {
            throw new IllegalArgumentException("Cell already occupied at "
                    + toCoords(column, row) + " in move-" + (journal.size() + 1));
        }
        both[turn % 2][row] |= bsel;
        char opponent = turn % 2 == 0 ? WHITE_STONE : BLACK_STONE;
        Set<Long> found = new HashSet<>();
        for (int[] d : DIRS) {
            int c = column + d[0];
            int r = row + d[1];
            if (onBoard(c, r) && getAtPos(c, r) == opponent && !hasLiberties(c, r)) {
                findCaptureGroup(c, r, found);
            }
        }
        boolean tookPrisoners = !found.isEmpty();
        if (tookPrisoners) {
            clearGroup(found, row, column);
        }
        if (!hasLiberties(column, row)) {
            undoCurrent();
            throw new IllegalArgumentException("illegal suicide move at "
                    + toCoords(column, row) + " in move-" + (journal.size() + 1));
        }
        lastTwo[0] = lastTwo[1];
        lastTwo[1] = new long[][]{Arrays.copyOf(black, height), Arrays.copyOf(white, height)};
        ++turn;
        return tookPrisoners;
    }

    private String toCoords(int column, int row) {
        return Integer.toString(row + 1) + (char) ('A' + column);
    }

    private static int[] parseCoords(String coords) {
        Matcher m = COORDS.matcher(coords);
        if (m.matches()) {
            int row = Integer.parseInt(m.group(1)) - 1;
            int col = COLUMN_LABELS.indexOf(m.group(2));
            return new int[]{col, row};
        }
        return null;
    }

    public void move(String... coords) {
        if (coords.length == 1 && coords[0].indexOf(',') > 0) {
            coords = coords[0].split(", ");
        }
        for (String c : coords) {
            oneMove(c);
        }
    }

    public void oneMove(String coords) {
        if ("pass".equalsIgnoreCase(coords) || "-".equalsIgnoreCase(coords)) {
            passTurn();
        } else if (coords.startsWith("H")) {
            handicapStones(Integer.parseInt(coords.substring(1)));
        } else {
            int[] pt = parseCoords(coords);
            if (pt != null) {
                move(pt[0], pt[1]);
                journal.add(coords);
            } else {
                throw new IllegalArgumentException("Invalid move " + coords);
            }
        }
    }

    public void rollBack(int turnCount) {
        if (turnCount > journal.size()) {
            throw new IllegalArgumentException("turnCount exceeds number of recorded turns");
        } else if (turnCount > 0) {
            List<String> replay = new ArrayList<>(journal.subList(0, journal.size() - turnCount));
            reset();
            for (String mv : replay) {
                move(mv);
            }
        }
    }

    private void undoCurrent() {
        System.arraycopy(lastTwo[1][0], 0, black, 0, height);
        System.arraycopy(lastTwo[1][1], 0, white, 0, height);
    }

    public char getPosition(String coords) {
        int[] pt = parseCoords(coords);
        if (pt != null) {
            return getAtPos(pt[0], pt[1]);
        }
        throw new IllegalArgumentException("Invalid coordinates " + coords);
    }

    public char getAtPos(int column, int row) {
        if (!onBoard(column, row)) {
            return OUTSIDE_SQUARE;
        }
        long bsel = 1L << column;
        if ((black[row] & bsel) != 0) {
            return BLACK_STONE;
        } else if ((white[row] & bsel) != 0) {
            return WHITE_STONE;
        }
        return EMPTY_SQUARE;
    }

    public char[][] getBoard() {
        char[][] board = new char[height][width];
        for (int r = 0; r < height; ++r) {
            for (int c = 0; c < width; ++c) {
                board[height - 1 - r][c] = getAtPos(c, r);
            }
        }
        return board;
    }

    public void printColumnLabels(int width) {
        System.out.print("  ");
        for (int i = 0; i < width; ++i) {
            System.out.print(" " + COLUMN_LABELS.charAt(i));
        }
        System.out.println();
    }

    public void printBoard(char[][] board) {
        printColumnLabels(board[0].length);
        for (int r = 0; r < board.length; ++r) {
            System.out.printf("%2d", board.length - r);
            for (int i = 0; i < board[r].length; ++i) {
                System.out.print(" " + board[r][i]);
            }
            System.out.println();
        }
        printColumnLabels(board[0].length);
        System.out.println("Journal(" + journal.size() + ") " + journal + ", " + getTurn() + "'s move");
    }
}
