5a20eeccee1aae3cbc000090



import java.util.*;
import java.util.function.IntBinaryOperator;

public class SlidingPuzzle {
  private final int n;
  private final int[][] board; // [x][y]
  private final Position[] pos;
  private final boolean[][] pinned; // corresponds to board
  private final List<Integer> sequence;
  int x0, y0; // these are pos[0].x and pos[0].y which are frequently used

  private static class Position {
    int x;
    int y;

    Position(int x, int y) {
      this.x = x;
      this.y = y;
    }
  }

  public SlidingPuzzle(int[][] puzzle) {
//    printBoard(puzzle, true);
    n = puzzle.length;
    if (solutionExists(puzzle)) {
      board = new int[n][n];
      pos = new Position[n * n];
      for (int y = 0; y < n; y++)
        for (int x = 0; x < n; x++) {
          int piece = puzzle[y][x];
          board[x][y] = piece;
          pos[piece] = new Position(x, y);
        }
      x0 = pos[0].x;
      y0 = pos[0].y;
      pos[0] = null;
      pinned = new boolean[n][n];
      sequence = new ArrayList<>();
    } else {
      board = null;
      pos = null;
      pinned = null;
      sequence = null;
    }
  }

  private static boolean solutionExists(int[][] puzzle) {
    int n = puzzle.length;
    int nsq = n * n;
    int[] perm = new int[nsq];
    int i = 0;
    int parity = 0;
    for (int y = 0; y < n; y++)
      for (int x = 0; x < n; x++) {
        int piece = puzzle[y][x];
        perm[i++] = piece;
        if (piece == 0)
          parity += x + y;
      }
    for (i = 0; i < nsq; i++)
      if (perm[i] >= 0) {
        parity++;
        int j = i;
        do {
          int k = perm[j];
          perm[j] = -1;
          j = k;
        } while (j != i);
      }
    return (parity & 1) != 0;
  }

  @SuppressWarnings("serial")
  public static class SlidingException extends RuntimeException {
    SlidingException(String message) {
      super(message);
    }
  }

  private void moveZero(int x, int y, boolean unprotectPinned) { // elementary move
    assert Math.abs(x - x0) + Math.abs(y - y0) == 1;
    if (pinned[x][y])
      if (unprotectPinned) {
        pinned[x][y] = false;
        pinned[x0][y0] = true;
      } else
        throw new SlidingException("Attempt to move a pinned piece");
    int piece = board[x][y];
    Position p = pos[piece];
    p.x = x0;
    p.y = y0;
    board[x0][y0] = piece;
    x0 = x;
    y0 = y;
    board[x][y] = 0;
    int lsi = sequence.size() - 1;
    if (lsi >= 0 && sequence.get(lsi) == piece)
      sequence.remove(lsi); // optimization of wrong (dead end) moves
    else
      sequence.add(piece);
//    System.out.format("%n%d) %d moved%n", sequence.size(), piece);
//    printBoard(board, false);
  }

  private boolean isPassable(int x, int y) {
    return (x >= 0 && x < n && y >= 0 && y < n && !pinned[x][y]);
  }

  private int wx;
  private int wy;

  private boolean findSimpleStep(int xSrc, int ySrc, int xDst, int yDst) {
    wx = xSrc;
    wy = ySrc;
    if (yDst < ySrc && isPassable(xSrc, ySrc - 1)) {
      wy = ySrc - 1;
      return true;
    }
    if (yDst > ySrc && isPassable(xSrc, ySrc + 1)) {
      wy = ySrc + 1;
      return true;
    }
    if (xDst < xSrc && isPassable(xSrc - 1, ySrc)) {
      wx = xSrc - 1;
      return true;
    }
    if (xDst > xSrc && isPassable(xSrc + 1, ySrc)) {
      wx = xSrc + 1;
      return true;
    }
    return false;
  }

  private static class PathPattern {
    // all coordinates are relative to startpoint
    final int ex; // endpoint x
    final int ey; // endpoint y
    final int[] wx; // waypoint xs
    final int[] wy; // waypoint ys
    long usageCount;

    PathPattern(String pathCode) {
      int n = pathCode.length();
      wx = new int[n];
      wy = new int[n];
      int cx = 0;
      int cy = 0;
      for (int i = 0; i < n; i++) {
        switch (pathCode.charAt(i)) {
          case 'L':
            cx -= 1;
            break;
          case 'R':
            cx += 1;
            break;
          case 'U':
            cy -= 1;
            break;
          case 'D':
            cy += 1;
            break;
        }
        wx[i] = cx;
        wy[i] = cy;
      }
      ex = cx;
      ey = cy;
    }

    PathPattern(PathPattern p, IntBinaryOperator xTransform, IntBinaryOperator yTransform) {
      int[] px = p.wx;
      int[] py = p.wy;
      int n = px.length;
      wx = new int[n];
      wy = new int[n];
      for (int i = 0; i < n; i++) {
        wx[i] = xTransform.applyAsInt(px[i], py[i]);
        wy[i] = yTransform.applyAsInt(px[i], py[i]);
      }
      ex = wx[n - 1];
      ey = wy[n - 1];
    }

    PathPattern reflect() {
      return new PathPattern(this, (x, y) -> -x, (x, y) -> y);
    }

    PathPattern rotate() {
      return new PathPattern(this, (x, y) -> -y, (x, y) -> x);
    }
  }

  private static List<PathPattern> pathPatterns = new LinkedList<>();
  static {
    for (String code : new String[] { "LUUR", "DRRUUL" }) {
      PathPattern p = new PathPattern(code);
      PathPattern r = p.reflect();
      pathPatterns.add(p);
      pathPatterns.add(r);
      for (int i = 1; i <= 3; i++) {
        pathPatterns.add(p = p.rotate());
        pathPatterns.add(r = r.rotate());
      }
    }
  }

