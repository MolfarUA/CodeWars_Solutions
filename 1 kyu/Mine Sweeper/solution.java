import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;



/** HELPER CLASS */
class Pos extends ArrayList<Integer> {
    public Pos(int x, int y)                      {super(Arrays.asList(x,y));}
}

/** HELPER CLASS */
class PosSet extends HashSet<Pos> {
    public PosSet()                               {super();}
    public PosSet(Pos pos)                        {super(); this.add(pos);}
    public PosSet(Collection<Pos> cp)             {super(cp);}
    
    public PosSet addAndReturn(Pos pos)           {this.add(pos);      return this;}
    public PosSet addAllAndReturn(Set<Pos> ps)    {this.addAll(ps);    return this;}
    public PosSet removeAndReturn(Pos pos)        {this.remove(pos);   return this;}
    public PosSet removeAllAndReturn(Set<Pos> ps) {this.removeAll(ps); return this;}
    public PosSet retainAllAndReturn(Set<Pos> ps) {this.retainAll(ps); return this;}
}



class MineSweeper {
    
    
    private static boolean IS_DEBUG = false;
    private static int[][] ARROUND = new int[][] {{-1,-1}, {-1,0}, {-1,1}, {0,-1}, {0,1}, {1,-1}, {1,0}, {1,1}};
    
    private Map<Pos, String> map;
    private PosSet posToWorkOn, unknowns, flagged;
    private int nMines, lX, lY;

    
    /** MineSweeper(String board, int nMines)
     *      
     * @param board:    initial map, as a String
     * @param nMines:   number of mines in the map.
     */
    public MineSweeper(final String board, final int nMines) {
        
        Map<Pos, String> map = new HashMap<Pos, String>();
        PosSet posToWorkOn = new PosSet(), unknowns = new PosSet(), flagged = new PosSet();
        Pos coords;
        String[] lines = board.split("\n");
        
        for (int x = 0 ; x < lines.length ; x++) {
            String[] cols = lines[x].split(" ");
            for (int y = 0 ; y < cols.length ; y++) {
                coords = new Pos(x,y);
                map.put(coords, cols[y]);
                if (cols[y].equals("?")) unknowns.add(coords);
                else                     posToWorkOn.add(coords);
            }
        }
        this.map         = map;                                 // Map<Pos, String> representing the state of each scares of the board ("?", "x", "0", ...)
        this.unknowns    = unknowns;                            // Set of all the positions with a "?" 
        this.posToWorkOn = posToWorkOn;                         // Set of all the positions that have "?" square(s) in their neighborhood and only those ones (avoid the iteration on the "0" or on the squares that will have all their mines flagged afterward)
        this.flagged     = flagged;                             // Set of all the flagged positions (with a "x")
        this.nMines      = nMines;                              // mines in the board
        this.lX          = lines.length;                        // dimensions of the board, as array[lX][lY]
        this.lY          = lines[0].split(" ").length;
    }
    
    
    
    /** solve()
     * 
     * @return:  "?" if the game isn't solvable, or the string of the solved map.
     */
    public String solve() {

        PosSet archive_PosToWorkOn;                                             // Enlarge the scope of the variable
        do {
            do { archive_PosToWorkOn = new PosSet(posToWorkOn);                 // Storage for comparisons

                openAndFlag_OnTheFly();             printDebug();
                complexSearch_OpenAndFlag();        printDebug();
                
            } while (!archive_PosToWorkOn.equals(posToWorkOn));
            
            complexSearch_CombineOnBorders();       printDebug();
            
        } while (!archive_PosToWorkOn.equals(posToWorkOn));
        
        if (nMines == flagged.size())                            openThosePos(new PosSet(unknowns));   // Use a copy of unknowns because the set will be modified during the execution (iteration)
        else if (nMines == flagged.size() + unknowns.size())     flagThosePos(new PosSet(unknowns));   // Use a copy of unknowns because the set will be modified during the execution (iteration)
        printDebug();
        
        return unknowns.isEmpty() ? stringify() : "?";
    }
    
    
    
