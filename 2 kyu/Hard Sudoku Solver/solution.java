import java.util.*;
import java.util.stream.Collectors;

@SuppressWarnings("Duplicates")
public class SudokuSolver {

    private static final String digits = "123456789";
    private static final String rows = "ABCDEFGHI";
    private static final String cols = digits;

    private final int[][] grid;
    private final List<Map<String, String>> solved = new ArrayList<>();

    private String[] squares;
    private List<List<String>> unitList = new ArrayList<>();
    private Map<String, List<List<String>>> units = new HashMap<>();
    private Map<String, Set<String>> peers = new HashMap<>();

    private Map<String, String> values = new HashMap<>();

    public SudokuSolver(int[][] grid) {
        this.grid = grid;

        initSqaures();
        initUnitLists();
        initUnits();
        initPeers();
    }

    // used constraint propagation technique. refer to https://towardsdatascience.com/peter-norvigs-sudoku-solver-25779bb349ce
    public int[][] solve() {
        parseGrid(grid);
        search(values);

        if (solved.size() > 1) throw new IllegalArgumentException();

        Map<String, String> solvedValues = solved.get(0);
        int[][] solvedArray = new int[9][9];
        for (int i = 0; i < squares.length; i++) {
            solvedArray[i / 9][i % 9] = Integer.parseInt(solvedValues.get(squares[i]));
        }

        return solvedArray;
    }

    private void parseGrid(int[][] grid) {
        // convert grid to a map of possible values
        // or throw exception if a contradiction is detected.
        // to start, every square can be any digit, then assign values from the grid
        if (grid.length != 9) throw new IllegalArgumentException();

        List<Integer> gridValues = gridValues(grid);
        if (gridValues.size() != 81) throw new IllegalArgumentException();
        for (int value : gridValues) {
            if (value < 0 || 9 < value) throw new IllegalArgumentException();
        }

        for (String s : squares) values.put(s, digits);
        for (int i = 0; i < 81; i++) {
            if (gridValues.get(i) > 0) {
                Map<String, String> assigned = assign(values, squares[i], String.valueOf(gridValues.get(i)));
                if (assigned == null) throw new IllegalArgumentException();
            }
        }
    }

    // used constraint propagation technique. refer to https://towardsdatascience.com/peter-norvigs-sudoku-solver-25779bb349ce
    private void search(Map<String, String> values) {
        // using depth-first search and propagation, try all possible values
        if (values == null) return;
        if (isSolved(values)) {
            solved.add(values);
            return;
        }

        // chose the unfilled square s with the fewest possibilities
        int min = 10;
        String ms = "";
        for (String s : squares) {
            int length = values.get(s).length();
            if (length > 1 && length < min) {
                min = length;
                ms = s;
            }
        }

        for (char d : values.get(ms).toCharArray()) {
            Map<String, String> copied = new HashMap<>(values);
            search(assign(copied, ms, "" + d));
        }
    }

    private boolean isSolved(Map<String, String> values) {
        for (String value : values.values()) {
            if (value.length() != 1) return false;
        }

        return true;
    }

    private List<Integer> gridValues(int[][] grid) {
        List<Integer> gridValues = new ArrayList<>();
        for (int i = 0; i < 9; i++) {
            if (grid[i].length != 9) throw new IllegalArgumentException();
            List<Integer> gridRow = new ArrayList<>();
            for (int j = 0; j < 9; j++) {
                gridValues.add(grid[i][j]);
                gridRow.add(grid[i][j]);
            }

            System.out.println(gridRow);
        }

        return gridValues;
    }

    private Map<String, String> assign(Map<String, String> values, String s, String d) {
        String otherValues = values.get(s).replace(d, "");
        for (char d2 : otherValues.toCharArray()) {
            if (eliminate(values, s, "" + d2) == null) return null;
        }

        return values;
    }