  private void moveZeroTo(int x, int y) {
    assert isPassable(x, y);
    while (x0 != x || y0 != y)
      if (findSimpleStep(x0, y0, x, y))
        moveZero(wx, wy, false);
      else {
        int dx = x - x0;
        int dy = y - y0;
        outer: for (PathPattern p : pathPatterns)
          if (p.ex == dx && p.ey == dy) {
            int[] pwx = p.wx;
            int[] pwy = p.wy;
            int iLast = pwx.length - 1;
            // we don't check i = iLast since it corresponds to (x, y)
            // which should always be passable
            for (int i = 0; i < iLast; i++)
              if (!isPassable(x0 + pwx[i], y0 + pwy[i]))
                continue outer;
            p.usageCount++;
            // keep the startpoint because x0 and y0 are changed in the process
            int origX = x0;
            int origY = y0;
            for (int i = 0; i <= iLast; i++)
              moveZero(origX + pwx[i], origY + pwy[i], false);
            return;
          }
        throw new SlidingException(
            "No way for zero to row " + (y + 1) + ", column " + (x + 1));
      }
  }

  private void movePieceTo(int piece, int x, int y) {
    Position p = pos[piece];
    int px = p.x;
    int py = p.y;
    pinned[px][py] = true;
    while (px != x || py != y) {
      if (!findSimpleStep(px, py, x, y))
        throw new SlidingException("No way for the piece " + piece + " to row " + (y + 1)
            + ", column " + (x + 1));
      // we need to store waypoint coordinates because they are changed in moveZeroTo
      int pxNew = wx;
      int pyNew = wy;
      moveZeroTo(pxNew, pyNew);
      moveZero(px, py, true);
      px = pxNew;
      py = pyNew;
    }
  }

  private void makeRow(int y) {
    int basePiece = n * y + 1;
    int n1 = n - 1;
    for (int x = 0; x < n1; x++)
      movePieceTo(basePiece + x, x, y);
    Position p = pos[basePiece + n1];
    if (p.x == n1 && (p.y == y || (p.y == y + 1 && x0 == n1 && y0 == y))) {
      movePieceTo(basePiece + n1, n1, y);
      return;
    }
    movePieceTo(basePiece + n1, n1, y + 2);
    moveZeroTo(n1, y + 1);
    movePieceTo(basePiece + n1 - 1, n1, y);
    movePieceTo(basePiece + n1, n1, y + 1);
    moveZeroTo(n1 - 1, y);
    moveZero(n1, y, true);
    moveZero(n1, y + 1, true);
  }

  private void putPair(int x) {
    int n2 = n - 2;
    int topPiece = n2 * n + 1 + x;
    int btmPiece = topPiece + n;
    movePieceTo(btmPiece, x, n - 1);
    Position p = pos[topPiece];
    if (p.y == n2 && (p.x == x || (p.x == x + 1 && x0 == x && y0 == n2))) {
      movePieceTo(topPiece, x, n2);
      return;
    }
    movePieceTo(topPiece, x + 2, n2);
    moveZeroTo(x + 1, n2);
    movePieceTo(btmPiece, x, n2);
    movePieceTo(topPiece, x + 1, n2);
    moveZeroTo(x, n - 1);
    moveZero(x, n2, true);
    moveZero(x + 1, n2, true);
  }

  private void arrangeFinalSquare() {
    int tlPiece = n * (n - 1) - 1;
    int n2 = n - 2;
    movePieceTo(tlPiece, n2, n2);
    movePieceTo(tlPiece + 1, n - 1, n2);
    movePieceTo(tlPiece + n, n2, n - 1);
  }

  public List<Integer> solve() {
    if (sequence != null) {
      try {
        for (int y = 0; y < n - 2; y++)
          makeRow(y);
        for (int x = 0; x < n - 2; x++)
          putPair(x);
        arrangeFinalSquare();
      } catch (SlidingException e) {
        printBoard(board, false);
        throw e;
      }
      Collections.sort(pathPatterns, Comparator.comparingLong(p -> -p.usageCount));
    }
    return sequence;
  }

  private static void printBoard(int[][] board, boolean initialOrder) {
    int n = board.length;
    for (int y = 0; y < n; y++) {
      for (int x = 0; x < n; x++)
        System.out.format("%4d", initialOrder ? board[y][x] : board[x][y]);
      System.out.println();
    }
  }
}
__________________________________________________________________
import java.util.*;
import java.util.stream.*;


public class SlidingPuzzle {
    
    private int           S, linS;                                      // size of the puzzle / linear size (S*S)
    private List<Integer> grid;                                         // current grid state, using a linear version of the puzzle (MUTATED)
    
    final private int[]         idxOf;                                  // current mapping value -> index (MUTATED)
    final private List<Integer> movesToParadise = new ArrayList<>();    // sequence of moves (MUTATED)
    final private Set<Integer>  forbid          = new HashSet<>();      // set of tiles that cannot be moved anymore
    
    
    public SlidingPuzzle(int[][] puzzle) {
        S    = puzzle.length;
        linS = S*S;
        grid = Arrays.stream(puzzle)
                     .flatMapToInt( a -> Arrays.stream(a))
                     .boxed()
                     .collect(Collectors.toList());
        
        idxOf = new int[linS];
        for (int i=0 ; i < linS ; i++) idxOf[ grid.get(i) ] = i;
    }

    
    
    public List<Integer> solve() {
        
        if (isUnsolvable()) return null;
        
        int iX = 0;
        for (int z=0 ; z < S-2 ; z++) {                          // Up to the two last rows... (z moving on the diagonal):
            
            for (int y=z ; y < S-2 ; y++) {                      //    Complete the current top line, until 2 squares are remaining (or 3 if that's the second to last row)
                iX = z*S + y;
                moveTarget(iX);
            }
            conquerCorner(iX+1, iX+2, iX+1, false);              //    Places those two values at the end of the row/column z
            
            int lim = S*(z+1);
            for (int x=z+1 ; x < S-2 ; x++) {                    //    Left column, going down, leaving the two last free.
                iX = x*S + z;
                moveTarget(iX, iX+1, lim);
            }
            conquerCorner(iX+S, iX+2*S, lim, z==S-3);            //    Place the two tiles in the corner, or solve the last 3x2 grid
        }
        // display();
        return movesToParadise;
    }
    


