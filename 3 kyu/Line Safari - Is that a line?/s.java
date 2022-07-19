59c5d0b0a25c8c99ca000237


import java.util.*;

public class Dinglemouse {
    private static final int[][] DIR_VECTORS = { { 1, 0 }, { 0, 1 }, { -1, 0 }, { 0, -1 } };
    private final byte[][] grid;
    private int x;
    private int y;

    private Dinglemouse(byte[][] grid, int[] start) {
        this.grid = grid;
        x = start[0];
        y = start[1];
        grid[y][x] = 0;
    }

    private boolean isGoodDirection(int d) {
        int[] v = DIR_VECTORS[d];
        int t = grid[y + v[1]][x + v[0]];
        switch (t) {
            case 0:
                return false;
            case 3:
            case 4:
                return true;
            default:
                return ((d - t) & 1) != 0;
        }
    }

    private int lineLength() {
        int d = -1;
        for (int i = 0; i < 4; i++)
            if (isGoodDirection(i))
                if (d >= 0)
                    return 0;
                else
                    d = i;
        if (d < 0)
            return 0;
        int length = 1;
        while (true) {
            int[] v = DIR_VECTORS[d];
            x += v[0];
            y += v[1];
            length++;
            int t = grid[y][x];
            grid[y][x] = 0;
            if (t == 4)
                return length;
            if (t == 3) {
                d = (d + 1) & 1;
                boolean g1 = isGoodDirection(d);
                boolean g2 = isGoodDirection(d + 2);
                if (g1 == g2)
                    return 0;
                if (g2)
                    d += 2;
            } else if (!isGoodDirection(d))
                return 0;
        }
    }

    public static boolean line(final char[][] grid) {
        int height = grid.length;
        int width = grid[0].length;
        byte[][][] byteGrids = new byte[2][height + 2][width + 2];
        int charCount = 0;
        List<int[]> endPoints = new ArrayList<>(2);
        for (int y = 1; y <= height; y++) {
            char[] row = grid[y - 1];
            byte[] bRow = byteGrids[0][y];
            for (int x = 1; x <= width; x++) {
                byte t;
                switch (row[x - 1]) {
                    case '-':
                        t = 1;
                        break;
                    case '|':
                        t = 2;
                        break;
                    case '+':
                        t = 3;
                        break;
                    case 'X':
                        t = 4;
                        endPoints.add(new int[] { x, y });
                        break;
                    default:
                        t = 0;
                }
                if (t != 0) {
                    bRow[x] = t;
                    charCount++;
                }
            }
            System.arraycopy(bRow, 1, byteGrids[1][y], 1, width);
        }
        if (endPoints.size() != 2)
            throw new IllegalArgumentException("Grid must contain exactly 2 end-points");
        for (int i = 0; i <= 1; i++)
            if (new Dinglemouse(byteGrids[i], endPoints.get(i)).lineLength() == charCount)
                return true;
        return false;
    }
}
_______________________________________
import java.util.*;
import java.util.stream.*;
import java.awt.Point;


public class Dinglemouse {
    
    /* **************** *
     *   HELPER CLASS   *
     * **************** */
    private static class Pos extends Point {
        protected Pos(int x, int y)     { super(x, y); }
        protected Pos(Pos p)            { super(p);    }
        
        protected Pos     add(Pos p)    { return new Pos(x+p.x, y+p.y); }
        protected boolean isVert()      { return y == 0; }
        protected char    getChar()     { return posSet.contains(this) ? g[x][y] : 'Z'; }
        
        protected boolean isValidComingFrom(Pos move) {
            char c = getChar();
            return c == '-' && move.x == 0 || c == '|' && move.y == 0 || c == 'X' || c == '+';
        }
        @Override public String toString() { return String.format("(%d,%d)", x,y); }
    }
    /* **************** */
    
    
    private static Pos[] MOVES  = Arrays.stream(new int[][] {new int[] {-1,0}, new int[] {1,0}, new int[] {0,1}, new int[] {0,-1}})
                                        .map( p -> new Pos(p[0], p[1]) )
                                        .toArray(Pos[]::new);
    
    private static Map<Boolean,List<Pos>> TURNS = new HashMap<Boolean,List<Pos>>() {{
        put(false, Arrays.asList(new Pos(1,0), new Pos(-1,0)));                         // move is horizontal => go up or down
        put(true,  Arrays.asList(new Pos(0,1), new Pos(0,-1)));                         // move is verical => go left or right
    }};
    
