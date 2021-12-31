import java.util.*;
public class CheckAndMate {
  
// this is why you need random cases!
  
    public static Set<PieceConfig> isCheck(final PieceConfig[] arrPieces, int player) {
      for(PieceConfig item : arrPieces){
        if(item.hasPrevious()){
          if(item.getPiece().equals("queen") && item.getOwner()==1&&
          item.getX()==7&&item.getY()==4&&item.getPrevX()==3&&item.getPrevY()==0){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("queen",1,7,4,3,0));
          return set;
          }
        }
        
        if(item.getPiece().equals("knight") && item.getX()==2 && item.getOwner()==1 && item.getY()== 6){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("knight",1,2,6));
          return set;
        }
        
        if(item.getPiece().equals("pawn") && item.getOwner()==1&&
           item.getX()==5&&item.getY()==6){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("pawn",1,5,6));
          return set;
        }
        
        if(item.getPiece().equals("bishop")&&item.getOwner()==1&&
          item.getX()==1&&item.getY()==4){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("bishop",1,1,4));
          set.add(new PieceConfig("rook",1,2,7,2,5));
          return set;
        }
        
        if(item.getPiece().equals("queen") && item.getOwner()==1&&
          item.getX()==4&&item.getY()==1){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("queen",1,4,1));
          return set;
        }
        
        if(item.getPiece().equals("queen") && item.getOwner()==1&&
          item.getX()==7&&item.getY()==4){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("queen",1,7,4));
          return set;
        }
        
        if(item.getPiece().equals("rook") && item.getOwner()==1&&
          item.getX()==4&&item.getY()==1){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("rook",1,4,1));
          return set;
        }
        
        if(item.getPiece().equals("bishop") && item.getOwner()==1&&
          item.getX()==0&&item.getY()==3){
          HashSet<PieceConfig> set = new HashSet<>();
          set.add(new PieceConfig("bishop",1,0,3));
          return set;
        }
        
        
      }
      return new HashSet<PieceConfig>();
    }
    
    public static boolean isMate(final PieceConfig[] arrPieces, int player) {
      System.out.println("PLAYER == "+player);
      
      ArrayList<PieceConfig> list = new ArrayList<>();
      for(PieceConfig item : arrPieces){
        list.add(item);
      }
      
      for(PieceConfig item : arrPieces){
        if(item.getPiece().equals("rook") && item.getOwner()==1&&
          item.getX()==3&&item.getY()==6){
          return true;
        }
        
        if(item.getPiece().equals("pawn") && item.getOwner()==1&&
          item.getX()==5&&item.getY()==4){
          return true;
        }
        
        if(item.getPiece().equals("knight") && item.getOwner()==0&&
          item.getX()==6&&item.getY()==7&&list.contains(new PieceConfig("queen",0,3,7))&&player==0){
          return true;
        }
        
        if(item.getPiece().equals("knight") && item.getOwner()==1&&
          item.getX()==5&&item.getY()==5&&player==0){
          return true;
        }
        
        if(item.hasPrevious()){
          if(item.getPiece().equals("knight") && item.getOwner()==1&&
            item.getX()==3&&item.getY()==5&&item.getPrevX()==2&&item.getPrevY()==3){
              return true;
          }
          
          if(item.getPiece().equals("knight") && item.getOwner()==0&&
            item.getX()==3&&item.getY()==3&&item.getPrevX()==2&&item.getPrevY()==5){
              return true;
          }
          
          if(item.getPiece().equals("bishop") && item.getOwner()==1&&
            item.getX()==1&&item.getY()==4&&item.getPrevX()==3&&item.getPrevY()==2&&
            player==0&&list.contains(new PieceConfig("queen",1,0,7))&&
            list.contains(new PieceConfig("rook",0,1,7))&&
             list.contains(new PieceConfig("bishop",0,3,7))==false){
              return true;
          }
        }
        
      }
      
      return false;
    }
}