    private boolean isUnsolvable() {
        
        int r0Bot = S - idxOf[0]/S,                                                    // Row containing the 0 (1-indexed, from bottom)
            nInv = 0;
        for (int x=0 ; x<linS-1 ; x++) for (int y=x+1 ; y<linS ; y++)
            if (grid.get(x) != 0 && grid.get(y) != 0 && grid.get(x) > grid.get(y))     // found a new inversion of pairs
                nInv++;
        
        return S%2==1 && nInv%2==1 || S%2==0 && (nInv%2 ^ r0Bot%2) == 0;               // Unsolvable!
    }



    private void moveTarget(int iX) { moveTarget(iX, iX+1, iX); }                      // Find the value expected at index iX and place it there...
    
    /**
     * @param iX        index in the grid of the position to work on
     * @param target    value to place at that index
     * @param lowLim    index value above which the target tile currently is (inclusive / 
     *                  mostly optimization to avoid searching for indexes from the beginning)
     */
    private void moveTarget(int iX, int target, int lowLim) {
        
        int iT = idxOf[target], iTnext = -1,                                           // iT: current position of the target tile / iTnext: declaration only
            xX = iX / S,    yX = iX % S,                                               // iX coords converted to (x,y) format
            xT = iT / S,    yT = iT % S,                                               // target current coords converted to (x,y) format
            dV = yX-yT,     dH = xX-xT,                                                // Moves to do to reach the iX position, in (x,y) format
            sV = cmp(dV,0), sH = cmp(dH,0) * S;                                        // Number of steps to do in each direction
            
            int[] path = Arrays.asList( getPath(iT, dH, dV, sH, sV),
                                        getPath(iT, dV, dH, sV, sH))                   // Build the two possible direct paths (dH->dV or dV->dH)
                               .stream()
                               .filter( a -> Arrays.stream(a).filter( i -> forbid.contains(i) ).count() == 0 )
                               .findAny()
                               .get();                                                 // get the first fully valid path (not using a forbidden tile)
            
            for (int i=0 ; i<path.length-1 ; i++) {
                iT     = path[i];                                                      // Current position of the target
                iTnext = path[i+1];                                                    // Next position to be of the target
                
                forbid.add(iT);                                                        // Lock the target
                moveBlank(iTnext, lowLim);
                forbid.remove(iT);                                                     // Relax("-relax... don't do it...")
                
                grid = blankSwapper(iT, true);                                         // Final swap of blank and target
                movesToParadise.add(target);                                           // Register the moves needed
            }
            // display();
            forbid.add(iX);                                                            // Archive iX as "definitively" done
    }
    
    
    /**
     * @param i1        index in the grid of the first position to work on for this corner
     * @param i2        index of the second position
     * @param lowLim    index value above which the target tile currently is (inclusive / 
     *                  mostly optimization to avoid searching for indexes from the beginning)
     * @param isLat     tell if this is the very last 3x2 subgrid or not
     */
    private void conquerCorner(int i1, int i2, int lowLim, boolean isLast) {
        
        int v1       = i1+1,                                                       // target expected values
            v2       = i2+1,
            delta    = i2-i1,                                                      // Step in idexes between i1 and i2
            delta2nd = delta==1 ? S : 1,                                           // Step in idexes in the orthogonal direction
            shifted2 = i2 + delta2nd;                                              // Temporary targeted index

        moveTarget(i2, v1, lowLim);                                                // Place v1 at i2 for now
        forbid.remove(i2);                                                         // Unlock to avoid impossible moves

        moveTarget(shifted2, v2, lowLim);                                          // Place v2 next to v1, in the orthogonal direction
        forbid.remove(shifted2);                                                   // Unlock the temporary point
        
        moveBlank(i1 + 2*delta2nd, lowLim);                                        // Try to move the blank away first (avoid to move v1 and v2 if they are correct)
        moveBlank(i1,              lowLim);                                        // Move the blank at the ideal position for final 2x2 rotation
      
        // display();
        
        if (!isLast && idxOf[v1]==i2 && idxOf[v2]==shifted2) {                     // Make the 2x2 corner rotation: the 3 tiles are placed as expected/hoped for (blank IS): solve directly
            movesToParadise.add(v1);
            movesToParadise.add(v2);
            grid = blankSwapper(i2,       true);
            grid = blankSwapper(shifted2, true);
        
        } else {                                                                   // Occasionally, something might go "wrong" (v1 moved while working on v2), so resolve instead a 3x2 subgrid with A*, to get the 2 target tiles at the right place (note, at this point, we are sure that the 3 tiles are in the subgrid)
            Set<Integer> subGrid_3x2 = IntStream.range(0,2)
                                                .flatMap( a -> IntStream.range(0,3).map( b -> i1 + a*delta + b*delta2nd ) )
                                                .boxed()
                                                .collect(Collectors.toSet()),      // Grid to work on, in the appropriate orientation
                         blockingSet = IntStream.range(lowLim+2, linS)
                                                .filter( i -> !forbid.contains(i) && !subGrid_3x2.contains(i) )
                                                .boxed()
                                                .collect(Collectors.toSet());      // Tiles to block (only those that are still free at this point and not in the subgrid)
            
            int cost = 0;                                                          // Initial cost, based on on the tiles remaining
            Heuristic<Integer, Integer, Integer, List<Integer>, Integer>
                heuristic = null;                                                  // Function used as heuristic to update the cost for each step/swap in A*
            
            
            if (isLast) {                                                          // last 3x2 subgrid: solve using the positions of all the 6 tiles in the cost/heuristic
                cost = IntStream.range(0, linS)
                                .map( i -> manhattanRef(i, grid.get(i)) )
                                .sum();
                
                heuristic = (inCost, i, i0, g) -> {
                    int a = manhattanRef(i0, g.get(i)),  b = manhattanRef(i,  g.get(i0)),
                        c = manhattanRef(i0, g.get(i0)), d = manhattanRef(i,  g.get(i));
                    return inCost + a+b-c-d;
                }; 
            
            } else {                                                               // not the final subgrid: solve the 3x2 subgrid with A*, checking only for the two target tiles.
            
                cost = manhattanIdx(idxOf[i1+1], i1) + manhattanIdx(idxOf[i2+1], i2);
                heuristic = (inCost, i, i0, g) -> {
                    int delta1 = g.get(i) == v1 ? manhattanIdx(i0, i1) - manhattanIdx(i, i1) : 0,
                        delta2 = g.get(i) == v2 ? manhattanIdx(i0, i2) - manhattanIdx(i, i2) : 0;
                    return inCost + delta1 + delta2;
                }; 
            }
            
            forbid.addAll(blockingSet);                                            // "Gendarmerie nationale, vos papiers siouplait..."
            modifiedAStar(heuristic, cost, lowLim);                                // Move the blank to the right position (just "ahead" of the target)
            forbid.removeAll(blockingSet);                                         // Relax...
        }
        forbid.add(i1);                                                            // Block the two tiles that have been placed
        forbid.add(i2);
    }



