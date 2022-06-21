5c1d796370fee68b1e000611


import java.util.*;

public class Loopover {
    private final int height;
    private final int width;
    private final int[] board; // permutation of 0, 1, ..., area - 1, represents the current (mixed-up) board
    private final int[] position; // the inverse of the above permutation
    private final List<String> moves = new ArrayList<>();

    private Loopover(char[][] mixedUpBoard, char[][] solvedBoard) {
        height = solvedBoard.length;
        width = solvedBoard[0].length;
        if (height < 2 || width < 2)
            throw new IllegalArgumentException("Board is too small");
        int area = height * width;
        board = new int[area];
        position = new int[area];
        Map<Character, Integer> indexMap = new HashMap<>(); // maps characters to their positions in solvedBoard
        int i = 0;
        for (char[] row : solvedBoard) {
            if (row == null || row.length != width)
                throw new IllegalArgumentException("Ragged solvedBoard");
            for (char c : row)
                if (indexMap.put(c, i++) != null)
                    throw new IllegalArgumentException("Duplicate symbol in solvedBoard: " + c);
        }
        if (mixedUpBoard.length != height)
            throw new IllegalArgumentException("mixedUpBoard of different height");
        i = 0;
        for (char[] row : mixedUpBoard) {
            if (row == null || row.length != width)
                throw new IllegalArgumentException("Wrong mixedUpBoard's row size");
            for (char c : row) {
                Integer p = indexMap.put(c, -1);
                if (p == null)
                    throw new IllegalArgumentException("This symbol does not appear in solvedBoard: " + c);
                else if (p < 0)
                    throw new IllegalArgumentException("Duplicate symbol in mixedUpBoard: " + c);
                board[i] = p;
                position[p] = i++;
            }
        }
    }

    private static boolean oddPermutation(int[] perm) {
        boolean parity = false;
        for (int i = 1, len = perm.length; i < len; i++) {
            int pi = perm[i];
            for (int j = 0; j < i; j++)
                parity ^= perm[j] > pi;
        }
        return parity;
    }

    private List<String> slide(boolean row, int line, int crossLineFrom, int crossLineTo) {
        int dist = crossLineTo - crossLineFrom;
        boolean forward = dist > 0;
        if (!forward)
            dist = -dist;
        int supl = (row ? width : height) - dist;
        if (supl < dist) {
            dist = supl;
            forward ^= true;
        }
        char dirChar = row ? (forward ? 'R' : 'L') : (forward ? 'D' : 'U');
        String slideCode = dirChar + Integer.toString(line);
        return Collections.nCopies(dist, slideCode);
    }

    // (row1, col1) -> (row1, col2) -> (row2, col1) -> (row1, col1), or backwards
    private void rotateTriple(int row1, int row2, int col1, int col2, boolean reverse) {
        List<String> slide1 = slide(false, col1, row2, row1);
        List<String> slide2 = slide(true, row1, col2, col1);
        List<String> slide3 = slide(false, col1, row1, row2);
        List<String> slide4 = slide(true, row1, col1, col2);
        if (reverse) {
            moves.addAll(slide2);
            moves.addAll(slide1);
            moves.addAll(slide4);
            moves.addAll(slide3);
        } else {
            moves.addAll(slide1);
            moves.addAll(slide2);
            moves.addAll(slide3);
            moves.addAll(slide4);
        }
        int index1 = row1 * width + col1;
        int index2 = row1 * width + col2;
        int index3 = row2 * width + col1;
        if (reverse) {
            int t = index1;
            index1 = index3;
            index3 = t;
        }
        int value1 = board[index1];
        int value2 = board[index2];
        int value3 = board[index3];
        board[index2] = value1;
        board[index3] = value2;
        board[index1] = value3;
        position[value1] = index2;
        position[value2] = index3;
        position[value3] = index1;
    }

    private void putInPlace(int y, int x) {
        int dest = y * width + x;
        int src = position[dest];
        if (src == dest)
            return;
        int ys = src / width;
        int xs = src % width;
        if (x == xs) {
            int x2 = x < width - 1 ? x + 1 : x - 1;
            rotateTriple(ys, y, x, x2, true);
        } else if (y == ys) {
            int y2 = y < height - 1 ? y + 1 : y - 1;
            rotateTriple(y, y2, xs, x, false);
        } else if (y < ys)
            rotateTriple(ys, y, x, xs, false);
        else
            rotateTriple(y, ys, xs, x, true);
    }

    private List<String> solve() {
        if (oddPermutation(board)) {
            boolean oddHeight = (height & 1) != 0;
            boolean oddWidth = (width & 1) != 0;
            if (oddHeight && oddWidth) // unsolvable
                return null;
            // Change the parity of the permutation by sliding a line of even size
            int b0 = board[0];
            if (!oddWidth) {
                moves.add("L0");
                int last = width - 1;
                for (int i = 0; i < last; i++) {
                    int x = board[i + 1];
                    board[i] = x;
                    position[x] = i;
                }
                board[last] = b0;
                position[b0] = last;
            } else {
                moves.add("U0");
                int last = (height - 1) * width;
                for (int i = 0; i < last; i += width) {
                    int x = board[i + width];
                    board[i] = x;
                    position[x] = i;
                }
                board[last] = b0;
                position[b0] = last;
            }
        }
        // The main movement
        int h2 = height - 2;
        int h1 = height - 1;
        for (int y = 0; y < h2; y++)
            for (int x = 0; x < width; x++)
                putInPlace(y, x);
        for (int x = 0, w1 = width - 1; x < w1; x++) {
            putInPlace(h2, x);
            putInPlace(h1, x);
        }
        assert board[height * width - 1] == height * width - 1;
        return moves;
    }

    public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {
        return new Loopover(mixedUpBoard, solvedBoard).solve();
    }
}

##########################################
import java.util.*;

public class Loopover {
  
  public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {    
    List<String> solution = new ArrayList<String>();
    List<String> tempMoves;
    int lastRow = mixedUpBoard.length - 1;
    int lastCol = mixedUpBoard[0].length - 1;
    
    // Solving every row but the last
    for(int row = 0; row <= lastRow - 1; row++) {
      for(int col = 0; col <= lastCol; col++) {
        int[] pos = findPos(solvedBoard[row][col], mixedUpBoard);
        tempMoves = movePiece(pos[0], pos[1], row, col);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);
      }
    }
    