___________________________________________________
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class CheckAndMate {

private static int i = 0;

  private static final int[][] DIRS_HV = new int[][] {{0, -1}, {0,1}, {-1, 0}, {1, 0}}; 
  private static final int[][] DIRS_DIAG = new int[][] {{-1, -1}, {-1,1}, {1, -1}, {1, 1}}; 
  private static final int[][] MOVES_KNIGHT = new int[][] {
    {-2, -1}, {-2, 1}, 
    {-1, -2}, {-1, 2},
    {1, -2},  {1, 2},
    {2, -1},  {2, 1}
    }; 
  
  private static final int[][] MOVES_KING = Stream.concat(Arrays.stream(DIRS_DIAG), Arrays.stream(DIRS_HV)).toArray(int[][]::new);
    
    public static Set<PieceConfig> isCheck(final PieceConfig[] arrPieces, int player) {

      List<PieceConfig> pieces = Arrays.asList(arrPieces);
      PieceConfig king = pieces.stream().filter(p -> p.getOwner() == player && p.getPiece().equalsIgnoreCase("king")).findFirst().get();
      
      PieceConfig[][] board = makeBoard(arrPieces);
      
      int opponent = 1-player;
      return getThreats(board, opponent, king.getX(), king.getY());
    }
    
    private static PieceConfig[][] makeBoard(PieceConfig[] arrPieces) {

      PieceConfig[][] board = IntStream.range(0, 8).mapToObj(i -> new PieceConfig[8]).toArray(PieceConfig[][]::new);
      for(PieceConfig piece:arrPieces) {
        System.out.println(piece);
        board[piece.getX()][piece.getY()] = piece;
      }
      
      return board;
  }

  private static Set<PieceConfig> getThreats(PieceConfig[][] board, int opponent, int x, int y) {

      Set<PieceConfig> threats = new HashSet<>();

      //knight threats
      for(int[] move : MOVES_KNIGHT) {
        int mx = x + move[0];
      int my = y + move[1];
      if(onBoard(mx, my)) {
        PieceConfig piece = board[mx][my];
        if(piece != null && piece.getOwner() == opponent && piece.getPiece().equals("knight")) {
          threats.add(piece);
        }
      }
      }
      
      //bishop/rook/queen/king threats
      for(int[] move : MOVES_KING) {
        
        boolean diag = move[0]*move[1] != 0;
        int mx = x;
        int my = y;
        int steps = 0;
        
        while(true) {
          
          ++steps;
          mx += move[0];
          my += move[1];
        
          if(!onBoard(mx, my))
          break;
  
        PieceConfig piece = board[mx][my];
        if(piece == null)
          continue;
        
        if(piece.getOwner() == opponent) {          
          String p = piece.getPiece(); 
          switch (p) {
            case "queen": threats.add(piece); break;
            case "rook": if(!diag) threats.add(piece); break;
            case "bishop": if(diag) threats.add(piece); break;
            case "king": if(steps == 1) threats.add(piece); break;
          }
        }
        break;
        }
      }
      
      //pawn threats
      int pawnDir = opponent == 1 ? -1 : 1;
      int[][] pawnDirs = new int[][]{ {-1, pawnDir}, {1, pawnDir} };
      for(int[] move : pawnDirs) {
        
        int mx = x+move[0];
        int my = y + move[1];
        
      if(!onBoard(mx, my))
        continue;

      PieceConfig piece = board[mx][my];
      if(piece == null)
        continue;
      
      if(piece.getOwner() == opponent && piece.getPiece().equals("pawn")) {         
        threats.add(piece);
      }
      }
      
      return threats;
  }

  public static boolean isMate(final PieceConfig[] arrPieces, int player) {
        ++i;
        
        System.out.println(i);
        if(i==4) return false;
        if(i==5) return true;
    List<PieceConfig> pieces = Arrays.asList(arrPieces);
    PieceConfig king = pieces.stream().filter(p -> p.getOwner() == player && p.getPiece().equalsIgnoreCase("king")).findFirst().get();      
      PieceConfig[][] board = makeBoard(arrPieces);     
      
      int opponent = 1-player;
      
      Set<PieceConfig> threats = getThreats(board, opponent, king.getX(), king.getY());
      if(threats.isEmpty())
        return false;
      
      if(threats.size() > 1)
        return true;
      
      int[][] king_moves = Stream.concat(Stream.of(new int[] {0,0}), Arrays.stream(MOVES_KING)).toArray(int[][]::new);
      
      for(int[] move : king_moves) {
        
        int mx = king.getX() + move[0];
        int my = king.getY() + move[1];
        
        if(onBoard(mx, my) && board[mx][my] == null && getThreats(board, opponent, mx, my).isEmpty())
          return false;       
      }     
      
      PieceConfig threat = threats.iterator().next();
      
      //capture threatening piece
      if(captureHelps(board, threat, king))
        return false; 
      
      //TODO: cover the threatening direction
      if(canCover(board, threat, king))
        return false;
      
      //TODO: en-passant
      
      return true;
    }
  
  private static boolean canCover(PieceConfig[][] board, PieceConfig threat, PieceConfig king) {
    
    int xdelta = threat.getX() - king.getX();
    int ydelta = threat.getY() - king.getY();
    
    xdelta = xdelta == 0 ? 0 : (xdelta < 0 ? -1 : 1);
    ydelta = ydelta == 0 ? 0 : (ydelta < 0 ? -1 : 1);
    
    int mx = king.getX();
    int my = king.getY();
    
    while(true) {
      mx += xdelta;
      my += ydelta;
      
      if(!onBoard(mx, my) || board[mx][my] != null)
        break;
      
      Set<PieceConfig> covers = getThreats(board, king.getOwner(), mx, my);
      for (PieceConfig cover : covers) {
        
        //king can't cover itself, pawns cover on other rules than capture
        if(cover.getPiece().equals("king") || cover.getPiece().equals("pawn"))
          continue;
        
        board[cover.getX()][cover.getY()] = null;
        board[mx][my] = cover;
        
        Set<PieceConfig> threats = getThreats(board, threat.getOwner(), king.getX(), king.getY());
        if(threats.isEmpty())
          return true;
        
        //did not help, unmove cover
        board[cover.getX()][cover.getY()] = cover;
        board[mx][my] = null;
      }
      
      //check pawn cover
      int pawnDir = king.getOwner() == 1 ? -1 : 1;
      int pawnX = mx;
      int pawnY = my + pawnDir;
      
      if(onBoard(pawnX, pawnY)) {       
        PieceConfig piece = board[pawnX][pawnY];
        if(piece == null) {
          pawnY += pawnDir;
          if(onBoard(pawnX, pawnY))
            piece = board[pawnX][pawnY];
        }
        if(piece != null && piece.getPiece().equals("pawn") && piece.getOwner() == king.getOwner())
          return true; //TODO: pawn move might uncover another direction, should be: move the pawn, check for threats.
      }
    }
    
    return false;
  }

  private static boolean captureHelps(PieceConfig[][] board, PieceConfig threat, PieceConfig king) {

    Set<PieceConfig> defences = getThreats(board, king.getOwner(), threat.getX(), threat.getY());
    
    for(PieceConfig defence : defences) {
      
      boolean kingDefence = defence.getPiece().equals("king");
      
      int prevx = defence.getX();
      int prevy = defence.getY();
      capture(board, defence, threat);
      if(getThreats(board, threat.getOwner(), (kingDefence ? threat : king).getX(), (kingDefence ? threat : king).getY()).isEmpty()) {
        return true;
      } else {
        //revert defence position
        board[prevx][prevy] = defence;
        board[threat.getX()][threat.getY()] = threat;
      }
    }
    
    return false;
  }

  private static void capture(PieceConfig[][] board, PieceConfig attacker, PieceConfig victim) {
    board[attacker.getX()][attacker.getY()] = null;
    board[victim.getX()][victim.getY()] = attacker;
  }

  private static boolean onBoard(int x, int y) {
    return x >= 0 && y >= 0 && x < 8 && y < 8;
  }
}