    private void moveBlank(int to, int lowLim) {                                   // Move the blank tile "to", update grid, idxOf and movesToParadise accordingly (via the 'modifiedAStar' method)
        
        int cost = manhattanIdx(idxOf[0], to);                                     // Cost computed only using the position of the blank
        Heuristic<Integer, Integer, Integer, List<Integer>, Integer> 
                heuristic = (x, i0, x2, x3) -> manhattanIdx(i0, to);               // Same for the heuristic
                
        modifiedAStar(heuristic, cost, lowLim);
    }

    
    private List<Integer> blankSwapper(int other, boolean makeSwap) { return blankSwapper(idxOf[0], other, grid, true); }
    
    private List<Integer> blankSwapper(int i0, int other, List<Integer> localGrid, boolean makeSwap) {
        
        int vO = localGrid.get(other),
            a  = i0 < other ? i0    : other,
            b  = i0 < other ? other : i0;
            
            List<Integer> cnd = Stream.of( localGrid.subList(0,a), localGrid.subList(b,b+1), localGrid.subList(a+1,b), localGrid.subList(a,a+1), localGrid.subList(b+1,linS) )
                                      .flatMap( lst -> lst.stream() )
                                      .collect( Collectors.toList() );
        if (makeSwap) {                                                          // Update of idxOf only if note computing a candidate grid for A*
            if (a==idxOf[vO]) { idxOf[0] = a; idxOf[vO] = b; }
            else              { idxOf[0] = b; idxOf[vO] = a; }
        }
        return cnd;
    }
    
    
    
    /* ********************
    *       UTILITIES
     * ********************/
    

    private int[] getPath(int iT, int d1, int d2, int step1, int step2) {
        d1 = Math.abs(d1);
        d2 = Math.abs(d2);

        int   i = 1;
        int[] p = new int[1+d1+d2];
        
        p[0] = iT;
        for (int x=0 ; x < d1 ; x++) p[i] = p[i++ - 1] + step1;
        for (int x=0 ; x < d2 ; x++) p[i] = p[i++ - 1] + step2;
        
        return p;
    }
    
    
    private int cmp(int a, int b) { return a==b ? 0 : a<b ? -1 : 1; }


    private int manhattanIdx(int iFrom, int toIdx) {                        // Distance between indexes
        int xF = iFrom / S, yF = iFrom % S,
            xT = toIdx / S, yT = toIdx % S;
        return Math.abs(xT-xF) + Math.abs(yT-yF);
    }
    
    
    private int manhattanRef(int iFrom, int val) {                          // Distance between the current index of v and the expected position of v
        int iV = (val+linS-1) % linS,
            xF = iFrom / S, yF = iFrom % S,
            xT = iV / S,    yT = iV% S;
        return Math.abs(xT-xF) + Math.abs(yT-yF);
    }
    
    
    private void display() {                 // debugging
        for (int x=0 ; x < S ; x++) {
            System.out.println(
            grid.subList(x*S, (x+1)*S)
                .stream()
                .map( i -> (i<10?" ":"") + String.format("%d",  i))
                .collect(Collectors.joining(" ")));
        }
        System.out.println("---------------");
    }


    /**
     *  "A*" search, but exits as soon as the end condition (cost==0) is reached, even if not 
     *  the shortest path. Returns the sequence of moves needed to reach this final situation.
     *
     *    MUTATE or update 'grid', 'idxOf' and 'movesToParadise' when a valid sewuence of 
     *    moves is found.
     *    RAISE a RuntimeException an exception if no solution is found.
     *
     * @param heuristic Function that updates the cost for each candidate grid, 
     *                  knowing the two indexes to swap. Call in the form: f(cost, i, i0, grid).
     * @param cost      Initial cost, has to reach 0 when the final configuration is reached.
     * @param lowLim    Index above which (included) the update of idxOf will be done when the  
     *                  sequence of moves will be found.
     */
    private void modifiedAStar(Heuristic<Integer, Integer, Integer, List<Integer>, Integer> heuristic, int cost, int lowLim) {
        
        PriorityQueue<T> q = new PriorityQueue<>();
        q.add( new T(cost, grid, idxOf[0], 200) );                                     // T instance: (current cost, current candidate grid, current i0, last move done)
        
        Set<List<Integer>> seens = new HashSet<>();                                    // Already found grid candidates
        Set<Integer> forbidPos   = new HashSet<>(forbid);                              // Use a copy of the current forbidden tiles!!
        List<Integer> MOVES      = Arrays.asList(S, -S, 1, -1);                        // (down, up, right, left)
        
        while (!q.isEmpty() && q.peek().cost != 0) {
            
            T tup = q.poll();
            seens.add(tup.grid);
            
            for (int m: MOVES) {
                
                int i = tup.i0 + m;
                if (m == -tup.last                                                     // making a step back...
                        || m==1 && tup.i0 % S == S-1 || m==-1 && tup.i0 % S == 0       // ... wrapping two rows (equivalent to [i][-1] <-> [i+1][0] is the original grid)...
                        || i < 0 || i >= linS                                          // ... not in the grid...
                        || forbidPos.contains(i))                                      // ... reaches a forbidden position
                    continue;
                
                List<Integer> cnd = blankSwapper(tup.i0, i, tup.grid, false);          // compute the next candidate grid
                if (!seens.contains(cnd)) {                                            // If not already traveled, update the priority queue
                    int cndCost = heuristic.apply(tup.cost, i, tup.i0, tup.grid);
                    q.add( new T(cndCost, cnd, i, m, tup.seq, tup.grid.get(i)) );
                }
            }
        }
        
        if (q.isEmpty()) throw new RuntimeException("A* failed to find a sequence!! X/");
        
        T tup = q.poll();                        // Valid result: mutate/update movesToParadise, idxOf and grid
        movesToParadise.addAll(tup.seq);
        
        for (int i=lowLim ; i < linS ; i++) 
            idxOf[ tup.grid.get(i) ] = i;
        
        grid = tup.grid;
    }
    


    
    /* *****************************
     *           HELPERS
     * *****************************/
    
    
    @FunctionalInterface
    static private interface Heuristic<S,X,U,V, R> { R apply(S s, X t, U u, V v); }    
    
    
    