    // Solving last row
    if(lastCol == 1) {
      // If 2 columns, just align last row
      if(mixedUpBoard[lastRow][0] != solvedBoard[lastRow][0]) {
        tempMoves = new ArrayList<String>(1);
        tempMoves.add("R" + lastRow);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);
      }
    } else {
      // If > 2 columns solve each piece and hope for no parity
      for(int col = 1; col <= lastCol - 1; col++) {
        int[] posNext = findPos(solvedBoard[lastRow][col], mixedUpBoard);
        int[] posPrev = findPos(solvedBoard[lastRow][col - 1], mixedUpBoard);
      
        tempMoves = solveLLPiece(posNext, posPrev, lastRow, lastCol);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);      
      }
    }
    
    // Check parity
    if(mixedUpBoard[lastRow][lastCol] != solvedBoard[lastRow][lastCol]) {
      if(lastCol % 2 == 1 || lastRow % 2 == 1) {
        // If parity is solvable, add the parity alg
        tempMoves = parityAlg(lastRow, lastCol);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);         
      } else {
        // Unsolvable parity
        return null;
      }
    }
    
    return solution;   
  }
  
  
  /**
  *  Returns the row and column of where input char should be
  *  in the solved board
  */
  private static int[] findPos(char c, char[][] mixedUpBoard) {
    for(int row = 0; row < mixedUpBoard.length; row++)
      for(int col = 0; col < mixedUpBoard[0].length; col++)
        if(c == mixedUpBoard[row][col])
          return new int[]{row, col};
    return null;
  }
  
  
  /**
  *  Returns a list of moves that moves a piece from one position to another
  *  without desturbing pieces above and left of target position
  */
  private static List<String> movePiece(int fromRow, int fromCol, int toRow, int toCol) {
    List<String> moves = new ArrayList<String>();
    
    // If piece is solved, return empty move list
    if(fromRow == toRow && fromCol == toCol)
      return moves;
    
    if(fromRow == toRow) {
      // If piece is in target row, move it out
      moves.add("D" + fromCol);
      fromRow++;
      moves.add("R" + fromRow);
      moves.add("U" + fromCol);
      moves.add("L" + fromRow);
    } else if(fromCol == toCol) {
      // If piece is in targer col, move it to the side
      moves.add("R" + fromRow);
      fromCol++;
    }
    
    // Insert the piece without desturbing toRow or erlier rows
    int dRow = fromRow - toRow;
    int dCol = Math.abs(fromCol - toCol);
    String colDir = fromCol < toCol ? "R" : "L";
    for(int i = 0; i < dRow; i++)
      moves.add("D" + toCol);
    for(int i = 0; i < dCol; i++)
      moves.add(colDir + fromRow);
    for(int i = 0; i < dRow; i++)
      moves.add("U" + toCol);
    
    return moves;
  }
  
  
  /**
  *  Returns a list of moves that puts a piece (nextPiece) to the left of
  *  another piece (prevPiece) in the last row
  */
  private static List<String> solveLLPiece(int[] nextPiece, int[] prevPiece, int lastRow, int lastCol) {
    List<String> moves = new ArrayList<String>();
    
    if(nextPiece[0] == 0) {
      // Next piece is in buffer locations (top right corner)
      int dCol = Math.abs(prevPiece[1] - (lastCol - 1));
      String colDir = prevPiece[1] < (lastCol - 1) ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      
      moves.add("U" + lastCol);
      moves.add("L" + lastRow);
      moves.add("D" + lastCol);
      
      System.out.println(moves);
      return moves;
    } else {
      // Next piece is somewhere in last row
      int dCol = Math.abs(nextPiece[1] - lastCol);
      String colDir = nextPiece[1] < lastCol ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      prevPiece[1] += dCol;
      
      moves.add("U" + lastCol);
      
      dCol = Math.abs(prevPiece[1] - (lastCol - 1));
      colDir = prevPiece[1] < (lastCol - 1) ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      
      moves.add("D" + lastCol);
      moves.add("L" + lastRow);
      
      return moves;
    }
  }
  
  
  /**
  *  Returns a list of moves that switches pieces at the
  *  top right and bottom right locations. Only works if
  *  number of rows or number of columns are even
  */
  private static List<String> parityAlg(int lastRow, int lastCol) {
    List<String> result = new ArrayList<String>();
    
    // Decide direction
    String[] moves = null;
    int[] index = null;
    if(lastCol % 2 == 1) {
      moves = new String[]{"L", "U", "D"};
      index = new int[]{lastRow, lastCol};
    } else if(lastRow % 2 == 1) {
      moves = new String[]{"U", "L", "R"};
      index = new int[]{lastCol, lastRow};
    }
    
    // Add moves
    result.add(moves[0] + index[0]);
    for(int i = 0; i <= index[1]; i++) {
      if(i % 2 == 0)
        result.add(moves[1] + index[1]);
      else
        result.add(moves[2] + index[1]);
      result.add(moves[0] + index[0]);     
    }
    
    // Add 3-cycle for parity alg with odd columns
    if(moves[0].equals("U")) {
      result.add("U" + lastCol);
      result.add("L" + lastRow);
      result.add("D" + lastCol);
      result.add("R" + lastRow);
    }
    
    return result;
  }
  
  
  /**
  *  Apply the moves in the input list to the input board
  */
  private static void applyMoves(List<String> moves, char[][] board) {
    for(String move: moves) {
      switch(move.charAt(0)) {
          case 'U': applyMove(false, Character.getNumericValue(move.charAt(1)), -1, board); break;
          case 'D': applyMove(false, Character.getNumericValue(move.charAt(1)), 1, board); break;
          case 'R': applyMove(true, Character.getNumericValue(move.charAt(1)), 1, board); break;
          case 'L': applyMove(true, Character.getNumericValue(move.charAt(1)), -1, board); break;
      }
    }
  }
  
  
  /**
  *  Apply one move to the input board  
  *
  *  @param rowOrCol: true -> row, false -> col
  */
  private static void applyMove(boolean rowOrCol, int index, int dir, char[][] board) {
    char temp;
    if(rowOrCol) {
      // Move a row
      if(dir == -1) {
        temp = board[index][0];
        for(int i = 0; i < board[index].length - 1; i++)
          board[index][i] = board[index][i + 1];
        board[index][board[index].length - 1] = temp;
      } else if (dir == 1) {
        temp = board[index][board[index].length - 1];
        for(int i = board[index].length - 1; i > 0; i--)
          board[index][i] = board[index][i - 1];
        board[index][0] = temp;
      }
    } else {
        // Move a col
      if(dir == -1) {
        temp = board[0][index];
        for(int i = 0; i < board.length - 1; i++)
          board[i][index] = board[i + 1][index];
        board[board.length - 1][index] = temp;
      } else if (dir == 1) {
        temp = board[board.length - 1][index];
        for(int i = board.length - 1; i > 0; i--)
          board[i][index] = board[i - 1][index];
        board[0][index] = temp;
      }
    }
  }
}

##################################
import java.util.*;
import java.util.function.BiPredicate;
import java.util.function.Consumer;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import static java.lang.Character.*;

public class Loopover {
    private static class Node {
        private static final Comparator<Character> ValueComparator = Node::compare;
        
        int row_num = -1, col_num = -1;
        Node up = null, down = null, left = null, right = null;
        char value = '?';
      
        public Node(char value) {
            this.value = value;
        }
        public Node(char value, int row_num, int col_num) {
            this.value = value;
            this.row_num = row_num;
            this.col_num = col_num;
        }
        public Node(char value, Node up, Node left) {
            this.value = value;
            this.up = up;
            this.left = left;

            if (up != null) {
                this.col_num = up.col_num;
                this.row_num = up.row_num+1;
            }
            else if (left != null) {
                this.col_num = left.col_num+1;
                this.row_num = left.row_num;
            }

        }
        public Node(char value, Node up, Node left, Node down, Node right) {
            this.value = value;
            this.up = up;
            this.left = left;
            this.down = down;
            this.right = right;

            if (up != null) {
                this.col_num = up.col_num;
                this.row_num = up.row_num+1;
            }
            else if (left != null) {
                this.col_num = left.col_num+1;
                this.row_num = left.row_num;
            }
            else if (down != null) {
                this.row_num = down.row_num - 1;
                this.col_num = right.col_num;
            }
            else if (right != null) {
                this.row_num = right.row_num;
                this.col_num = right.col_num - 1;
            }
        }
        
