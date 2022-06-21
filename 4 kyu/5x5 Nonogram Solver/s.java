5a479247e6be385a41000064


import java.util.Arrays;


public class Nonogram {

    private static int[] baseSolutions(int[] in){
        if(Arrays.equals(in, new int[]{0})){
            return new int[]{0, 0, 0, 0, 0};
        } else if(Arrays.equals(in, new int[]{1, 1, 1})){
            return new int[]{1, 0, 1, 0, 1};
        } else if(Arrays.equals(in, new int[]{1, 3})){
            return new int[]{1, 0, 1, 1, 1};
        } else if(Arrays.equals(in, new int[]{2, 2})){
            return new int[]{1, 1, 0, 1, 1};
        } else if(Arrays.equals(in, new int[]{3, 1})){
            return new int[]{1, 1, 1, 0, 1};
        } else if(Arrays.equals(in, new int[]{5})){
            return new int[]{1, 1, 1, 1, 1};
        } else if(Arrays.equals(in, new int[]{4})){
            return new int[]{-1, 1, 1, 1, -1};
        } else if(Arrays.equals(in, new int[]{3})){
            return new int[]{-1, -1, 1, -1, -1};
        } else if(Arrays.equals(in, new int[]{2,1})) {
            return new int[]{-1, 1, -1, -1, -1};
        } else if(Arrays.equals(in, new int[]{1,2})){
                return new int[]{-1, -1, -1, 1, -1};
        } else
            return null;
    }

    public static int[][] solve(int[][][] clues) {

        //result tömb készítése és feltöltése -1-gyel
        int[][] result = new int[5][5];
        for (int[] ints : result) {
            System.arraycopy(new int[]{-1, -1, -1, -1, -1},0, ints,0,5);
        }

        //össz kocka és megoldott kocka deklarálás
        int solvedAmount = 0;
        int allAmount = 0;

        //össz kocka megszámolása
        allAmount = Arrays.stream(clues[0]).flatMapToInt(Arrays::stream).sum();

        //biztos sorok feltöltése
        for (int i = 0; i < 5; i++) {
            int[] rowValue= clues[1][i];
            if(baseSolutions(rowValue)!=null){
                System.arraycopy(baseSolutions(rowValue),0,result[i],0,5);
            }
        }

        //biztos oszlopok feltöltés
        for (int i = 0; i < 5; i++) {
            int[] columnValue = clues[0][i];
            if (baseSolutions(columnValue) != null){
                int[] actSolution = baseSolutions(columnValue);
                for (int j = 0; j < 5; j++) {
                    if (result[j][i] == -1){
                        result[j][i] = actSolution[j];
                    }
                }
            }
        }

        //végső kitötés
        while(solvedAmount<allAmount){
            //sorok
            for (int i = 0; i < 5; i++) {
                int[] rowValue = clues[1][i];
                int[] actSolution = furtherSolutions(rowValue,result[i]);
                if (actSolution != null) {
                    for (int j = 0; j < 5; j++) {
                        if (result[i][j] == -1 && actSolution[j] != -1) result[i][j] = actSolution[j];
                    }
                }
            }
            //oszlopok
            for (int i = 0; i < 5; i++) {
                int[] columnValue= clues[0][i];
                int[] actColumn = new int[5];
                for (int j = 0; j < 5; j++) {
                    actColumn[j] = result[j][i];
                }
                int[] actSolution = furtherSolutions(columnValue, actColumn);
                if (actSolution != null) {
                    for (int j = 0; j < 5; j++) {
                        if (result[j][i] == -1 && actSolution[j] != -1) result[j][i] = actSolution[j];
                    }
                }
            }
            solvedAmount = Arrays.stream(result).flatMapToInt(Arrays::stream).sum();
        }


        return result;
    }