    private Map<String, String> eliminate(Map<String, String> values, String s, String d) {
        if (!values.get(s).contains(d)) return values;  // already eliminated

        values.put(s, values.get(s).replace(d, ""));

        // (1) if a square s is reduced to one value d2, then eliminate d2 from the peers
        if (values.get(s).isEmpty()) {
            return null;   // contradiction: removed last value
        } else if (values.get(s).length() == 1) {
            String d2 = values.get(s);
            for (String s2 : peers.get(s)) {
                if (eliminate(values, s2, d2) == null) return null;
            }
        }

        // (2) if a unit u is reduced to only one place for a value d, then put it there.
        for (List<String> u : units.get(s)) {
            List<String> dplaces = u.stream().filter(us -> values.get(us).contains(d)).collect(Collectors.toList());
            if (dplaces.size() == 0) {
                return null;    // contradiction: no place for this value
            } else if (dplaces.size() == 1) {
                // d can only be in one place in unit; assign it there
                if (assign(values, dplaces.get(0), d) == null) return null;
            }
        }

        return values;
    }

    private void initSqaures() {
        List<String> sqauresList = cross(rows, cols);
        squares = sqauresList.toArray(new String[0]);
    }

    private void initUnitLists() {
        for (char r : rows.toCharArray()) {
            unitList.add(cross("" + r, cols));
        }

        for (char c : cols.toCharArray()) {
            unitList.add(cross(rows, "" + c));
        }

        for (String rs : new String[] {"ABC", "DEF", "GHI"}) {
            for (String cs : new String[] {"123", "456", "789"}) {
                unitList.add(cross(rs, cs));
            }
        }
    }

    private void initUnits() {
        for (String s : squares) {
            for (List<String> u : unitList) {
                if (u.contains(s)) {
                    if (!units.containsKey(s)) units.put(s, new ArrayList<>());
                    units.get(s).add(u);
                }
            }
        }
    }

    private void initPeers() {
        for (String s : squares) {
            Set<String> unitSet = new HashSet<>();
            for (List<String> unit : units.get(s)) {
                for (String square : unit) {
                    if (!square.equals(s)) unitSet.add(square);
                }
            }

            peers.put(s, unitSet);
        }
    }

    private List<String> cross(String rows, String cols) {
        List<String> crosses = new ArrayList<>();
        for (char r : rows.toCharArray()) {
            for (char c : cols.toCharArray()) {
                crosses.add("" + r + c);
            }
        }

        return crosses;
    }
    
}
_______________________________________________
import java.util.*;
import java.util.stream.*;


public class SudokuSolver {
    
    final private static Set<Integer> BASE   = new HashSet<>(Arrays.asList(1,2,3,4,5,6,7,8,9));
    final private static int[][]      COORDS = IntStream.range(0,9)
                                                        .mapToObj( x -> IntStream.range(0, 9).mapToObj( y -> new int[] {x,y}))
                                                        .flatMap(st->st)
                                                        .toArray(int[][]::new);
    
    final private static List<List<Set<Integer>>> BASE_GRID_SET = genBaseGridSet();
    
    
    private List<List<Set<Integer>>> gridSet = deepCopyGridSet(BASE_GRID_SET);
    private int[][]                  store   = null, 
                                     ans     = new int[9][9];
    
    
    public SudokuSolver(int[][] grid) {
        
        if (!isValidGrid(grid)) throw new IllegalArgumentException("Invalid grid");
        
        for (int x=0 ; x<9 ; x++) for (int y=0 ; y<9 ; y++)
            if (grid[x][y] != 0) {
                gridSet.get(x).get(y).retainAll(Arrays.asList( grid[x][y] ));
            }
    }

    
    private boolean isValidGrid(int[][] grid) {
        
        boolean check = grid.length==9 && Arrays.stream(grid).allMatch( a -> a.length==9 && checkValidNine(a) );
        if (!check) return check;
        
        for (int y=0 ; y<9 && check ; y++) { int yy = y; check &= checkValidNine(IntStream.range(0,9).map(x->grid[x][yy]).toArray()); }
        for (int z=0 ; z<9 && check ; z++) {             check &= checkValidSquare(grid, 3*(z/3), 3*(z%3)); }
        
        return check;
    }