        @Override
        public String toString() {
            return Character.toString(value);
        }

        private static int compare(Character a, Character b) {
            if (getType(a) == getType(b)) {
                return a.compareTo(b);
            }
            else if (isLetterOrDigit(a) ^ isLetterOrDigit(b)) {
                return isLetterOrDigit(a)? -1 : 1;
            }
            else if (isLetter(a) ^ isLetter(b)) {
                return isUpperCase(a)? -1 : isLowerCase(b)? -1 : 1;
            }
            else if (isUpperCase(a) ^ isUpperCase(b)) {
                return isUpperCase(a) ? -1 : 1;
            }
            return a.compareTo(b);
        }
    }
    
    private final static int max_num_rows = 9, max_num_columns = 9, min_num_rows = 2, min_num_columns = 2;
    
    private final HashMap<Character, Node> characterNodeHashMap;
    private final ArrayList<String> movelist;
    private final boolean printAll;
    private final int num_rows, num_columns;
    
    Loopover (char[][] mixedUpBoard) {
        printAll = false;
        num_rows = mixedUpBoard.length;
        num_columns = mixedUpBoard[0].length;
        characterNodeHashMap = new HashMap<Character, Node>();
        movelist = new ArrayList<String>();
        Node above=null, left=null, curr=null, row_head=null, col_head;
        for (int i=0; i < num_rows; i++) {
            left = null;
            row_head = null;
            for (int j = 0; j < mixedUpBoard[i].length; j++) {
                if (i > 0)
                    above = characterNodeHashMap.get(mixedUpBoard[i-1][j]);
                curr = new Node(mixedUpBoard[i][j], above, left);
                if (row_head == null)
                    row_head = curr;
                if (above != null)
                    above.down = curr;
                if (left != null)
                    left.right = curr;
                if (curr.row_num < 0 || curr.col_num < 0) {
                    curr.col_num = 0;
                    curr.row_num = 0;
                }
                characterNodeHashMap.put(curr.value, curr);
                left = curr;
            }
            if (row_head != null)
                row_head.left = left;
            if (left != null)
                left.right = row_head;
        }
        for (int i=0; i < num_columns; i++) {
            col_head = characterNodeHashMap.get(mixedUpBoard[0][i]);
            for (curr=col_head; curr.down != null; curr=curr.down);
            col_head.up = curr;
            curr.down=col_head;
        }
    }
    Loopover (char[][] mixedUpBoard, boolean printAll) {
        this.printAll = printAll;
        num_rows = mixedUpBoard.length;
        num_columns = mixedUpBoard[0].length;
        characterNodeHashMap = new HashMap<Character, Node>();
        movelist = new ArrayList<String>();
        Node above=null, left=null, curr=null, row_head=null, col_head;
        for (int i=0; i < num_rows; i++) {
            left = null;
            row_head = null;
            for (int j = 0; j < mixedUpBoard[i].length; j++) {
                if (i > 0)
                    above = characterNodeHashMap.get(mixedUpBoard[i-1][j]);
                curr = new Node(mixedUpBoard[i][j], above, left);
                if (row_head == null)
                    row_head = curr;
                if (above != null)
                    above.down = curr;
                if (left != null)
                    left.right = curr;
                if (curr.row_num < 0 || curr.col_num < 0) {
                    curr.col_num = 0;
                    curr.row_num = 0;
                }
                characterNodeHashMap.put(curr.value, curr);
                left = curr;
            }
            if (row_head!=null)
                row_head.left = left;
            if (left != null)
                left.right = row_head;
        }
        for (int i=0; i < num_columns; i++) {
            col_head = characterNodeHashMap.get(mixedUpBoard[0][i]);
            for (curr=col_head; curr.down != null; curr=curr.down);
            col_head.up = curr;
            curr.down=col_head;
        }
    }
    
    @Override
    public String toString() {
        int offset, idx;
        StringBuilder grid = new StringBuilder(characterNodeHashMap.size() + num_rows + 1);
        grid.setLength(characterNodeHashMap.size() + num_rows);
        for (int i = 1; i <= num_rows; i++) {
            idx = i > 1 ? i * num_columns + i-1: i * num_columns;
            grid.setCharAt( idx,'\n');
        }

        for (Node n : characterNodeHashMap.values()) {
            offset = n.row_num * num_columns + n.col_num;
            offset += offset / num_columns;
            grid.setCharAt(offset, n.value);
        }
        grid.append('\n');
        return grid.toString();
    }
  
    private void moveToColumn(char target_char, int intended_col_num) {
        moveToColumn(target_char, intended_col_num, true);
    }
    private void moveToColumn(char target_char, int intended_col_num, boolean record_move) {
        Node target_node;
        int dist_left, dist_right;
        Consumer<Character> moveRight = (tar_char) -> {
            char tmp_char = characterNodeHashMap.get(tar_char).left.value;
            Node current_node = characterNodeHashMap.get(tar_char).left;
            while (true){
                current_node.value = current_node.left.value;
                current_node = current_node.left;
                if (current_node.value == target_char) {
                    current_node.value = tmp_char;
                    break;
                }
            }
            while (true) {
                assert current_node != null;
                if (characterNodeHashMap.get(current_node.value).value == current_node.value)
                    break;
                current_node = characterNodeHashMap.replace(current_node.value, current_node);
            }
        };
        Consumer<Character> moveLeft = (tar_char) -> {
            char tmp_char = characterNodeHashMap.get(target_char).right.value;
            Node current_node = characterNodeHashMap.get(target_char).right;
            while (true) {
                current_node.value = current_node.right.value;
                current_node = current_node.right;
                if (current_node.value == target_char) {
                    current_node.value = tmp_char;
                    break;
                }
            }
            while (true) {
                assert current_node != null;
                if (characterNodeHashMap.get(current_node.value).value == current_node.value)
                    break;
                current_node = characterNodeHashMap.replace(current_node.value, current_node);
            }
        };
        while (true) {
            target_node = characterNodeHashMap.get(target_char);
            if (target_node.col_num == intended_col_num)
                break;
            
            if (target_node.col_num > intended_col_num) {
                dist_left = target_node.col_num - intended_col_num;
                dist_right = num_columns - dist_left;
            } else {
                dist_right = intended_col_num - target_node.col_num;
                dist_left = num_columns - dist_right;
            }
                
            if (dist_left < dist_right) {
                moveLeft.accept(target_char);
                if (record_move) movelist.add("L" + target_node.row_num);
            } else {
                moveRight.accept(target_char);
                if (record_move) movelist.add("R" + target_node.row_num);
            }
        }
    }
    private void moveToRow(char target_char, int intended_row_num) {
      moveToRow(target_char, intended_row_num, true);
    }
    private void moveToRow(char target_char, int intended_row_num, boolean record_move) {
        Node target_node;
        int dist_up, dist_down;
        Consumer<Character> moveDown = (tar_char) -> {
            char tmp_char = characterNodeHashMap.get(tar_char).up.value;
            Node current_node = characterNodeHashMap.get(tar_char).up;
            while (true){
                current_node.value = current_node.up.value;
                current_node = current_node.up;
                if (current_node.value == target_char) {
                    current_node.value = tmp_char;
                    break;
                }
            }
            while (true) {
                assert current_node != null;
                if (characterNodeHashMap.get(current_node.value).value == current_node.value)
                    break;
                current_node = characterNodeHashMap.replace(current_node.value, current_node);
            }
        };
        Consumer<Character> moveUp = (tar_char) -> {
            char tmp_char = characterNodeHashMap.get(target_char).down.value;
            Node current_node = characterNodeHashMap.get(target_char).down;
            while (true) {
                current_node.value = current_node.down.value;
                current_node = current_node.down;
                if (current_node.value == target_char) {
                    current_node.value = tmp_char;
                    break;
                }
            }
            while (true) {
                assert current_node != null;
                if (characterNodeHashMap.get(current_node.value).value == current_node.value)
                    break;
                current_node = characterNodeHashMap.replace(current_node.value, current_node);
            }
        };

        while (true){
            target_node = characterNodeHashMap.get(target_char);
            if (target_node.row_num == intended_row_num)
                break;

            if (target_node.row_num > intended_row_num) {
                dist_up = target_node.row_num - intended_row_num;
                dist_down = num_rows - dist_up;
            } else {
                dist_down = intended_row_num - target_node.row_num;
                dist_up = num_rows - dist_down;
            }

            if (dist_up < dist_down) {
                moveUp.accept(target_char);
                if (record_move) movelist.add("U" + target_node.col_num);
            } else {
                moveDown.accept(target_char);
                if (record_move) movelist.add("D" + target_node.col_num);
            }
        }
    }