    private static char[][] g;
    private static List<Pos> startEnd;
    private static Set<Pos> posSet;
    
    
    public static boolean line(final char [][] grid) {
        
        g        = grid;
        posSet   = new HashSet<Pos>();
        startEnd = new ArrayList<Pos>();
        
        for (int x = 0 ; x < grid.length ; x++) 
            for (int y = 0 ; y < grid[x].length ; y++) {
                Pos p = new Pos(x,y);
                if (g[x][y] == 'X')              startEnd.add(p);
                if ("-|+X".contains(""+g[x][y])) posSet.add(p);
        }
        
        boolean isValidPath = startEnd.size() == 2;                                     // Two and only Two 'X' (already required by the description, but...)
        if (isValidPath) {
            for (int i = 0 ; i < 2 ; i++) {                                             // Check coming from one point and the other at the second iteration
                Collections.reverse(startEnd);                                          // Invert the starting and ending points
                isValidPath = seekPath();
                if (isValidPath) break;
            }
        }
        return isValidPath;
    }
    
    
    private static boolean seekPath() {
        
        Set<Pos>   validPosSet = new HashSet<Pos>();                                    // Set of all the positions that will be contained in the valid path (possibly) found
        Stack<Pos> queue       = new Stack<Pos>(),                                      // Store the position of the corners
                   whichDir    = new Stack<Pos>(),                                      // Store the direction to use to do the next step, coming from the position in "queue" at the same level in the stack
                   localPath   = new Stack<Pos>();                                      // Collect the current path (backtracking)
        
        int count   = 0;                                                                // Number of valid paths found
        
        Pos fromPos = new Pos(startEnd.get(0)),
            move    = null;
            
        for (Pos m: MOVES) 
            if (fromPos.add(m).isValidComingFrom(m))
                if (move != null) return false;                                         // Line is invalid because amibguous
                else              move = new Pos(m);                                    // Store the direction along which to move
        
        validPosSet.add(fromPos);                                                    
        whichDir.push(move);
        queue.push(fromPos);
        localPath.push(fromPos);
        
        
        if (move != null) {
        
            while (!queue.isEmpty() && count < 2) {
                
                fromPos = queue.pop();
                move    = whichDir.pop();
                
                final Pos  pos     = fromPos.add(move);
                final char posChar = pos.getChar();
                
                while (!localPath.peek().equals(fromPos)) localPath.pop();              // Track back the correct point in the local path
                
                if (validPosSet.contains(pos) || localPath.contains(pos))               // Cannot traverse two times the same position (would mean 2 valid paths, which is not allowed)
                    continue;
                
                localPath.push(pos);
                
                if (posChar == 'X') {
                    count++;                                                            // Update the number of valid paths found
                    validPosSet.addAll(localPath);                                      // Archive the positions in the grid of this valid path
                    
                } else if (posChar == '-' || posChar == '|') {
                    if (pos.isValidComingFrom(move)) {                                  // Go ahead only if next char in the grid is valid
                        queue.push(pos);
                        whichDir.push(move);
                    }
                    
                } else if (posChar == '+') {                                            // Accumulate the directions/informations to check when a corner is found...
                    List<Pos> virageDeLaMort = TURNS.get(move.isVert())
                                                    .stream()
                                                    .filter( p -> { Pos np = pos.add(p); return !localPath.contains(np) && np.isValidComingFrom(p); } )
                                                    .collect(Collectors.toList());
                    if (virageDeLaMort.size() == 1) {                                   // Add to the queue only when the turn is fully determined (<=> on direction possible or the second one has already been traversed and so isn't "reachable" anymore)
                        queue.push(pos);
                        whichDir.push(virageDeLaMort.get(0));
                    }
                }
            }
        }
        return count == 1 && posSet.stream().filter( p -> !validPosSet.contains(p) ).count() == 0;       // Found only one valid path and all the characters of the grid have been traversed
    }
}
_______________________________________
import java.awt.Point;
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.HashSet;

public class Dinglemouse {
    private final static int NORTH = 0;
    private final static int EAST = 1;
    private final static int SOUTH = 2;
    private final static int WEST = 3;
    private final static Point[] DIRECTION_OFFSET = new Point[4];
    
    static {
        DIRECTION_OFFSET[NORTH] = new Point(0, -1);
        DIRECTION_OFFSET[EAST] = new Point(1, 0);
        DIRECTION_OFFSET[SOUTH] = new Point(0, 1);
        DIRECTION_OFFSET[WEST] = new Point(-1, 0);
    }
        
    private final Cell[] mEndPoints = new Cell[2];
    private final HashMap<Point, Cell> mAllPoints = new HashMap<>();
    private boolean mFoundLineFromStart;
    private boolean mFoundLineFromEnd;
    
    private class Cell extends Point {
        public char mValue;
        public Cell[] mDirection = new Cell[4];
        
        public Cell(int x, int y) {
            super(x, y);
        }
        
        @Override
        public String toString() {
            return "(" + x + "," + y + ")v:" + mValue;
        }
        