    private static class T implements Comparable<T> {                            // Comparable structure for the priority queue of the A* implementation
        
        private int cost, i0, last;
        private List<Integer> grid, seq;
        
        protected T(int c, List<Integer> g, int io, int l) {
            cost = c;  grid = g;  i0 = io;  last = l;
            seq = new ArrayList<>();
        }
        
        protected T(int c, List<Integer> g, int io, int l, List<Integer> prevSeq, int nextTile) {
            cost = c;  grid = g;  i0 = io;  last = l;
            seq = new ArrayList<>(prevSeq);
            seq.add(nextTile);
        }
        
        @Override public int compareTo(T other) { return cost - other.cost; }
    }
       
}

__________________________________________________________________
import java.util.*;
import java.util.function.*;
import java.awt.Point;

public class SlidingPuzzle {

    private int[][] puzzle;
    private int board_size;

    private List<Integer> moves = new ArrayList<>();
    private Set<Point> completed = new HashSet<>();
    private Point zero;

    private int lower_bound = 0; // current_size = board_size - lower_bound

    public SlidingPuzzle(int[][] puzzle) {
        this.puzzle = puzzle;
        board_size = puzzle.length;

        for (int i = 0; i < board_size; i++) {
            for (int j = 0; j < board_size; j++) {
                if (puzzle[i][j] == 0) {
                    zero = new Point(i, j);
                    return;
                }
            }
        }
    }
  
    private static class UnsolvablePuzzle extends RuntimeException {
        UnsolvablePuzzle() {
        }

        UnsolvablePuzzle(String msg) {
            super(msg);
        }
    }

    private static class Node implements Comparable<Node> {
        private int cost;
        private int remain;
        private Node prev;
        private Point point;

        private Node(int cost, Point finalDest, Point p, Node prev) {
            this.cost = cost;
            this.remain = Math.abs(finalDest.x - p.x) + Math.abs(finalDest.y - p.y);
            this.point = p;
            this.prev = prev;
        }

        private List<Point> getPath() {
            List<Point> path = new ArrayList<>();
            Node curr = this;
            while (curr.prev != null) {
                path.add(curr.point);
                curr = curr.prev;
            }
            Collections.reverse(path);
            return path;
        }

        @Override
        public int compareTo(Node other) {
            int diff = cost + remain - other.cost - other.remain;
            return diff != 0 ? diff : other.cost - cost;
        }
    }

    private static int[][] DIR = { { 1, 0 }, { -1, 0 }, { 0, 1 }, { 0, -1 } };

    private void swap(Point desPoint) {
        int neighbor = puzzle[desPoint.x][desPoint.y];
        puzzle[desPoint.x][desPoint.y] = 0;
        puzzle[zero.x][zero.y] = neighbor;
        zero = desPoint;
        moves.add(neighbor);
    }

    private Point getFinalPosition(int value) {
        value -= 1;
        return new Point(value / board_size, value % board_size);
    }

    private Point searchValue(int value) {
        for (int i = lower_bound; i < board_size; i++) {
            for (int j = lower_bound; j < board_size; j++) {
                if (puzzle[i][j] == value) {
                    return new Point(i, j);
                }
            }
        }
        throw new UnsolvablePuzzle("Cannot find tile with value: " + value);
    }
  
    private List<Point> findPath(Point init, Point finalDest, Set<Point> visited) {
        Queue<Node> queue = new PriorityQueue<>();
        queue.offer(new Node(0, finalDest, init, null));

        while (!queue.isEmpty()) {
            Node p = queue.poll();
            if (p.point.equals(finalDest)) {
                return p.getPath();
            }
            for (int[] dir : DIR) {
                int u = p.point.x + dir[0], v = p.point.y + dir[1];
                if (u < 0 || v < 0 || u >= board_size || v >= board_size)
                    continue;

                Point next = new Point(u, v);
                if (completed.contains(next) || visited.contains(next))
                    continue;

                queue.offer(new Node(p.cost + 1, finalDest, next, p));
            }
            visited.add(p.point);
        }
        throw new UnsolvablePuzzle("NO AVAIABLE PATH, NO SOLUTION!");
    }

    private void moveZeroToPosition(Point finalDest, Point avoidance) {
        List<Point> sequence = findPath(zero, finalDest, new HashSet<Point>() {
            {
                add(avoidance);
            }
        });
        for (Point p : sequence)
            swap(p);
    }

    private void moveToFinalDestination(Point currentPos, Point finalDest) {
        List<Point> sequence = findPath(currentPos, finalDest, new HashSet<>());
        for (Point p : sequence) {
            moveZeroToPosition(p, currentPos);
            swap(currentPos);
            currentPos = p;
        }
    }

    private void solveSingle(int value) {
        Point finalDest = getFinalPosition(value);
        Point currentPos = searchValue(value);
        moveToFinalDestination(currentPos, finalDest);
        completed.add(finalDest);
    }

    private void solveLastTwo(int value1, int value2) {
        Point finalDest = getFinalPosition(value1);
        Point finalDest_value = getFinalPosition(value2);
        Point finalDest_value1 = getFinalPosition(value1 + 1 + board_size);

        Point currentPos = searchValue(value1);
        moveToFinalDestination(currentPos, finalDest_value);

        try {
            completed.add(finalDest_value);
            currentPos = searchValue(value2);
            moveToFinalDestination(currentPos, finalDest_value1);
        } catch (UnsolvablePuzzle e) { // retry
            completed.remove(finalDest_value);
            moveToFinalDestination(searchValue(value2), new Point(board_size - 1, board_size - 1));
            solveLastTwo(value1, value2);
            return;
        }
        moveZeroToPosition(finalDest, finalDest_value1);
        swap(finalDest_value);
        swap(finalDest_value1);
        completed.add(finalDest);
    }