    private static int[] furtherSolutions(int[] in, int[] sample){
        if(Arrays.equals(in, new int[]{1})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
        } else if(Arrays.equals(in, new int[]{1, 1})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
            else if (sample[0] == 1) return new int[]{1, 0, -1, -1, -1};
            else if (sample[1] == 1) return new int[]{0, 1, 0, -1, -1};
            else if (sample[2] == 1) return new int[]{-1, 0, 1, 0, -1};
            else if (sample[3] == 1) return new int[]{-1, -1, 0, 1, 0};
            else if (sample[4] == 1) return new int[]{-1, -1, -1, 0, 1};
        } else if(Arrays.equals(in, new int[]{1, 2})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
            else if (sample[4] == 1 || sample[2] == 0) return new int[]{-1, -1, 0, 1, 1};
            else if (sample[0] == 1 || sample[1] == 0) return new int[]{1, 0, -1, -1, -1};
            else if (sample[4] == 0  || sample[2] == 1) return new int[]{1, 0, 1, 1, 0};
            else if (sample[0] == 0  || sample[1] == 1) return new int[]{0, 1, 0, 1, 1};
        } else if(Arrays.equals(in, new int[]{2})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
            else if (sample[0] == 1) return new int[]{1, 1, 0, 0, 0};
            else if (sample[4] == 1) return new int[]{0, 0, 0, 1, 1};
            else if (sample[1] == 1 || sample[3] == 0) return new int[]{-1, 1, -1, 0, 0};
            else if (sample[2] == 1) return new int[]{0, -1, 1, -1, 0};
            else if (sample[3] == 1 || sample[1] == 0) return new int[]{0, 0, -1, 1, -1};
        } else if(Arrays.equals(in, new int[]{2, 1})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
            else if (sample[0] == 1 || sample[2] == 0) return new int[]{1, 1, 0, -1, -1};
            else if (sample[4] == 1 || sample[3] == 0) return new int[]{-1, -1, -1, 0, 1};
            else if (sample[0] == 0  || sample[2] == 1) return new int[]{0, 1, 1, 0, 1};
            else if (sample[4] == 0  || sample[3] == 1) return new int[]{1, 1, 0, 1, 0};
        } else if(Arrays.equals(in, new int[]{3})){
            if(fullFill(in,sample) != null){
                return fullFill(in,sample);
            }
            else if (sample[1] == 0  || sample[4] == 1) return new int[]{0, 0, 1, 1, 1};
            else if (sample[0] == 1 || sample[3] == 0) return new int[]{1, 1, 1, 0, 0};
            else if (sample[1] == 1 || sample[4] == 0) return new int[]{-1, 1, 1, -1, 0};
            else if (sample[3] == 1  || sample[0] == 0) return new int[]{0, -1, 1, 1, -1};
        } else if(Arrays.equals(in, new int[]{4})){
            if (sample[0] == 1 || sample[4] == 0) return new int[]{1, 1, 1, 1, 0};
            else if (sample[0] == 0 || sample[4] == 1) return new int[]{0, 1, 1, 1, 1};
        }
        return null;
    }

