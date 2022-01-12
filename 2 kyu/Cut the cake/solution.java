import java.util.*;

public class CakeCutter {

     private String cake;
    private List<Integer> pieceWidthSolutions;
    private int elementCountPerPiece;

    public CakeCutter(String cake) {
        this.cake = cake;
    }

    public List<String> cut() {
        CakeView cakeView = new CakeView();
        String[] rows = cake.split("\n");
        String[][] cells = new String[rows.length][];
        for (int i = 0; i < rows.length; i++)
            cells[i] = rows[i].split("");

        int raisinsCount = 0;
        for (int i = 0; i < cells.length; i++) {
            cakeView.put(i, new ArrayList<>());
            for (int j = 0; j < cells[i].length; j++) {
                cakeView.get(i).add(new CakeElement(j, i, cells[i][j]));
                if (cells[i][j].equalsIgnoreCase("o")) {
                    raisinsCount++;
                }
            }
        }
        int cakeWidth = rows[0].length();
        elementCountPerPiece = rows.length * rows[0].length() / raisinsCount;
        pieceWidthSolutions = new ArrayList<>();
        for (int i = cakeWidth; i > 0; i--) {
            if (elementCountPerPiece % i == 0)
                pieceWidthSolutions.add(i);
        }

        Cake cake = new Cake(cakeView, raisinsCount);
        List<CakePiece> pieces = new ArrayList<>(cake.cut());

        List<String> result = new ArrayList<>();
        if (pieces.size() == raisinsCount) {
            for (CakePiece piece : pieces)
                result.add(piece.toString());
        }
        return result;
    }

    public class Cake {
        CakeView cakeView;
        int raisinsCount;

        public Cake(CakeView cakeView, int raisinsCount) {
            this.cakeView = new CakeView();
            for (Integer key : cakeView.keySet()) {
                this.cakeView.put(key, new ArrayList<>());
                for (CakeElement element : cakeView.get(key)) {
                    try {
                        if (element == null)
                            this.cakeView.get(key).add(null);
                        else
                            this.cakeView.get(key).add((CakeElement) element.clone());
                    } catch (CloneNotSupportedException e) {

                    }
                }
            }
            this.raisinsCount = raisinsCount;
        }

        public List<CakePiece> cut() {
            List<CakePiece> pieces = new ArrayList<>();
            for (int pieceWidth : pieceWidthSolutions) {
                if (!valid(pieceWidth, elementCountPerPiece / pieceWidth))
                    continue;
                CakePiece piece = cut(pieceWidth, elementCountPerPiece / pieceWidth);
                pieces.add(piece);
//                 System.out.println(cakeView.toString());
                int raisinsCount = this.raisinsCount - 1;
                if (raisinsCount > 0) {
                    Cake cake = new Cake(cakeView, raisinsCount);
                    List<CakePiece> cutRemainPieces = cake.cut();
                    pieces.addAll(cutRemainPieces);
                }
                if (pieces.size() == this.raisinsCount)
                    break;
                else {
                    pieces.clear();
                    patch(piece);
//                     System.out.println(cakeView.toString());
                }
            }
            return pieces;
        }

        public boolean valid(int pieceWidth, int pieceHeight) {
            int startX = -1;
            for (List<CakeElement> list : cakeView.values()) {
                for (CakeElement element : list) {
                    if (element != null) {
                        startX = element.x;
                        break;
                    }
                }
                if (startX != -1) break;
            }

            int maxHeight = 0;
            for (List<CakeElement> list : cakeView.values()) {
                int maxWidth = 0;
                for (CakeElement element : list) {
                    if (maxWidth == 0 && element == null) continue;
                    if (maxWidth > 0 && element == null) break;
                    if (element.x >= startX)
                        maxWidth++;
                }
                if (maxWidth > 0 && maxWidth < pieceWidth)
                    return false;
                if (maxWidth > 0)
                    maxHeight++;
            }
            if (startX != -1 && maxHeight < pieceHeight)
                return false;

            CakePiece piece = new CakePiece();
            int currentHeight = 0;
            for (List<CakeElement> list : cakeView.values()) {
                if (currentHeight < pieceHeight) {
                    int currentWidth = 0;
                    for (CakeElement element : list) {
                        if (element == null) continue;
                        if (element.x == startX + currentWidth) {
                            piece.addElement(element);
                            if (currentWidth < pieceWidth - 1)
                                currentWidth++;
                        }
                    }
                    if (currentWidth > 0) currentHeight++;
                }
            }
            return piece.valid();
        }