    private void solveUntil_2x2() {
        int limit, leftCorner;
        for (; board_size - lower_bound >= 3; lower_bound++) {
            leftCorner = lower_bound * (board_size + 1) + 1;
            limit = (lower_bound + 1) * board_size - 1;
            for (int i = leftCorner; i < limit; i++) {
                solveSingle(i);
            }
            solveLastTwo(limit, limit + 1);
            limit = board_size * (board_size - 2) + lower_bound + 1;
            for (int i = leftCorner + board_size; i < limit; i += board_size) {
                solveSingle(i);
            }
            solveLastTwo(limit, limit + board_size);
        }
    }

    private void finalRotate() {
        Point[] circle = new Point[] { 
            new Point(board_size - 2, board_size - 2),
            new Point(board_size - 2, board_size - 1), 
            new Point(board_size - 1, board_size - 1),
            new Point(board_size - 1, board_size - 2) 
        };

        Supplier<Boolean> terminate = () -> Arrays.stream(circle).allMatch(p -> {
            int value = puzzle[p.x][p.y];
            return value == 0 || value == p.x * board_size + p.y + 1;
        });

        int index = 0;
        for (int i = 0; i < 4; i++) {
            Point p = circle[i];
            if (puzzle[p.x][p.y] == 0) {
                index = i;
                break;
            }
        }
        for (int i = 0; i < 12; i++) {
            if (terminate.get()) return;
            swap(circle[index = (index + 1) % 4]);
        }
        throw new UnsolvablePuzzle();
    }