    private boolean checkValidSquare(int[][] grid, int a, int b) {
        return checkValidNine( IntStream.range(0,3)
                                        .flatMap( x -> IntStream.range(0,3).map( y -> grid[a+x][b+y]) )
                                        .toArray() );
    }

    private boolean checkValidNine(int[] nine) {
        Map<Integer,Long> cnt = Arrays.stream(nine).boxed().collect(Collectors.groupingBy(k->k, Collectors.counting()));
        cnt.remove(0);
        return cnt.isEmpty() || BASE.containsAll(cnt.keySet())
                                && cnt.values().stream().max(Long::compareTo).get()==1;
    }
    
    

    public int[][] solve() {
        dfs(0);
        if (store==null) throw new IllegalArgumentException("Unsolvable grid");
        return store;
    }
    
    
    
    private void dfs(int count) {
        
        boolean changed = true;
        while (changed && count != 81) {
            changed = false;
            for (int x=0 ; x<9 ; x++)
                for (int y=0 ; y<9 ; y++) {
                    
                    int s = gridSet.get(x).get(y).size();
                    if (ans[x][y] == 0 && s <= 1) {
                        if (s==0) return;                               // no remaining candidates: invalid
                        changed = true;
                        count   = filterGridSets(x,y,count);
                        if (count==0) return;
                    }
                }
        }
        
        int[][] source = deepCopy(ans);
                
        if (count==81) {
            if (store != null) throw new IllegalArgumentException("Multiple solutions");
            store = source;
        
        } else {
            final List<List<Set<Integer>>> archive = deepCopyGridSet(gridSet);
            int[] min_xy = Arrays.stream(COORDS)
                                 .filter( xy -> ans[xy[0]][xy[1]] == 0)
                                 .min( (xy,ab) -> archive.get(xy[0]).get(xy[1]).size() - archive.get(ab[0]).get(ab[1]).size())
                                 .orElse(new int[0]);
            if (min_xy.length==0) return;
            
            int x = min_xy[0], y = min_xy[1];
            Set<Integer> hash = gridSet.get(x).get(y);
            for (int v: hash) {
                ans     = deepCopy(source);
                gridSet = deepCopyGridSet(archive);
                gridSet.get(x).set(y, new HashSet<Integer>(Arrays.asList(v)));
                dfs(count);
            }
            
        }
    }

    private int filterGridSets(int x, int y, int count) {
        
        int v = gridSet.get(x).get(y).stream().findAny().get(),
            a = 3*(x/3),
            b = 3*(y/3);
        
        ans[x][y] = v;
        for (int z=0 ; z<9 ; z++) {
            if (checker(z,y, v, x,y)                                // check in column
             || checker(x,z, v, x,y)                                // check in row
             || checker(a+z/3, b+z%3, v, x,y)) {                    // check in square
                return 0;
            }   
        }
        return count+1;
    }
    
    
    private boolean checker(int x, int y, int v, int x0, int y0) {
        
        if (ans[x][y] == 0) {
            gridSet.get(x).get(y).remove(v);
            if (gridSet.get(x).get(y).isEmpty() && (x!=x0 || y!=y0)) {
                return true;       // invalid
            }
        }
        return false;
    }
    
    
    
    private static int[][] deepCopy(int[][] arr) {
        int[][] ret = new int[9][];
        for (int x=0 ; x<9 ; x++) ret[x] = Arrays.copyOf(arr[x],9);
        return ret;
    }
    

    private static List<List<Set<Integer>>> genBaseGridSet() {
        List<List<Set<Integer>>> grid = new ArrayList<>(9);
        for (int r=0 ; r<9 ; r++) {
            List<Set<Integer>> row = new ArrayList<>(9); 
            grid.add(row);
            for (int y=0 ; y<9 ; y++) {
                row.add(y, new HashSet<Integer>(BASE));
            }
        }
        return grid;
    }
    