    private static int[] fullFill(int[] clues, int[] sample){
        if(Arrays.stream(clues).sum() == Arrays.stream(sample).filter(a -> a==1).count()){
            return Arrays.stream(sample)
                    .map(a -> {
                        if(a == -1) return 0;
                        return -1;
                    })
                    .toArray();
        } else if (Arrays.stream(clues).sum() == 5 - Arrays.stream(sample).filter(a -> a==0).count()){
            return Arrays.stream(sample)
                    .map(a -> {
                        if(a == -1) return 1;
                        return -1;
                    })
                    .toArray();
        }
        return null;
    }

}
__________________________
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Nonogram {


    private static HashMap<String, int[][]> operations = new HashMap<>() {{
        put("5", new int[][]{{1, 1, 1, 1, 1}});
        put("3,1", new int[][]{{1, 1, 1, -1, 1}});
        put("1,3", new int[][]{{1, -1, 1, 1, 1}});
        put("2,2", new int[][]{{1, 1, -1, 1, 1}});
        put("1,1,1", new int[][]{{1, -1, 1, -1, 1}});
        put("4", new int[][]{{1, 1, 1, 1, -1}, {-1, 1, 1, 1, 1}});
        put("3", new int[][]{{1, 1, 1, -1, -1}, {-1, 1, 1, 1, -1}, {-1, -1, 1, 1, 1}});
        put("1,2", new int[][]{{1, -1, 1, 1, -1}, {1, -1, -1, 1, 1}, {-1, 1, -1, 1, 1}});
        put("2,1", new int[][]{{1, 1, -1, 1, -1}, {1, 1, -1, -1, 1}, {-1, 1, 1, -1, 1}});
        put("2", new int[][]{{1, 1, -1, -1, -1}, {-1, 1, 1, -1, -1}, {-1, -1, 1, 1, -1}, {-1, -1, -1, 1, 1}});
        put("1", new int[][]{{1, -1, -1, -1, -1}, {-1, 1, -1, -1, -1}, {-1, -1, 1, -1, -1}, {-1, -1, -1, 1, -1}, {-1, -1, -1, -1, 1}});
        put("1,1", new int[][]{{1, -1, 1, -1, -1}, {1, -1, -1, 1, -1}, {1, -1, -1, -1, 1}, {-1, 1, -1, 1, -1}, {-1, 1, -1, -1, 1}, {-1, -1, 1, -1, 1}});
    }};

    private static String asClue(int[] row) {
        return Arrays.stream(row).mapToObj(v -> Integer.toString(v)).collect(Collectors.joining(","));
    }

    private static boolean canMerge(int[] existing, int[] testing) {
        for (int i = 0; i < existing.length; ++i) {
            if (existing[i] == -1 && testing[i] > 0 || testing[i] == -1 && existing[i] > 0) return false;
        }
        return true;
    }

    private static List<int[]> findMatches(String clue, int[] currentRow) {
        var poss = operations.get(clue);
        if (poss == null) throw new Error("Clue not found " + clue);
        return Arrays.stream(poss).filter(v -> canMerge(currentRow, v)).collect(Collectors.toList());
    }


    private static boolean isSolved(int[][] board, List<String> vclues) {
        if (Arrays.stream(board).anyMatch(l -> Arrays.stream(l).anyMatch(v -> v == 0))) return false;
        for (int i = 0; i < board.length; ++i) {
            final int j = i;
            var lst = Arrays.stream(board).map(l -> Integer.toString(l[j])).collect(Collectors.joining(","));
            var oneMatch = Arrays.stream(operations.get(vclues.get(j))).anyMatch(c -> asClue(c).equals(lst));
            if (!oneMatch) return false;
        }
        return true;
    }

    private static int[][] attemptConstruct(int[][] map, List<String> hClues, List<String> vClues, final int index) {
        if (isSolved(map, vClues)) return map;
        if (index >= hClues.size()) return null;

        var currentClue = hClues.get(index);
        final var before = map[index].clone();
        var matches = findMatches(currentClue, before);
        for (var m : matches) {
            map[index] = m.clone();
            var subMap = attemptConstruct(map, hClues, vClues, index + 1);
            if (subMap != null) {
                return subMap;
            }
        }
        map[index] = before;
        return null;
    }

    private static int[][] normalize(int[][] map) {
        for (var l : map) {
            for (int i = 0; i < l.length; ++i) {
                l[i] = Math.max(l[i], 0);
            }
        }
        return map;
    }

    public static int[][] solve(int[][][] clues) {
        return normalize(attemptConstruct(new int[5][5],
                Arrays.stream(clues[1]).map(i -> asClue(i)).collect(Collectors.toList()),
                Arrays.stream(clues[0]).map(i -> asClue(i)).collect(Collectors.toList()),
                0));
    }

}
__________________________
import java.util.Arrays;