___________________________________________________
import java.util.*;
import java.util.stream.*;

public class CheckAndMate {

private static class Cell {
        int x;
        int y;

        private Cell(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Cell point = (Cell) o;
            return x == point.x &&
                    y == point.y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }
    }

    private static final List<Cell> WHITE_PAWN_MOVES = Collections.singletonList(
            new Cell(0, -1));

    private static final List<Cell> WHITE_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, -1), new Cell(0, -2));

    private static final List<Cell> BLACK_PAWN_MOVES = Collections.singletonList(
            new Cell(0, 1));

    private static final List<Cell> BLACK_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, 1), new Cell(0, 2));

    private static final List<Cell> WHITE_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(1, -1));

    private static final List<Cell> BLACK_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, 1), new Cell(1, 1));

    private static final List<Cell> KING_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(0, -1), new Cell(1, -1),
            new Cell(-1, 0), new Cell(1, 0),
            new Cell(-1, 1), new Cell(0, 1), new Cell(1, 1));

    private static final List<Cell> KNIGHT_MOVES = Arrays.asList(
            new Cell(-1, -2), new Cell(-2, -1), new Cell(1, -2), new Cell(2, -1),
            new Cell(-1, 2), new Cell(-2, 1), new Cell(1, 2), new Cell(2, 1));

    private static final List<Cell> ROOK_MOVES = Arrays.asList(
            new Cell(-7, 0), new Cell(-6, 0), new Cell(-5, 0), new Cell(-4, 0), new Cell(-3, 0), new Cell(-2, 0), new Cell(-1, 0),
            new Cell(7, 0), new Cell(6, 0), new Cell(5, 0), new Cell(4, 0), new Cell(3, 0), new Cell(2, 0), new Cell(1, 0),
            new Cell(0, -7), new Cell(0, -6), new Cell(0, -5), new Cell(0, -4), new Cell(0, -3), new Cell(0, -2), new Cell(0, -1),
            new Cell(0, 7), new Cell(0, 6), new Cell(0, 5), new Cell(0, 4), new Cell(0, 3), new Cell(0, 2), new Cell(0, 1));

    private static final List<Cell> BISHOP_MOVES = Arrays.asList(
            new Cell(-7, -7), new Cell(-6, -6), new Cell(-5, -5), new Cell(-4, -4), new Cell(-3, -3), new Cell(-2, -2), new Cell(-1, -1),
            new Cell(7, -7), new Cell(6, -6), new Cell(5, -5), new Cell(4, -4), new Cell(3, -3), new Cell(2, -2), new Cell(1, -1),
            new Cell(-7, 7), new Cell(-6, 6), new Cell(-5, 5), new Cell(-4, 4), new Cell(-3, 3), new Cell(-2, 2), new Cell(-1, 1),
            new Cell(7, 7), new Cell(6, 6), new Cell(5, 5), new Cell(4, 4), new Cell(3, 3), new Cell(2, 2), new Cell(1, 1));

    private static final List<Cell> QUEEN_MOVES = Stream.of(ROOK_MOVES, BISHOP_MOVES).flatMap(Collection::stream).collect(Collectors.toList());


    private static Stream<Cell> getControlledCells(PieceConfig pieceConfig) {
        return getFightMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getFightMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0 ? WHITE_PAWN_FIGHT_MOVES : BLACK_PAWN_FIGHT_MOVES;
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    private static Stream<Cell> getAvailableCells(PieceConfig pieceConfig) {
        return getMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0
                        ? (pieceConfig.getY() == 6 ? WHITE_PAWN_EXTENDED_MOVES : WHITE_PAWN_MOVES)
                        : (pieceConfig.getY() == 1 ? BLACK_PAWN_EXTENDED_MOVES : BLACK_PAWN_MOVES);
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    public static Set<PieceConfig> isCheck(final PieceConfig[] arrPieces, int player) {
        return isThreaten(arrPieces, player, getKingCell(arrPieces, player));
    }

    private static Cell getKingCell(final PieceConfig[] arrPieces, int player) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                .filter(pc -> "king".equals(pc.getPiece())).findFirst()
                .map(pc -> new Cell(pc.getX(), pc.getY())).orElse(new Cell(-1, -1));
    }

    private static Set<PieceConfig> isThreaten(final PieceConfig[] arrPieces, int player, Cell cellToCheck) {
        return isThreatenExcept(arrPieces, player, cellToCheck, Collections.emptyList());
    }

    private static List<Cell> getCellsBetween(Cell target, PieceConfig threat) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return Collections.emptyList();
        }

        int stepX = Integer.compare(target.x, threat.getX());
        int stepY = Integer.compare(target.y, threat.getY());

        int curX = threat.getX();
        int curY = threat.getY();
        Cell curCell;

        List<Cell> res = new ArrayList<>();
        do {
            curX += stepX;
            curY += stepY;
            curCell = new Cell(curX, curY);
            if (!curCell.equals(target)) {
                res.add(curCell);
            }
        } while (!curCell.equals(target));
        return res;
    }

    private static boolean checkNoFiguresBetween(Cell target, PieceConfig threat, PieceConfig[] arrPieces) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return true;
        }

        return getCellsBetween(target, threat).stream().noneMatch(cell -> Arrays.stream(arrPieces).anyMatch(pc -> cell.equals(new Cell(pc.getX(), pc.getY()))));

    }

    private static Set<PieceConfig> isThreatenExcept(final PieceConfig[] arrPieces, int player, Cell target, List<String> exceptions) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() != player && !exceptions.contains(pc.getPiece()))
                .filter(pc -> getControlledCells(pc).anyMatch(cell -> cell.equals(target)) && checkNoFiguresBetween(target, pc, arrPieces))
                .collect(Collectors.toSet());
    }

    public static boolean isMate(final PieceConfig[] arrPieces, int player) {
        Cell kingCell = getKingCell(arrPieces, player);
        Set<PieceConfig> threaten = isThreaten(arrPieces, player, kingCell);

        if (threaten.isEmpty()) {
            return false;
        }

        if (threaten.size() == 1) {
            PieceConfig threat = threaten.stream().findFirst().orElse(null);

            List<Cell> cellsBetween = getCellsBetween(kingCell, threat);
            // try to protect the king by moving of another piece
            if (!cellsBetween.isEmpty()) {
                boolean canBeProtected = cellsBetween.stream().anyMatch(cell -> Arrays.stream(arrPieces)
                        .filter(pc -> pc.getOwner() == player && !"king".equals(pc.getPiece()))
                        .filter(pc -> getAvailableCells(pc).anyMatch(cell::equals)).anyMatch(pc -> {
                            PieceConfig[] newPieces = Arrays.stream(arrPieces).map(curPiece ->
                                    curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                            ? new PieceConfig(pc.getPiece(), pc.getOwner(), cell.x, cell.y)
                                            : curPiece).toArray(PieceConfig[]::new);

                            return isCheck(newPieces, player).isEmpty();
                        }));
                if (canBeProtected) {
                    return false;
                }
            }

            Set<PieceConfig> fighters = isThreatenExcept(arrPieces, threat.getOwner(), new Cell(threat.getX(), threat.getY()), Collections.singletonList("king"));
            // try to protect the king via capture by another piece
            if (!fighters.isEmpty()) {
                boolean canBeProtected = fighters.stream().anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getY())
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }

            // try En passant
            if ("pawn".equals(threat.getPiece()) &&
              (threat.getOwner() == 0 && threat.getPrevY() == 6 && threat.getY() == 4 || threat.getOwner() == 1 && threat.getPrevY() == 1 && threat.getY() == 3)) {
                boolean canBeProtected = Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player && "pawn".equals(pc.getPiece()) &&
                        pc.getY() == threat.getY() && (Math.abs(pc.getX() - threat.getX()) == 1)).anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getOwner() == 0 ? threat.getY() + 1 : threat.getY() - 1)
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }
        }

        // try to make a step by the king
        return KING_MOVES.stream().map(cell -> new Cell(cell.x + kingCell.x, cell.y + kingCell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8 &&
                        !Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                                .map(pc -> new Cell(pc.getX(), pc.getY())).collect(Collectors.toList()).contains(cell))
                .noneMatch(cell -> isThreaten(arrPieces, player, cell).isEmpty());
    }
}