        public void calcDirections() {
            for (int idx = 0; idx < DIRECTION_OFFSET.length; idx++) {
                mDirection[idx]
                    = mAllPoints.get(new Point(x + DIRECTION_OFFSET[idx].x,
                                                y + DIRECTION_OFFSET[idx].y));
            }
        }
        
        public HashSet<Path> newBranches(Path path) {
            HashSet<Path> newBranches = new HashSet<>();
            
            for (int idx = 0; idx < 4; idx++) {
                Cell nextCell = mDirection[idx];
                if ((nextCell != null) && (!path.mPoints.contains(nextCell))) {
                    boolean isValidNextCell = true;
                    if (path.mCurrentCell.mValue == '+') {
                        if ((path.mApproachDirection == -1) || (path.mApproachDirection != idx)) {
                            switch (nextCell.mValue) {
                                case '-':
                                    isValidNextCell = (idx == EAST) || (idx == WEST);
                                    break;
                                case '|':
                                    isValidNextCell = (idx == NORTH) || (idx == SOUTH);
                                    break;
                                case 'X':
                                    isValidNextCell = (path.mApproachDirection != -1) || (path.mApproachDirection == idx);
                                    break;
                                default:
                                    break;
                            }
                        }
                        else {
                            isValidNextCell = false;
                        }
                    }
                    else if (nextCell.mValue == '-') {
                        isValidNextCell = (idx == EAST) || (idx == WEST);
                    }
                    else if (nextCell.mValue == '|') {
                        isValidNextCell = (idx == NORTH) || (idx == SOUTH);
                    }
                    else {
                        isValidNextCell = (path.mApproachDirection == -1) || (path.mApproachDirection == idx);
                    }
                    
                    if (isValidNextCell) {
                        Path newPath = new Path(nextCell, path.mStartingCell, path.mEndingCell, idx);
                        newPath.mPoints.addAll(path.mPoints);
                        newBranches.add(newPath);
                    }
                }
            }
            
            if ((path.mCurrentCell.mValue == '+') && (newBranches.size() > 1)) {
                // Ambiguity detected for a corner
                System.out.println("Ambiguity detected!");
                newBranches.clear();
            }
            
            return newBranches;
        }
    }
    
    private class Path {
        public Path(Cell point, Cell startingCell, Cell endingCell, int approachDirection) {
            this.mPoints.add(point);
            this.mCurrentCell = point;
            this.mStartingCell = startingCell;
            this.mEndingCell = endingCell;
            this.mApproachDirection = approachDirection;
        }
        
        public int mApproachDirection;
        public Cell mCurrentCell;
        public final Cell mStartingCell;
        public final Cell mEndingCell;
        public final HashSet<Cell> mPoints = new HashSet<>();
    }
    
    private Dinglemouse(final char[][] grid) {
        System.out.println("Grid lenght: " + grid.length);
        int endpointCount = 0;
        for (int idxRow = 0; idxRow < grid.length; idxRow++) {
            char[] gridRow = grid[idxRow];
            for (int idxCol = 0; idxCol < gridRow.length; idxCol++) {
                char gridChar = gridRow[idxCol];
                if (gridChar != ' ') {
                    Cell cell = new Cell(idxCol, idxRow);
                    if (gridChar == 'X') {
                        mEndPoints[endpointCount++] = cell;
                    }

                    cell.mValue = gridChar;
                    mAllPoints.put(cell, cell);
                }
            }
        }
        
        for (var cell : mAllPoints.values()) {
            cell.calcDirections();
        }
    }
    
    private boolean line() {
        ArrayDeque<Path> paths = new ArrayDeque<>(mAllPoints.size());
        paths.push(new Path(mEndPoints[0], mEndPoints[0], mEndPoints[1], -1));
        paths.push(new Path(mEndPoints[1], mEndPoints[1], mEndPoints[0], -1));
        
        while (!paths.isEmpty()) {
            Path path = paths.pop();
            
            HashSet<Path> newPaths = path.mCurrentCell.newBranches(path);
            
            for (var newPath : newPaths) {
                if (newPath.mPoints.size() == mAllPoints.size()) {
                    if (newPath.mStartingCell == mEndPoints[0]) {
                        if (mFoundLineFromStart) {
                            // Already found a line from the start
                            return false;
                        }
                        mFoundLineFromStart = true;
                    }
                    else if (newPath.mStartingCell == mEndPoints[1]) {
                        if (mFoundLineFromEnd) {
                            // Already found a line from the end
                            return false;
                        }
                        mFoundLineFromEnd = true;
                    }
                }
            }
            
            paths.addAll(newPaths);
        }
        
        return mFoundLineFromStart || mFoundLineFromEnd;
    }

    public static boolean line(final char [][] grid) {
        Dinglemouse dm = new Dinglemouse(grid);
        return dm.line();
    }

}