    /** stringify()
     *  @return a string version of the current state of the map.
     */
    private String stringify(){
        
        String[][] arrMap = new String[lX][lY];
        for (int x = 0 ; x < lX ; x++) for (int y = 0 ; y < lY ; y++) arrMap[x][y] = map.get(Arrays.asList(x,y));
        return Arrays.stream(arrMap)
                     .map( line -> String.join(" ", line))
                     .collect(Collectors.joining("\n"));
    }
    
    
    /** printDebug()
     *  Print the current state of the map to the console
     */
    private void printDebug() { if (IS_DEBUG) System.out.println("-----------------\n" + stringify()); }
    
    
    /** getValAt(Pos coords)
     * 
     * @param coords: coordinates in the map, as (x,y) <=> arrMapEquiv[x][y]. (x,y) has to match to a numeric String.
     * @return        the int value corresponding to the location asked for.
     */
    private int getValAt(final Pos coords) { return Integer.parseInt(map.get(coords)); }
    
    
    /** getNeighbors(final Pos coords)
     * 
     * @param coords: coordinates in the map ((x,y) as would be for arrMapEquiv[x][y]).
     *                (x,y) has to match to a numeric String in the game map.
     * @return:       PosSet of all the coordinates (Pos) of the neighbors (existing or not)
     */
    private PosSet getNeighbors(final Pos coord){
        
        PosSet neigh = new PosSet();
        for (int[] deltas : ARROUND) neigh.add(new Pos(deltas[0] + coord.get(0),
                                                       deltas[1] + coord.get(1)));
        return neigh;
    }
    
    
    /** lookAroundThisPos(final Pos coord)
     * 
     * @param coord: location from where to look around
     * @return:      a Map<String, PosSet> containing sets of coordinates that are either "?" or "x" around 
     *               the current position, in the associated fields ("?" and "x").
     */
    private Map<String, PosSet> lookAroundThisPos(final Pos coord){
        
        Map<String, PosSet> BigBrother = new HashMap<String, PosSet>();
        BigBrother.put("?", new PosSet());
        BigBrother.put("x", new PosSet());
        
        for (Pos neigh : getNeighbors(coord)) { 
            if (map.getOrDefault(neigh, "").equals("?"))   BigBrother.get("?").add(neigh);
            if (map.getOrDefault(neigh, "").equals("x"))   BigBrother.get("x").add(neigh);
        }
        return BigBrother;
    }
    
    
    /** flagThosePos(final PosSet posSet)
     * 
     * @param posSet: set of all the coordinates to flag. Update the map, remove the
     *                positions from the "unknowns" set and add them to the "flagged" one.
     */
    private void flagThosePos(final PosSet posSet){
        
        for (Pos pos: posSet) 
            map.put(pos, "x");
        unknowns.removeAll(posSet);
        flagged.addAll(posSet);
    }
    
    
    /** openThosePos(final PosSet posSet)
     * 
     * @param posSet: Set of all the coordinates to open. Update the map, remove the positions from
     *                the "unknowns" set and add them to "posToWorkOn" if the opened pos isn't "0".
     * @return:       True if some positions have been removed from unknowns (so, if squares have 
     *                been opened), false otherwise.
     */
    private boolean openThosePos(final PosSet posSet){
        
        for (Pos pos: posSet) {
            map.put(pos, String.valueOf( Game.open(pos.get(0), pos.get(1)) ));
            if (!map.get(pos).equals("0")) posToWorkOn.add(pos);
        }
        return unknowns.removeAll(posSet);
    }
    
    
    /** openablePosAround_FlagOnTheFly(final Pos pos)
     *      Analyze the squares around the "pos" argument and:
     *          - search for openable unknown squares around
     *          - search for squares around that can be flagged and flag them 
     *          - identify if we can get rid of the current "pos" (posToWorkOn) 
     * 
     * @param pos:  position in the map that is worked on.
     * @return      array of size 2 of PosSets: 1) coordinates of all the Pos that will be opened
     *                                          2) coordinates of all Pos that will be removed from posToWorkOn
     */
    private PosSet[] openablePosAround_FlagOnTheFly(final Pos pos) {
        
        Map<String, PosSet> around = lookAroundThisPos(pos);
        PosSet[] ans = new PosSet[] {new PosSet(), new PosSet()};                       // first set: positions that can be opened / second: position to remove from posToWorkOn 
        
        if ( getValAt(pos) == around.get("?").size() + around.get("x").size()) {        // All the unknown squares can be or are already flagged...
            flagThosePos(around.get("?"));                                              // ...flag those that aren't yet...
            ans[1].add(pos);                                                            // ... and prepare the removing of this position from posToWorkOn.
        
        } else if (getValAt(pos) == around.get("x").size())                             // All mines around already found: assign pos to the "openable set"
            ans[0].addAll(around.get("?"));
        
        return ans;
    }
    
    
    /** openAndFlag_OnTheFly()
     *      Run through posToWorkOn to search for simple matches:
     *          - either positions with already the good number of flagged squares around.
     *          - or exact matches between the number of remaining mines to find against the number of "?" around.
     *      Open all the "?" that can be opened around the different positions, flag all those that can be flagged 
     *      (100% sure), and remove the positions from posToWorkOn if all informations about their neighborhood 
     *      becomes useless.
     *      Do that in a loop, while modifications are made (either open or flag some squares or remove some
     *      position from posToWorkOn).  
     */
    private void openAndFlag_OnTheFly() {
        
        PosSet openables, getRidOfThem;
        do {openables = new PosSet(); getRidOfThem = new PosSet();                  // Initialized at each loop (needed for the "while" check)
            
            for (Pos pos: posToWorkOn) {                                            // Data accumulation 
                PosSet[] tmp =  openablePosAround_FlagOnTheFly(pos);
                openables.addAll(tmp[0]);
                getRidOfThem.addAll(tmp[1]);
            }
        } while (openThosePos(openables) | posToWorkOn.removeAll(getRidOfThem));    // Execute while modifications are made (DO NOT use shortcut boolean operator!)
    }
    
    
    /** complexSearch_OpenAndFlag()
     *      Complex algorithm, using clever assumptions and comparisons to deduce things...
     *      Open or flag appropriately some squares if possible.
     */
    private void complexSearch_OpenAndFlag(){

        PosSet openables = new PosSet(),
               markables = new PosSet();
            
        for (Pos pos: posToWorkOn) {                                            // Data accumulation 
            PosSet[] tmp =  Intelligencia_OpenAndFlag(pos);
            openables.addAll(tmp[0]);
            markables.addAll(tmp[1]);
        }
        openThosePos(openables);
        flagThosePos(markables);
    }
    
    
    /** Intelligencia_OpenAndFlag(Pos pos)
     * 
     * @param pos:  The "?" square that is seeing the doctor
     * @return      Array of PosSets: 1) PosSet of squares that can be opened
     *                                2) PosSet of squares that can be flagged
     */
    private PosSet[] Intelligencia_OpenAndFlag(final Pos pos) {
        
        Map<String, PosSet> mapAround = lookAroundThisPos(pos);                                     // Map of the '?' and 'x' squares around the current Pos
        
        int[]  rMines           = new int[] {getValAt(pos) - mapAround.get("x").size(), 0};         // Prepare an array with: 1) the number of remaining mines to find for the current position / 2)same for the neighbor that will be worked on later
        PosSet neighToWorkOn    = getNeighbors(pos).retainAllAndReturn(posToWorkOn),                // Neighbors to work on (only useful ones... Meaning: self.getValAt(posNeighbour) is a number and this neighbor still misses some mines)
               openables        = new PosSet(),                                                     // Set of positions that will be open
               markables        = new PosSet();                                                     // Set of positions that will be flagged
        List<PosSet> knownParts = new ArrayList<PosSet>();                                          // list of each intersections of the '?' squares of the current Pos and each of its neighbors
        
        for (Pos pos2 : neighToWorkOn) {
            
            Map<String, PosSet> mapAround2 = lookAroundThisPos(pos2);                                                               // Map of the '?' and 'x' squares around the current neighbor
            
            rMines[1]      = getValAt(pos2) - mapAround2.get("x").size();                                                           // Update the number of mines still to find for the current neighbor
            PosSet[] onlys = new PosSet[] {new PosSet(mapAround.get("?" )).removeAllAndReturn(mapAround2.get("?")),
                                           new PosSet(mapAround2.get("?")).removeAllAndReturn(mapAround.get("?" ))};                // Define the '?' that are owned only by the current Pos (first element), and only by the current neighbor ("pos2" / second element)
            
            int r0 = rMines[0] - onlys[0].size(),
                r1 = rMines[1] - onlys[1].size();
            int mInter = r0 > r1 ? r0 : r1;                                                                                         // Define the minimum (yes "minimum", even if "max" is used!) number of mines that HAVE TO BE in the '?' squares that are owned at the same time by Pos and it's current neighbor pos2
            
            if (mInter <= 0 || !(rMines[0] == 1 || rMines[1] == 1)) continue;                                                       // In these cases, there is nothing to "guess" at the current position...
            
            PosSet currentIntersect = new PosSet(mapAround.get("?")).retainAllAndReturn(mapAround2.get("?"));                       // Calculate the current intersection of "?" of Pos and "?" of the current neighbor
            if (!currentIntersect.isEmpty()) knownParts.add(currentIntersect);                                                      // Store (only if it exists to avoid the addition of empty sets in the List) the current intersection of '?' cases for further checks
            
            for (int i = 0 ; i < 2 ; i++) {                                                                                         // Work on the two current "LOCATIONS" (Pos, pos2)
                if (onlys[i].size() == rMines[i]-mInter) markables.addAll(onlys[i]);                                                // The number of '?' squares that are only around the treated LOCATION matches the number mines shown at this LOCATION that are out of the intersection "Pos & pos2". So, those squares will be flagged
                else if (mInter == rMines[i])            openables.addAll(onlys[i]);                                                // If the number of mines surely present in the intersection "Pos & pos2" matches the number of mines still to found around the current LOCATION, all the squares that are out of the intersection can be opened
            }
        }
        
        PosSet unionIntersects = new PosSet();
        for (PosSet ps: knownParts) unionIntersects.addAll(ps);                                                                     // Union of all the intersections for the current position and its different neighbors
        if (knownParts.size() == rMines[0] && unionIntersects.size() == knownParts.stream().mapToInt( ps -> ps.size() ).sum()) {    // If some '?' squares of the current location weren't involved in any intersection while we can be sure that all the remaining mines are elsewhere (even without knowing their exact position), these leftovers squares can be opened
            mapAround.get("?").removeAll(unionIntersects);  // WARNING : mutate the Map. But it's never used after that...
            openables.addAll(mapAround.get("?"));
        }
        
        return new PosSet[] {openables, markables};
    }
    

    
    