    private static List<List<Set<Integer>>> deepCopyGridSet(List<List<Set<Integer>>> g) {

        List<List<Set<Integer>>> grid = new ArrayList<>(9);
        for (int r=0 ; r<9 ; r++) {
            List<Set<Integer>> row = new ArrayList<>(9); 
            grid.add(row);
            for (int y=0 ; y<9 ; y++) {
                row.add(new HashSet<Integer>( g.get(r).get(y) ));
            }
        }
        return grid;
    }

    private void display() { display(ans); }
    private void display(int[][] xx) {
        System.out.println("------------------");
        Arrays.stream(xx).forEachOrdered( a -> System.out.println(Arrays.toString(a)));
    }
    
}
_______________________________________________
import java.util.*;
import java.util.function.Consumer;

public class SudokuSolver {
    private static final int SIZE1 = 3;
    private static final int SIZE2 = SIZE1 * SIZE1;
    private final int[][] grid;

    public SudokuSolver(int[][] grid) {
        if (grid.length != SIZE2)
            throw new IllegalArgumentException("Wrong grid size");
        this.grid = new int[SIZE2][];
        for (int y = 0; y < SIZE2; y++) {
            int[] row = grid[y];
            if (row == null || row.length != SIZE2)
                throw new IllegalArgumentException("Wrong grid row size");
            for (int t : row)
                if (t < 0 || t > SIZE2)
                    throw new IllegalArgumentException("Invalid cell value: " + t);
            this.grid[y] = row.clone();
        }
    }

    private static boolean nextPermutation(int[] perm) {
        int n = perm.length - 1;
        int x = perm[n];
        int m = n;
        do
            if (--m < 0)
                return false;
        while (x <= (x = perm[m]));
        int k = m + 1;
        do {
        } while (++k <= n && perm[k] > x);
        perm[m] = perm[--k];
        perm[k] = x;
        for (int i = m + 1, j = n; i < j; i++, j--) {
            x = perm[i];
            perm[i] = perm[j];
            perm[j] = x;
        }
        return true;
    }

    private static class Arrangement { // for a square SIZE1 x SIZE1
        final int horizontalPresenceMask;
        final int verticalPresenceMask;

        Arrangement(int[] perm) { // argument is a permutation of 0, 1, ..., SIZE2 - 1
            int hpm = 0;
            int vpm = 0;
            int i = 0;
            for (int y = 0; y < SIZE1; y++)
                for (int x = 0; x < SIZE1; x++) {
                    int n = perm[i++];
                    hpm |= 1 << (n + SIZE2 * y);
                    vpm |= 1 << (n + SIZE2 * x);
                }
            horizontalPresenceMask = hpm;
            verticalPresenceMask = vpm;
        }

        int valueAt(int x, int y) {
            return Integer.numberOfTrailingZeros(
                    horizontalPresenceMask >> (SIZE2 * y) & verticalPresenceMask >> (SIZE2 * x));
        }
    }

    private static final List<Arrangement> ARRANGEMENTS = new ArrayList<>();
    static {
        int[] perm = new int[SIZE2];
        Arrays.setAll(perm, i -> i);
        do
            ARRANGEMENTS.add(new Arrangement(perm));
        while (nextPermutation(perm));
    }

    private static class Splitter<E> extends AbstractCollection<E> {
        final Object[] data;
        int activeCount;
        final Stack<Integer> snapshots = new Stack<>();

        Splitter(Collection<E> elements) {
            data = elements.toArray();
            activeCount = data.length;
        }

        @Override
        public Iterator<E> iterator() {
            return new Iterator<E>() {
                int cursor = 0;
                Object lastReturned;

                @Override
                public boolean hasNext() {
                    return cursor < activeCount;
                }

                @SuppressWarnings("unchecked")
                @Override
                public E next() {
                    if (cursor >= activeCount)
                        throw new NoSuchElementException();
                    return (E)(lastReturned = data[cursor++]);
                }

                @Override
                public void remove() {
                    if (lastReturned == null)
                        throw new IllegalStateException();
                    data[--cursor] = data[--activeCount];
                    data[activeCount] = lastReturned;
                    lastReturned = null;
                }
            };
        }