    private boolean solvePosition(int intended_row_num, int intended_col_num, char[][] solvedBoard) {
        char target_char = solvedBoard[intended_row_num][intended_col_num];
        Node target_node = characterNodeHashMap.get(target_char), displace_me = target_node, rc_handle;
        if (target_node.row_num == intended_row_num && target_node.col_num == intended_col_num)
            return true;

        if (intended_row_num == 0) {
            if (target_node.row_num == intended_row_num) {
                while (displace_me.col_num != intended_col_num)
                    if (displace_me.col_num > intended_col_num)
                        displace_me = displace_me.left;
                    else
                        displace_me = displace_me.right;
                rc_handle = target_node.up;
                moveToRow(target_char, intended_row_num + 1);
                moveToRow(displace_me.value, intended_row_num + 1);
                moveToColumn(target_char, intended_col_num);
                moveToRow(target_char, intended_row_num);
                moveToRow(rc_handle.value, intended_row_num);
            } else if (target_node.col_num == intended_col_num && intended_col_num != num_rows - 1) {
                while (displace_me.row_num != intended_row_num)
                    if (displace_me.row_num > intended_row_num)
                        displace_me = displace_me.up;
                    else
                        displace_me = displace_me.down;
                rc_handle = target_node.left;
                moveToColumn(target_char, target_node.right.col_num);
                moveToColumn(displace_me.value, characterNodeHashMap.get(target_char).col_num);
                moveToRow(target_char, intended_row_num);
                moveToColumn(target_char, intended_col_num);
                moveToColumn(rc_handle.value, intended_col_num);
            } else {
                moveToColumn(target_char, intended_col_num);
                moveToRow(target_char, intended_row_num);
            }
        }
        else if (intended_row_num < num_rows-1) {
            while (displace_me.col_num != intended_col_num) {
                if (displace_me.col_num > intended_col_num)
                    displace_me = displace_me.left;
                else
                    displace_me = displace_me.right;
            }
            while (displace_me.row_num != intended_row_num) {
                if (displace_me.row_num > intended_row_num)
                    displace_me = displace_me.up;
                else
                    displace_me = displace_me.down;
            }
            if (target_node.row_num == intended_row_num && intended_col_num != 0) {
                moveToRow(target_char, intended_row_num-1);
                moveToColumn(displace_me.value, target_node.col_num);
                moveToRow(target_char, intended_row_num);
                moveToColumn(target_char, intended_col_num);
            } else {
                if (target_node.col_num == intended_col_num) {
                    moveToColumn(target_char, target_node.right.col_num);
                }
                moveToRow(displace_me.value, target_node.row_num);
                moveToColumn(target_char, intended_col_num);
                moveToRow(target_char, intended_row_num);
            }
        } else {
            if (intended_col_num == 0)
                moveToColumn(target_char, intended_col_num);
            else {
                moveToColumn(target_char, num_columns-1);
                moveToRow(target_char, intended_row_num-1);
                char expat_value = characterNodeHashMap.get(target_char).down.value;
                moveToColumn(solvedBoard[intended_row_num][intended_col_num-1], num_columns-2);
                moveToRow(target_char, intended_row_num);
                moveToColumn(expat_value, num_columns-2);
                Node sanchk = characterNodeHashMap.get(expat_value).up;

                for (int i=0; i < num_columns; i++) {
                    if (sanchk.right.down.value != expat_value && Node.ValueComparator.compare(sanchk.right.down.value, target_char) > 0)
                        break;
                    else
                        moveToColumn(target_node.value, target_node.right.col_num);
                }
                if (Node.ValueComparator.compare(sanchk.right.down.value, target_char) > 0 || intended_col_num < num_columns-2) {
                    moveToRow(sanchk.right.value, sanchk.right.up.row_num);
                    moveToColumn(expat_value, num_columns - 1);
                    moveToRow(expat_value, characterNodeHashMap.get(expat_value).down.row_num);
                    moveToColumn(target_char, intended_col_num);
                } else {
                    BiPredicate<Node, char[][]> checkEdgesSolved = (corner, solvedboard)-> {
                        char corner_val = corner.value;
                        do {
                            if (corner.value != solvedBoard[corner.row_num][corner.col_num])
                                return false;
                            corner = corner.left;
                        } while (corner.value != corner_val);
                        do {
                            if (corner.value != solvedBoard[corner.row_num][corner.col_num])
                                return false;
                            corner = corner.up;
                        } while (corner.value != corner_val);
                        return true;
                    };
                    for (int i=0; i < num_columns/2+1; i++) {
                        moveToRow(sanchk.right.value, sanchk.right.up.row_num);
                        moveToColumn(sanchk.down.value, sanchk.down.left.col_num);
                        if (checkEdgesSolved.test(sanchk.down.right, solvedBoard)) {
                            return true;
                        }
                        moveToRow(sanchk.right.value, sanchk.right.down.row_num);
                        moveToColumn(sanchk.down.value, sanchk.down.left.col_num);
                        if (checkEdgesSolved.test(sanchk.down.right, solvedBoard)) {
                            return true;
                        }
                    }
                    moveToRow(sanchk.right.value, sanchk.right.up.up.row_num);
                    char expat_replacement;
                    for (int i = 0; i < num_rows; i++) {
                        expat_replacement = sanchk.right.down.value;
                        moveToColumn(expat_value, sanchk.right.down.col_num);
                        moveToRow(expat_value, sanchk.right.row_num);
                        expat_value = expat_replacement;
                        if (checkEdgesSolved.test(sanchk.down.right, solvedBoard))
                            return true;
                    }
                    return false;
                }
            }
        }
        return true;
    }