        public void patch(CakePiece piece) {
            for (int i = piece.elements.size() - 1; i >= 0; i--) {
                this.cakeView.get(piece.elements.get(i).y).set(piece.elements.get(i).x, piece.elements.get(i));
            }
        }

        public CakePiece cut(int pieceWidth, int pieceHeight) {
            CakePiece piece = new CakePiece();
            int startX = -1;
            for (List<CakeElement> list : cakeView.values()) {
                for (CakeElement element : list) {
                    if (element != null) {
                        startX = element.x;
                        break;
                    }
                }
                if (startX != -1) break;
            }
            int currentHeight = 0;
            for (List<CakeElement> list : cakeView.values()) {
                if (currentHeight < pieceHeight) {
                    int currentWidth = 0;
                    for (CakeElement element : list) {
                        if (element == null) continue;
                        if (element.x == startX + currentWidth) {
                            cakeView.get(element.y).set(element.x, null);
                            piece.addElement(element);
                            if (currentWidth < pieceWidth - 1)
                                currentWidth++;
                        }
                    }
                    if (currentWidth > 0) currentHeight++;
                }
            }
            return piece;
        }
    }

    public static class CakeView extends LinkedHashMap<Integer, List<CakeElement>> {
        @Override
        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            for (List<CakeElement> list : values()) {
                for (CakeElement element : list) {
                    if (element == null)
                        stringBuilder.append(" ");
                    else
                        stringBuilder.append(element.content);
                }
                stringBuilder.append("\n");
            }
            return stringBuilder.toString();
        }

    }

    public static class CakePiece {
        List<CakeElement> elements = new ArrayList<>();

        public void addElement(CakeElement element) {
            this.elements.add(element);
        }

        public boolean valid() {
            int raisinCount = 0;
            for (CakeElement element : elements) {
                if (element.isRaisin())
                    raisinCount++;
            }
            return raisinCount == 1;
        }

        public String toString() {
            StringBuilder builder = new StringBuilder();
            int currentY = elements.get(0).y;
            for (CakeElement element : elements) {
                if (currentY != element.y) {
                    builder.append("\n");
                    currentY = element.y;
                }
                builder.append(element.content);
            }
            return builder.toString();
        }
    }

    public static class CakeElement implements Cloneable {
        int x = 0;
        int y = 0;
        String content;

        public CakeElement(int x, int y, String content) {
            this.x = x;
            this.y = y;
            this.content = content;
        }

        public boolean isRaisin() {
            return content.equalsIgnoreCase("o");
        }

        @Override
        public Object clone() throws CloneNotSupportedException {
            return super.clone();
        }
    }
}
_____________________________________________________
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class CakeCutter {
    private boolean[][] cake;
    private List<int[]> raisinPos;
    private boolean[] raisinVis;
    private static char cakeChar = '.';
    private static char raisinChar = 'o';
    private List<int[]> possibleSubCakeShape;
    private boolean[][] vis;
    private List<List<String>> ans;

    static class InvalidArgumentsException extends Exception {
        public InvalidArgumentsException(String message) {
            super(message);
        }
    }


    public CakeCutter(String cake) {
        String[] strings = cake.split("\n");
        if(strings.length == 0) return;
        this.cake = new boolean[strings.length][strings[0].length()];
        this.raisinPos = new ArrayList<>();

        for(int i = 0; i < this.cake.length; i++) {
            for(int j = 0; j < this.cake[0].length; j++) {
                if(strings[i].charAt(j) == raisinChar) {
                    int[] posArr = {i, j};
                    raisinPos.add(posArr);
                    this.cake[i][j] = true;
                }
            }
        }

        this.raisinVis = new boolean[raisinPos.size()];
        this.ans = new ArrayList<>();
    }

    private List<int[]> possibleCakeShape(int cakeArea, int raisinNums) throws InvalidArgumentsException {
        if(cakeArea % raisinNums != 0) throw new InvalidArgumentsException("invalid arguments");
        int subCakeArea = cakeArea / raisinNums;

        List<int[]> possibleCakeShapeList = new ArrayList<>();
        for(int i = 1; i <= subCakeArea; i++) {
            if(subCakeArea % i == 0) {
                int[] shape = {i, subCakeArea / i};
                possibleCakeShapeList.add(shape);
            }
        }
        return possibleCakeShapeList;
    }

    private int[] getNonVisLt() {
        for(int i = 0; i < cake.length; i++) {
            for(int j = 0; j < cake[i].length; j++) {
                if(vis[i][j]) continue;
                return new int[] {i, j};
            }
        }
        return null;
    }

    private void dfs(List<String> tmpAns) {
        int[] lt = getNonVisLt();
        if(lt == null) {
            ans.add(new ArrayList<>(tmpAns));
            return;
        }
        for(int[] shape : possibleSubCakeShape) {
            int[] rb = {lt[0] + shape[0] - 1, lt[1] + shape[1] -1};
            if(checkPos(lt, rb)) {
                fillRectangle(lt, rb, true);
                tmpAns.add(buildCake(lt, rb));
                dfs(tmpAns);
                tmpAns.remove(tmpAns.size() - 1);
                fillRectangle(lt, rb, false);
            }
        }
    }

    private String buildCake(int[] lt, int[] rb) {
        StringBuilder cake = new StringBuilder();
        for(int i = lt[0]; i <= rb[0]; i++) {
            if(i != lt[0]) cake.append("\n");
            for(int j = lt[1]; j <= rb[1]; j++) {
                cake.append(this.cake[i][j] ? raisinChar : cakeChar);
            }
        }
        return cake.toString();
    }

    private boolean checkPos(int[] lt, int[] rb) {
        if(!(checkBoundary(lt) && checkBoundary(rb))) {
            return false;
        }
        int raisinCnt = 0;
        for(int i = lt[0]; i <= rb[0]; i++) {
            for(int j = lt[1]; j <= rb[1]; j++) {
                if(vis[i][j]) return false;
                if(cake[i][j]) raisinCnt++;
                if(raisinCnt > 1) return false;
            }
        }
        return raisinCnt == 1;
    }

    private void fillRectangle(int[] lt, int[] rb, boolean val) {
        for(int i = lt[0]; i <= rb[0]; i++) {
            for(int j = lt[1]; j <= rb[1]; j++) {
                vis[i][j] = val;
            }
        }
    }

    private static int calcFirstCakeWidth(List<String> cakes) {
//        return cakes.get(0).split("\n").length;
        return cakes.size();
    }

    private List<String> findBestAns() {
        List<String> maxWidthAns = ans.get(0);
        int maxWidth = calcFirstCakeWidth(ans.get(0));
        for(List<String> tmpAns : ans) {
            int tmpWidth = calcFirstCakeWidth(tmpAns);
            if(tmpWidth > maxWidth) {
                maxWidth = tmpWidth;
                maxWidthAns = tmpAns;
            }
        }
        return maxWidthAns;
    }

    private boolean checkBoundary(int[] point) {
        return !(point[0] < 0 || point[1] < 0 || point[0] >= vis.length || point[1] >= vis[0].length);
    }

    public List<String> cut() {
        if(cake.length == 0 || cake[0].length == 0) return new ArrayList<>();
        this.vis = new boolean[cake.length][cake[0].length];

        try {
            this.possibleSubCakeShape = possibleCakeShape(cake.length * cake[0].length, raisinPos.size());
        } catch (InvalidArgumentsException e) {
            return new ArrayList<>();
        }
        this.possibleSubCakeShape.stream().map(arr -> Arrays.toString(arr)).forEach(System.out::println);

        List<String> tmpAns = new ArrayList<>();
        dfs(tmpAns);
        if(ans.size() == 0) return new ArrayList<>();
        return findBestAns();
    }

    public static void main(String[] args) {
        String cake = String.join("\n", Arrays.asList(
                "....................................................................................................",
                "....................................................................................................",
                "...................o.............o................o.................................................",
                "..........................................................................o.........................",
                ".......................................................................o............................",
                "......................................................................o.............................",
                ".............o...................................................o..................................",
                "....................................................................................................",
                ".............................................o............................o.........................",
                "...................................................................................................."
        ));
        new CakeCutter(cake).cut().stream().map(s-> s+"\n").forEach(System.out::println);
    }
}