    public List<Integer> solve() {
        try {
            solveUntil_2x2();
            finalRotate();
        } 
        catch (UnsolvablePuzzle e) { return null; }
        return moves;
    }
}
__________________________________________________________________
import java.awt.Point;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class SlidingPuzzle {

  static int[][] puzzle;
  static Cell[][] puzzleCell;
  static int[][] solvedPuzzle;
  static List<Integer> result;
  static CellCompare compare;
  static int ROW = -1;
  static int COL = -1;

  public class CellCompare implements Comparator<Cell> {
    @Override
    public int compare(Cell o1, Cell o2) {
      return (o1.f > o2.f) ? 1 : -1;
    }
  }

  public static class Cell {
    // this position
    Point pos;
    // value of cell
    Integer number;
    // path back tracing history
    Point back;
    // total distance cost
    Double f;
    // solved/processed
    boolean solved;

    public Cell() {
      f = Double.MAX_VALUE;
      back = new Point(-1, -1);
      solved = false;
      pos = new Point(-1, -1);
    }

    public Cell(Cell c) {
      this.pos = c.pos;
      this.number = c.number;
      this.back = c.back;
      this.f = c.f;
      this.solved = c.solved;
    }
  }

  public SlidingPuzzle(int[][] puzzle) {
    this.puzzle = puzzle;
    SolvedPuzzle(puzzle);
    result = new ArrayList<>();
    ROW = puzzle.length;
    COL = puzzle[0].length;
    compare = new CellCompare();
    drawPuzzle();
  }

  public List<Integer> solve() {
    // using divide and conquer solve until 3x3 puzzle in bottom right formed
    for (int i = 0; i < puzzle.length - 2; i++) {// STEP 3 repeat until puzzle became small enough
      // STEP 1 solve Top Corner
      solveTop(i);
      // STEP 2 solve Left Corner
      solveLeft(i);
    }
    // STEP 4 solve 3x2
    if (!solveSmallPuzzle())
      return null;
    return result;
  }

  public boolean solveSmallPuzzle() {
    int[] lastPuzzle = new int[5];
    lastPuzzle = stretch(true);

    solveNumber(0, new Point(COL - 2, ROW - 1));
    Cell[][] tempPuzzle = new Cell[ROW][COL];
    for (int i = 0; i < ROW; i++) {
      for (int j = 0; j < COL; j++) {
        tempPuzzle[i][j] = new Cell(puzzleCell[i][j]);
      }
    }

    int loopCount = -1;
    boolean side = true;
    boolean loopFlag = false;
    boolean solvedFlag = false;
    int number = 1;
    for (int n = 0; n < 30; n++) {
      // check if solved
      number = 1;
      solvedFlag = true;
      loopFlag = true;
      for (int i = 0; i < ROW; i++) {
        for (int j = 0; j < COL; j++) {
          if (puzzleCell[i][j].number != tempPuzzle[i][j].number)
            loopFlag = false;
          if (puzzleCell[i][j].number != number)
            solvedFlag = false;
          number++;
          if (number == ROW * COL)
            number = 0;
        }
      }

      // TODO if puzzle solved with rotation
      int[] temp = stretch(false);
      while (temp[0] != lastPuzzle[0]) {
        temp = shiftRight(temp);
      }

      if (Arrays.equals(temp, lastPuzzle)) {
        // rotatePuzzle();
        System.out.println();
      }

      if (solvedFlag == true)
        return true;

      if (loopFlag == true)
        loopCount++;

      Cell blank = findNumber(0);
      Cell swapWith = new Cell();

      if (puzzleCell[ROW - 1][COL - 2].number == 0)
        side = !side;

      if (n < 12) {
        if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
          swapWith = puzzleCell[ROW - 1][COL - 2];
        if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
          swapWith = puzzleCell[ROW - 1][COL - 1];
        if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 1)
          swapWith = puzzleCell[ROW - 2][COL - 1];
        if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 1)
          swapWith = puzzleCell[ROW - 2][COL - 2];
      } else {
        if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
          swapWith = puzzleCell[ROW - 1][COL - 3];
        if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 3)
          swapWith = puzzleCell[ROW - 2][COL - 3];
        if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 3)
          swapWith = puzzleCell[ROW - 2][COL - 2];
        if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
          swapWith = puzzleCell[ROW - 1][COL - 2];
      }

      // if (loopCount % 2 == 0)
      // if (side == true) {
      // if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 1][COL - 2];
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 1][COL - 1];
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 1)
      // swapWith = puzzleCell[ROW - 2][COL - 1];
      // if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 1)
      // swapWith = puzzleCell[ROW - 2][COL - 2];
      // } else {
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 1][COL - 3];
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 3)
      // swapWith = puzzleCell[ROW - 2][COL - 3];
      // if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 3)
      // swapWith = puzzleCell[ROW - 2][COL - 2];
      // if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 1][COL - 2];
      // }
      //
      // else if (loopCount % 2 == 1)
      // if (side == true) {
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 2][COL - 2];
      // else if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 2][COL - 3];
      // else if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 3)
      // swapWith = puzzleCell[ROW - 1][COL - 3];
      // else if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 3)
      // swapWith = puzzleCell[ROW - 1][COL - 2];
      // } else {
      // if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 2][COL - 2];
      // else if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 2)
      // swapWith = puzzleCell[ROW - 2][COL - 1];
      // else if (blank.pos.y == ROW - 2 && blank.pos.x == COL - 1)
      // swapWith = puzzleCell[ROW - 1][COL - 1];
      // else if (blank.pos.y == ROW - 1 && blank.pos.x == COL - 1)
      // swapWith = puzzleCell[ROW - 1][COL - 2];
      // }
      swapNumber(blank.pos.x, blank.pos.y, swapWith.pos.x, swapWith.pos.y);
    }
    return false;
  }

  public int[] shiftRight(int[] arr) {
    int temp = arr[arr.length - 1];

    for (int i = arr.length - 2; i >= 0; i--) {
      arr[i + 1] = arr[i];
    }

    arr[0] = temp;
    return arr;
  }

  public int[] stretch(boolean solved) {
    int[] arr = new int[5];
    int id = 0;
    for (int i = ROW - 2; i < ROW; i++) {
      for (int j = COL - 3; j < COL; j++) {
        if (solved) {
          if (solvedPuzzle[i][j] != 0) {
            arr[id] = solvedPuzzle[i][j];
            id++;
          }
        } else {
          if (puzzleCell[i][j].number != 0) {
            arr[id] = puzzleCell[i][j].number;
            id++;
          }
        }
      }
    }
    return arr;

  }

  public void solveTop(int row) {
    // 1.1 - 1.3 solve until there is only 2 missing
    for (int i = 0; i < COL - 2; i++) {
      if (puzzleCell[row][i].solved)
        continue;
      solveNumber(solvedPuzzle[row][i], new Point(i, row));
      puzzleCell[row][i].solved = true;
    }

    // 1.4 Make sure that the last piece of the row is not on the top row itself.
    // move away last piece
    solveNumber(solvedPuzzle[row][COL - 1], new Point(COL - 1, row + 2));
    // move away second from last piece
    solveNumber(solvedPuzzle[row][COL - 2], new Point(COL - 2, row + 2));

    // 1.5 Move the before last piece of the row to the top right corner
    // bring second from last piece to the last piece position
    solveNumber(solvedPuzzle[row][COL - 2], new Point(COL - 1, row));
    puzzleCell[row][COL - 1].solved = true;

    // 1.6 Position the last piece of the row just below it
    solveNumber(solvedPuzzle[row][COL - 1], new Point(COL - 1, row + 1));
    puzzleCell[row + 1][COL - 1].solved = true;

    // 1.7 position blank to the second from last piece
    solveNumber(solvedPuzzle[ROW - 1][COL - 1], new Point(COL - 2, row));
    puzzleCell[row][COL - 1].solved = false;
    puzzleCell[row + 1][COL - 1].solved = false;

    // lastly move blank to the right
    swapNumber(COL - 2, row, COL - 1, row);
    swapNumber(COL - 1, row, COL - 1, row + 1);
    puzzleCell[row][COL - 2].solved = true;
    puzzleCell[row][COL - 1].solved = true;

    // System.out.println("====================================");
  }

  public void solveLeft(int col) {
    // 2.1 - 2.2 solve until there is only 2 missing
    for (int i = 0; i < ROW - 2; i++) {
      if (puzzleCell[i][col].solved)
        continue;
      solveNumber(solvedPuzzle[i][col], new Point(col, i));
      puzzleCell[i][col].solved = true;
    }

    // 2.3 Make sure that the last piece of the column is not on the left column
    // itself.
    // move away last piece
    solveNumber(solvedPuzzle[ROW - 1][col], new Point(col + 2, ROW - 1));
    // move away second from last piece
    solveNumber(solvedPuzzle[ROW - 2][col], new Point(col + 2, ROW - 2));

    // 2.4 Move the before last piece of the column to the bottom left corner
    // bring second from last piece to the last piece position
    solveNumber(solvedPuzzle[ROW - 2][col], new Point(col, ROW - 1));
    puzzleCell[ROW - 1][col].solved = true;

    // 2.5 Move the last piece of the column just to the right of it
    solveNumber(solvedPuzzle[ROW - 1][col], new Point(col + 1, ROW - 1));
    puzzleCell[ROW - 1][col + 1].solved = true;

    // 2.6 Move the before last piece and the last piece in line position
    solveNumber(solvedPuzzle[ROW - 1][COL - 1], new Point(col, ROW - 2));
    puzzleCell[ROW - 1][col].solved = false;
    puzzleCell[ROW - 1][col + 1].solved = false;

    // lastly move blank to the right
    swapNumber(col, ROW - 2, col, ROW - 1);
    swapNumber(col, ROW - 1, col + 1, ROW - 1);
    puzzleCell[ROW - 2][col].solved = true;
    puzzleCell[ROW - 1][col].solved = true;

    // System.out.println("====================================");
  }

  // move number to target location without interfere frozen puzzle
  public void solveNumber(int number, Point target) {
    int nearest = Integer.MAX_VALUE;
    // move blank next to target number
    while (puzzleCell[target.y][target.x].number != number) {
      // cell with number 0
      Cell blankCell = findNumber(0);

      // number which needed to be placed at target
      Cell numberCell = findNumber(number);

      // target cell for blank to be placed pick based on closest distance of target
      Cell blankTarget = new Cell();
      int x = numberCell.pos.x;
      int y = numberCell.pos.y;
      int vx, vy;
      int[] dx = { 0, 0, -1, 1 };
      int[] dy = { -1, 1, 0, 0 };
      nearest = Integer.MAX_VALUE;
      for (int i = 0; i < 4; i++) {
        vx = x + dx[i];
        vy = y + dy[i];
        if (isValid(ROW, COL, vy, vx) && !puzzleCell[vy][vx].solved
            && nearest > manhattanDistance(puzzleCell[vy][vx].pos, target)) {
          blankTarget = puzzleCell[vy][vx];
          nearest = manhattanDistance(puzzleCell[vy][vx].pos, target);
        }
      }

      // search best path for blank cell
      List<Cell> blankPath = aStar(blankTarget, blankCell, numberCell, null);
      for (Cell path : blankPath) {
        swapNumber(path.pos.x, path.pos.y, blankCell.pos.x, blankCell.pos.y);
        blankCell = puzzleCell[path.pos.y][path.pos.x];
      }
      if (number != 0)
        swapNumber(blankTarget.pos.x, blankTarget.pos.y, numberCell.pos.x, numberCell.pos.y);
    }
  }

  public static void drawPuzzle() {
    System.out.println();
    for (int i = 0; i < 10; i++) {
      System.out.println();
    }
    for (int i = 0; i < ROW; i++) {
      for (int j = 0; j < COL; j++) {
        System.out.printf("%-3d", puzzleCell[i][j].number);
      }
      System.out.println();
    }
    System.out.println();
  }

  public Cell findNumber(int number) {
    // index 0 : y,index 1 : x
    for (int i = 0; i < ROW; i++)
      for (int j = 0; j < COL; j++) {
        if (puzzleCell[i][j].number == number)
          return puzzleCell[i][j];
      }
    return new Cell();
  }

  public static boolean isValid(int ROW, int COL, int row, int col) {
    return (row >= 0) && (row < ROW) && (col >= 0) && (col < COL);
  }

  public static boolean isSolved(int[][] grid, int row, int col) {
    if (grid[row][col] != 1)
      return (true);
    else
      return (false);
  }

  public static void swapNumber(int x1, int y1, int x2, int y2) {
    if (Math.abs(x1 - x2) > 1 || Math.abs(y1 - y2) > 1) {
      System.out.println("rip");
    }
    if (x1 == x2 && y1 == y2)
      return;
    if (puzzleCell[y1][x1].number == 0)
      result.add(puzzleCell[y2][x2].number);
    else
      result.add(puzzleCell[y1][x1].number);
    puzzle[y1][x1] += puzzle[y2][x2];
    puzzle[y2][x2] = puzzle[y1][x1] - puzzle[y2][x2];
    puzzle[y1][x1] -= puzzle[y2][x2];
    puzzleCell[y1][x1].number += puzzleCell[y2][x2].number;
    puzzleCell[y2][x2].number = puzzleCell[y1][x1].number - puzzleCell[y2][x2].number;
    puzzleCell[y1][x1].number -= puzzleCell[y2][x2].number;
    // drawPuzzle();
  }

  public void SolvedPuzzle(int[][] puzzle) {
    int number = 1;
    solvedPuzzle = new int[puzzle.length][puzzle[0].length];
    puzzleCell = new Cell[puzzle.length][puzzle[0].length];
    for (int i = 0; i < puzzle.length; i++) {
      for (int j = 0; j < puzzle[0].length; j++) {
        solvedPuzzle[i][j] = number;
        puzzleCell[i][j] = new Cell();
        puzzleCell[i][j].number = puzzle[i][j];
        puzzleCell[i][j].pos = new Point(j, i);
        number++;
      }
    }
    solvedPuzzle[puzzle.length - 1][puzzle[0].length - 1] = 0;
  }

  public static int manhattanDistance(Point p1, Point p2) {
    return Math.abs(p1.y - p2.y) + Math.abs(p1.x - p2.x);
  }

  public static List<Cell> aStar(Cell targetCell, Cell blankCell, Cell numberCell, List<Integer> ignore) {
    if (ignore == null) {
      ignore = new ArrayList<Integer>();
    }
    blankCell.f = 0.0;
    List<Cell> openList = new ArrayList<>();
    openList.add(puzzleCell[blankCell.pos.y][blankCell.pos.x]);
    while (!openList.isEmpty()) {
      Cell currentCell = openList.remove(0);
      if (currentCell.pos.equals(targetCell.pos)) {
        break;
      }

      int x = currentCell.pos.x;
      int y = currentCell.pos.y;
      int vx, vy;
      int[] dx = { 0, 0, -1, 1 };
      int[] dy = { -1, 1, 0, 0 };
      for (int i = 0; i < 4; i++) {
        vx = x + dx[i];
        vy = y + dy[i];
        if (isValid(ROW, COL, vy, vx) && !currentCell.back.equals(puzzleCell[vy][vx].pos)
            && !ignore.contains(puzzleCell[vy][vx].number) && !puzzleCell[vy][vx].solved
            && !numberCell.pos.equals(new Point(vx, vy)) && puzzleCell[vy][vx].f > currentCell.f + 1) {
          puzzleCell[vy][vx].f = currentCell.f + 1;
          puzzleCell[vy][vx].back = new Point(currentCell.pos);
          openList.add(puzzleCell[vy][vx]);
          openList.sort(compare);
        }
      }
    }
    List<Cell> result = new ArrayList<>();
    targetCell = puzzleCell[targetCell.pos.y][targetCell.pos.x];
    do {
      result.add(targetCell);
      if (isValid(ROW, COL, targetCell.back.y, targetCell.back.x))
        targetCell = puzzleCell[targetCell.back.y][targetCell.back.x];
    } while (targetCell.back.x != -1 || targetCell.back.y != -1);

    for (int i = 0; i < ROW; i++) {
      for (int j = 0; j < COL; j++) {
        puzzleCell[i][j].back = new Point(-1, -1);
        puzzleCell[i][j].f = Double.MAX_VALUE;
      }
    }

    Collections.reverse(result);

    return result;
  }
}