    public static char [][][] generateBoards() {
        return generateBoards(0, 0);
    }
    public static char [][][] generateBoards(int num_rows, int num_columns) {
        Random random = new Random();
        if (num_rows < min_num_rows || num_rows > max_num_rows)
            num_rows = random.nextInt(max_num_rows - min_num_rows + 1) + min_num_rows;
        if (num_columns < min_num_columns || num_columns > max_num_columns)
            num_columns = random.nextInt(max_num_columns - min_num_columns + 1) + min_num_columns;

        char [][][] scrambled_solved_pair_array = new char[2][num_rows][num_columns];
        Character[] custom_sorted_chars = new Character[num_rows * num_columns];

        String upper, lower, nums, symbols;
        StringBuilder choices = new StringBuilder(num_rows*num_columns);
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        lower = "abcdefghijklmnopqrstuvwxyz";
        nums = "0123456789";
        symbols = ")*+,-./:;<=>?@[\\]^_`";

        if (choices.capacity() < upper.length())
            choices.append(upper, 0, choices.capacity());
        else
            choices.append(upper);
        if (choices.length() < choices.capacity()) {
            int remaining = choices.capacity() - choices.length();
            if (remaining < nums.length())
                choices.append(nums, 0, remaining);
            else
                choices.append(nums);
        }
        if (choices.length() < choices.capacity()) {
            int remaining = choices.capacity() - choices.length();
            if (remaining < lower.length())
                choices.append(lower, 0, remaining);
            else
                choices.append(lower);
        }
        if (choices.length() < choices.capacity()) {
            int remaining = choices.capacity() - choices.length();
            if (remaining < symbols.length())
                choices.append(symbols, 0, remaining);
            else
                choices.append(symbols);
        }

        String str_choices = choices.toString();
        for (int i=0; i < choices.length(); i++)
            custom_sorted_chars[i] = str_choices.charAt(i);
        Arrays.sort(custom_sorted_chars, Node.ValueComparator);

        int idx, counter=0;
        while (choices.length()>0) {
            idx = random.nextInt(choices.length());
            scrambled_solved_pair_array[0][counter/num_columns][counter%num_columns] = choices.charAt(idx);
            scrambled_solved_pair_array[1][counter/num_columns][counter%num_columns] = custom_sorted_chars[counter++];
            choices.deleteCharAt(idx);
        }
        return scrambled_solved_pair_array;
    }
  
    public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {
        int num_rows = solvedBoard.length, num_columns = solvedBoard[0].length;
        Loopover puzzle = new Loopover(mixedUpBoard);
        for (int intended_row_num=0; intended_row_num < num_rows; intended_row_num++) {
            for (int intended_col_num=0; intended_col_num < num_columns; intended_col_num++) {
                if (!puzzle.solvePosition(intended_row_num, intended_col_num, solvedBoard)) {
                    return null;
                }
            }
        }
        return puzzle.movelist;
    }

    public static boolean verifySolution(List<String> movelist, char[][] mixedUpBoard, char[][] solvedBoard) {
        Loopover puzzle = new Loopover(mixedUpBoard);
        if (movelist == null) {
            return solvedBoard==null;
        } else if (solvedBoard==null) {
            return false;
        }
        Node handle = puzzle.characterNodeHashMap.get(mixedUpBoard[0][0]);
        int rc_num;
        for (String move : movelist) {
            rc_num = Integer.parseInt(move, 1, 2, 10);
            if (move.charAt(0) == 'L' || move.charAt(0) == 'R')
                while (handle.row_num != rc_num)
                    handle = handle.row_num < rc_num ? handle.down : handle.up;
            else
                while (handle.col_num != rc_num)
                    handle = handle.col_num < rc_num ? handle.right : handle.left;

            if (move.charAt(0) == 'L')
                puzzle.moveToColumn(handle.value, handle.left.col_num);
            else if (move.charAt(0) == 'U')
                puzzle.moveToRow(handle.value, handle.up.row_num);
            else if (move.charAt(0) == 'R')
                puzzle.moveToColumn(handle.value, handle.right.col_num);
            else if (move.charAt(0) == 'D')
                puzzle.moveToRow(handle.value, handle.down.row_num);
        }
        for (Node node: puzzle.characterNodeHashMap.values())
            if (node.value != solvedBoard[node.row_num][node.col_num])
                return false;
        return true;
    }
}
#############################
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;

enum SlideDir {
    U(-1, 0), D(1, 0), L(0, -1), R(0, 1);

    final int dr;
    final int dc;

    SlideDir(int dr, int dc) {
        this.dr = dr;
        this.dc = dc;
    }

    SlideDir opposite() {
        for (SlideDir opp : values()) {
            if (opp.dr == -dr && opp.dc == -dc) {
                return opp;
            }
        }
        return this;
    }
}

class Coords {
    final int r;
    final int c;

    public Coords(int r, int c) {
        this.r = r;
        this.c = c;
    }

    public Coords move(SlideDir dir, Coords wrap) {
        return new Coords((r + wrap.r + dir.dr) % wrap.r, (c + wrap.c + dir.dc) % wrap.c);
    }

    @Override
    public String toString() {
        return "[" + r + "," + c + "]";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coords coords = (Coords) o;
        return r == coords.r && c == coords.c;
    }

    @Override
    public int hashCode() {
        return Objects.hash(r, c);
    }
}

class SlideMove {
    final SlideDir dir;
    final Coords start;
    final int length;

    public SlideMove(SlideDir dir, int idx, Coords wrap) {
        this.dir = dir;
        if (dir.dc == 0) {
            length = wrap.r;
            start = new Coords(dir.dr > 0 ? 0 : length, idx);
        } else {
            length = wrap.c;
            start = new Coords(idx, dir.dc > 0 ? 0 : length);
        }
    }

    public SlideMove(String mv, Coords wrap) {
        this(SlideDir.valueOf(mv.substring(0, 1).toUpperCase()), Integer.parseInt(mv.substring(1)), wrap);
    }

    public String toString() {
        return dir.name() + (dir.dc == 0 ? start.c : start.r);
    }

    public SlideMove undoer(Coords wrap) {
        return new SlideMove(dir.opposite(), (dir.dc == 0 ? start.c : start.r), wrap);
    }
}

class SliderBoard {
    final char[][] rows;
    final Coords wrap;
    final List<String> moves = new ArrayList<>();

    public SliderBoard(char[][] rows) {
        this.rows = rows;
        wrap = new Coords(rows.length, rows[0].length);
        for (char[] row : rows) {
            if (row.length != wrap.c) {
                System.err.println("differing row length!=" + wrap.c + ": " + new String(row) + " " + Arrays.toString(row));
            }
        }
    }

    public static SliderBoard from(String board) {
        String[] rowtxt = board.split("\n");
        char[][] rows = new char[rowtxt.length][];
        int c = 0;
        for (int i = 0; i < rowtxt.length; ++i) {
            String rt = rowtxt[i].trim();
            rows[i] = rt.toCharArray();
        }
        return new SliderBoard(rows);
    }