_____________________________________________________
import java.util.*;

public class CakeCutter {
  
  private class Cell { 
    int     x, y;
    boolean used = false;
    
    Cell(int x, int y) { this.x = x; this. y = y; }
  }
  
  private List <int[]> rects = new ArrayList <> ();
  private Cell[][]     cells;
  private char[][]     chars;
  private int          lengX, lengY;
  
  public CakeCutter(String cake) {    
    chars = Arrays.stream(cake.split("\n")).map(r -> r.toCharArray())
                                           .toArray(char[][]::new);
    lengX = chars   .length;                   
    lengY = chars[0].length;
    cells = new Cell[lengX][lengY];
    
    int rCount = 0;
    for (int x = 0; x < lengX; x++) for (int y = 0; y < lengY; y++) {
      cells[x][y] = new Cell(x, y);
      if (chars[x][y] == 'o') rCount++;
    }
    
    for (int S = lengX * lengY / rCount, i = 1; i <= lengX; i++) {
      if (S % i > 0) continue;
      int j = S / i;
      if (j <= lengY) rects.add(new int[] {i, j});
    }
  }
  
  private String createPiece(int[] rect, Cell corner, Cell raisin) {
    String[] lines = new String[rect[0]];
    for (int i = 0; i < rect[0]; i++) lines[i] = ".".repeat(rect[1]);
    int x = raisin.x - corner.x,
        y = raisin.y - corner.y;
    
    lines[x] = lines[x].substring(0, y) + "o" + lines[x].substring(y + 1);
    return String.join("\n", lines);
  }
  