    private void complexSearch_CombineOnBorders(){
        
        int rMines = nMines - flagged.size();                                                                                               // Number of remaining mines to flag
        if (rMines == 0 || rMines == unknowns.size())  return;                                                                              // Quick exit : the system is perfectly determined, so no need for combinations
        
        List<PosSet> matchPos   = new ArrayList<PosSet>();                                                                                  // List that will contain all the Sets of flagged positions that matches the number of mines of all known "posToWorkOn"
        PosSet border           = new PosSet();
        for (Pos pos: posToWorkOn) border.addAll(lookAroundThisPos(pos).get("?"));                                                          // Extract the "?" squares that are "on the border" (reduce the domain of combinations needed) 
        
        printDebug();
        
        Set<PosSet> combinations = generateAllCombinations(border,                                                                          // Calculate all the combinations 
                                                           new PosSet(unknowns).removeAllAndReturn(border).isEmpty() ? rMines : 1,          // Minimum of mines to combine: if the "borders" correspond to all the unknown "?" squares, fill in the exact number of remaining mines, 1 otherwise.  
                                                           rMines <= border.size()-1  ? rMines : border.size()-1);                          // Maximum of mines to combine: at most, rMines, at least the number of squares on the "border" (minus 1, to fasten a bit the combinations)
        
        for (PosSet psOfMines: combinations) {                                                                                              // for each combination found, check if the positions of all the mine are coherent with the number of mines of the squares from "posToWorkOn" 
            boolean isNotBroken = true;
            for (Pos pos: posToWorkOn) {
                Map<String, PosSet> mapAround = lookAroundThisPos(pos);
                if (getValAt(pos) != mapAround.get("x").size() + new PosSet(mapAround.get("?")).retainAllAndReturn(psOfMines).size() ) {    // count of mines isn't good, break
                    isNotBroken = false;
                    break;
                }
            }
            if (isNotBroken) matchPos.add(psOfMines);                                                                                       // if the loop didn't break, add the current combination to the list of the valid ones. 
        }
        
        if (matchPos.size() == 1) flagThosePos(matchPos.get(0));                                                                            // only one solution: flag all the found position of the combination.
        printDebug();
        
        PosSet untouched = border.removeAllAndReturn( matchPos.stream().flatMap( ps -> ps.stream() ).collect(Collectors.toSet()) );         // Search for "?" squares that were never flagged in the different combinations (these squares can be opened !)
        openThosePos(untouched);
    }
    
    
    /** generateAllCombinations(PosSet posToCombine, int minComb, int maxComb)
     * 
     * @param posToCombine: Set of the positions of the unknown squares in which the combinations are made.
     * @param minComb:      minimum number of positions in one combination
     * @param maxComb:      maximum number of positions in one combination
     * @return              a Set of posSet, representing all the possible combinations from minComb to maxComb positions, amidst the initial set of positions.
     */
    private Set<PosSet> generateAllCombinations(final PosSet posToCombine, final int minComb, final int maxComb) {
        
        Set<PosSet> combs = new HashSet<PosSet>();
        if (maxComb < 1) return combs;
        
        if (minComb > maxComb)
            throw new RuntimeException("Impossible to generate combinations of n elements amidst m, with n > m");
        
        for (Pos pos: posToCombine) {
            combs.add(new PosSet(pos));                                                                 // Add a new PosSet with the current element alone
            List<PosSet> tmp = combs.stream().map( ps -> new PosSet(ps)).collect(Collectors.toList());  // Deep copy !!!
            for (PosSet ps: tmp) if (ps.size() < maxComb) ps.add(pos);                                  // Mutazione...
            combs.addAll(tmp);                                                                          // Union
        }
        combs = combs.stream().filter( ps -> ps.size() >= minComb ).collect(Collectors.toSet());        // remove to combinations with too few elements
        return combs;
    }

}
______________________________________________________________________________________
import java.util.*;

public class MineSweeper {
    private final int height;
    private final int width;
    private final int extWidth;
    private final int[] board;
    private static final int UNKNOWN = -1;
    private static final int MINE = -2;
    private int unknownMineCount;
    private final int[] neighbours;
    private final int[] extNeighbours;
    private final Queue<SingularClue> pendingCells = new ArrayDeque<>();
    private final Queue<GroupClue> pendingGroups = new ArrayDeque<>();
    private final List<GroupClue>[] clues;
    private final int[] plate;
    private int markNumber;

    public MineSweeper(String boardStr, int nMines) {
        String[] rowStrings = boardStr.split("\n");
        height = rowStrings.length;
        width = rowStrings[0].split(" ").length;
        int extHeight = height + 4;
        extWidth = width + 4;
        int area = extHeight * extWidth;
        board = new int[area];
        if (nMines < 0)
            throw new IllegalArgumentException("Negative mine count");
        unknownMineCount = nMines;
        int maxMines = height * width;
        neighbours = composeNeighbourShifts(extWidth, false);
        extNeighbours = composeNeighbourShifts(extWidth, true);
        int index = extWidth * 2 + 2; // skip 2 rows and 2 columns (border)
        for (String rowStr : rowStrings) {
            String[] row = rowStr.split(" ");
            if (row.length != width)
                throw new IllegalArgumentException("Board is not rectangular");
            Arrays.fill(board, index, index + width, UNKNOWN);
            for (String s : row) {
                if (!s.equals("?")) {
                    determined(index, checkedAdjMines(Integer.parseInt(s)));
                    maxMines--;
                }
                index++;
            }
            index += 4; // skip right and left borders
        }
        if (unknownMineCount > maxMines)
            error();
        clues = cluesArray(area);
        plate = new int[area];
    }

    private static int checkedAdjMines(int mineCount) {
        if (mineCount >= 0 || mineCount <= 8)
            return mineCount;
        throw new RuntimeException("Wrong mine count: " + mineCount);
    }

    private static void error() {
        throw new IllegalArgumentException("Inconsistent board");
    }

    @SuppressWarnings("unchecked")
    private static List<GroupClue>[] cluesArray(int area) {
        return new List[area];
    }