        void saveState() {
            snapshots.push(activeCount);
        }

        void restoreState() { // order of currently active elements isn't preserved
            activeCount = snapshots.pop();
        }

        void shrink(int newSize) {
            if (newSize < 0 || newSize > activeCount)
                throw new IllegalArgumentException("Invalid size: " + newSize);
            activeCount = newSize;
        }

        @Override
        public int size() {
            return activeCount;
        }
    }

    private static class DependentSquares {
        final boolean verticalDependency;
        final Splitter<Arrangement> masterSplitter;
        final Splitter<Arrangement> slaveSplitter;
        int examinedMSACount; // master square's possible arrangements count, last examined for this pair

        DependentSquares(int masterSquare, int slaveSquare, Splitter<Arrangement>[] possibilities) {
            verticalDependency = (masterSquare - slaveSquare) % SIZE1 == 0;
            masterSplitter = possibilities[masterSquare];
            slaveSplitter = possibilities[slaveSquare];
            examinedMSACount = masterSplitter.size();
        }

        int change() {
            return examinedMSACount - masterSplitter.size();
        }

        boolean lap() {
            int masterPresence = -1;
            Iterator<Arrangement> slaveIterator = slaveSplitter.iterator();
            if (verticalDependency) {
                for (Arrangement a : masterSplitter)
                    masterPresence &= a.verticalPresenceMask;
                if (masterPresence != 0)
                    while (slaveIterator.hasNext())
                        if ((masterPresence & slaveIterator.next().verticalPresenceMask) != 0)
                            slaveIterator.remove();
            } else { // horizontal dependency
                for (Arrangement a : masterSplitter)
                    masterPresence &= a.horizontalPresenceMask;
                if (masterPresence != 0)
                    while (slaveIterator.hasNext())
                        if ((masterPresence & slaveIterator.next().horizontalPresenceMask) != 0)
                            slaveIterator.remove();
            }
            examinedMSACount = masterSplitter.size();
            return !slaveSplitter.isEmpty();
        }
    }

    private void solveNarrowed(Splitter<Arrangement>[] possibilities, int narrowedSquare,
            Consumer<int[][]> solutionProcessor) {
        boolean rootCall = narrowedSquare < 0;
        DependentSquares[][] sqPairs = new DependentSquares[SIZE2][2 * (SIZE1 - 1)];
        for (int masterSquare = 0; masterSquare < SIZE2; masterSquare++) {
            DependentSquares[] masterPairs = sqPairs[masterSquare];
            int i = 0;
            // Horizontal dependencies
            for (int slaveSquare = masterSquare - masterSquare % SIZE1, nextRow = slaveSquare + SIZE1;
                    slaveSquare < nextRow; slaveSquare++)
                if (slaveSquare != masterSquare)
                    masterPairs[i++] = new DependentSquares(masterSquare, slaveSquare, possibilities);
            // Vertical dependencies
            for (int slaveSquare = masterSquare % SIZE1; slaveSquare < SIZE2; slaveSquare += SIZE1)
                if (slaveSquare != masterSquare)
                    masterPairs[i++] = new DependentSquares(masterSquare, slaveSquare, possibilities);
            if (rootCall || masterSquare == narrowedSquare) {
                int bootstrapMSACount = rootCall ? ARRANGEMENTS.size() : 2;
                for (DependentSquares ds : masterPairs)
                    ds.examinedMSACount = bootstrapMSACount;
            }
        }
        while (true) {
            int change = 0;
            DependentSquares bestPair = null;
            for (DependentSquares[] dsRow : sqPairs)
                for (DependentSquares ds : dsRow) {
                    int ch = ds.change();
                    if (ch > change) {
                        change = ch;
                        bestPair = ds;
                    }
                }
            if (change > 0) {
                if (!bestPair.lap())
                    return; // no solutions at this level
            } else {
                narrowedSquare = -1;
                int minSize = Integer.MAX_VALUE;
                for (int i = 0; i < SIZE2; i++) {
                    int sz = possibilities[i].size();
                    if (sz > 1 && sz < minSize) {
                        narrowedSquare = i;
                        minSize = sz;
                    }
                }
                if (narrowedSquare < 0)
                    break; // unique solution found for this level
                for (Splitter<Arrangement> splitter : possibilities)
                    splitter.saveState();
                Splitter<Arrangement> narrowedSplitter = possibilities[narrowedSquare];
                narrowedSplitter.shrink(1);
                solveNarrowed(possibilities, narrowedSquare, solutionProcessor);
                for (Splitter<Arrangement> splitter : possibilities)
                    splitter.restoreState();
                Iterator<Arrangement> it = narrowedSplitter.iterator();
                it.next();
                it.remove(); // examined in the above recursive call
            }
        }
        int[][] solution = new int[SIZE2][SIZE2];
        int i = 0;
        for (int squareY = 0; squareY < SIZE2; squareY += SIZE1)
            for (int squareX = 0; squareX < SIZE2; squareX += SIZE1) {
                Arrangement a = possibilities[i++].iterator().next();
                for (int y = 0; y < SIZE1; y++)
                    for (int x = 0; x < SIZE1; x++)
                        solution[squareY + y][squareX + x] = a.valueAt(x, y) + 1;
            }
        solutionProcessor.accept(solution);
    }

