import java.util.*;
import java.util.stream.Collectors;

public class Skyscrapers {

    private static final int SIZE = 7;
    private static final String digits = "1234567";
    private static final String rows = "ABCDEFG";
    private static final String cols = digits;
    private static final String r_rows = new StringBuilder(rows).reverse().toString();
    private static final String r_cols = new StringBuilder(cols).reverse().toString();

    private int[] clues;
    private Map<String, String> values = new HashMap<>();

    private String[] squares;
    private List<List<String>> unitList = new ArrayList<>();
    private Map<String, List<List<String>>> units = new HashMap<>();
    private Map<String, Set<String>> peers = new HashMap<>();

    private Map<Integer, List<String>> clueUnits = new HashMap<>();
    private Map<String, List<Integer>> squareClues = new HashMap<>();

    public Skyscrapers(int[] clues) {
        this.clues = clues;
        initSqaures();
        initUnitLists();
        initUnits();
        initPeers();
        initClueUnits();
        initSquareClues();
    }

    public static int[][] solvePuzzle(int[] clues) {
        Skyscrapers sc = new Skyscrapers(clues);
        Map<String, String> values = sc.solve();
        int[][] solved = new int[SIZE][SIZE];
        for (int i = 0; i < sc.squares.length; i++) {
            solved[i / SIZE][i % SIZE] = Integer.parseInt(values.get(sc.squares[i]));
        }
        return solved;
    }

    private void parseGrid() {
        for (String s : squares) values.put(s, digits);
        // assign initializing value calculated by the easy clues.
        for (int i = 0; i < 4*SIZE; i++) {
            int clue = clues[i];
            if (clue == 1) {
                assign(values, clueUnits.get(i).get(0), ""+SIZE);
            } else if (clue == SIZE) {
                for (int j = 0; j < SIZE; j++) {
                    String s = clueUnits.get(i).get(j);
                    assign(values, s, "" + (j + 1));
                }
            } else {
                for (int j = 0; j < clue - 1; j++) {
                    for (int k = SIZE - clue + 2 + j; k <= SIZE; k++)
                        eliminate(values, clueUnits.get(i).get(j), "" + k);
                }
            }
        }
    }

    private Map<String, String> solve() {
        parseGrid();
        return search(values);
    }

    // used constraint propagation technique. refer to https://towardsdatascience.com/peter-norvigs-sudoku-solver-25779bb349ce
    private Map<String, String> search(Map<String, String> values) {
        // using depth-first search and propagation, try all possible values
        if (values == null) return null;
        if (isSolved(values)) return values;

        // chose the unfilled square s with the fewest possiblities
        int min = SIZE+1;
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
            Map<String, String> searched = search(assign(copied, ms, "" + d));
            if (searched != null) return searched;
        }