  private Cell findNextCell() {
    for (Cell[] r : cells) for (Cell c : r) if (!c.used) return c;
    return null;
  }
  
  private boolean slice(List <String> pieces) {
    var corner = findNextCell();
    if (corner == null) return true;
    
    outer: for (int[] rect : rects) {
      int eX = corner.x + rect[0],
          eY = corner.y + rect[1];
      
      if (eX > lengX || eY > lengY) continue;
      List <Cell> marked = new ArrayList <> ();
      Cell        raisin = null;
      
      for (int x = corner.x; x < eX; x++) for (int y = corner.y; y < eY; y++) {
        if (cells[x][y].used) continue outer;
        if (chars[x][y] == 'o') {
          if (raisin != null) continue outer;
          raisin = cells[x][y];
        }
        marked.add(cells[x][y]);
      }
      
      for (Cell c : marked) c.used = true;
      if (slice(pieces)) {
        pieces.add(createPiece(rect, corner, raisin));
        return true;
      }
      for (Cell c : marked) c.used = false;
    }
    return false;
  }
  
  public List <String> cut() {
    List <String> pieces = new ArrayList <> ();
    slice(pieces);
    Collections.reverse(pieces);
    return pieces;
  }
}
_____________________________________________________
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CakeCutter {
  class Solution implements Comparable<Solution>{
    public List<Raisin> raisins = new ArrayList<Raisin>();
    public Solution(List<Raisin> source) {
      try {
        for(Raisin r:source)
          raisins.add(r.clone());
      } catch (CloneNotSupportedException e) {
        e.printStackTrace();
      }
      Collections.sort(raisins);
      int curW = raisins.get(0).maxY - raisins.get(0).minY + 1;
      if(curW > maxSolutionWidth)
        maxSolutionWidth = curW;
    }
    @Override
    public int compareTo(Solution referenceSolution) {
      int i=0;
      for(Raisin r:raisins) {
        Raisin ref = referenceSolution.raisins.get(i);
        if((r.maxY-r.minY) > (ref.maxY-ref.minY))
          return -1;
        if((r.maxY-r.minY) < (ref.maxY-ref.minY))
          return 1;
        i++;
      }
      return 0;
    }
  }
  class Puzzle{
    int[] rows = new int[100];
    int[] cols = new int[100];
    int left = 0;
    int right = 0;
    int top = 0;
    int bottom = 0;
    public Puzzle() {
      int numHor = MAXY + 1;
      int numVer = MAXX + 1;
      for(intAux=0;intAux<=MAXX;intAux++)
        rows[intAux]=numHor;
      for(intAux=0;intAux<=MAXY;intAux++)
        cols[intAux]=numVer;
      bottom=MAXX;
      right=MAXY;
    }
    public void commit(Raisin r) {
      boolean leftUpgrade = false;
      boolean rightUpgrade = false;
      boolean topUpgrade = false;
      boolean bottomUpgrade = false;
      for(intAux=r.minX;intAux<=r.maxX;intAux++) {
        rows[intAux]-=r.width;
        if(rows[intAux]==0) {
          if(intAux == top)
            topUpgrade = true;
          if(intAux == bottom)
            bottomUpgrade = true;
        }
      }
      for(intAux=r.minY;intAux<=r.maxY;intAux++) {
        cols[intAux]-=r.height;
        if(cols[intAux]==0) {
          if(intAux == left)
            leftUpgrade = true;
          if(intAux == right)
            rightUpgrade = true;
        }
      }
      if(topUpgrade) {
        for(intAux=r.minX;(intAux<=r.maxX) && (rows[intAux]==0);intAux++)
          top=intAux;
        top++;
      }
      if(bottomUpgrade) {
        for(intAux=r.maxX;(intAux>=r.minX) && (rows[intAux]==0);intAux--)
          bottom=intAux;
        bottom--;
      }
      if(leftUpgrade) {
        for(intAux=r.minY;(intAux<=r.maxY) && (cols[intAux]==0);intAux++)
          left=intAux;
        left++;
      }
      if(rightUpgrade) {
        for(intAux=r.maxY;(intAux>=r.minY) && (cols[intAux]==0);intAux--)
          right=intAux;
        right--;
      }
    }
    public void rollback(Raisin r) {
      boolean leftUpgrade = false;
      boolean rightUpgrade = false;
      boolean topUpgrade = false;
      boolean bottomUpgrade = false;
      for(intAux=r.minX;intAux<=r.maxX;intAux++) {
        if(rows[intAux]==0) {
          if(intAux == (top-1))
            topUpgrade = true;
          if(intAux == (bottom+1))
            bottomUpgrade = true;
        }
        rows[intAux]+=r.width;
      }
      for(intAux=r.minY;intAux<=r.maxY;intAux++) {
        if(cols[intAux]==0) {
          if(intAux == (left-1))
            leftUpgrade = true;
          if(intAux == (right+1))
            rightUpgrade = true;
        }
        cols[intAux]+=r.height;
      }
      if(topUpgrade) { 
        for(intAux=0;(intAux<=r.maxX) && (rows[intAux]==0);intAux++)
          top=intAux;
        if(intAux==0)
          top=0;
        else
          top++;
      }
      if(bottomUpgrade) { 
        for(intAux=MAXX;(intAux>=r.minX) && (rows[intAux]==0);intAux--)
          bottom=intAux;
        if(intAux==MAXX)
          bottom=MAXX;
        else
          bottom--;
      }
      if(leftUpgrade) { 
        for(intAux=0;(intAux<=r.maxY) && (cols[intAux]==0);intAux++)
          left=intAux;
        if(intAux==0)
          left=0;
        else
          left++;
      }
      if(rightUpgrade) {
        for(intAux=MAXY;(intAux>=r.minY) && (cols[intAux]==0);intAux--)
          right=intAux;
        if(intAux==MAXY)
          right=MAXY;
        else
          right--;
      }
    }
  }
  class SolutionFoundException extends Exception{
    private static final long serialVersionUID = 1L;}
  class CannotMoveException extends Exception{
    private static final long serialVersionUID = 1L;}
  class RightBoundException extends Exception{
    private static final long serialVersionUID = 1L;}
  class LowerBoundException extends Exception{
    private static final long serialVersionUID = 1L;}
  class Rectangle{
    int width = 0;
    int height = 0;
    public Rectangle(int width, int height) {
      this.width = width;
      this.height = height;
    }
  }
  public class Point implements Comparable<Point>{
      private int x;
      private int y;
      public Integer threshold = 0;
      private Raisin raisin = null;
      public void setRaisin(Raisin r) {
        raisin = r;
      }
    public int getX() {
      return x;
    }
    public void setX(int x) {
      this.x = x;
      setThreshold();
    }
    public int getY() {
      return y;
    }
    public void setY(int y) {
      this.y = y;
      setThreshold();
    }
    private void setThreshold() {
      threshold = x * raisin.cakeCutter.WIDTH + y; 
    }
    @Override
    public int compareTo(Point o) {
      return threshold.compareTo(o.threshold);
    }
  }
  class Raisin implements Comparable<Raisin>{
    int number = 0;
    int x = 0;
    int y = 0;
    private int maxX = 0;
    private int maxY = 0;
    private int minX = 0;
    private int minY = 0;
    private int width = 0;
    private int height = 0;
    private Point bottomLeft = new Point();
      private Point topRight = new Point();
      private boolean first = false;
      public boolean last = false;
    
    private CakeCutter cakeCutter = null;
    private boolean shadow() {
      return shadowOnTop() || 
          shadowOnLeft() || 
          shadowOnRight() ||
          shadowOnBottom();
    }
    private boolean shadowOnTop() {
      if(minX == puzzle.top)
        return false;
      for(intAux=number+1;intAux<numRaisins;intAux++)
          if(raisins.get(intAux).x < minX)
            return false;
      if(allRowsAlreadyCovered(puzzle.top,minX-1))
        return false;
      //trace(" >> shadowOnTop("+number+")",DEBUG);
      return true;
    }
    private boolean allRowsAlreadyCovered(int begin, int end) {
      for(int i=begin;i<=end;i++) 
        for(int j=minY;j<=maxY;j++)
          if(!pointAlreadyCovered(i,j))
            return false;
      return true;
    }
    private boolean allCoLsAlreadyCovered(int begin, int end) {
      for(int i=begin;i<=end;i++) 
        for(int j=minX;j<=maxX;j++)
          if(!pointAlreadyCovered(j,i))
            return false;
      return true;
    }
    private boolean pointAlreadyCovered(int posx, int posy) {
      for(Raisin r:cakeCutter.raisins)
        if((r.number < number) &&
            (posx >= r.minX) &&
            (posx <= r.maxX) &&
            (posy >= r.minY) &&
            (posy <= r.maxY))
          return true;
      return false;
    }
    private boolean shadowOnLeft() {
      if(minY == puzzle.left)
        return false;
      for(intAux=number+1;intAux<numRaisins;intAux++)
          if(raisins.get(intAux).y < minY)
            return false;
      if(allCoLsAlreadyCovered(puzzle.left,minY-1))
        return false;
      //trace(" >> shadowOnLeft("+number+")",DEBUG);
      return true;
    }
    private boolean shadowOnRight() {
      if(maxY == puzzle.right)
        return false;
      for(intAux=number+1;intAux<numRaisins;intAux++) 
          if(raisins.get(intAux).y > maxY)
            return false;
      if(allCoLsAlreadyCovered(maxY+1,puzzle.right))
        return false;
      //trace(" >> shadowOnRight("+number+")",DEBUG);
      return true;
    }
    private boolean shadowOnBottom() {
      if(maxX == puzzle.bottom)
        return false;
      for(intAux=number+1;intAux<numRaisins;intAux++)
          if(raisins.get(intAux).x > maxX)
            return false;
      if(allRowsAlreadyCovered(maxX+1,puzzle.bottom))
        return false;
      //trace(" >> shadowOnBottom("+number+")",DEBUG);
      return true;
    }
    public Raisin(CakeCutter cakeCutter,  int number, int x, int y) {
      this.number = number;
      this.x = x;
      this.cakeCutter = cakeCutter;
      bottomLeft.setRaisin(this);
      topRight.setRaisin(this);
      setMinX(x);
      setMaxX(x);
      this.y = y;
      setMinY(y);
      setMaxY(y);     
      trace(" >> "+number+" new Raisin("+x+", "+y+")",DEBUG);
    }
    public boolean collision(Raisin other) throws LowerBoundException{
      if (this.topRight.getY() < other.bottomLeft.getY() 
              || this.bottomLeft.getY() > other.topRight.getY()) {
                return false;
            }
            if (this.topRight.getX() < other.bottomLeft.getX() 
              || this.bottomLeft.getX() > other.topRight.getX()) {
                return false;
            }
            if(this.x <= other.minX)
            throw lbe;
            return true;
    }
    public String printIt() {
      String response = "";
      for(int i=minX;i<=maxX;i++) {
        for(int j=minY;j<=maxY;j++)
          response+=cake[i][j];
        if(i < maxX)
          response+='\n';
      }
      trace(" >>printIt("+number+")",DEBUG);
      trace(response,DEBUG);
      return response;
    }     
    private void setMaxY(int max) {
      maxY = max;
      topRight.setY(max);
    }
    private void setMinX(int min) {
      minX = min;
      bottomLeft.setX(min);
    }   
    private void setMinY(int min) {
      minY = min;
      bottomLeft.setY(min);
    }   
    private void setMaxX(int max) {
      maxX = max;
      topRight.setX(max);
    }
    public void move() throws SolutionFoundException {
      trace(" >> move("+number+")",DEBUG);
      for(Rectangle r:cakeCutter.rectangles) {
        int lowerHorBound = y-r.width+1;
        lowerHorBound = (lowerHorBound > puzzle.left)?lowerHorBound:puzzle.left;
        int lowerVerBound = x-r.height+1;
        lowerVerBound = (lowerVerBound > puzzle.top)?lowerVerBound:puzzle.top;
        int upperHorBound = puzzle.right - r.width +1;
        upperHorBound = (y < upperHorBound)?y:upperHorBound;
        int upperVerBound = puzzle.bottom - r.height +1;
        upperVerBound = (x < upperVerBound)?x:upperVerBound;
        for(int i=lowerHorBound;i<=upperHorBound;i++) {
          if((i==puzzle.left) ||
             (i >= (puzzle.left + minRectWidth)))
            for(int j=lowerVerBound;j<=upperVerBound;j++) 
              if(!solutionFound ||
                    (i!=0) ||
                    (j!=0) ||
                    (maxSolutionWidth<=r.width)
                    )
                  try {
                    move(i,j,r);                        
                    if(last) {
                      solutions.add(new Solution(cakeCutter.raisins));
                      solutionFound = true;
                      throw cme;                          
                    }
                    else
                      if(!shadow()) {
                        puzzle.commit(this);
                        raisins.get(number+1).move();
                        puzzle.rollback(this);
                      }
                    
                  }catch(CannotMoveException e) {
                    cakeCutter.restoreFrom(number+1);
                  } catch (LowerBoundException e) {
                    break;
                  }
        }
        if((first) && 
            solutionFound &&
            (x==minRaisinX) &&
            (y==minRaisinY))
          return;
      }
      restore();
    }
    public void move(int hor_slide, int ver_slide, Rectangle re) throws CannotMoveException,LowerBoundException{
      setMinY(hor_slide);
      setMaxY(hor_slide+re.width-1);
      setMinX(ver_slide);
      setMaxX(ver_slide+re.height-1);
      width=re.width;
      height=re.height;
      for(Raisin ra: cakeCutter.raisins)
        if((ra!=this) 
            && (collision(ra)))
          throw cme;
    }
    public void restore(int newNumber) {
      number = newNumber;
      restore();
    }
    public void restore() {
      setMinX(x);
      setMaxX(x);
      setMinY(y);
      setMaxY(y); 
    }
    public int compareTo(Raisin o) {
      return bottomLeft.compareTo(o.bottomLeft);
    }
    public Raisin clone() throws CloneNotSupportedException {
      Raisin returned = new Raisin(cakeCutter,number,x,y);
      returned.setMaxX(maxX);
      returned.setMaxY(maxY);
      returned.setMinX(minX);
      returned.setMinY(minY);
      return returned;
    }
  }
  private static final int SIZE = 150;
  private static final int NONE = 0;
  private static final int ERROR = 1;
  private static final int INFO = 2;
  private static final int DEBUG = 3;
  private static final int SUPER = 4;
  private static final int LEVEL = NONE;
  public int numMovements = 0;
  public int numRaisins = 0;
  private int MAXX = 0;
  private int MAXY = 0;
  private int WIDTH = 0;
  private int HEIGHT = 0;
  int numPoints = 0;
  private int share = 0;
  List<Rectangle> rectangles = new ArrayList<Rectangle>();
  private List<Raisin> raisins = new ArrayList<Raisin>();
  private List<Solution> solutions = new ArrayList<Solution>();
  private int minRectWidth = 0;
  Puzzle puzzle = null;
  List<String> response = new ArrayList<String>();
  char[][] cake = new char[SIZE][SIZE];
  public static final SolutionFoundException sfe =  (new CakeCutter()).new SolutionFoundException();
  public static final CannotMoveException cme =  (new CakeCutter()).new CannotMoveException();
  public static final RightBoundException rbe =  (new CakeCutter()).new RightBoundException();
  public static final LowerBoundException lbe =  (new CakeCutter()).new LowerBoundException();
  public boolean solutionFound = false;
  int intAux = 0;
  public int minRaisinX = Integer.MAX_VALUE;
  public int minRaisinY = Integer.MAX_VALUE;
  public int maxSolutionWidth = Integer.MIN_VALUE;
  private void loadCake(String cake) {
    int x = 0;
    int y = 0;
    int numRaisin = 0;
    for(int i=0;i<cake.length();i++) {
      char c = cake.charAt(i);
      if(c=='\n') {
        y=0;
        x++;
        if(i<(cake.length()-1))
          MAXX = x;
      }
      else {
        if(c=='o') {
          raisins.add(new Raisin(this,numRaisin++,x,y));
          if(x < minRaisinX)
            minRaisinX = x;
          if(x < minRaisinX)
            minRaisinY = y;
          numRaisins++;
        }
        this.cake[x][y] = c;
        if(y > MAXY)
          MAXY = y;
        y++;
      }     
    }
    HEIGHT = MAXX + 1;
    WIDTH = MAXY + 1;
    trace(" >> loadCake WIDTH="+WIDTH+" HEIGHT="+HEIGHT,DEBUG);
    numPoints = (MAXX + 1) * (MAXY + 1);    
    share = numPoints / numRaisins;
    trace(" >> loadCake numPoints="+numPoints+" share="+share,DEBUG);
    for(int i=share;i>0;i--) 
      if(((share%i)==0) && 
          (i<=WIDTH) &&
          ((share/i)<=HEIGHT)) {
        trace(" >> loadCake new Rectangle("+i+","+(share/i)+")",DEBUG);
        rectangles.add(new Rectangle(i,share/i));
      }
    minRectWidth=rectangles.get(rectangles.size()-1).width;
    if(!raisins.isEmpty()) {
      raisins.get(0).first=true;
      raisins.get(raisins.size()-1).last=true;
      puzzle = new Puzzle(); 
    }
  }
  public static void trace(String message, int level) {
      if(level <= LEVEL)
        System.out.println(message);
    }
  public void restoreFrom(int from) {
    for(Raisin r:raisins)
      if(r.number >= from)
        r.restore();
  }
  public CakeCutter() {
  }
    public CakeCutter(String cake) {
      trace(cake,INFO);
        loadCake(cake);
    }    
    private  void solve() throws SolutionFoundException, CannotMoveException{
      if(!raisins.isEmpty())
        raisins.get(0).move();
    }
    public void restoreAll() {
      int i=0;
      for(Raisin r:raisins) {
        r.restore(i);
        i++;
      }
    }
    public List<String> cut() {
      try {
      solve();
    } catch (SolutionFoundException e) {
              
    } catch (CannotMoveException e) {
    }
      fillResponse(); 
        return response;
    }
  private void fillResponse() {
    trace("fillResponse size="+solutions.size(),INFO);
    if(!solutions.isEmpty()) {
      Collections.sort(solutions);
      for(Raisin r : solutions.get(0).raisins)
        response.add(r.printIt());
    }
  }
}