    private static int[] composeNeighbourShifts(int rowSize, boolean extended) {
        int maxD = extended ? 2 : 1;
        int size = 2 * maxD + 1;
        int area = size * size;
        if (extended)
            area -= 4; // exclude corners
        int[] result = new int[area];
        int i = 0;
        for (int dy = -maxD; dy <= maxD; dy++)
            for (int dx = -maxD; dx <= maxD; dx++) {
                if (extended && Math.abs(dx) == maxD && Math.abs(dy) == maxD)
                    continue;
                result[i++] = rowSize * dy + dx;
            }
        return result;
    }

    private String composeOutput() {
        assert unknownMineCount == 0;
        StringBuilder sb = new StringBuilder();
        int cell = extWidth * 2 + 2;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int state = board[cell];
                if (state == MINE)
                    sb.append('x');
                else {
                    int nMines = 0;
                    for (int nShift : neighbours)
                        if (board[cell + nShift] == MINE)
                            nMines++;
                    if (state != nMines && state != UNKNOWN)
                        error();
                    sb.append(nMines);
                }
                sb.append(' ');
                cell++;
            }
            int lastCharIndex = sb.length() - 1;
            if (y < height - 1) {
                sb.setCharAt(lastCharIndex, '\n');
                cell += 4;
            } else
                sb.setLength(lastCharIndex);
        }
        return sb.toString();
    }

    private static class SingularClue {
        final int cell; // index in the board array
        final int value; // number of adjacent mines, or MINE if the cell itself contains a mine

        SingularClue(int cell, int value) {
            this.cell = cell;
            this.value = value;
        }
    }

    private void determined(int cell, int value) {
        int currenState = board[cell];
        if (currenState == UNKNOWN) {
            if (value == MINE) {
                if (unknownMineCount == 0)
                    error();
                unknownMineCount--;
            } else if (value == UNKNOWN)
                value = checkedAdjMines(Game.open(cell / extWidth - 2, cell % extWidth - 2)); // reveal
            board[cell] = value;
            pendingCells.add(new SingularClue(cell, value));
        } else if ((currenState == MINE) ^ (value == MINE))
            error();
    }

    private void determined(int[] cells, boolean mines) {
        int value = mines ? MINE : UNKNOWN;
        for (int cell : cells)
            determined(cell, value);
    }

    private static class GroupClue {
        // group consists of cells completely contained in some 3 x 3 square;
        // all of them are undetermined at the time of creation of this clue
        final int[] group;
        final int mineCount; // total number of mines in the group

        GroupClue(int[] group, int mineCount) {
            this.group = group;
            this.mineCount = mineCount;
        }
    }

    private void enqueueGroup(int[] group, int mineCount) {
        assert mineCount > 0 && mineCount < group.length;
        pendingGroups.add(new GroupClue(group, mineCount));
    }

    private int centerOf(int[] group) {
        int minX = width - 1;
        int minY = height - 1;
        for (int cell : group) {
            int x = cell % extWidth;
            if (x < minX)
                minX = x;
            int y = cell / extWidth;
            if (y < minY)
                minY = y;
        }
        return extWidth * (minY + 1) + (minX + 1);
    }

    private void processSingularClue(SingularClue clue) {
        int cell = clue.cell;
        int mineCount = clue.value;
        int mineInCenter = mineCount == MINE ? 1 : 0;
        for (int nShift : neighbours) {
            List<GroupClue> nClues = clues[cell + nShift];
            if (nClues == null)
                continue;
            Iterator<GroupClue> it = nClues.iterator();
            while (it.hasNext()) {
                GroupClue gClue = it.next();
                int[] group = gClue.group;
                int n = group.length;
                int i = 0;
                while (i < n && group[i] != cell)
                    i++;
                if (i == n)
                    continue;
                it.remove();
                int mc = gClue.mineCount - mineInCenter;
                n--;
                assert mc >= 0 && mc <= n;
                if (mc == 0 || mc == n) {
                    int value = mc == 0 ? UNKNOWN : MINE;
                    for (int j = 0; j <= n; j++)
                        if (j != i)
                            determined(group[j], value);
                } else {
                    int[] newGroup = new int[n];
                    System.arraycopy(group, 0, newGroup, 0, i);
                    System.arraycopy(group, i + 1, newGroup, i, n - i);
                    enqueueGroup(newGroup, mc);
                }
            }
        }
        if (mineInCenter == 0) {
            int unc = 0; // undetermined neighbours count
            for (int nShift : neighbours) {
                int nState = board[cell + nShift];
                if (nState == UNKNOWN)
                    unc++;
                else if (nState == MINE)
                    mineCount--;
            }
            if (mineCount < 0 || mineCount > unc)
                error();
            if (unc > 0) {
                boolean allKnown = mineCount == 0 || mineCount == unc;
                int[] group = allKnown ? null : new int[unc];
                int value = mineCount == 0 ? UNKNOWN : MINE;
                int i = 0;
                for (int nShift : neighbours) {
                    int nCell = cell + nShift;
                    if (board[nCell] == UNKNOWN)
                        if (allKnown)
                            determined(nCell, value);
                        else
                            group[i++] = nCell;
                }
                if (!allKnown)
                    enqueueGroup(group, mineCount);
            }
        }
    }

    private void processGroupClue(GroupClue clue) {
        int[] group = clue.group;
        int mineCount = clue.mineCount;
        int uc = 0; // the number of still undetermined cells in group
        for (int cell : group) {
            int state = board[cell];
            if (state == UNKNOWN)
                uc++;
            else if (state == MINE)
                mineCount--;
        }
        if (mineCount < 0 || mineCount > uc)
            error();
        if (uc != group.length) {
            if (uc == 0)
                return;
            boolean allKnown = mineCount == 0 || mineCount == uc;
            int[] newGroup = allKnown ? null : new int[uc];
            int value = mineCount == 0 ? UNKNOWN : MINE;
            int i = 0;
            for (int cell : group)
                if (board[cell] == UNKNOWN)
                    if (allKnown)
                        determined(cell, value);
                    else
                        newGroup[i++] = cell;
            if (allKnown)
                return;
            else
                clue = new GroupClue(newGroup, mineCount);
        }
        int[] leftGroup = clue.group;
        int center = centerOf(leftGroup);
        markNumber++;
        for (int cell : leftGroup)
            plate[cell] = markNumber;
        int leftMines = clue.mineCount;
        for (int nShift : extNeighbours) {
            List<GroupClue> nClues = clues[center + nShift];
            if (nClues == null)
                continue;
            Iterator<GroupClue> it = nClues.iterator();
            while (it.hasNext()) {
                // Juxtapose two group clues
                GroupClue nClue = it.next();
                int[] rightGroup = nClue.group;
                int intrSize = 0; // intersection size
                for (int cell : rightGroup)
                    if (plate[cell] == markNumber)
                        intrSize++;
                if (intrSize < 2)
                    continue;
                int leftOnly = leftGroup.length - intrSize;
                int rightOnly = rightGroup.length - intrSize;
                int rightMines = nClue.mineCount;
                int mineDiff = rightMines - leftMines;
                if (mineDiff < -leftOnly || mineDiff > rightOnly)
                    error();
                if (leftOnly == 0 || rightOnly == 0 || leftOnly == -mineDiff || rightOnly == mineDiff) {
                    if (leftOnly == 0 && rightOnly == 0) // leftGroup coincides with rightGroup
                        return;
                    it.remove();
                    int intrMines = leftOnly == 0 || rightOnly == mineDiff ? leftMines : rightMines;
                    int[] leftDifference = new int[leftOnly];
                    int[] intersection = new int[intrSize];
                    int[] rightDifference = new int[rightOnly];
                    int i = 0;
                    int j = 0;
                    markNumber++;
                    for (int cell : rightGroup)
                        if (++plate[cell] == markNumber)
                            intersection[i++] = cell;
                        else
                            rightDifference[j++] = cell;
                    i = 0;
                    for (int cell : leftGroup)
                        if (plate[cell] != markNumber)
                            leftDifference[i++] = cell;
                    if (leftOnly != 0) {
                        int leftOnlyMines = leftMines - intrMines;
                        if (leftOnlyMines == 0)
                            determined(leftDifference, false);
                        else if (leftOnlyMines == leftOnly)
                            determined(leftDifference, true);
                        else
                            enqueueGroup(leftDifference, leftOnlyMines);
                    }
                    enqueueGroup(intersection, intrMines);
                    if (rightOnly != 0) {
                        int rightOnlyMines = rightMines - intrMines;
                        if (rightOnlyMines == 0)
                            determined(rightDifference, false);
                        else if (rightOnlyMines == rightOnly)
                            determined(rightDifference, true);
                        else
                            enqueueGroup(rightDifference, rightOnlyMines);
                    }
                    return;
                }
            }
        }
        List<GroupClue> clueList = clues[center];
        if (clueList == null) {
            clueList = new LinkedList<>();
            clues[center] = clueList;
        }
        clueList.add(clue);
    }

    private static final int EDGE_SIZE_THRESHOLD = 15;

    private boolean reanimateQueue() {
        int unknownCount = 0;
        int unknEdgeSize = 0;
        Map<Integer, Integer> edgeIndexMap = new HashMap<>();
        List<int[]> groupList = new ArrayList<>();
        List<Integer> mineCountList = new ArrayList<>();
        int[] group = new int[8];
        for (int y = 0; y < height; y++)
            for (int cell = extWidth * (y + 2) + 2, end = cell + width; cell < end; cell++) {
                int adjMines = board[cell];
                if (adjMines < 0) { // UNKNOWN or MINE
                    if (adjMines == UNKNOWN)
                        unknownCount++;
                    continue;
                }
                int unknNeighbours = 0;
                for (int nShift : neighbours) {
                    if (nShift == 0)
                        continue;
                    int neighbour = cell + nShift;
                    int nState = board[neighbour];
                    if (nState == UNKNOWN) {
                        Integer index = edgeIndexMap.putIfAbsent(neighbour, unknEdgeSize);
                        if (index == null)
                            index = unknEdgeSize++;
                        group[unknNeighbours++] = index;
                    } else if (nState == MINE)
                        adjMines--;
                }
                if (unknNeighbours == 0)
                    continue;
                groupList.add(Arrays.copyOf(group, unknNeighbours));
                assert adjMines > 0 && adjMines < unknNeighbours;
                mineCountList.add(adjMines);
            }
        if (unknownCount == unknownMineCount) {
            for (int cell = 0, end = board.length; cell < end; cell++)
                if (board[cell] == UNKNOWN)
                    determined(cell, MINE);
            return true;
        }
        if (unknEdgeSize == 0 || unknEdgeSize > EDGE_SIZE_THRESHOLD)
            return false;
        int knownEdgeSize = groupList.size();
        int[][] groups = new int[knownEdgeSize][];
        int[] mineCounts = new int[knownEdgeSize];
        for (int i = 0; i < knownEdgeSize; i++) {
            groups[i] = groupList.get(i);
            mineCounts[i] = mineCountList.get(i);
        }
        int minEdgeMines = unknownMineCount - (unknownCount - unknEdgeSize);
        boolean[][] possibleMines = new boolean[unknEdgeSize][2]; // mine states for each cell in solutions
        outer:
        for (int edge = 0, end = 1 << unknEdgeSize; edge < end; edge++) {
            int mineCount = Integer.bitCount(edge);
            if (mineCount < minEdgeMines || mineCount > unknownMineCount)
                continue;
            for (int i = 0; i < knownEdgeSize; i++) {
                mineCount = mineCounts[i];
                for (int j : groups[i])
                    mineCount -= edge >> j & 1;
                if (mineCount != 0)
                    continue outer;
            }
            // solution on the edge of unknowns found
            for (int j = 0; j < unknEdgeSize; j++)
                possibleMines[j][edge >> j & 1] = true;
        }
        if (!possibleMines[0][0] && !possibleMines[0][1]) // no solution
            error();
        boolean certainFound = false;
        for (Map.Entry<Integer, Integer> e : edgeIndexMap.entrySet()) {
            int index = e.getValue();
            if (possibleMines[index][0] ^ possibleMines[index][1]) {
                certainFound = true;
                determined(e.getKey(), possibleMines[index][1] ? MINE : UNKNOWN);
            }
        }
        return certainFound;
    }

    public String solve() {
        while (unknownMineCount > 0) {
            SingularClue cClue = pendingCells.poll();
            if (cClue != null) {
                processSingularClue(cClue);
                continue;
            }
            GroupClue gClue = pendingGroups.poll();
            if (gClue != null) {
                processGroupClue(gClue);
                continue;
            }
            if (reanimateQueue())
                continue;
            else
                return "?"; // cannot solve
        }
        return composeOutput();
    }
}
________________________________________________________________
import java.util.*;
import java.util.function.IntToLongFunction;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import static java.lang.Math.*;

