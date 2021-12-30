import java.util.*;
import java.util.stream.*;


public class Nonogram {
    
    final static private Map<List<Integer>, Set<List<Integer>>> CLUE_TO_CNDS = buildAllCndsForClues();
    final static private int B=15, H=1, V=0,
                             TOP_BIN = (1<<B)-1;
    
    
    private static Map<List<Integer>, Set<List<Integer>>> buildAllCndsForClues() {
        Map<List<Integer>, Set<List<Integer>>> dct = new HashMap<>();
        IntStream.rangeClosed(0,TOP_BIN)
                 .mapToObj(Nonogram::toPaddedBinaryString)
                 .forEach( s -> dct.computeIfAbsent(lineAsStringToClue(s), k -> new HashSet<List<Integer>>() )
                                   .add( lineAsStringToList(s) ));
        return dct;
    }
    
    private static String toPaddedBinaryString(int n) {
        String s = Integer.toBinaryString(n);
        return new String(new char[B-s.length()]).replace("\0","0") + s;
    }
    
    private static List<Integer> lineAsStringToClue(String line) {
    
        List<Integer> lst   = new ArrayList<>();
        boolean       wasIn = false;
        int           cnt   = 0;
        for (char c: (line+"0").toCharArray()) {
            if      (c=='0' && wasIn) { wasIn = false; lst.add(cnt); cnt = 0; }
            else if (c=='1')          { wasIn = true;  cnt++; }
        }
        return lst;
    }
    
    private static List<Integer> lineAsStringToList(String s) {
        return s.chars().map( c -> c-48 ).boxed().collect(Collectors.toList());
    }
    
    
    //------------------------------------------------------------------
    
    
    private int[][][] clues;
    private Map<List<Integer>, List<List<Integer>>> lines;
    
    public Nonogram(int[][][] cl) { clues = cl; }
    
    
    public int[][] solve() {
    
        buildLinesFromClues();
        boolean changed = true;
        
        while (changed) {
            changed = false;
            
            for (int x=0 ; x<B ; x++) for (int y=0 ; y<B ; y++) {
                final int     iH   = y,
                              iV   = x;
                List<Integer> keyH = Arrays.asList(H,iV), 
                              keyV = Arrays.asList(V,iH);
                
                if (lines.get(keyH).size()==1 && lines.get(keyV).size()==1) continue;
                
                Set<Integer> sH = extractPossibleTilesFromLine_At(keyH, iH),
                             sV = extractPossibleTilesFromLine_At(keyV, iV),
                             intersect = new HashSet<>(sH);
                intersect.retainAll(sV);
                
                changed |= checkAndRemoveWrongCandidatesFromLine(keyH, y, sH, intersect)
                        |  checkAndRemoveWrongCandidatesFromLine(keyV, x, sV, intersect);      // WITHOUT boolean shortcut operators...
            }
        }
        return getOutput();
    }
    
    
    private void buildLinesFromClues() {
        lines = new HashMap<>();
        for (int dim=0 ; dim<2 ; dim++) for (int z=0 ; z<B ; z++) {
            lines.put( Arrays.asList(dim,z),
                       getListFromClueCopy(clues[dim][z]) );
        }
    }
    
    private List<List<Integer>> getListFromClueCopy(int[] clue) {
        return CLUE_TO_CNDS.get( IntStream.of(clue).boxed().collect(Collectors.toList()) )
                           .stream()
                           .collect(Collectors.toList());
    }
    
    private Set<Integer> extractPossibleTilesFromLine_At(List<Integer> key, int idx) {
        return lines.get(key).stream().map( lst -> lst.get(idx) ).collect(Collectors.toSet());
    }
    
    private boolean checkAndRemoveWrongCandidatesFromLine(List<Integer> key, int idx, Set<Integer> tilesSet, Set<Integer> intersect) {
        if (tilesSet.size()==2 && intersect.size()==1) {
            int uniq = new ArrayList<>(intersect).get(0);
            lines.get(key).removeIf( line -> uniq != line.get(idx) );
            return true;
        }
        return false;
    }
    
    private int[][] getOutput() {
        return IntStream.range(0,B)
                        .mapToObj( i -> lines.get(Arrays.asList(H,i))
                                             .get(0)
                                             .stream()
                                             .mapToInt(Integer::intValue)
                                             .toArray() )
                        .toArray(int[][]::new);
    }
}