    public String toString() {
        return Arrays.stream(rows).map(String::new).collect(Collectors.joining("\n"));
    }

    public char getAt(Coords pos) {
        char[] row = rows[pos.r % wrap.r];
        return row[(row.length + pos.c) % row.length];
    }

    public void setAt(Coords pos, char ch) {
        char[] row = rows[pos.r % wrap.r];
        row[(row.length + pos.c) % row.length] = ch;
    }

    public SlideMove createMove(String mv) {
        return new SlideMove(mv, wrap);
    }

    public SlideMove createMove(SlideDir dir, int idx) {
        return new SlideMove(dir, idx, wrap);
    }

    public SliderBoard applyMoves(Iterable<String> moves) {
        if (moves != null) {
            for (String mv : moves) {
                applyMove(createMove(mv));
            }
        }
        return this;
    }

    public void applyMove(SlideMove mv) {
        Coords pos = mv.start;
        char ch = getAt(pos);
        for (int i = 0; i < mv.length; ++i) {
            pos = pos.move(mv.dir, wrap);
            char nxt = getAt(pos);
            setAt(pos, ch);
            ch = nxt;
        }
        int ms = moves.size();
        if (ms > 0 && moves.get(ms - 1).equals(mv.undoer(wrap).toString())) {
            moves.remove(ms - 1);
        } else {
            moves.add(mv.toString());
        }
    }

    public Map<Character, Coords> getLocations() {
        Map<Character, Coords> locs = new LinkedHashMap<>();
        for (int r = 0; r < rows.length; ++r) {
            for (int c = 0; c < rows[r].length; ++c) {
                locs.put(rows[r][c], new Coords(r, c));
            }
        }
        if (locs.size() != wrap.r * wrap.c) {
            System.err.println("Warning duplicate symbols in " + wrap + " board " + this
                    + "; expected " + (wrap.r * wrap.c) + " but found " + locs.size() + ": " + locs);
        }
        return locs;
    }

    public Coords getLocation(char ch) {
        for (int r = 0; r < rows.length; ++r) {
            for (int c = 0; c < rows[r].length; ++c) {
                if (rows[r][c] == ch) {
                    return new Coords(r, c);
                }
            }
        }
        System.out.println("Warning! " + ch + " not found on board " + this);
        return null;
    }

    private Coords moveHorizontalTo(Coords pnt, int destc) {
        SlideDir dir;
        int nc = wrap.c;
        destc %= wrap.c;
        if (destc > pnt.c && destc - pnt.c <= nc / 2 || destc < pnt.c && pnt.c - destc > nc / 2) {
            dir = SlideDir.R;
        } else {
            dir = SlideDir.L;
        }
        while (pnt.c != destc) {
            applyMove(createMove(dir, pnt.r));
            pnt = pnt.move(dir, wrap);
        }
        return pnt;
    }

    private Coords moveVerticalTo(Coords pnt, int destr) {
        SlideDir dir;
        int nr = wrap.r;
        destr %= nr;
        if (destr > pnt.r && destr - pnt.r <= nr / 2 || destr < pnt.r && pnt.r - destr > nr / 2) {
            dir = SlideDir.D;
        } else {
            dir = SlideDir.U;
        }
        while (pnt.r != destr) {
            applyMove(createMove(dir, pnt.c));
            pnt = pnt.move(dir, wrap);
        }
        return pnt;
    }

    private Coords rotateLeftOne(Coords pnt) {
        int r = pnt.r;
        int c = pnt.c;
        applyMoves(Arrays.asList("D" + c, "R" + r, "U" + c, "L" + r, "L" + r, "D" + c, "R" + r, "U" + c));
        return pnt.move(SlideDir.L, wrap);
    }

    private Coords rotateUpOne(Coords pnt) {
        int r = pnt.r;
        int c = pnt.c;
        applyMoves(Arrays.asList("R" + r, "D" + c, "L" + r, "U" + c, "U" + c, "R" + r, "D" + c, "L" + r));
        return pnt.move(SlideDir.U, wrap);
    }

    private Coords rotateLeftTwo(Coords pnt) {
        int r = pnt.r;
        int c = (pnt.c + rows[r].length - 1) % rows[r].length;
        applyMoves(Arrays.asList("U" + c, "L" + r, "D" + c, "R" + r, "R" + r, "U" + c, "L" + r, "D" + c));
        return pnt.move(SlideDir.L, wrap).move(SlideDir.L, wrap);
    }

    boolean swapLastTwoHorizontal(Coords pnt) {
        // swap only the last two
        if ((wrap.c & 1) == 0) {
            applyMove(createMove(SlideDir.R, pnt.r));
            for (int c = 1; c < pnt.c; c += 2) {
                rotateLeftOne(new Coords(pnt.r, c));
            }
            return true;
        } else if ((wrap.r & 1) == 0) {
            applyMove(createMove(SlideDir.D, pnt.c));
            for (int r = 1; r < pnt.r; r += 2) {
                rotateUpOne(new Coords(r, pnt.c));
            }
            applyMoves(Arrays.asList("R" + pnt.r, "D" + pnt.c, "L" + pnt.r, "U" + pnt.c));
            return true;
        }
        return false;
    }

    Coords rotateHorizontal(Coords pnt, int destc) {
        while (pnt.c > destc + 1) {
            pnt = rotateLeftTwo(pnt);
        }
        if (pnt.c == destc + 1) {
            pnt = rotateLeftOne(pnt);
        }
        return pnt;
    }

    public List<String> solve(SliderBoard solvedBoard) {
        Map<Character, Coords> destinations = solvedBoard.getLocations();
        if (!destinations.keySet().equals(getLocations().keySet())) {
            System.err.println("Alphabet not equal in " + solvedBoard + " and " + this);
            return null;
        }
        for (Map.Entry<Character, Coords> lme : destinations.entrySet()) {
            Coords src = getLocation(lme.getKey());
            Coords dst = lme.getValue();
            if (!src.equals(dst)) {
                int dr = dst.r;
                int dc = dst.c;
                if (dr == 0 && dc == 0) {
                    // First location, just move it straight there
                    src = moveHorizontalTo(src, dc);
                    moveVerticalTo(src, dr);
                } else if (dr == 0) {
                    // First row
                    if (src.r == 0) {
                        // move down if already in first row
                        src = moveVerticalTo(src, 1);
                    }
                    // now move across and up into place
                    src = moveHorizontalTo(src, dc);
                    moveVerticalTo(src, dr);
                } else if (dc == 0 && src.r == dr) {
                    // First column of the new row, just move across
                    moveHorizontalTo(src, dc);
                } else if (src.r == dr && dr + 1 == wrap.r) {
                    // rotate in threes
                    if (src.c + 1 == wrap.c && dc + 2 == wrap.c) {
                        // the last two
                        if (!swapLastTwoHorizontal(src)) {
                            System.out.println("Can't solve last two of " + this);
                            return null;
                        }
                    } else {
                        rotateHorizontal(src, dc);
                    }
                } else {
                    // Below first row, have to keep first row intact
                    String undo = null;
                    if (src.r == dr) {
                        // same row, move down first
                        src = moveVerticalTo(src, src.r + 1);
                        undo = "U" + src.c;
                    } else if (src.c == dc) {
                        // same column, move right first
                        src = moveHorizontalTo(src, src.c + 1);
                        undo = "L" + src.r;
                    }
                    // move dst square down ready to receive
                    dst = moveVerticalTo(dst, src.r);
                    // move src square across to dst
                    moveHorizontalTo(src, dc);
                    // move dst square back up into place
                    moveVerticalTo(dst, dr);
                    if (undo != null) {
                        applyMove(createMove(undo));
                    }
                }
            }
        }
        return moves;
    }
}