        return null;
    }

    private boolean isSolved(Map<String, String> values) {
        for (String value : values.values()) {
            if (value.length() != 1) return false;
        }
        for (int i = 0; i < clues.length; i++) {
            if (!validateClue(values, i)) return false;
        }
        return true;
    }

    private Map<String, String> assign(Map<String, String> values, String s, String d) {
        // valdiate rules with clues
        if (!validateClues(values, s)) return null;

        String otherValues = values.get(s).replace(d, "");
        for (char d2 : otherValues.toCharArray()) {
            if (eliminate(values, s, "" + d2) == null) return null;
        }
        return values;
    }

    private boolean validateClues(Map<String, String> values, String s) {
        for (int clueIndex : squareClues.get(s)) {
            if (!validateClue(values, clueIndex)) return false;
        }

        return true;
    }

    private boolean validateClue(Map<String, String> values, int clueIndex) {
        int clue = clues[clueIndex];
        if (clue == 0) return true;

        List<String> clueUnit = clueUnits.get(clueIndex);

        int count = 0;
        int maxHeight = 0;
        for (String us : clueUnit) {
            String val = values.get(us);
      if (val.length() > 1) return true;   // if a row/column is not all set, stop validating
            int height = Integer.parseInt(val);
            if (height > maxHeight) {
                maxHeight = height;
                count++;
            }
        }

        return count == clue;
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
            List<String> unit = cross("" + r, cols);
            unitList.add(unit);
        }

        for (char c : cols.toCharArray()) {
            List<String> unit = cross(rows, "" + c);
            unitList.add(unit);
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
                for (String sqaure : unit) {
                    if (!sqaure.equals(s)) unitSet.add(sqaure);
                }
            }

            peers.put(s, unitSet);
        }
    }

    private void initClueUnits() {
        for (int i = 0; i < SIZE; i++) clueUnits.put(i, cross(rows, "" + (i + 1)));
        for (int i = SIZE; i < 2*SIZE; i++) clueUnits.put(i, cross(rows.toCharArray()[i - SIZE] + "", r_cols));
        for (int i = 2*SIZE; i < 3*SIZE; i++) clueUnits.put(i, cross(r_rows, cols.toCharArray()[3*SIZE-1 - i] + ""));
        for (int i = 3*SIZE; i < 4*SIZE; i++) clueUnits.put(i, cross(rows.toCharArray()[4*SIZE-1 - i] + "", cols));
    }

    // indicate which square is affected by which clues
    private void initSquareClues() {
        for (String s : squares) {
            for (int i = 0; i < clueUnits.size(); i++) {
                if (clueUnits.get(i).contains(s)) {
                    List<Integer> clues = squareClues.getOrDefault(s, new ArrayList<>());
                    clues.add(i);
                    squareClues.put(s, clues);
                }
            }
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
_________________________________________________
import java.util.*;
import java.util.stream.Collectors;

public class Skyscrapers {

    private static final String digits = "1234567";
    private static final String rows = "ABCDEFG";
    private static final String cols = digits;

    private int[] clues;
    private Map<String, String> values = new HashMap<>();

    private String[] squares;
    private List<List<String>> unitList = new ArrayList<>();
    private Map<String, List<List<String>>> units = new HashMap<>();
    private Map<String, Set<String>> peers = new HashMap<>();

    private Map<Integer, List<String>> clueUnits = new HashMap<>();     // a list of squares that clues relates
    private Map<String, List<Integer>> squareClues = new HashMap<>();

    public Skyscrapers(int[] clues) {
        this.clues = clues;

        initSqaures();
        initUnitLists();
        initUnits();
        initPeers();
        initClueUnits();
        initSquareClues();
    }

    private void parseGrid() {
        for (String s : squares) values.put(s, digits);

        // assign initializing value calculated by the easy clues.
        for (int i = 0; i < 28; i++) {
            int clue = clues[i];
            if (clue == 1) {
                assign(values, clueUnits.get(i).get(0), "7");
            } else if (clue == 7) {
                for (int j = 0; j < 7; j++) {
                    String s = clueUnits.get(i).get(j);
                    assign(values, s, "" + (j + 1));
                }
            } else {
                for (int j = 0; j < clue - 1; j++) {
                    for (int k = 7 - clue + 2 + j; k <= 7; k++)
                        eliminate(values, clueUnits.get(i).get(j), "" + k);
                }
            }
        }
    }

    private Map<String, String> solve() {
        parseGrid();
        return search(values);
    }

    // used constrant propagation technique. refer to https://towardsdatascience.com/peter-norvigs-sudoku-solver-25779bb349ce
    private Map<String, String> search(Map<String, String> values) {
        // using depth-first search and propagation, try all possible values
        if (values == null) return null;
        if (isSolved(values)) return values;

        // chose the unfilled square s with the fewest possiblities
        int min = 8;
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
            Map<String, String> searched = search(assign(copied, ms, "" + d));
            if (searched != null) return searched;
        }

        return null;
    }

    private boolean isSolved(Map<String, String> values) {
        for (String value : values.values()) {
            if (value.length() != 1) return false;
        }

        for (int i = 0; i < clues.length; i++) {
            if (!validateClue(values, i)) return false;
        }

        return true;
    }

    private Map<String, String> assign(Map<String, String> values, String s, String d) {
        // valdiate rules with clues
        if (!validateClues(values, s)) return null;

        String otherValues = values.get(s).replace(d, "");
        for (char d2 : otherValues.toCharArray()) {
            if (eliminate(values, s, "" + d2) == null) return null;
        }

        return values;
    }

    private boolean validateClues(Map<String, String> values, String s) {
        for (int clueIndex : squareClues.get(s)) {
            if (!validateClue(values, clueIndex)) return false;
        }

        return true;
    }

    private boolean validateClue(Map<String, String> values, int clueIndex) {
        int clue = clues[clueIndex];
        if (clue == 0) return true;

        List<String> clueUnit = clueUnits.get(clueIndex);

        int count = 0;
        int maxHeight = 0;
        for (String us : clueUnit) {
            if (values.get(us).length() > 1) return true;   // if a row/column is not all set, stop validating
            int height = Integer.parseInt(values.get(us));
            if (height > maxHeight) {
                maxHeight = height;
                count++;
            }
        }

        return count == clue;
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
            List<String> unit = cross("" + r, cols);
            unitList.add(unit);
        }

        for (char c : cols.toCharArray()) {
            List<String> unit = cross(rows, "" + c);
            unitList.add(unit);
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
                for (String sqaure : unit) {
                    if (!sqaure.equals(s)) unitSet.add(sqaure);
                }
            }

            peers.put(s, unitSet);
        }
    }

    private void initClueUnits() {
        for (int i = 0; i < 7; i++) {
            clueUnits.put(i, cross(rows, "" + (i + 1)));
        }

        for (int i = 7; i < 14; i++) {
            clueUnits.put(i, cross(rows.toCharArray()[i - 7] + "", "7654321"));
        }

        for (int i = 14; i < 21; i++) {
            clueUnits.put(i, cross("GFEDCBA", cols.toCharArray()[20 - i] + ""));
        }

        for (int i = 21; i < 28; i++) {
            clueUnits.put(i, cross(rows.toCharArray()[27 - i] + "", cols));
        }
    }

    // indicate which square is affected by which clues
    private void initSquareClues() {
        for (String s : squares) {
            for (int i = 0; i < clueUnits.size(); i++) {
                if (clueUnits.get(i).contains(s)) {
                    List<Integer> clues = squareClues.getOrDefault(s, new ArrayList<>());
                    clues.add(i);
                    squareClues.put(s, clues);
                }
            }
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

    public static int[][] solvePuzzle(int[] clues) {
        Skyscrapers sc = new Skyscrapers(clues);
        Map<String, String> values = sc.solve();

        int[][] solved = new int[7][7];
        for (int i = 0; i < sc.squares.length; i++) {
            solved[i / 7][i % 7] = Integer.parseInt(values.get(sc.squares[i]));
        }

        return solved;
    }
    
}
__________________________________________________
import java.util.*;

public class Skyscrapers {
    
    static final int N = 7; // adjust to desired puzzle size less than 10
    
    static int[]seq = new int[N];         // reusable int array
    static String[]c_seq = new String[N]; // reusable String array
    
    static int[][] result = new int[N][N]; // where the finish product is to be stored
    
    static int[][] cloos; 
    /* 
       A 2d array. the number of rows (cloos.length) is the amount of clues that aren't 0.
       each row has 2 elements, one is the index 'c' which represents the position of the clue (see description)
       and the second element is the clue at position c (the amount of skyscrapers to be viewed)
       for example:
     
       in this board, cloos[1] = [5, 3] (cloos[1] because it is the second non-zero clue around the clock,
                                         5 because it's the 5th clue if we count the 0s, and 3 is the number of buildings we can see.)
       the goal here is to not waste
       our time where there are 0s
    
       0 0 0 1 0
    4 |0|0|0|0|0| 3 <- cloos[1][1]
    0 |0|0|0|0|0| 0
    2 |0|0|0|0|0| 0
    0 |0|0|0|0|0| 1 
    1 |0|0|0|0|0| 0
       0 0 0 0 0
      
    */
    
    static String[] numbers = new String[N+1]; // holds numbers 1-N as a string
    static String options = ""; // a string containing numbers one through N
                                // it represents the possibilities of each square at the start of the puzzle
                                // these are the candidates.
    static {
        for (int X = 1; X <= N; X++) {
            options += X;
            numbers[X] = ""+X;
        }
    }
    // this removes a candidate from a "clue_sequence"
    // a clue sequence is a section of the board that's being viewed by a given clue.
    // this methods affects the board and candidates
    static void remove_in_clueseq(int[][]board, String[][]candidates, int c, int i, int X) {
        
        if (c < N)               slim_options(board,candidates,i,c,X);
        if (N-1 < c && c < 2*N)  slim_options(board,candidates,c-N,N-1-i,X);
        if(2*N-1 < c && c < 3*N) slim_options(board,candidates,N-1-i,3*N-1-c,X);
        if(3*N-1 < c)            slim_options(board,candidates,4*N-1-c,i,X);
    }
    // places a number in the board, from the perspective of a clue sequence
    // this method also affects the board and candidates
    static void set_bldg_in_clueseq(int[][]board, String[][]candidates, int c, int i, int X) {
        
        if (c < N)               place_number(board,candidates,i,c,X);
        if (N-1 < c && c < 2*N)  place_number(board,candidates,c-N,N-1-i,X);
        if(2*N-1 < c && c < 3*N) place_number(board,candidates,N-1-i,3*N-1-c,X);
        if(3*N-1 < c)            place_number(board,candidates,4*N-1-c,i,X);
    }
    // method for 'retrieving' a clue sequence as an array.
    // It makes use of our reusable static array 'seq' (to avoid creating more objects)
    // and represents a slice of the board with the perspective 'c' given.
    // modifying it does not affect the clues and candidates.
    // necessary method for checking if the viewcount equals the clue.
    static void clue_sequence(int[][]board, int c) {
        
        if (c < N)               for (int i = 0; i < N; i++) seq[i] = board[  i ][  c ];
        if (N-1 < c && c < 2*N)  for (int i = 0; i < N; i++) seq[i] = board[ c-N][N-1-i];
        if(2*N-1 < c && c < 3*N) for (int i = 0; i < N; i++) seq[i] = board[N-1-i][3*N-1-c];
        if(3*N-1 < c)            for (int i = 0; i < N; i++) seq[i] = board[4*N-1-c][  i];
    }
    // same as clue_sequence, but get's a slice of the candidates board instead
    // will be used for checking invalidation and solving
    static void clue_sequence(String[][]candidates, int c) {
    
        if (c < N)               for (int i = 0; i < N; i++) c_seq[i] = candidates[  i ][  c ];
        if (N-1 < c && c < 2*N)  for (int i = 0; i < N; i++) c_seq[i] = candidates[ c-N][N-1-i];
        if(2*N-1 < c && c < 3*N) for (int i = 0; i < N; i++) c_seq[i] = candidates[N-1-i][3*N-1-c];
        if(3*N-1 < c)            for (int i = 0; i < N; i++) c_seq[i] = candidates[4*N-1-c][  i];
    }
    
    public static int[][] solvePuzzle(int[] clues) {
        
        // initializing 'cloos' with the right elements.. no 0 clues
        int length = 0, counter = 0;
        for (int c = 0; c < 4*N; c++) if (clues[c] != 0) length++;
        cloos = new int[length][];
        for (int c = 0; c < 4*N; c++)  if (clues[c] != 0)  cloos[counter++] = new int[]{c,clues[c]};
                
        String[][] candidates = new String[N][N];
        int   [][] board      = new int   [N][N];
        // all candidates[i][j] are strings containing 123...N
        for (String[] r : candidates) Arrays.fill(r, options);
        
        // presolve
        for (int[] cloo : cloos) {
            // for clues of 1, place a 6 right infront of it
            if (cloo[1] == 1) set_bldg_in_clueseq(board, candidates, cloo[0], 0, N);
            
            // for clues of 2, it's impossible that the second skyscraper in the clue sequence is N-1
            // so we remove it from the candidates
            if (cloo[1] == 2) remove_in_clueseq(board, candidates, cloo[0], 1, N-1);
            
            /* 
                does a "deepcut" of the clue candidates
                for example:
                let's assume N is 6 (the tallest skyscraper)
                  in a clue of 3 the possibilities for skyscrapers [1234,12345,123456,123456,123456,123456]
                  for a clue of 4 the possibilities are            [123 ,1234 ,12345 ,123456,123456,123456]
                  etc.
            */
            for (int X = 0; X < N; X++)
                for (int Y = 1; Y <= N; Y++)
                    if (cloo[1] > Y+X) remove_in_clueseq(board,candidates,cloo[0],Y-1,N-X);
        }
        rowcol_unique_check(board,candidates);
        
        work_on_clues_of_2(board,candidates,cloos);
        
        brutalforce(board,candidates, cloos);
        
        return result;
    }
    //backtracking algorithm
    static boolean brutalforce(int[][]board, String[][]candidates, int[][] cloos) {
        
        int C = -1, x = -1, C1 = -1;
        for (int[] cloo : cloos) {
            clue_sequence(board,cloo[0]);
            for (int i = 0; i < N; i++) if (seq[i] == 0) {
                C = cloo[0];
                C1 = cloo[1];
                x = i;
                break;
            }
        }
        if (C < 0) {
            if (clue_test(board, cloos)) result = board;
            return false;
        }
        clue_sequence(candidates,C);
        String c_seqx = c_seq[x];
        for (int guess = N; guess > 0; guess--) if (c_seqx.contains(numbers[guess])) {
          
         
            String[][]cands2 = new String[N][N];
            int[][]board2 = new int[N][N];
            for (int i = 0; i < N; i++) {
                board2[i] = board[i].clone();
                cands2[i] = candidates[i].clone();
            }
            set_bldg_in_clueseq(board2,cands2,C,x,guess);
            
            clue_sequence(board2,C);
            if (!Arrays.toString(seq).contains("0") && viewcount(seq) != C1) continue;
            
            work_on_clues_of_2(board2,cands2,cloos);
            rowcol_unique_check(board2, cands2);
            
            if (!clue_quiz(board2, cloos) || contradicts(board2, cands2)) continue;
            
            brutalforce(board2,cands2,cloos);
        }
        return false;    
    }
    // checks if all finished clue_sequences are correct
    static boolean clue_quiz(int[][] board, int[][] cloos) {
    
        loop: for (int[] cloo : cloos) {
            
            clue_sequence(board, cloo[0]);
            for (int i = 0; i < N; i++) if (seq[i] == 0) continue loop;
            
            if (cloo[1] != viewcount(seq)) {
                return false;
            }
    
        }
        return true;
        
    }
    // checks if all clue_sequences are correct and assumes they are all finished
    static boolean clue_test(int[][] board, int[][] cloos) {
    
        for (int[] cloo : cloos) {
            
            clue_sequence(board, cloo[0]);
            
            if (cloo[1] != viewcount(seq)) {
                return false;
            }
    
        }
        return true;
    
    }
    
    static boolean contradicts(int[][] board, String[][]candidates) {
        
        for (int c = 0; c < N*2; c++) {
            clue_sequence(board, c);
            clue_sequence(candidates, c);
            String bs = Arrays.toString(seq),
                   cs = Arrays.toString(c_seq);
            String bc = bs + cs;
            
            for (int X = 1; X <= N; X++)  {
                String x = numbers[X];
                if ( bs.indexOf(x) != bs.lastIndexOf(x) || !bc.contains(x)) return true;
            }
        }
        return false;
    }
    // looks for single elements in a clue_sequence of candidates, and places the element there
    static void rowcol_unique_check(int[][]board, String[][] candidates) {
        
        for (int c = 0; c < 12; c++) {
            clue_sequence(candidates, c);
            clue_sequence(board, c);
            String a = String.join("",c_seq);
            String b = Arrays.toString(seq);
            for (int X = 1; X <= N; X++) {
                String S = numbers[X];
                if (!b.contains(S) && a.indexOf(S) == a.lastIndexOf(S) && a.indexOf(S) >= 0) {
                    for (int i = 0; i < N; i++)
                        if (c_seq[i].contains(S)) {
                            set_bldg_in_clueseq(board,candidates,c,i,X);
                            rowcol_unique_check(board, candidates);
                            return;
                        }
                }
            }
        }
    }
    // places a number, removes this number from all the candidates that share a row and column with it.
    static void place_number(int[][]board, String[][]candidates, int r, int c, int x) {
        board[r][c] = x;
        candidates[r][c] = "";
        for (int i = 0; i < N; i++) {
            slim_options(board, candidates, i, c, x);
            slim_options(board, candidates, r, i, x);
        }
    }
    // removes a candidate, but also if the resulting string is length 1, we place that number.
    static void slim_options(int[][]board, String[][]candidates, int r, int c, int x) {
        if (candidates[r][c].isEmpty()) return;
        candidates[r][c] = candidates[r][c].replace(numbers[x],"");
       
        if (candidates[r][c].length() == 1) {
            place_number(board,candidates,r,c,Integer.parseInt(candidates[r][c]));
        }
    }
    // amount of buildings that can be seen from a clue sequence
    static int viewcount(int[] arr) {
        int res = 1, t = arr[0];
        for (int i = 0; i < N; i++) if (t < arr[i]) {
            res++;
            t = arr[i];
        }
        return res;
    }
    // assume the clue is 2 for everything here
    static void work_on_clues_of_2(int[][]board, String[][]candidates, int[][]cloos) {
        boolean repeat = true;
        while (repeat) {
            repeat = false;
            for (int[] cloo : cloos) if (cloo[1] == 2) {
            
                clue_sequence(board, cloo[0]);
                clue_sequence(candidates, cloo[0]);
                // if the closest clue is a 1, and the next clue is a 0, set a skyscraper of height N next to the 1
                if (seq[0] == 1 && seq[1] == 0) set_bldg_in_clueseq(board,candidates,cloo[0],1,N);
                // more stuff
                if (seq[0] == 0) {
                    boolean b = false;
                    for (int i = N-1; i > 0; i--)
                        if (seq[i] == N) {
                            b = true;
                            for (int j = N-1; j > i; j--)
                                if (seq[j] == N-1 || c_seq[j].contains(numbers[N-1])) b = false;
                        }
                        
                    if (b) { 
                        set_bldg_in_clueseq(board,candidates,cloo[0],0,N-1); 
                        repeat = true; 
                    }
                }
            }
            rowcol_unique_check(board,candidates);
        }
    }
    
}
____________________________________________________________________
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Supplier;

public class Skyscrapers {
  public static class Permutations implements Supplier<int[]> {
    private final int n;
    private final int[] perm;
    private boolean finished;

    public Permutations(int size) {
      if (size <= 0)
        throw new IllegalArgumentException("Size of permutations should be positive");
      n = size;
      perm = new int[n];
      for (int i = 0; i < n; i++)
        perm[i] = i + 1;
    }

    @Override
    public int[] get() {
      if (finished)
        return null;
      int[] result = perm.clone();
      int m = n;
      int x = 0, y;
      do {
        y = x;
        x = perm[--m];
      } while (x > y && m > 0);
      if (x > y)
        finished = true;
      else {
        for (int i = m + 1, j = n - 1; i < j; i++, j--) {
          int t = perm[i];
          perm[i] = perm[j];
          perm[j] = t;
        }
        int i = m;
        do
          y = perm[++i];
        while (y < x);
        perm[m] = y;
        perm[i] = x;
      }
      return result;
    }
  }

  private Set<int[]>[] possibleSetsArray() {
    @SuppressWarnings("unchecked")
    Set<int[]>[] result = new Set[size + 1];
    for (int i = 0; i <= size; i++)
      result[i] = new HashSet<>();
    return result;
  }

  private List<int[]>[] possibleListsArray() {
    @SuppressWarnings("unchecked")
    List<int[]>[] result = new List[2 * size];
    return result;
  }

  @SuppressWarnings("unchecked")
  private static List<int[]> cloneLinkedList(List<int[]> list) {
    return (List<int[]>)((LinkedList<int[]>)list).clone();
  }

  // Counts visible skyscrapers
  private static int visibleCount(int[] line, boolean oppositeViewpoint) {
    int count = 0;
    int highest = 0;
    int maxInd = line.length - 1;
    for (int i = 0; i <= maxInd; i++) {
      int x = line[oppositeViewpoint ? maxInd - i : i];
      if (x > highest) {
        count++;
        highest = x;
      }
    }
    return count;
  }

  public final int size;
  private final Set<int[]>[] possibleDirectLines;
  private final Set<int[]>[] possibleOppositeLines;
  private final int permutationCount;

  public Skyscrapers(int cluesLength) {
    if (cluesLength <= 0 || cluesLength % 4 != 0)
      throw new IllegalArgumentException("Wrong length (" + cluesLength + ") of the clues array");
    size = cluesLength / 4;
    possibleDirectLines = possibleSetsArray();
    possibleOppositeLines = possibleSetsArray();
    Set<int[]> allLines = possibleDirectLines[0];
    Supplier<int[]> permSupl = new Permutations(size);
    int[] line;
    while ((line = permSupl.get()) != null) {
      allLines.add(line);
      possibleDirectLines[visibleCount(line, false)].add(line);
      possibleOppositeLines[visibleCount(line, true)].add(line);
    }
    permutationCount = allLines.size();
  }

  // May hold large references, create small solver via solver(4) to GC them
  private static Skyscrapers solverCache;

  public static Skyscrapers solver(int cluesLength) {
    Skyscrapers s = solverCache;
    if (s == null || 4 * s.size != cluesLength)
      solverCache = s = new Skyscrapers(cluesLength);
    return s;
  }

  public static Skyscrapers solver(int[] clues) {
    Skyscrapers s = solver(clues.length);
    s.checkClues(clues);
    return s;
  }

  @SuppressWarnings("serial")
  public static class SkyscraperException extends RuntimeException {
    public SkyscraperException(String reason, int[] clues) {
      super(reason + " clues array: " + Arrays.toString(clues));
    }
  }

  private void checkClues(int[] clues) {
    if (clues.length != size * 4)
      throw new SkyscraperException("Wrong length (" + clues.length + ") of the", clues);
    for (int clue : clues)
      if (clue < 0 || clue > size)
        throw new SkyscraperException("Wrong clue (" + clue + ") in the", clues);
  }

  public static boolean isLatinSquare(int[][] candidate) {
    int size = candidate.length;
    if (size == 0)
      return false;
    boolean[] exists = new boolean[size + 1]; // first element isn't used
    // check rows
    for (int[] row : candidate) {
      if (row.length != size) // not a square
        return false;
      Arrays.fill(exists, false);
      for (int x : row)
        if (x <= 0 || x > size || exists[x])
          return false;
        else
          exists[x] = true;
    }
    // check columns
    for (int i = 0; i < size; i++) {
      Arrays.fill(exists, false);
      for (int j = 0; j < size; j++) {
        int x = candidate[j][i];
        if (exists[x])
          return false;
        else
          exists[x] = true;
      }
    }
    return true;
  }

  public static boolean isSolution(int[] clues, int[][] candidate) {
    int size = candidate.length;
    if (size == 0)
      throw new IllegalArgumentException("Candidate of zero size");
    if (clues.length != 4 * size || !isLatinSquare(candidate))
      return false;
    int[] column = new int[size];
    for (int i = 0; i < size; i++) {
      int[] row = candidate[i];
      int clue = clues[4 * size - 1 - i]; // left
      if (clue != 0 && clue != visibleCount(row, false))
        return false;
      clue = clues[size + i]; // right
      if (clue != 0 && clue != visibleCount(row, true))
        return false;
      for (int j = 0; j < size; j++) // compose i-th column
        column[j] = candidate[j][i];
      clue = clues[i]; // top
      if (clue != 0 && clue != visibleCount(column, false))
        return false;
      clue = clues[3 * size - 1 - i]; // bottom
      if (clue != 0 && clue != visibleCount(column, true))
        return false;
    }
    return true;
  }

  // May be used to generate puzzles, some clues may be removed.
  // No guarantee that the puzzle will have unique solution.
  public static int[] fullClues(int[][] solution) {
    if (!isLatinSquare(solution))
      throw new IllegalArgumentException("Not a Latin square");
    int size = solution.length;
    int[] clues = new int[4 * size];
    int[] column = new int[size];
    for (int i = 0; i < size; i++) {
      int[] row = solution[i];
      clues[4 * size - 1 - i] = visibleCount(row, false); // left
      clues[size + i] = visibleCount(row, true); // right
      for (int j = 0; j < size; j++) // compose i-th column
        column[j] = solution[j][i];
      clues[i] = visibleCount(column, false); // top
      clues[3 * size - 1 - i] = visibleCount(column, true); // bottom
    }
    return clues;
  }

  // Only for puzzles of size < 10
  public static int[] parseClues(String s) {
    s = s.replaceAll("\\s", "");
    int[] clues = new int[s.length()];
    int i = 0;
    for (char c : s.toCharArray()) {
      int x = c - '0';
      if (x < 0 || x > 9)
        throw new IllegalArgumentException("Illegal character in input string: " + c);
      clues[i++] = x;
    }
    return clues;
  }

  // Only for puzzles of size < 10
  public static String picture(int[] clues, int[][] solution) {
    int n = solution.length;
    if (n > 9)
      throw new IllegalArgumentException("Square is too large");
    StringBuilder sb = new StringBuilder();
    sb.append(" \u2502");
    for (int i = 0; i < n; i++)
      sb.append(clues[i]);
    sb.append("\u2502 \n\u2500\u253c");
    for (int i = 0; i < n; i++)
      sb.append('\u2500');
    sb.append("\u253c\u2500\n");
    for (int i = 0; i < n; i++) {
      sb.append(clues[4 * n - 1 - i]).append('\u2502');
      int[] sLine = solution[i];
      for (int j = 0; j < n; j++)
        sb.append(sLine[j]);
      sb.append('\u2502').append(clues[n + i]).append('\n');
    }
    sb.append("\u2500\u253c");
    for (int i = 0; i < n; i++)
      sb.append('\u2500');
    sb.append("\u253c\u2500\n \u2502");
    for (int i = 0; i < n; i++)
      sb.append(clues[3 * n - 1 - i]);
    sb.append("\u2502 \n");
    return sb.toString();
  }

  private int iterationCounter;

  public int iterationCount() { // for debugging purposes, may be used to estimate puzzle difficulty
    return iterationCounter;
  }

  private static class Cross {
    final int row;
    final int column;
    int knownRows; // last known possible rows count
    int knownColumns; // last known possible columns count
    int realRows; // real possible rows count
    int realColumns; // real possible columns count

    Cross(int rowIndex, int columnIndex, int possibleRows, int possibleColumns) {
      row = rowIndex;
      column = columnIndex;
      knownRows = realRows = possibleRows;
      knownColumns = realColumns = possibleColumns;
    }

    int change() {
      return (knownRows - realRows) + (knownColumns - realColumns);
    }
  }

  private void solveNarrowed(List<int[]>[] basePossibilities, int narrowedLineIndex,
      Consumer<int[][]> solutionProcessor) {
    boolean rootCall = narrowedLineIndex < 0;
    List<int[]>[] possibilities = rootCall ? basePossibilities : possibleListsArray();
    if (!rootCall)
      for (int i = 0; i < 2 * size; i++) {
        List<int[]> choices = basePossibilities[i];
        if (i == narrowedLineIndex) {
          Iterator<int[]> it = choices.iterator();
          int[] chosenPossibility = it.next(); // uniqualized at this call
          it.remove(); // exclude from upper level of recursion
          choices = new LinkedList<>();
          choices.add(chosenPossibility);
        } else
          choices = cloneLinkedList(choices);
        possibilities[i] = choices;
      }
    Cross[][] crosses = new Cross[size][size];
    for (int row = 0; row < size; row++) {
      int possibleRowCount = possibilities[row + size].size();
      for (int column = 0; column < size; column++) {
        Cross cross = new Cross(row, column, possibleRowCount, possibilities[column].size());
        if (rootCall)
          cross.knownRows = cross.knownColumns = permutationCount;
        crosses[row][column] = cross;
      }
    }
    if (!rootCall) {
      int baseCount = basePossibilities[narrowedLineIndex].size() + 1;
      if (narrowedLineIndex < size) // column uniqualized
        for (int row = 0; row < size; row++)
          crosses[row][narrowedLineIndex].knownColumns = baseCount;
      else { // row uniqualized
        narrowedLineIndex -= size;
        for (int column = 0; column < size; column++)
          crosses[narrowedLineIndex][column].knownRows = baseCount;
      }
    }
    boolean[] impossibleInRow = new boolean[size + 1];
    boolean[] impossibleInColumn = new boolean[size + 1];
    while (true) {
      iterationCounter++;
      int change = 0;
      Cross cross = null;
      for (Cross[] row : crosses)
        for (Cross cr : row) {
          int ch = cr.change();
          if (ch > change) {
            change = ch;
            cross = cr;
          }
        }
      if (change == 0) {
        narrowedLineIndex = -1;
        int minSize = Integer.MAX_VALUE;
        for (int i = 0; i < 2 * size; i++) {
          int sz = possibilities[i].size();
          if (sz > 1 && sz < minSize) {
            narrowedLineIndex = i;
            minSize = sz;
          }
        }
        if (narrowedLineIndex < 0)
          break; // unique solution found for this level
        solveNarrowed(possibilities, narrowedLineIndex, solutionProcessor);
        minSize--;
        if (narrowedLineIndex < size) // column removed
          for (int i = 0; i < size; i++)
            crosses[i][narrowedLineIndex].realColumns = minSize;
        else { // row removed
          narrowedLineIndex -= size;
          for (int i = 0; i < size; i++)
            crosses[narrowedLineIndex][i].realRows = minSize;
        }
        continue;
      }
      int row = cross.row;
      List<int[]> possibleRows = possibilities[row + size];
      Arrays.fill(impossibleInRow, true);
      int column = cross.column;
      List<int[]> possibleColumns = possibilities[column];
      Arrays.fill(impossibleInColumn, true);
      for (int[] r : possibleRows)
        impossibleInRow[r[column]] = false;
      for (int[] c : possibleColumns)
        impossibleInColumn[c[row]] = false;
      boolean excessiveRowChoices = false;
      boolean excessiveColumnChoices = false;
      for (int x = 1; x <= size; x++)
        if (impossibleInColumn[x] ^ impossibleInRow[x])
          if (impossibleInColumn[x])
            excessiveRowChoices = true;
          else
            excessiveColumnChoices = true;
      if (excessiveRowChoices) {
        Iterator<int[]> it = possibleRows.iterator();
        while (it.hasNext())
          if (impossibleInColumn[it.next()[column]])
            it.remove();
        int newChoiceCount = possibleRows.size();
        if (newChoiceCount == 0)
          return; // no solutions at this level
        for (int i = 0; i < size; i++)
          crosses[row][i].realRows = newChoiceCount;
      }
      if (excessiveColumnChoices) {
        Iterator<int[]> it = possibleColumns.iterator();
        while (it.hasNext())
          if (impossibleInRow[it.next()[row]])
            it.remove();
        int newChoiceCount = possibleColumns.size();
        if (newChoiceCount == 0)
          return; // no solutions at this level
        for (int i = 0; i < size; i++)
          crosses[i][column].realColumns = newChoiceCount;
      }
      cross.knownRows = possibleRows.size();
      cross.knownColumns = possibleColumns.size();
    }
    int[][] solution = new int[size][];
    for (int i = 0; i < size; i++)
      solution[i] = possibilities[i + size].get(0).clone();
    solutionProcessor.accept(solution);
  }

  private List<int[]> choicesFromClues(int directClue, int oppositeClue) {
    List<int[]> choices = new LinkedList<>();
    if (oppositeClue == 0)
      choices.addAll(possibleDirectLines[directClue]);
    else {
      choices.addAll(possibleOppositeLines[oppositeClue]);
      if (directClue != 0)
        choices.retainAll(possibleDirectLines[directClue]);
    }
    return choices;
  }

  // The main starter
  public void solveComplete(int[] clues, Consumer<int[][]> solutionProcessor) {
    checkClues(clues);
    iterationCounter = 0;
    List<int[]>[] possibilities = possibleListsArray(); // columns, then rows
    for (int i = 0; i < 2 * size; i++) {
      possibilities[i] = choicesFromClues(i < size ? clues[i] : clues[5 * size - 1 - i],
          i < size ? clues[3 * size - 1 - i] : clues[i]);
      if (possibilities[i].isEmpty())
        return; // no solutions
    }
    solveNarrowed(possibilities, -1, solutionProcessor);
  }

  // Convenience method that takes care of creating a new solver
  public static void solve(int[] clues, Consumer<int[][]> solutionProcessor) {
    solver(clues.length).solveComplete(clues, solutionProcessor);
//    System.out.println(solver(clues.length).iterationCount() + " iterations");
  }

  // Several wrappers for various use cases

  public static int[][] solvePuzzle(int[] clues) {
    int[][][] solutions = new int[1][][];
    solve(clues, solution -> {
      if (solutions[0] != null)
        throw new SkyscraperException("More than one solution for this", clues);
      solutions[0] = solution;
    });
    if (solutions[0] == null)
      throw new SkyscraperException("Unsolvable puzzle,", clues);
    return solutions[0];
  }

  public static List<int[][]> solutionList(int[] clues, int limit) {
    if (limit < 1)
      throw new IllegalArgumentException("Wrong solution limit: " + limit);
    List<int[][]> list = new ArrayList<>();
    try {
      solve(clues, solution -> {
        list.add(solution);
        if (list.size() == limit)
          throw new SkyscraperException("Solution limit reached for this", clues);
      });
    } catch (SkyscraperException e) {
    }
    return list;
  }

  public static int solutionCount(int[] clues) {
    int[] counter = new int[1];
    solve(clues, solution -> counter[0]++);
    return counter[0];
  }

  public static void printAllSolutions(int[] clues) {
    solve(clues, solution -> System.out.println(picture(clues, solution)));
    System.out.println();
  }

  public static void printAllSolutions(String clues) {
    printAllSolutions(parseClues(clues));
  }

  public static void check(int[] clues, int[][] expected, boolean showSolution) {
    if (!isSolution(clues, expected)) {
      solver(expected.length * 4).checkClues(clues);
      if (!isLatinSquare(expected))
        throw new RuntimeException("Provided array is not a Latin square:\n" + Arrays.deepToString(expected));
      else
        throw new RuntimeException("Provided array is not a solution:\n\n" + picture(clues, expected));
    }
    int[][] actual = Skyscrapers.solvePuzzle(clues);
    if (!isSolution(clues, actual))
      throw new RuntimeException("Returned array is not a solution:\n\n" + picture(clues, actual));
    if (showSolution)
      System.out.println(picture(clues, actual));
    if (!Arrays.deepEquals(expected, actual))
      throw new RuntimeException(
          "Solution differs from expected:\n\n" + picture(clues, showSolution ? expected : actual));
  }

  public static void check(int[] clues, int[][] expected) {
    check(clues, expected, true);
  }

  public static void main(String[] args) {
    printAllSolutions(new int[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0 });
    int[] clues = new int[] { 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0 };
    for (int[][] solution : solutionList(clues, 3))
      System.out.println(picture(clues, solution));
    check(new int[] { 0, 0, 0, 0 }, new int[][] { { 1 } });
    check(new int[] { 0, 0, 0, 0, 0, 0, 2, 1 }, new int[][] { { 2, 1 }, { 1, 2 } });
    check(new int[] { 7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4 },
        new int[][] { { 1, 5, 6, 7, 4, 3, 2 }, { 2, 7, 4, 5, 3, 1, 6 }, { 3, 4, 5, 6, 7, 2, 1 },
            { 4, 6, 3, 1, 2, 7, 5 }, { 5, 3, 1, 2, 6, 4, 7 }, { 6, 2, 7, 3, 1, 5, 4 },
            { 7, 1, 2, 4, 5, 6, 3 } });
    printAllSolutions("000402 003203 000350 330040");
    printAllSolutions("0043300 0333002 0050422 0030206");
  }
}