____________________________________________________________
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Nonogram {
  //stores values for nonogram
  //-1 = undecided
  // 0 = white
  // 1 = black
  private int[][] grid;
  
  //stores clues in 3D array
  //clues[0] contains the column clues, with clues[0][0] containing the clues for the first column
  //clues[1] contains the row clues, with clues[1][2] containing the clues for the third row
  private int[][][] clues;
  
  //holds the queue for which rows/columns will be being checked next
  private ArrayList<Integer> queue;
  
  //creates the grid with the specified dimensions and populates it with -1, and adds the clues
  public Nonogram(int[][][] myClues) {
    int width = myClues[0].length;
    int height = myClues[1].length;
    grid = new int[height][width];
    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        grid[y][x] = -1;
      }
    }
    clues = myClues;
  }
  
  //solves nonogram by going through rows/cols in queue and finding any squares which can be filled in
  public int[][] solve() {
    //build the queue, starting with the clues with the most total cells known
    ArrayList<Clue> clueList = new ArrayList<>();
    for (int i = 0; i < clues[1].length; i++) {
      int rowClueSum = 0;
      for (int clue : clues[1][i]) rowClueSum += clue + 1;
      clueList.add(new Clue(i, rowClueSum));
    }
    for (int i = 0; i < clues[0].length; i++) {
      int colClueSum = 0;
      for (int clue : clues[0][i]) colClueSum += clue + 1;
      clueList.add(new Clue(i + clues[1].length, colClueSum));
    }
    Collections.sort(clueList, new ClueComparator());
    queue = new ArrayList<Integer>();
    for (Clue clue : clueList) queue.add(clue.clueID);
    //solve puzzle
    while (queue.size() > 0) {
      solveRowCol(queue.get(0));
    }
    return grid;
  }
  
  //class to contain clue ID and length
  private class Clue {
    public int clueID;
    public int clueLength;
    
    public Clue(int ID, int len) {
      clueID = ID;
      clueLength = len;
    }
  }
  
  //comparator for Clues
  private class ClueComparator implements Comparator<Clue> {
    @Override
    public int compare(Clue clue1, Clue clue2) {
      return clue1.clueLength - clue2.clueLength;
    }
  }
  
  //goes through a row or column, tries all possible solutions consistent with the clues and available squares
  //then updates any squares which are the same in every possible solution
  //finally, updates the queue
  private void solveRowCol(int rowColNum) {
    //determine if the ID corresponds to a row or a column (rows will go first)
    boolean isRow = rowColNum < grid.length;
    //return if the id isn't valid
    if (rowColNum > grid.length + grid[0].length) return;
    //get the possiblities for the row or column;
    int rowColLength = (isRow) ? grid[0].length : grid.length;
    int[] rowCol = new int[rowColLength];
    int[] rcClues;
    if (isRow) {
      rowCol = grid[rowColNum].clone();
      rcClues = clues[1][rowColNum].clone();
    } else {
      for (int i = 0; i < grid.length; i++) rowCol[i] = grid[i][rowColNum - grid[0].length];
      rcClues = clues[0][rowColNum - grid[0].length].clone();
    }
    generateRCPossibilities(rcClues, rowCol.clone(), 0, 0);
    //go through possibilities and find which of the squares are the same in each one
    boolean[][] beenWB = new boolean[rowCol.length][2];
    for (int[] combo : rowColCombos) {
      for (int i = 0; i < combo.length; i++) {
        beenWB[i][combo[i]] = true;
      }
    }
    boolean rowColComplete = true;
    for (int i = 0; i < rowCol.length; i++) {
      if (!beenWB[i][0]) {
        rowCol[i] = 1;
      } else if (!beenWB[i][1]) {
        rowCol[i] = 0;
      } else {
        rowColComplete = false;
      }
    }
    //update grid with new information
    if (isRow) {
      for (int i = 0; i < grid[0].length; i++) {
        if (grid[rowColNum][i] != rowCol[i]) {
          //move the column which has been changed to the front of the queue
          Collections.rotate(queue.subList(1, queue.indexOf(grid.length + i) + 1), 1);
          grid[rowColNum][i] = rowCol[i];
        }
      }
    } else {
      for (int i = 0; i < grid.length; i++) {
        if (grid[i][rowColNum - grid.length] != rowCol[i]) {
          //move the row which has been changed to the front of the queue
          Collections.rotate(queue.subList(1, queue.indexOf(i) + 1), 1);
          grid[i][rowColNum - grid.length] = rowCol[i];
        }
      }
    }
    //if the row/column is complete, remove it from the queue
    //otherwise, move it to the back of the queue
    if (rowColComplete) {
      queue.remove(0);
    } else {
      Collections.rotate(queue, -1);
    }
  }
  
  //ArrayList for the possibilities for a row or column, to be used by the function below
  private ArrayList<int[]> rowColCombos;
  
  //recursive function to generate the possiblities for a row or column
  //it does this by trying every possibility of gap length which works
  private void generateRCPossibilities(int[] clues, int[] rowCol, int gapID, int startAt) {
    //if gapID is 0 then this is the first function call, so reset the ArrayList
    int endBefore = 0;
    if (gapID == 0) {
      rowColCombos = new ArrayList<int[]>();
    } else {
      //if gapID isn't 0, then this isn't the first function call, so we want to add the black squares from the current clue
      endBefore = startAt + clues[gapID-1];
      for (int i = startAt; i < endBefore; i++) {
        //if we know the square is unfilled, then this combination can't work, so return
        if (i >= rowCol.length || rowCol[i] == 0) return; 
        //otherwise, fill the square
        rowCol[i] = 1;
      }
    }
    //if gapID is the same as clues length then we have a complete combo, so fill in all undecided as white; add to list and return
    if (gapID == clues.length) {
      for (int i = endBefore; i < rowCol.length; i++) {
        //if there are any black after the combination, this can't be correct so return
        if (rowCol[i] == 1) return;
        if (rowCol[i] == -1) rowCol[i] = 0;
      }
      rowColCombos.add(rowCol);
      return;
    }
    //try possibilities for next gap length
    int maxGapLength = rowCol.length - endBefore + 1;
    for (int i = gapID; i < clues.length; i++) maxGapLength -= 1 + clues[i];
    gapLengthLoop:
    for (int gapLength = (gapID == 0) ? 0 : 1; gapLength <= maxGapLength; gapLength++) {
      //try gap length
      int[] currentAttempt = rowCol.clone();
      for (int i = endBefore; i < endBefore + gapLength; i++) {
        //if one of the cells is already black, then this and any longer gaps must be wrong
        if (currentAttempt[i] == 1) break gapLengthLoop;
        currentAttempt[i] = 0;
      }
      //call function recursively
      generateRCPossibilities(clues, currentAttempt, gapID + 1, endBefore + gapLength);
    }
  }
}