public class Nonogram {
    private static final int SIZE = 5;
    private static final int CLUE_INDEX_BITS;
    private static final int[] FIBO = new int[SIZE + 1];
    private static final int POSSIBLE_LINES = 1 << SIZE;
    private static final int POSSIBLE_TABLES = 1 << (SIZE * SIZE);
    private static final int[] ROW_TO_COLUMN = new int[POSSIBLE_LINES];
    private static final int LINE_MASK = POSSIBLE_LINES - 1;
    private static final int[] TABLE_TO_SIDE_CLUES = new int[POSSIBLE_TABLES];
    static {
        FIBO[0] = 1;
        FIBO[1] = 2;
        for (int n = 2; n <= SIZE; n++)
            FIBO[n] = FIBO[n - 2] + FIBO[n - 1];
        CLUE_INDEX_BITS = Integer.SIZE - Integer.numberOfLeadingZeros(FIBO[SIZE] - 1);
        int[] lineToClueIndex = new int[POSSIBLE_LINES];
        int[] clue = new int[(SIZE + 1) / 2];
        for (int line = 0; line < POSSIBLE_LINES; line++) {
            int x = line;
            int k = -1;
            boolean space = true;
            for (int i = 0; i < SIZE; i++) {
                if ((x & 1) == 0)
                    space = true;
                else if (space) {
                    clue[++k] = 1;
                    space = false;
                } else
                    clue[k]++;
                x >>= 1;
            }
            lineToClueIndex[line] = clueToIndex(Arrays.copyOf(clue, k + 1));
            x = line;
            int y = 0;
            int t = 1;
            for (int i = 0; i < SIZE; i++) {
                if ((x & 1) != 0)
                    y += t;
                x >>= 1;
                t <<= SIZE;
            }
            ROW_TO_COLUMN[line] = y;
        }
        for (int table = 0; table < POSSIBLE_TABLES; table++) {
            int verticalClues = 0;
            int x = table;
            for (int i = 0; i < SIZE; i++) {
                verticalClues <<= CLUE_INDEX_BITS;
                verticalClues += lineToClueIndex[x & LINE_MASK];
                x >>= SIZE;
            }
            TABLE_TO_SIDE_CLUES[table] = verticalClues;
        }
    }

    private static int clueToIndex(int[] clue, int size, int begin, int subtract) {
        if (begin == clue.length) // includes the case size == 0
            return 0;
        if (size == 1)
            return 1;
        if (clue[begin] - subtract == 1)
            return 1 + clueToIndex(clue, size - 2, begin + 1, 0);
        else
            return FIBO[size - 2] + clueToIndex(clue, size - 1, begin, subtract + 1);
    }

    private static int clueToIndex(int[] clue) {
        int s = 0;
        int len = clue.length;
        for (int i = 0; i < len; i++) {
            int x = clue[i];
            s += x + 1;
            if (x <= 0 || s > SIZE + 1)
                throw new IllegalArgumentException("Wrong clues: " + Arrays.toString(clue));
        }
        return clueToIndex(clue, SIZE, 0, 0);
    }

    private static int sideCluesToIndex(int[][] clues) {
        int index = 0;
        for (int[] clue : clues) {
            index <<= CLUE_INDEX_BITS;
            index += clueToIndex(clue);
        }
        return index;
    }

    private static int transpose(int table) {
        int result = 0;
        int shift = 0;
        for (int i = 0; i < SIZE; i++) {
            result += ROW_TO_COLUMN[table & LINE_MASK] << shift++;
            table >>= SIZE;
        }
        return result;
    }

    private static int[][] tableToArray(int table) {
        int[][] result = new int[SIZE][SIZE];
        for (int[] row : result)
            for (int i = 0; i < SIZE; i++) {
                if ((table & 1) != 0)
                    row[i] = 1;
                table >>= 1;
            }
        return result;
    }

    public static int[][] solve(int[][][] clues) {
        int horizontalClues = sideCluesToIndex(clues[0]);
        int verticalClues = sideCluesToIndex(clues[1]);
        for (int table = 0; table < POSSIBLE_TABLES; table++)
            if (TABLE_TO_SIDE_CLUES[table] == verticalClues
                    && TABLE_TO_SIDE_CLUES[transpose(table)] == horizontalClues)
                return tableToArray(table);
        throw new RuntimeException("No solution for " + Arrays.deepToString(clues));
    }
}