public class Loopover {
    public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {
        return new SliderBoard(mixedUpBoard).solve(new SliderBoard(solvedBoard));
    }
}
##########################################################
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Loopover {
    public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {
        Grid grid = new Grid(mixedUpBoard, solvedBoard);
        grid.resolveInitLines();
        boolean flag = grid.resolveLastLine(0);
        return flag ? grid.steps : null;
    }

    private static class Grid {
        int[][] grid;
        int xLen;
        int yLen;
        int xCache[];
        int yCache[];

        List<String> steps = new ArrayList<>();

        Grid(char[][] mixedUpBoard, char[][] solvedBoard) {
            yLen = solvedBoard.length;
            xLen = solvedBoard[0].length;
            Map<Character, Integer> transMap = new HashMap<>();
            for (int i = 0; i < yLen; i++) {
                for (int j = 0; j < xLen; j++) {
                    transMap.put(solvedBoard[i][j], i * xLen + j);
                }
            }
            grid = new int[yLen][xLen];
            for (int i = 0; i < yLen; i++) {
                for (int j = 0; j < xLen; j++) {
                    grid[i][j] = transMap.get(mixedUpBoard[i][j]);
                }
            }
            xCache = new int[xLen]; yCache = new int[yLen];
        }

        void resolveInitLines() {
            for (int i = 0; i < yLen - 1; i++) {
                for (int j = 0; j < xLen; j++) {
                    int findX = 0, findY = 0;
                    finder:for (int ii = i; ii < yLen; ii++) {
                        for (int jj = 0; jj < xLen; jj++) {
                            if (grid[ii][jj] == i * xLen + j) {
                                findX = jj; findY = ii;
                                break finder;
                            }
                        }
                    }
                    if (i == findY && j == findX) {
                        continue;
                    } else if (i == findY) {
                        up(j, -1); up(findX, -1);
                        left(findY + 1, findX - j);
                        up(j, 1); up(findX, 1);
                    } else if (j == findX) {
                        left(findY, -1); up(findX, i - findY);
                        left(findY, 1); up(findX, findY - i);
                    } else {
                        up(j, i - findY);
                        left(findY, findX - j);
                        up(j, findY - i);
                    }
                }
            }
        }

        boolean resolveLastLine(int num) {
            int start = (yLen - 1) * xLen;
            for (int i = 0; i < xLen - 2; i++) {
                if (grid[yLen - 1][i] == start + i) continue;
                else {
                    int findX = 0;
                    for (int ii = i + 1; ii < xLen; ii++) {
                        if (grid[yLen - 1][ii] == start + i) {
                            findX = ii;
                            break;
                        }
                    }
                    if (findX == xLen - 1) {
                        left(yLen - 1, -1);
                        up(xLen - 1, -1);
                        left(yLen - 1, 1);
                        up(xLen - 1, 1);
                        left(yLen - 1, i - findX);
                        up(xLen - 1, -1);
                        left(yLen - 1, xLen - 1 - i - 1);
                        up(xLen - 1, 1);
                        left(yLen - 1, 1);
                    } else {
                        up(xLen - 1, -1);
                        left(yLen - 1, findX - xLen + 1);
                        up(xLen - 1, 1);
                        left(yLen - 1, i - findX);
                        up(xLen - 1, -1);
                        left(yLen - 1, xLen - 1 - i);
                        up(xLen - 1, 1);
                    }
                }
            }
            if (grid[yLen - 1][xLen - 2] == start + xLen - 1 && num < 5) {
                if (xLen == 2) {
                    left(yLen - 1, 1);
                    return true;
                }
                if (xLen % 2 == 1 && yLen % 2 == 0) {
                    up(xLen - 1, 1);
                    left(yLen - 1, -1);
                    up(xLen - 1, -1);
                    left(yLen - 1, 1);
                    return resolveLastLineColumn(0);
                }
                up(xLen - 1, 1);
                left(yLen - 1, 1);
                up(xLen - 1, -1);
                left(yLen - 1, 1);
                up(xLen - 1, 1);
                left(yLen - 1, -2);
                up(xLen - 1, -1);
                left(yLen - 1, 1);
                return resolveLastLine(num + 1);
            }
            for (int i = 0; i < xLen - 1; i++) {
                if (grid[yLen - 1][i] != start + i) return false;
            }
            return true;
        }

        boolean resolveLastLineColumn(int num) {
            for (int i = 0; i < yLen - 2; i++) {
                if (grid[i][xLen - 1] == (i + 1) * xLen - 1) continue;
                else {
                    int findY = 0;
                    for (int ii = i + 1; ii < yLen; ii++) {
                        if (grid[ii][xLen - 1] == (i + 1) * xLen - 1) {
                            findY = ii;
                            break;
                        }
                    }
                    if (findY == yLen - 1) {
                        up(xLen - 1, -1);
                        left(yLen - 1, -1);
                        up(xLen - 1, 1);
                        left(yLen - 1, 1);
                        up(xLen - 1, i - findY);
                        left(yLen - 1, -1);
                        up(xLen - 1, yLen - 1 - i - 1);
                        left(yLen - 1, 1);
                        up(xLen - 1, 1);
                    } else {
                        left(yLen - 1, -1);
                        up(xLen - 1, findY - yLen + 1);
                        left(yLen - 1, 1);
                        up(xLen - 1, i - findY);
                        left(yLen - 1, -1);
                        up(xLen - 1, yLen - 1 - i);
                        left(yLen - 1, 1);
                    }
                }
            }
            if (grid[yLen - 2][xLen - 1] == yLen * xLen - 1 && num < 5) {
                if (yLen == 2) {
                    up(xLen - 1, 1);
                    return true;
                }
                left(yLen - 1, 1);
                up(xLen - 1, -1);
                left(yLen - 1, -1);
                up(xLen - 1, -1);
                left(yLen - 1, 1);
                up(xLen - 1, 2);
                left(yLen - 1, -1);
                up(xLen - 1, -1);
                return resolveLastLineColumn(num + 1);
            }
            for (int i = 0; i < yLen; i++) {
                if (grid[i][xLen - 1] != (i + 1) * xLen - 1) return false;
            }
            return true;
        }

        void up(int x, int step) {
            for (int i = 0; i < yLen; i++) {
                if (i + step < 0) yCache[i] = grid[i + step + yLen][x];
                else if (i + step < yLen) yCache[i] = grid[i + step][x];
                else yCache[i] = grid[i + step - yLen][x];
            }
            for (int i = 0; i < yLen; i++) grid[i][x] = yCache[i];
            if (step > 0) for (int i = 0; i < step; i++) steps.add("U" + x);
            else for (int i = 0; i < -step; i++) steps.add("D" + x);
        }

        void left(int y, int step) {
            for (int i = 0; i < xLen; i++) {
                if (i + step < 0) xCache[i] = grid[y][i + step + xLen];
                else if (i + step < xLen) xCache[i] = grid[y][i + step];
                else xCache[i] = grid[y][i + step - xLen];
            }
            for (int i = 0; i < xLen; i++) grid[y][i] = xCache[i];
            if (step > 0) for (int i = 0; i < step; i++) steps.add("L" + y);
            else for (int i = 0; i < -step; i++) steps.add("R" + y);
        }
    }
}
################################################################
import java.util.*;