____________________________________________________________
import java.util.ArrayList;
import java.util.Collections;

public class Nonogram {
  //stores values for nonogram
  //-1 = undecided
  // 0 = white
  // 1 = black
  private int[][] grid;
  
  //stores clues in 3D array
  //clues[0] contains the column clues, with clues[0][0] containing the clues for the first column
  //clues[1] contains the row clues, with clues[1][2] containing the clues for the third row
  private int[][][] clues;
  
  //holds the queue for which rows/columns will be being checked next
  private ArrayList<Integer> queue;
  
  //creates the grid with the specified dimensions and populates it with -1, and adds the clues
  public Nonogram(int[][][] myClues) {
    int width = myClues[0].length;
    int height = myClues[1].length;
    grid = new int[height][width];
    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        grid[y][x] = -1;
      }
    }
    clues = myClues;
  }
  
  //solves nonogram by checking each row/col at front of queue and finding any squares which can be filled in
  public int[][] solve() {
    int totalRowsCols = grid.length + grid[0].length;
    queue = new ArrayList<Integer>();
    for (int i = 0; i < totalRowsCols; i++) queue.add(i);
    while (queue.size() > 0) {
      solveRowCol(queue.get(0));
    }
    return grid;
  }
  
  //goes through a row or column, tries all possible solutions consistent with the clues and available squares
  //then updates any squares which are the same in every possible solution
  //finally, updates the queue
  private void solveRowCol(int rowColNum) {
    //determine if the ID corresponds to a row or a column (rows will go first)
    boolean isRow = rowColNum < grid.length;
    //return if the id isn't valid
    if (rowColNum > grid.length + grid[0].length) return;
    //get the possiblities for the row or column;
    int rowColLength = (isRow) ? grid[0].length : grid.length;
    int[] rowCol = new int[rowColLength];
    int[] rcClues;
    if (isRow) {
      rowCol = grid[rowColNum].clone();
      rcClues = clues[1][rowColNum].clone();
    } else {
      for (int i = 0; i < grid.length; i++) rowCol[i] = grid[i][rowColNum - grid[0].length];
      rcClues = clues[0][rowColNum - grid[0].length].clone();
    }
    generateRCPossibilities(rcClues, rowCol.clone(), 0, 0);
    //go through possibilities and find which of the squares are the same in each one
    boolean[][] beenWB = new boolean[rowCol.length][2];
    for (int[] combo : rowColCombos) {
      for (int i = 0; i < combo.length; i++) {
        beenWB[i][combo[i]] = true;
      }
    }
    boolean rowColComplete = true;
    for (int i = 0; i < rowCol.length; i++) {
      if (!beenWB[i][0]) {
        rowCol[i] = 1;
      } else if (!beenWB[i][1]) {
        rowCol[i] = 0;
      } else {
        rowColComplete = false;
      }
    }
    //update grid with new information
    if (isRow) {
      for (int i = 0; i < grid[0].length; i++) {
        if (grid[rowColNum][i] != rowCol[i]) {
          //move the column which has been changed to the front of the queue
          Collections.rotate(queue.subList(1, queue.indexOf(grid.length + i) + 1), 1);
          grid[rowColNum][i] = rowCol[i];
        }
      }
    } else {
      for (int i = 0; i < grid.length; i++) {
        if (grid[i][rowColNum - grid.length] != rowCol[i]) {
          //move the row which has been changed to the front of the queue
          Collections.rotate(queue.subList(1, queue.indexOf(i) + 1), 1);
          grid[i][rowColNum - grid.length] = rowCol[i];
        }
      }
    }
    //if the row/column is complete, remove it from the queue
    //otherwise, move it to the back of the queue
    if (rowColComplete) {
      queue.remove(0);
    } else {
      Collections.rotate(queue, -1);
    }
  }
  
  //ArrayList for the possibilities for a row or column, to be used by the function below
  private ArrayList<int[]> rowColCombos;
  
  //recursive function to generate the possiblities for a row or column
  //it does this by trying every possibility of gap length which works
  private void generateRCPossibilities(int[] clues, int[] rowCol, int gapID, int startAt) {
    //if gapID is 0 then this is the first function call, so reset the ArrayList
    int endBefore = 0;
    if (gapID == 0) {
      rowColCombos = new ArrayList<int[]>();
    } else {
      //if gapID isn't 0, then this isn't the first function call, so we want to add the black squares from the current clue
      endBefore = startAt + clues[gapID-1];
      for (int i = startAt; i < endBefore; i++) {
        //if we know the square is unfilled, then this combination can't work, so return
        if (i >= rowCol.length || rowCol[i] == 0) return; 
        //otherwise, fill the square
        rowCol[i] = 1;
      }
    }
    //if gapID is the same as clues length then we have a complete combo, so fill in all undecided as white; add to list and return
    if (gapID == clues.length) {
      for (int i = endBefore; i < rowCol.length; i++) {
        //if there are any black after the combination, this can't be correct so return
        if (rowCol[i] == 1) return;
        if (rowCol[i] == -1) rowCol[i] = 0;
      }
      rowColCombos.add(rowCol);
      return;
    }
    //try possibilities for next gap length
    int maxGapLength = rowCol.length - endBefore + 1;
    for (int i = gapID; i < clues.length; i++) maxGapLength -= 1 + clues[i];
    gapLengthLoop:
    for (int gapLength = (gapID == 0) ? 0 : 1; gapLength <= maxGapLength; gapLength++) {
      //try gap length
      int[] currentAttempt = rowCol.clone();
      for (int i = endBefore; i < endBefore + gapLength; i++) {
        //if one of the cells is already black, then this and any longer gaps must be wrong
        if (currentAttempt[i] == 1) break gapLengthLoop;
        currentAttempt[i] = 0;
      }
      //call function recursively
      generateRCPossibilities(clues, currentAttempt, gapID + 1, endBefore + gapLength);
    }
  }
}