    public void solveComplete(Consumer<int[][]> solutionProcessor) {
        @SuppressWarnings("unchecked")
        Splitter<Arrangement>[] startingPossibilities = new Splitter[SIZE2];
        int i = 0;
        for (int squareY = 0; squareY < SIZE2; squareY += SIZE1)
            for (int squareX = 0; squareX < SIZE2; squareX += SIZE1) {
                int hpm = 0;
                int vpm = 0;
                for (int y = 0; y < SIZE1; y++)
                    for (int x = 0; x < SIZE1; x++) {
                        int n = grid[squareY + y][squareX + x] - 1;
                        if (n >= 0) {
                            hpm |= 1 << (n + SIZE2 * y);
                            vpm |= 1 << (n + SIZE2 * x);
                        }
                    }
                List<Arrangement> squarePossibilities = new ArrayList<>();
                for (Arrangement a : ARRANGEMENTS)
                    if ((a.horizontalPresenceMask & hpm) == hpm && (a.verticalPresenceMask & vpm) == vpm)
                        squarePossibilities.add(a);
                if (squarePossibilities.isEmpty())
                    return; // no solutions
                startingPossibilities[i++] = new Splitter<>(squarePossibilities);
            }
        solveNarrowed(startingPossibilities, -1, solutionProcessor);
    }

    public int[][] solve() {
        int[][][] solutions = new int[1][][];
        solveComplete(solution -> {
            if (solutions[0] != null)
                throw new IllegalArgumentException("Multiple solutions");
            solutions[0] = solution;
        });
        if (solutions[0] == null)
            throw new IllegalArgumentException("Unsolvable puzzle");
        return solutions[0];
    }
}
_______________________________________________
import java.util.*;
public class SudokuSolver {
    
    public ArrayList<ArrayList<Set<Integer>>> cboard;
    public int[][] board;
    