class MineSweeper /*implements PrintTest */ {

    private static final int UNKNOWN = -1;
    private static final int MINE = -2;

    private final int[][] board;
    private final int[][] boardReturn;
    private final int height;
    private final int width;
    private final TreeMap<Integer, TreeSet<Integer>> hvGroupByMineNumber;
    private int leftMines;
    private boolean boardChanged = true;

    public MineSweeper(final String board, final int nMines) {
        this.board = Stream.of(board.split("\n"))
                .map(s -> Arrays.stream(s.split(" "))
                        .mapToInt(sc -> sc.charAt(0))
                        .map(i -> (i == '?') ? UNKNOWN : i - '0')
                        .toArray())
                .toArray(int[][]::new);
        this.boardReturn = Arrays.stream(this.board).map(int[]::clone).toArray(int[][]::new);
        this.height = this.board.length;
        this.width = this.board[0].length;
        println("height " + height + " width " + width);

        this.hvGroupByMineNumber = new TreeMap<>();
        IntStream.range(0, 9).forEach(i -> hvGroupByMineNumber.put(i, new TreeSet<>()));
        allHv().filter(hv -> this.board[hv >> 8][hv & 0xff] == 0)
                .forEach(zeroHv -> hvGroupByMineNumber.get(0).add(zeroHv));
        println("get zeros " + hvGroupByMineNumber.get(0).stream().map(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | ")));

        this.leftMines = nMines;
    }

    public String solve() {
        while (boardChanged) {
            boardChanged = false;
            println("solved mines ----------------------------------");
            println("now has \n" + hvGroupByMineNumber.entrySet().stream().map(e -> e.getKey() + ":" + e.getValue().stream().map(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | "))).collect(Collectors.joining("\n")));
            hvGroupByMineNumber.forEach((n, hvSet) -> {
                if (hvSet.isEmpty())
                    return;
                // hv each number
                println("board:\n" + Arrays.stream(board)
                        .map(ary -> Arrays.stream(ary)
                                .mapToObj(i -> (i == -1) ? "?" : (i == -2) ? "x" : String.valueOf((char) (i + '0')))
                                .collect(Collectors.joining(" "))
                        ).collect(Collectors.joining("\n")));
                println("boardReturn :\n" + toString());
                for (Integer originHv : hvSet.stream().mapToInt(i -> i).toArray())
                    if (n == board[originHv >> 8][originHv & 0xff]) {
                        Set<Integer> unknownAround = around(originHv).filter(aroundHv -> board[aroundHv >> 8][aroundHv & 0xff] == UNKNOWN).collect(HashSet::new, HashSet::add, HashSet::addAll);
                        println("start solve " + (originHv >> 8) + ", " + (originHv & 0xff) + " " + unknownAround.size() + " unknowns around :" + unknownAround.stream().map(ahv -> (ahv >> 8) + ", " + (ahv & 0xff)).collect(Collectors.joining(" | ")));
                        if (unknownAround.size() > 0) {
                            if (n == unknownAround.size()) {
                                println("targetMines");
                                targetMines(unknownAround);
                                boardChanged = true;
                            } else if (n == 0) {
                                println("open");
                                open(unknownAround);
                                hvSet.remove(originHv);
                                boardChanged = true;
                            } else {
                                final int number = solveByRelation(originHv, n, unknownAround);
                                println("need to use relation. now number is " + number + " unknowns are {" + unknownAround.stream().map(ahv -> (ahv >> 8) + ", " + (ahv & 0xff)).collect(Collectors.joining(" | ")) + "}");
                                if (unknownAround.size() > 0)
                                    if (number == unknownAround.size()) {
                                        println("targetMines");
                                        targetMines(unknownAround);
                                        boardChanged = true;
                                    } else if (number == 0) {
                                        println("opening");
                                        open(unknownAround);
                                        boardChanged = true;
                                    }
                            }
                        } else {
                            hvSet.remove(originHv);
                        }
                    }
            });
            if (!boardChanged && allHv().anyMatch(hv -> boardReturn[hv >> 8][hv & 0xff] == UNKNOWN)) { // salvage (最后抢救一下)
                println("salvage time ----------------------------------");
                int[] unknownHvs = allHv().filter(hv -> board[hv >> 8][hv & 0xff] == UNKNOWN).toArray();
                /*
                 *    1  [?] <?>
                 *   [?] [?] <?>
                 *   <?> <?> <?>
                 *  [nearUnknown]  <hiddenUnknown>
                 */
                Predicate<int[]> canSalvage = mineHvs -> {
                    int[][] boardClone = Arrays.stream(this.board).map(int[]::clone).toArray(int[][]::new);
                    boolean notExcessive = Arrays.stream(mineHvs).allMatch(mineHv -> around(mineHv)
                            .filter(mineAroundHv -> boardClone[mineAroundHv >> 8][mineAroundHv & 0xff] >= 0)
                            .allMatch(mineAroundHv -> --boardClone[mineAroundHv >> 8][mineAroundHv & 0xff] >= 0));
                    boolean allNumberUsed = allHv().allMatch(hv -> boardClone[hv >> 8][hv & 0xff] <= 0);
                    println(((notExcessive && allNumberUsed) ? "perfect match !" : "no match") + " if mines are " + Arrays.stream(mineHvs).mapToObj(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | ")));
                    return notExcessive && allNumberUsed;
                };
                Map<Boolean, List<Integer>> nearAndHidden = Arrays.stream(unknownHvs)
                        .boxed()
                        .collect(Collectors.groupingBy(unknownHv -> around(unknownHv).anyMatch(hv -> board[hv >> 8][hv & 0xff] >= 0)));
                List<Integer> nearUnknowns = nearAndHidden.getOrDefault(true, Collections.emptyList());
                List<Integer> hiddenUnknowns = nearAndHidden.getOrDefault(false, Collections.emptyList());
                println("board has [" + nearUnknowns.size() + "(near), " + hiddenUnknowns.size() + "(hidden)" + " ? blocks , " + leftMines + " mines left");
                if (leftMines == 0) {
                    Arrays.stream(unknownHvs).forEach(hv -> boardReturn[hv >> 8][hv & 0xff] = Game.open(hv >> 8, hv & 0xff));
                } else if (hiddenUnknowns.size() == leftMines && nearUnknowns.size() == 0) {
                    hiddenUnknowns.forEach(mineHv -> boardReturn[mineHv >> 8][mineHv & 0xff] = MINE);
                } else if (hiddenUnknowns.size() > 0 && nearUnknowns.size() > leftMines && leftMines > hiddenUnknowns.size()
                        && IntStream.rangeClosed(leftMines - hiddenUnknowns.size(), leftMines - 1)
                        .boxed()
                        .flatMap(length -> combine(nearUnknowns.size(), length))
                        .map(indexes -> Arrays.stream(indexes).map(nearUnknowns::get).toArray())
                        .noneMatch(canSalvage)) {
                    println("salvage continue");
                    open(new HashSet<>(hiddenUnknowns));
                    boardChanged = true;
                } else {
                    println("start combine [" + nearUnknowns.size() + "(near)] by (" + abs(hiddenUnknowns.size() - leftMines) + " to " + min(nearUnknowns.size(), leftMines) + ")");
                    Set<Integer> nearUnknownsSet = new HashSet<>(nearUnknowns);
                    List<int[]> possibilities = IntStream.rangeClosed(abs(leftMines - hiddenUnknowns.size()), min(nearUnknowns.size(), leftMines))
                            .boxed()
                            .flatMap(length -> combine(nearUnknowns.size(), length))
                            .map(indexes -> Arrays.stream(indexes).map(nearUnknowns::get).toArray())
                            .filter(canSalvage)
                            .peek(possibility -> nearUnknownsSet.removeAll(Arrays.stream(possibility).boxed().collect(Collectors.toSet())))
                            .collect(Collectors.toList());
                    if (possibilities.size() == 1) {
                        println("salvage success");
                        Arrays.stream(possibilities.get(0))
                                .peek(i -> leftMines--)
                                .forEach(mineHv -> boardReturn[mineHv >> 8][mineHv & 0xff] = MINE);
                        if (leftMines != 0)
                            hiddenUnknowns
                                    .forEach(mineHv -> boardReturn[mineHv >> 8][mineHv & 0xff] = MINE);
                        Arrays.stream(unknownHvs)
                                .filter(hv -> boardReturn[hv >> 8][hv & 0xff] == UNKNOWN)
                                .forEach(hv -> boardReturn[hv >> 8][hv & 0xff] = Game.open(hv >> 8, hv & 0xff));
                    } else if (possibilities.size() > 1 && nearUnknownsSet.size() > 0) {
                        println("salvage continue");
                        open(nearUnknownsSet);
                        boardChanged = true;
                    } else {
                        println("salvage failed because perfect match contains all near or empty: \n" + possibilities.stream().map(hvs -> Arrays.stream(hvs).mapToObj(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | "))).collect(Collectors.joining("\n")));
                        return "?";
                    }

                }
            }

        }
        return toString();
    }


    private int solveByRelation(int hv, int number, Set<Integer> unknownHvs) {
        HashSet<Integer> clone = unknownHvs.stream().collect(HashSet::new, HashSet::add, HashSet::addAll);
        for (Integer unknownHv : clone) {
            for (int aroundUnknownHv : around(unknownHv).toArray()) {
                if (aroundUnknownHv != hv) {
                    int h = aroundUnknownHv >> 8;
                    int v = aroundUnknownHv & 0xff;
                    if (board[h][v] > 0 && board[h][v] <= number) {
                        HashSet<Integer> unknowns = around(aroundUnknownHv)
                                .filter(aroundAroundAroundHv -> board[aroundAroundAroundHv >> 8][aroundAroundAroundHv & 0xff] == UNKNOWN)
                                .collect(HashSet::new, HashSet::add, HashSet::addAll);
                        if (unknownHvs.containsAll(unknowns)) {
                            unknownHvs.removeAll(unknowns);
                            number -= board[h][v];
                        }
                    }
                }
            }
        }
        return number;
    }

    private void open(Set<Integer> safesHv) {
        println("start open >>> " + safesHv.stream().map(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | ")));
        for (int hv : safesHv) {
            int h = hv >> 8;
            int v = hv & 0xff;
            if (board[h][v] != UNKNOWN)
                continue;
            boardReturn[h][v] = Game.open(h, v);
            board[h][v] = boardReturn[h][v];
            println("open " + h + ", " + v + " and get number " + board[h][v]);
            long minesAround = around(hv).filter(mineHv -> board[mineHv >> 8][mineHv & 0xff] == MINE).count();
            board[h][v] -= minesAround;
            println(minesAround + " mines around, actuary number is " + board[h][v]);
            hvGroupByMineNumber.get(board[h][v]).add(hv);
        }
    }

    private void targetMines(Set<Integer> minesHv) {
        println("start targetMines >>> " + minesHv.stream().map(hv -> (hv >> 8) + ", " + (hv & 0xff)).collect(Collectors.joining(" | ")));
        for (int mineHv : minesHv) { // solved mine hv around each number hv
            int h = mineHv >> 8;
            int v = mineHv & 0xff;
            boardReturn[h][v] = MINE;
            board[h][v] = boardReturn[h][v];
            leftMines--;
            println(leftMines + " mines left");

            around(mineHv).forEach(mineAroundHv -> { // the hv around solved mine hv around each number hv
                int aroundH = mineAroundHv >> 8;
                int aroundV = mineAroundHv & 0xff;
                if (board[aroundH][aroundV] > 0) {
                    println("count down " + board[aroundH][aroundV] + " to " + (board[aroundH][aroundV] - 1) + " from " + (aroundH) + ", " + (aroundV));
                    hvGroupByMineNumber.get(board[aroundH][aroundV]).remove(mineAroundHv);
                    hvGroupByMineNumber.get(--board[aroundH][aroundV]).add(mineAroundHv);
                }
            });
        }
    }

    @Override
    public String toString() {
        return Arrays.stream(boardReturn)
                .map(ary -> Arrays.stream(ary)
                        .mapToObj(i -> (i == -1) ? "?" : (i == -2) ? "x" : String.valueOf((char) (i + '0')))
                        .collect(Collectors.joining(" "))
                ).collect(Collectors.joining("\n"));
    }

    private Stream<int[]> combine(int arrayLength, int combineLength) {
        IntToLongFunction factorial = (int n) -> {
            long result = 1;
            for (int factor = 2; factor <= n; factor++) {
                result *= factor;
            }
            return result;
        };
        long size = factorial.applyAsLong(arrayLength) / (factorial.applyAsLong(combineLength) * factorial.applyAsLong(arrayLength - combineLength));
        return Stream.iterate(IntStream.range(0, combineLength).toArray(), combine -> {
            combine = combine.clone();
            int i = combine.length - 1;
            while (i >= 0) {
                if (combine[i] != arrayLength - (combineLength - i)) {
                    combine[i]++;
                    if (i != combineLength - 1) {
                        for (int j = i + 1; j < combineLength; j++) {
                            combine[j] = combine[j - 1] + 1;
                            if (combine[j] == arrayLength)
                                return null;
                        }
                    }
                    return combine;
                } else i--;
            }
            return null;
        }).limit(size);
    }

    private IntStream allHv() {
        return IntStream.range(0, height).flatMap(h -> IntStream.range(0, width).map(v -> (h << 8) + v));
    }

    private IntStream around(int hv) {
        int h = hv >> 8, v = hv & 0xff;
        return IntStream.rangeClosed(max(0, h - 1), min(h + 1, height - 1))
                .flatMap(i -> IntStream.rangeClosed(max(0, v - 1), min(v + 1, width - 1)).map(j -> (i << 8) + j))
                .filter(roundHv -> roundHv != hv);
    }

    private void println(Object s) {
        // TODO if you need log
    }
}
___________________________________________________________
import java.util.List;
import java.util.ArrayList;
class MineSweeper {
    private List<List<Box>> boxes = new ArrayList<>();
    private List<List<Box>> testingBoxes = new ArrayList<>();
    private List<Box> unknownBoxes = new ArrayList<>();
    private List<Box> group = new ArrayList<>();
    private int missingMines = 0;
    private int totalMines;
    private boolean unsolvable = false;
    public MineSweeper(final String board, final int nMines) {
    
        totalMines = nMines;
        GenerateMatrix(board);
        
        do
        {
          LogicalSweeping();
          GetUnknowns(); 
          if(missingMines >= 10)
          {
            unsolvable = true; 
          }
          else if(missingMines > 0)
          {
            testingBoxes.clear();
            List<Integer> no = new ArrayList<>();
            RecurringFunction(0, missingMines-1, no);
            MakePossibleGroups();
            OpenNewBoxes();
          }
        }
        while(missingMines > 0 && !unsolvable);
    }
    
    public String solve() {
        
        if(unsolvable) return "?";
        
        String answer = "";
        for (int i = 0; i < boxes.size(); i++) {
            for (int j = 0; j < boxes.get(i).size(); j++) {
             //   System.out.print(boxes.get(i).get(j).number + " ");
             if (boxes.get(i).get(j).status == 2)
                answer += boxes.get(i).get(j).number + " ";
             else 
                answer += "x ";
             }
            answer = answer.substring(0, answer.length()-1);
            answer += "\n";
        }
        return answer.substring(0, answer.length()-1);
    }
    
    private void GenerateMatrix(final String board)
    {
        List<Box> _box = new ArrayList<>();
        int row = 0;
        int col = 0;
        for(int i = 0; i < board.length(); i++) 
        {
            if(board.charAt(i) != ' ')
            {
              if(board.charAt(i) != '\n')
                {
                    Box b;
                    switch (board.charAt(i)) 
                    {
                        case '0': b = new Box(row, col, 2, 0); //status 2 = opened. number 0
                            break;
                        default: b = new Box(row, col, 1, -1);// status 1 = closed. number -1 (unknown)
                            break;
                    }
                    _box.add(b);
                    col++;
                }
                else
                {
                   boxes.add(_box);
                   _box = new ArrayList<>();
                   row++; 
                   col = 0;
                }  
            }
        }
        boxes.add(_box);
    }
    
    private void LogicalSweeping()
    {
        boolean iamdone = false;
        int preCount = 0;
        int postCount = 0;
        while(!iamdone)
        {
            iamdone = true;
            for (int i = 0; i < boxes.size(); i++) 
            {
              for (int j = 0; j < boxes.get(i).size(); j++) 
              {
                if(boxes.get(i).get(j).iamdone == false && boxes.get(i).get(j).status == 2)
                {
                  if(boxes.get(i).get(j).number == 0)
                    boxes.get(i).get(j).LookAroundZero();
                  else
                    boxes.get(i).get(j).LookAroundNonZero();
                }
                if(boxes.get(i).get(j).iamdone == true)
                  postCount++;
              }
            }
            if(preCount != postCount)
            {
              iamdone = false;
              preCount = postCount;
              postCount = 0;
            }
        }
    }
    
    private void GetUnknowns()
    {
        unknownBoxes.clear();
        missingMines = 0;
        for (int i = 0; i < boxes.size(); i++) 
          {
            for (int j = 0; j < boxes.get(i).size(); j++) 
            {
              if(boxes.get(i).get(j).status == 1)
              {
                unknownBoxes.add(boxes.get(i).get(j));
                boxes.get(i).get(j).iDontHaveAMine = true;
              }
              else if(boxes.get(i).get(j).status == 3)
              {
                missingMines++;
              }
            }
          } 
        missingMines = totalMines - missingMines;
        if(missingMines == unknownBoxes.size())
        {
          for (int i = 0; i < unknownBoxes.size(); i++)
          {
            unknownBoxes.get(i).status = 3;
          }
          missingMines = 0;
        }
        else if(missingMines == 0)
        {
          for (int i = 0; i < unknownBoxes.size(); i++)
          {
            unknownBoxes.get(i).Open();
          }
        }
    }
    
   
    private void MakePossibleGroups()
    {
        boolean result;
        for(int i = 0; i < testingBoxes.size(); i++)
        {
            result = true;
            for(int j = 0; j < testingBoxes.get(i).size(); j++)
            {
                testingBoxes.get(i).get(j).status = 3;
            }
          
            for (int k = 0; k < boxes.size(); k++) 
            {
              for (int l = 0; l < boxes.get(k).size(); l++) 
              {
                if((boxes.get(k).get(l).status == 1|| boxes.get(k).get(l).status == 2) && boxes.get(k).get(l).number != 0)
                {
                    if (boxes.get(k).get(l).Finalize() == false)
                    {
                      result = false;
                      break;
                    }
                 }
               }
               if(result == false) break;
            }
            for(int j = 0; j < testingBoxes.get(i).size(); j++)
            {
              testingBoxes.get(i).get(j).status = 1;
              if(result) testingBoxes.get(i).get(j).iDontHaveAMine = false;
            }
        }
    }
    
    private void OpenNewBoxes()
    {
      unsolvable = true;
      for (int i = 0; i < unknownBoxes.size(); i++) 
      {
        if(unknownBoxes.get(i).iDontHaveAMine)
        {
          unknownBoxes.get(i).Open(); 
          unsolvable = false;
        }
      }
    }
    
    private void RecurringFunction(int a, int b, List<Integer> no)
    {
     for(int i = a; i < unknownBoxes.size() - b ; i++)
      {
        no.add(i);
        if(b == 0)
        {
          group = new ArrayList<>();
          for(int j = 0; j < no.size(); j++)
          {
            group.add(unknownBoxes.get(no.get(j)));
          }
          testingBoxes.add(group);
          
        }
        else
        {
          RecurringFunction(i + 1, b - 1, no);
        }
        no.remove(no.size() - 1);
      }
      
    }
    
    private class Box
    {
        public int row;
        public int col;
        public int status; //?
        public int number;
        public boolean iamdone = false;
        public boolean iDontHaveAMine = true;
        
        private int mines;
        private List<Box> unknowns = new ArrayList<>();
        private int knowns;
        
        public Box(int _row, int _col, int _status, int _number)
        {
            row = _row; 
            col = _col; 
            status = _status; 
            number = _number;
        }
        
        public void setStatus(int s)
        {
            status = s;
        }
        
        public void Open()
        {
            setStatus(2);
            number = Game.open(row,col);
        }
               
        public void LookAroundZero()
        {
          iamdone = true;
          for(int m = row - 1; m <= row + 1; m++)
            {
                for(int n = col - 1; n <= col + 1; n++)
                {
                    if(m >= 0 && m < boxes.size() && n >= 0 && n < boxes.get(0).size() && (m != row || n != col) )
                     boxes.get(m).get(n).Open();
                }
            }
        }
        
        public void LookAroundNonZero()
        {
             LookAroundToAnalyse();
                      
             if(number == mines)
              {
                for (int i = 0; i < unknowns.size(); i++) {
                  unknowns.get(i).Open();
                }
                iamdone = true;
              }
              else if (number == unknowns.size() + mines)
              {
                for (int i = 0; i < unknowns.size(); i++) {
                    unknowns.get(i).setStatus(3);
                    unknowns.get(i).iamdone = true;
                }
              }
            
         }
         
        public boolean Finalize()
        {
           LookAroundToAnalyse();
           if(status == 1)
           {
               if(mines == 0) return false;
               else return true;
           }
           if(number == mines)
               return true;
           else
               return false;  
        }
        
        private void LookAroundToAnalyse()
        {
          mines = 0; knowns = 0; unknowns.clear();
          
            for(int m = row - 1; m <= row + 1; m++)
            {
                for(int n = col - 1; n <= col + 1; n++)
                {
                    if(m >= 0 && m < boxes.size() && n >= 0 && n < boxes.get(0).size() && (m != row || n != col) )
                    {
                        switch (boxes.get(m).get(n).status) 
                            {
                                case 1: unknowns.add(boxes.get(m).get(n));
                                    break;
                                case 2: knowns++;
                                    break;
                                case 3: mines++;
                                    break;
                                default:
                                    break;
                            }
                    }
                }
            }
        }
    }
}