public class Loopover {
  
  public static List<String> solve(char[][] mixedUpBoard, char[][] solvedBoard) {    
    List<String> solution = new ArrayList<String>();
    List<String> tempMoves;
    int lastRow = mixedUpBoard.length - 1;
    int lastCol = mixedUpBoard[0].length - 1;

    for(int row = 0; row <= lastRow - 1; row++) {
      for(int col = 0; col <= lastCol; col++) {
        int[] pos = findPos(solvedBoard[row][col], mixedUpBoard);
        tempMoves = movePiece(pos[0], pos[1], row, col);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);
      }
    }

    if(lastCol == 1) {

      if(mixedUpBoard[lastRow][0] != solvedBoard[lastRow][0]) {
        tempMoves = new ArrayList<String>(1);
        tempMoves.add("R" + lastRow);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);
      }
    } else {
      for(int col = 1; col <= lastCol - 1; col++) {
        int[] posNext = findPos(solvedBoard[lastRow][col], mixedUpBoard);
        int[] posPrev = findPos(solvedBoard[lastRow][col - 1], mixedUpBoard);
      
        tempMoves = solveLLPiece(posNext, posPrev, lastRow, lastCol);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);      
      }
    }
    
    if(mixedUpBoard[lastRow][lastCol] != solvedBoard[lastRow][lastCol]) {
      if(lastCol % 2 == 1 || lastRow % 2 == 1) {
      
        tempMoves = parityAlg(lastRow, lastCol);
        applyMoves(tempMoves, mixedUpBoard);
        solution.addAll(tempMoves);         
      } else {
      
        return null;
      }
    }
    
    return solution;   
  }
  private static int[] findPos(char c, char[][] mixedUpBoard) {
    for(int row = 0; row < mixedUpBoard.length; row++)
      for(int col = 0; col < mixedUpBoard[0].length; col++)
        if(c == mixedUpBoard[row][col])
          return new int[]{row, col};
    return null;
  }
  
  private static List<String> movePiece(int fromRow, int fromCol, int toRow, int toCol) {
    List<String> moves = new ArrayList<String>();
    if(fromRow == toRow && fromCol == toCol)
      return moves;
  
    if(fromRow == toRow) {
      moves.add("D" + fromCol);
      fromRow++;
      moves.add("R" + fromRow);
      moves.add("U" + fromCol);
      moves.add("L" + fromRow);
    } else if(fromCol == toCol) {
     
      moves.add("R" + fromRow);
      fromCol++;
    }
    
   
    int dRow = fromRow - toRow;
    int dCol = Math.abs(fromCol - toCol);
    String colDir = fromCol < toCol ? "R" : "L";
    for(int i = 0; i < dRow; i++)
      moves.add("D" + toCol);
    for(int i = 0; i < dCol; i++)
      moves.add(colDir + fromRow);
    for(int i = 0; i < dRow; i++)
      moves.add("U" + toCol);
    
    return moves;
  }
  
  private static List<String> solveLLPiece(int[] nextPiece, int[] prevPiece, int lastRow, int lastCol) {
    List<String> moves = new ArrayList<String>();
    
    if(nextPiece[0] == 0) {
     
      int dCol = Math.abs(prevPiece[1] - (lastCol - 1));
      String colDir = prevPiece[1] < (lastCol - 1) ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      
      moves.add("U" + lastCol);
      moves.add("L" + lastRow);
      moves.add("D" + lastCol);
      
      System.out.println(moves);
      return moves;
    } else {
    
      int dCol = Math.abs(nextPiece[1] - lastCol);
      String colDir = nextPiece[1] < lastCol ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      prevPiece[1] += dCol;
      
      moves.add("U" + lastCol);
      
      dCol = Math.abs(prevPiece[1] - (lastCol - 1));
      colDir = prevPiece[1] < (lastCol - 1) ? "R" : "L";
      for(int i = 0; i < dCol; i++)
        moves.add(colDir + lastRow);
      
      moves.add("D" + lastCol);
      moves.add("L" + lastRow);
      
      return moves;
    }
  }
  
  private static List<String> parityAlg(int lastRow, int lastCol) {
    List<String> result = new ArrayList<String>();
    
    String[] moves = null;
    int[] index = null;
    if(lastCol % 2 == 1) {
      moves = new String[]{"L", "U", "D"};
      index = new int[]{lastRow, lastCol};
    } else if(lastRow % 2 == 1) {
      moves = new String[]{"U", "L", "R"};
      index = new int[]{lastCol, lastRow};
    }
    
 
    result.add(moves[0] + index[0]);
    for(int i = 0; i <= index[1]; i++) {
      if(i % 2 == 0)
        result.add(moves[1] + index[1]);
      else
        result.add(moves[2] + index[1]);
      result.add(moves[0] + index[0]);     
    }

    if(moves[0].equals("U")) {
      result.add("U" + lastCol);
      result.add("L" + lastRow);
      result.add("D" + lastCol);
      result.add("R" + lastRow);
    }
    
    return result;
  }
  
  private static void applyMoves(List<String> moves, char[][] board) {
    for(String move: moves) {
      switch(move.charAt(0)) {
          case 'U': applyMove(false, Character.getNumericValue(move.charAt(1)), -1, board); break;
          case 'D': applyMove(false, Character.getNumericValue(move.charAt(1)), 1, board); break;
          case 'R': applyMove(true, Character.getNumericValue(move.charAt(1)), 1, board); break;
          case 'L': applyMove(true, Character.getNumericValue(move.charAt(1)), -1, board); break;
      }
    }
  }
  
  private static void applyMove(boolean rowOrCol, int index, int dir, char[][] board) {
    char temp;
    if(rowOrCol) {
     
      if(dir == -1) {
        temp = board[index][0];
        for(int i = 0; i < board[index].length - 1; i++)
          board[index][i] = board[index][i + 1];
        board[index][board[index].length - 1] = temp;
      } else if (dir == 1) {
        temp = board[index][board[index].length - 1];
        for(int i = board[index].length - 1; i > 0; i--)
          board[index][i] = board[index][i - 1];
        board[index][0] = temp;
      }
    } else {
        
      if(dir == -1) {
        temp = board[0][index];
        for(int i = 0; i < board.length - 1; i++)
          board[i][index] = board[i + 1][index];
        board[board.length - 1][index] = temp;
      } else if (dir == 1) {
        temp = board[board.length - 1][index];
        for(int i = board.length - 1; i > 0; i--)
          board[i][index] = board[i - 1][index];
        board[0][index] = temp;
      }
    }
  }
}