    public SudokuSolver(int[][] board, ArrayList<ArrayList<Set<Integer>>> cboard) {
        this.board = board;
        this.cboard = cboard;
    }
    public boolean weAreGolden() {
        for(int i = 0; i < 9; i++){
            int col = 0, row = 0, box = 0;
            for(int j = 0; j < 9; j++){
                col += board[i][j];
                row += board[j][i];
                box += board[i/3*3 + j/3][i%3*3+j%3];
            }
            if(col != 45 || row != 45 || box != 45) return false;
        }
        return true;
    }
    public boolean DFS(int config) {
        if (weAreGolden()) return true;
        
        int[] configa = new int[]{9,9,0,0};
        int[] configb = new int[]{0,0,9,9};
        
        int[] configaa =new int[]{9,0,0,9};
        int[] configbb =new int[]{0,9,9,0};
        
        int[] configc1 = new int[]{-1,-1,1,1};
        int[] configc2 = new int[]{-1,1,1,-1};
        int a = configa[config];
        int b = configb[config];
        int aa = configaa[config];
        int bb = configbb[config];
        
        int inc = configc1[config];
        int inc2 =configc2[config];
        
        for (int r = Math.min(8,a); r!=b; r+=inc) for (int c = Math.min(8,a); c!=b; c+=inc)
            if (board[r][c] == 0) 
            {
            
                Set<Integer> options = cboard.get(r).get(c);
                if (options.size() == 0) return false;
                for (Integer x : options) {
                    // copy board and cboard
                    int[][] guessBoard = copyBoard();
                    ArrayList<ArrayList<Set<Integer>>> guessCboard = copyCboard();
                    SudokuSolver guess = new SudokuSolver(guessBoard,guessCboard);
                    guess.setPiece(x,r,c);
                    if (guess.board[r][c] < 0) return false;
                    if (guess.DFS(config)) {
                        this.board = guess.board;
                        return true;
                    }
                }
                return false;
                
            }
        return false;
    }
    public int[][] copyBoard() {
        int[][] board2 = new int[9][];
        for (int i=0; i<9; i++) board2[i] = board[i].clone();
        return board2;
    }
    public ArrayList<ArrayList<Set<Integer>>> copyCboard() {
        ArrayList<ArrayList<Set<Integer>>> cboard2 = 
        new ArrayList<ArrayList<Set<Integer>>>();
        for (int R=0; R<9; R++) {
            ArrayList<Set<Integer>> row = new ArrayList<Set<Integer>>();
            for (int C=0; C<9; C++) {
                Set<Integer> set = new HashSet<>();
                for (Integer X : cboard.get(R).get(C))
                    set.add(X);
                row.add(set);
            }
            cboard2.add(row);
        }
        return cboard2;
    }
    public SudokuSolver(int[][] grid) {
        this.board = grid;
        this.cboard = new ArrayList<ArrayList<Set<Integer>>>();
        for (int r=0; r<9; r++) {
            ArrayList<Set<Integer>> row = new ArrayList<Set<Integer>>();
            for (int c=0; c<9; c++) {
                Set<Integer> set = new HashSet<>(Arrays.asList(1,2,3,4,5,6,7,8,9));
                row.add(set);
            }
            cboard.add(row);
        }
    }
    public void throwit() { throw new IllegalArgumentException("bad board"); }
    public int[][] solve() {
        // check proper dimentions and at least 17 clues
        int count = 0;
        if (board.length != 9) throwit();
        for (int i=0; i<9; i++)
            if (board[i].length != 9) throwit();
        for (int r=0; r<9; r++)
            for (int c=0; c<9; c++) {
                if (board[r][c] == 0) count++;
                if (0 > board[r][c] || board[r][c] > 9) throwit();
            }
        if (count > 64) throwit();
        
        // check if it comes in with duplicates
        for (int i = 0; i < 9; i++) {
            String row = "";
            String col = ""; 
            String box = "";
            for (int j = 0; j < 9; j++) {
                if (board[i][j] > 0) row += board[i][j];
                if (board[j][i] > 0) col += board[j][i];
                if (board[ boxCenters[i][0]+moore[j][0] ][ boxCenters[i][1]+moore[j][1] ] > 0)
                    box += board[ boxCenters[i][0]+moore[j][0] ][ boxCenters[i][1]+moore[j][1] ];
            }
            for (int x = 1; x <=9; x++) {
            String X = String.valueOf(x);
            if ((row.indexOf(X) != row.lastIndexOf(X))
                || (col.indexOf(X) != col.lastIndexOf(X))
                || (box.indexOf(X) != box.lastIndexOf(X))) {
                    throwit();
                }
            }
        }
        
        initialCandidateUpdate();
        rowColBoxUniqueCheck();
        
        
        // copy board and cboard
        int[][] board2 = copyBoard();
        ArrayList<ArrayList<Set<Integer>>> cboard2 = copyCboard();
        SudokuSolver s1 = new SudokuSolver(board2,cboard2);
        
        board2 = copyBoard();
        cboard2 = copyCboard();
        SudokuSolver s2 = new SudokuSolver(board2,cboard2);
        
        board2 = copyBoard();
        cboard2 = copyCboard();
        SudokuSolver s3 = new SudokuSolver(board2,cboard2);
        
        if (!DFS(0)) throwit();
        if (!s1.DFS(1)) throwit();
        if (!s2.DFS(2)) throwit();
        if (!s3.DFS(3)) throwit();
        
        if (Arrays.deepToString(board).equals(Arrays.deepToString(s1.board))
        &&  Arrays.deepToString(board).equals(Arrays.deepToString(s2.board))
        &&  Arrays.deepToString(board).equals(Arrays.deepToString(s3.board))
        ) return board;
        
        throwit();
        return board;
    }
    public void initialCandidateUpdate() {
        for (int r=0; r<9; r++)
            for (int c=0; c<9; c++)
                if (board[r][c] > 0)
                    wipeOutFromCandidates(board[r][c],r,c);
    }
    public void wipeOutFromCandidates(int x, int r, int c) {
        cboard.get(r).get(c).clear();
        for (int i=0; i<9; i++) {
            removeAndCheck(x,r,i);
            removeAndCheck(x,i,c);
        }
        for (int[] rc : boxCenters) {
            int R = rc[0], C = rc[1];
            for (int[] RC : moore) {
                if (R+RC[0] == r && C+RC[1] == c) {
                    for (int[] m : moore) removeAndCheck(x,m[0] + R,m[1] + C);
                    return;
                }
            }
        }
    }
    public void removeAndCheck(int x, int r, int c) {
        cboard.get(r).get(c).remove(new Integer(x));
        if (cboard.get(r).get(c).size() == 1)
            setPiece(cboard.get(r).get(c).iterator().next(), r, c);
    }
    public void setPiece(int x, int r, int c) {
//         if (board[r][c] > 0) throw new RuntimeException("Cannot set a piece where there already is one.");
        if (board[r][c] > 0) { board[r][c] = -1; return; }
        board[r][c] = x;
        wipeOutFromCandidates(x,r,c);
    }
    public void rowColBoxUniqueCheck() {
        for (int x=1; x <=9; x++) {
            for (int i=0; i<9; i++) {
                int rcountx = 0, ccountx = 0, bcountx = 0;
                int[] boxrc = boxCenters[i];
                for (int j=0; j<9;j++){
                    if (cboard.get(i).get(j).contains(x)) rcountx++;
                    if (cboard.get(j).get(i).contains(x)) ccountx++;
                    
                    if (cboard.get(boxrc[0]+moore[j][0])
                              .get(boxrc[1]+moore[j][1]).contains(x)) bcountx++;
                }
                if (rcountx == 1) for (int j=0; j<9;j++) if (cboard.get(i).get(j).contains(x)) {
                    setPiece(x,i,j);
                    rowColBoxUniqueCheck();
                    return;
                }
                if (ccountx == 1) for (int j=0; j<9;j++) if (cboard.get(j).get(i).contains(x)) {
                    setPiece(x,j,i);
                    rowColBoxUniqueCheck();
                    return;
                }
                if (bcountx == 1) for (int j=0; j<9;j++) 
                    if (cboard.get(boxrc[0]+moore[j][0]) 
                    .get(boxrc[1]+moore[j][1]).contains(x)) {
                      
                    setPiece(x, boxrc[0]+moore[j][0], boxrc[1]+moore[j][1]);
                    rowColBoxUniqueCheck();
                    return;
                }
            }
        }
    }
    static int[][] boxCenters = new int[][]{{1,1},{1,4},{1,7},
                                            {4,1},{4,4},{4,7},
                                            {7,1},{7,4},{7,7}};
                                            
    static int[][] moore = new int[][] {{0,0},{ 0,1},{ 0,-1},
                                       { 1,0},{ 1,1},{ 1,-1},
                                       {-1,0},{-1,1},{-1,-1}};
                                       
    
}