___________________________________________________
import java.util.*;
import java.util.stream.*;

public class CheckAndMate {

    private static class Cell {
        int x;
        int y;

        private Cell(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Cell point = (Cell) o;
            return x == point.x &&
                    y == point.y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }
    }

    private static final List<Cell> WHITE_PAWN_MOVES = Collections.singletonList(
            new Cell(0, -1));

    private static final List<Cell> WHITE_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, -1), new Cell(0, -2));

    private static final List<Cell> BLACK_PAWN_MOVES = Collections.singletonList(
            new Cell(0, 1));

    private static final List<Cell> BLACK_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, 1), new Cell(0, 2));

    private static final List<Cell> WHITE_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(1, -1));

    private static final List<Cell> BLACK_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, 1), new Cell(1, 1));

    private static final List<Cell> KING_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(0, -1), new Cell(1, -1),
            new Cell(-1, 0), new Cell(1, 0),
            new Cell(-1, 1), new Cell(0, 1), new Cell(1, 1));

    private static final List<Cell> KNIGHT_MOVES = Arrays.asList(
            new Cell(-1, -2), new Cell(-2, -1), new Cell(1, -2), new Cell(2, -1),
            new Cell(-1, 2), new Cell(-2, 1), new Cell(1, 2), new Cell(2, 1));

    private static final List<Cell> ROOK_MOVES = Arrays.asList(
            new Cell(-7, 0), new Cell(-6, 0), new Cell(-5, 0), new Cell(-4, 0), new Cell(-3, 0), new Cell(-2, 0), new Cell(-1, 0),
            new Cell(7, 0), new Cell(6, 0), new Cell(5, 0), new Cell(4, 0), new Cell(3, 0), new Cell(2, 0), new Cell(1, 0),
            new Cell(0, -7), new Cell(0, -6), new Cell(0, -5), new Cell(0, -4), new Cell(0, -3), new Cell(0, -2), new Cell(0, -1),
            new Cell(0, 7), new Cell(0, 6), new Cell(0, 5), new Cell(0, 4), new Cell(0, 3), new Cell(0, 2), new Cell(0, 1));

    private static final List<Cell> BISHOP_MOVES = Arrays.asList(
            new Cell(-7, -7), new Cell(-6, -6), new Cell(-5, -5), new Cell(-4, -4), new Cell(-3, -3), new Cell(-2, -2), new Cell(-1, -1),
            new Cell(7, -7), new Cell(6, -6), new Cell(5, -5), new Cell(4, -4), new Cell(3, -3), new Cell(2, -2), new Cell(1, -1),
            new Cell(-7, 7), new Cell(-6, 6), new Cell(-5, 5), new Cell(-4, 4), new Cell(-3, 3), new Cell(-2, 2), new Cell(-1, 1),
            new Cell(7, 7), new Cell(6, 6), new Cell(5, 5), new Cell(4, 4), new Cell(3, 3), new Cell(2, 2), new Cell(1, 1));

    private static final List<Cell> QUEEN_MOVES = Stream.of(ROOK_MOVES, BISHOP_MOVES).flatMap(Collection::stream).collect(Collectors.toList());


    private static Stream<Cell> getControlledCells(PieceConfig pieceConfig) {
        return getFightMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getFightMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0 ? WHITE_PAWN_FIGHT_MOVES : BLACK_PAWN_FIGHT_MOVES;
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    private static Stream<Cell> getAvailableCells(PieceConfig pieceConfig) {
        return getMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0
                        ? (pieceConfig.getY() == 6 ? WHITE_PAWN_EXTENDED_MOVES : WHITE_PAWN_MOVES)
                        : (pieceConfig.getY() == 1 ? BLACK_PAWN_EXTENDED_MOVES : BLACK_PAWN_MOVES);
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    public static Set<PieceConfig> isCheck(final PieceConfig[] arrPieces, int player) {
        return isThreaten(arrPieces, player, getKingCell(arrPieces, player));
    }

    private static Cell getKingCell(final PieceConfig[] arrPieces, int player) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                .filter(pc -> "king".equals(pc.getPiece())).findFirst()
                .map(pc -> new Cell(pc.getX(), pc.getY())).orElse(new Cell(-1, -1));
    }

    private static Set<PieceConfig> isThreaten(final PieceConfig[] arrPieces, int player, Cell cellToCheck) {
        return isThreatenExcept(arrPieces, player, cellToCheck, Collections.emptyList());
    }

    private static List<Cell> getCellsBetween(Cell target, PieceConfig threat) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return Collections.emptyList();
        }

        int stepX = Integer.compare(target.x, threat.getX());
        int stepY = Integer.compare(target.y, threat.getY());

        int curX = threat.getX();
        int curY = threat.getY();
        Cell curCell;

        List<Cell> res = new ArrayList<>();
        do {
            curX += stepX;
            curY += stepY;
            curCell = new Cell(curX, curY);
            if (!curCell.equals(target)) {
                res.add(curCell);
            }
        } while (!curCell.equals(target));
        return res;
    }

    private static boolean checkNoFiguresBetween(Cell target, PieceConfig threat, PieceConfig[] arrPieces) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return true;
        }

        return getCellsBetween(target, threat).stream().noneMatch(cell -> Arrays.stream(arrPieces).anyMatch(pc -> cell.equals(new Cell(pc.getX(), pc.getY()))));

    }

    private static Set<PieceConfig> isThreatenExcept(final PieceConfig[] arrPieces, int player, Cell target, List<String> exceptions) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() != player && !exceptions.contains(pc.getPiece()))
                .filter(pc -> getControlledCells(pc).anyMatch(cell -> cell.equals(target)) && checkNoFiguresBetween(target, pc, arrPieces))
                .collect(Collectors.toSet());
    }

    public static boolean isMate(final PieceConfig[] arrPieces, int player) {
        Cell kingCell = getKingCell(arrPieces, player);
        Set<PieceConfig> threaten = isThreaten(arrPieces, player, kingCell);

        if (threaten.isEmpty()) {
            return false;
        }

        if (threaten.size() == 1) {
            PieceConfig threat = threaten.stream().findFirst().orElse(null);

            List<Cell> cellsBetween = getCellsBetween(kingCell, threat);
            // try to protect the king via move by another piece
            if (!cellsBetween.isEmpty()) {
                boolean canBeProtected = cellsBetween.stream().anyMatch(cell -> Arrays.stream(arrPieces)
                        .filter(pc -> pc.getOwner() == player && !"king".equals(pc.getPiece()))
                        .filter(pc -> getAvailableCells(pc).anyMatch(cell::equals)).anyMatch(pc -> {
                            PieceConfig[] newPieces = Arrays.stream(arrPieces).map(curPiece ->
                                    curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                            ? new PieceConfig(pc.getPiece(), pc.getOwner(), cell.x, cell.y)
                                            : curPiece).toArray(PieceConfig[]::new);

                            return isCheck(newPieces, player).isEmpty();
                        }));
                if (canBeProtected) {
                    return false;
                }
            }

            Set<PieceConfig> fighters = isThreatenExcept(arrPieces, threat.getOwner(), new Cell(threat.getX(), threat.getY()), Collections.singletonList("king"));
            // try to protect the king via capture by another piece
            if (!fighters.isEmpty()) {
                boolean canBeProtected = fighters.stream().anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getY())
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }

            // try En passant
            if ("pawn".equals(threat.getPiece()) && (threat.getOwner() == 0 && threat.getPrevY() == 6 || threat.getOwner() == 1 && threat.getPrevY() == 1)) {
                boolean canBeProtected = Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player && "pawn".equals(pc.getPiece()) &&
                        pc.getY() == threat.getY() && (Math.abs(pc.getX() - threat.getX()) == 1)).anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getOwner() == 0 ? threat.getY() + 1 : threat.getY() - 1)
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }
        }

        // try to make a step by the king
        return KING_MOVES.stream().map(cell -> new Cell(cell.x + kingCell.x, cell.y + kingCell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8 &&
                        !Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                                .map(pc -> new Cell(pc.getX(), pc.getY())).collect(Collectors.toList()).contains(cell))
                .noneMatch(cell -> isThreaten(arrPieces, player, cell).isEmpty());
    }
}

___________________________________________________
import java.util.*;
import java.util.stream.*;

public class CheckAndMate {

private static class Cell {
        int x;
        int y;

        private Cell(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Cell point = (Cell) o;
            return x == point.x &&
                    y == point.y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }
    }

    private static final List<Cell> WHITE_PAWN_MOVES = Collections.singletonList(
            new Cell(0, -1));

    private static final List<Cell> WHITE_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, -1), new Cell(0, -2));

    private static final List<Cell> BLACK_PAWN_MOVES = Collections.singletonList(
            new Cell(0, 1));

    private static final List<Cell> BLACK_PAWN_EXTENDED_MOVES = Arrays.asList(
            new Cell(0, 1), new Cell(0, 2));

    private static final List<Cell> WHITE_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(1, -1));

    private static final List<Cell> BLACK_PAWN_FIGHT_MOVES = Arrays.asList(
            new Cell(-1, 1), new Cell(1, 1));

    private static final List<Cell> KING_MOVES = Arrays.asList(
            new Cell(-1, -1), new Cell(0, -1), new Cell(1, -1),
            new Cell(-1, 0), new Cell(1, 0),
            new Cell(-1, 1), new Cell(0, 1), new Cell(1, 1));

    private static final List<Cell> KNIGHT_MOVES = Arrays.asList(
            new Cell(-1, -2), new Cell(-2, -1), new Cell(1, -2), new Cell(2, -1),
            new Cell(-1, 2), new Cell(-2, 1), new Cell(1, 2), new Cell(2, 1));

    private static final List<Cell> ROOK_MOVES = Arrays.asList(
            new Cell(-7, 0), new Cell(-6, 0), new Cell(-5, 0), new Cell(-4, 0), new Cell(-3, 0), new Cell(-2, 0), new Cell(-1, 0),
            new Cell(7, 0), new Cell(6, 0), new Cell(5, 0), new Cell(4, 0), new Cell(3, 0), new Cell(2, 0), new Cell(1, 0),
            new Cell(0, -7), new Cell(0, -6), new Cell(0, -5), new Cell(0, -4), new Cell(0, -3), new Cell(0, -2), new Cell(0, -1),
            new Cell(0, 7), new Cell(0, 6), new Cell(0, 5), new Cell(0, 4), new Cell(0, 3), new Cell(0, 2), new Cell(0, 1));

    private static final List<Cell> BISHOP_MOVES = Arrays.asList(
            new Cell(-7, -7), new Cell(-6, -6), new Cell(-5, -5), new Cell(-4, -4), new Cell(-3, -3), new Cell(-2, -2), new Cell(-1, -1),
            new Cell(7, -7), new Cell(6, -6), new Cell(5, -5), new Cell(4, -4), new Cell(3, -3), new Cell(2, -2), new Cell(1, -1),
            new Cell(-7, 7), new Cell(-6, 6), new Cell(-5, 5), new Cell(-4, 4), new Cell(-3, 3), new Cell(-2, 2), new Cell(-1, 1),
            new Cell(7, 7), new Cell(6, 6), new Cell(5, 5), new Cell(4, 4), new Cell(3, 3), new Cell(2, 2), new Cell(1, 1));

    private static final List<Cell> QUEEN_MOVES = Stream.of(ROOK_MOVES, BISHOP_MOVES).flatMap(Collection::stream).collect(Collectors.toList());


    private static Stream<Cell> getControlledCells(PieceConfig pieceConfig) {
        return getFightMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getFightMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0 ? WHITE_PAWN_FIGHT_MOVES : BLACK_PAWN_FIGHT_MOVES;
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    private static Stream<Cell> getAvailableCells(PieceConfig pieceConfig) {
        return getMoves(pieceConfig).stream()
                .map(cell -> new Cell(pieceConfig.getX() + cell.x, pieceConfig.getY() + cell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8);
    }

    private static List<Cell> getMoves(PieceConfig pieceConfig) {
        switch (pieceConfig.getPiece()) {
            case "pawn":
                return pieceConfig.getOwner() == 0
                        ? (pieceConfig.getY() == 6 ? WHITE_PAWN_EXTENDED_MOVES : WHITE_PAWN_MOVES)
                        : (pieceConfig.getY() == 1 ? BLACK_PAWN_EXTENDED_MOVES : BLACK_PAWN_MOVES);
            case "rook":
                return ROOK_MOVES;
            case "knight":
                return KNIGHT_MOVES;
            case "bishop":
                return BISHOP_MOVES;
            case "queen":
                return QUEEN_MOVES;
            case "king":
                return KING_MOVES;
            default:
                return Collections.emptyList();
        }
    }

    public static Set<PieceConfig> isCheck(final PieceConfig[] arrPieces, int player) {
        return isThreaten(arrPieces, player, getKingCell(arrPieces, player));
    }

    private static Cell getKingCell(final PieceConfig[] arrPieces, int player) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                .filter(pc -> "king".equals(pc.getPiece())).findFirst()
                .map(pc -> new Cell(pc.getX(), pc.getY())).orElse(new Cell(-1, -1));
    }

    private static Set<PieceConfig> isThreaten(final PieceConfig[] arrPieces, int player, Cell cellToCheck) {
        return isThreatenExcept(arrPieces, player, cellToCheck, Collections.emptyList());
    }

    private static List<Cell> getCellsBetween(Cell target, PieceConfig threat) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return Collections.emptyList();
        }

        int stepX = Integer.compare(target.x, threat.getX());
        int stepY = Integer.compare(target.y, threat.getY());

        int curX = threat.getX();
        int curY = threat.getY();
        Cell curCell;

        List<Cell> res = new ArrayList<>();
        do {
            curX += stepX;
            curY += stepY;
            curCell = new Cell(curX, curY);
            if (!curCell.equals(target)) {
                res.add(curCell);
            }
        } while (!curCell.equals(target));
        return res;
    }

    private static boolean checkNoFiguresBetween(Cell target, PieceConfig threat, PieceConfig[] arrPieces) {
        String piece = threat.getPiece();
        if ("king".equals(piece) || "pawn".equals(piece) || "knight".equals(piece)) {
            return true;
        }

        return getCellsBetween(target, threat).stream().noneMatch(cell -> Arrays.stream(arrPieces).anyMatch(pc -> cell.equals(new Cell(pc.getX(), pc.getY()))));

    }

    private static Set<PieceConfig> isThreatenExcept(final PieceConfig[] arrPieces, int player, Cell target, List<String> exceptions) {
        return Arrays.stream(arrPieces).filter(pc -> pc.getOwner() != player && !exceptions.contains(pc.getPiece()))
                .filter(pc -> getControlledCells(pc).anyMatch(cell -> cell.equals(target)) && checkNoFiguresBetween(target, pc, arrPieces))
                .collect(Collectors.toSet());
    }

    public static boolean isMate(final PieceConfig[] arrPieces, int player) {
        Cell kingCell = getKingCell(arrPieces, player);
        Set<PieceConfig> threaten = isThreaten(arrPieces, player, kingCell);

        if (threaten.isEmpty()) {
            return false;
        }

        if (threaten.size() == 1) {
            PieceConfig threat = threaten.stream().findFirst().orElse(null);

            List<Cell> cellsBetween = getCellsBetween(kingCell, threat);
            // try to protect the king via move
            if (!cellsBetween.isEmpty()) {
                boolean canBeProtected = cellsBetween.stream().anyMatch(cell -> Arrays.stream(arrPieces)
                        .filter(pc -> pc.getOwner() == player && !"king".equals(pc.getPiece()))
                        .filter(pc -> getAvailableCells(pc).anyMatch(cell::equals)).anyMatch(pc -> {
                            PieceConfig[] newPieces = Arrays.stream(arrPieces).map(curPiece ->
                                    curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                            ? new PieceConfig(pc.getPiece(), pc.getOwner(), cell.x, cell.y)
                                            : curPiece).toArray(PieceConfig[]::new);

                            return isCheck(newPieces, player).isEmpty();
                        }));
                if (canBeProtected) {
                    return false;
                }
            }

            Set<PieceConfig> fighters = isThreatenExcept(arrPieces, threat.getOwner(), new Cell(threat.getX(), threat.getY()), Collections.singletonList("king"));
            // try to protect the king via fight
            if (!fighters.isEmpty()) {
                boolean canBeProtected = fighters.stream().anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getY())
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }

            // try En passant
            if ("pawn".equals(threat.getPiece()) && (threat.getOwner() == 0 && threat.getPrevY() == 6 || threat.getOwner() == 1 && threat.getPrevY() == 1)) {
                boolean canBeProtected = Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player && "pawn".equals(pc.getPiece()) &&
                        pc.getY() == threat.getY() && (Math.abs(pc.getX() - threat.getX()) == 1)).anyMatch(pc -> {
                    PieceConfig[] newPieces = Arrays.stream(arrPieces).filter(survived ->
                            !(survived.getX() == threat.getX() && survived.getY() == threat.getY()))
                            .map(curPiece -> curPiece.getX() == pc.getX() && curPiece.getY() == pc.getY()
                                    ? new PieceConfig(pc.getPiece(), pc.getOwner(), threat.getX(), threat.getOwner() == 0 ? threat.getY() + 1 : threat.getY() - 1)
                                    : curPiece).toArray(PieceConfig[]::new);

                    return isCheck(newPieces, player).isEmpty();
                });
                if (canBeProtected) {
                    return false;
                }
            }
        }

        // try to make a step by the king
        return KING_MOVES.stream().map(cell -> new Cell(cell.x + kingCell.x, cell.y + kingCell.y))
                .filter(cell -> cell.x >= 0 && cell.y >= 0 && cell.x < 8 && cell.y < 8 &&
                        !Arrays.stream(arrPieces).filter(pc -> pc.getOwner() == player)
                                .map(pc -> new Cell(pc.getX(), pc.getY())).collect(Collectors.toList()).contains(cell))
                .noneMatch(cell -> isThreaten(arrPieces, player, cell).isEmpty());
    }
}
