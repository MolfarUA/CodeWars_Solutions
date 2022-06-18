591f3a2a6368b6658800020e


import java.util.*;

public class BreakEvilPieces {
  private final int height;
  private final int width;
  private final char[][] borders;
  private final Cell[][] cells;

  private BreakEvilPieces(String shape) {
    String[] lines = shape.split("\r?\n");
    height = lines.length;
    int w = 0;
    for (String line : lines)
      w = Math.max(w, line.length());
    width = w;
    borders = new char[height][];
    for (int i = 0; i < height; i++) {
      borders[i] = Arrays.copyOf(lines[i].toCharArray(), width);
      Arrays.fill(borders[i], lines[i].length(), width, ' ');
    }
    cells = new Cell[height + 1][width + 1];
    for (int y = 0; y <= height; y++) {
      Cell[] row = cells[y];
      for (int x = 0; x <= width; x++)
        row[x] = new Cell(x, y);
    }
  }

  private boolean horizontallyConnected(int xMin, int y) {
    if (xMin < 0 || xMin >= width)
      return false;
    if (y == 0 || y == height)
      return true;
    char b1 = borders[y - 1][xMin];
    char b2 = borders[y][xMin];
    return !((b1 == '|' || b1 == '+') && (b2 == '|' || b2 == '+'));
  }

  private boolean verticallyConnected(int x, int yMin) {
    if (yMin < 0 || yMin >= height)
      return false;
    if (x == 0 || x == width)
      return true;
    char b1 = borders[yMin][x - 1];
    char b2 = borders[yMin][x];
    return !((b1 == '-' || b1 == '+') && (b2 == '-' || b2 == '+'));
  }

  private class Cell {
    final int x;
    final int y;
    Piece piece;

    Cell(int x, int y) {
      this.x = x;
      this.y = y;
    }

    void getConnected(List<Cell> list) {
      list.clear();
      if (horizontallyConnected(x - 1, y))
        list.add(cells[y][x - 1]);
      if (horizontallyConnected(x, y))
        list.add(cells[y][x + 1]);
      if (verticallyConnected(x, y - 1))
        list.add(cells[y - 1][x]);
      if (verticallyConnected(x, y))
        list.add(cells[y + 1][x]);
    }
  }

  private class Piece {
    int left;
    int right;
    int top;
    int bottom;

    Piece() {
      left = top = Integer.MAX_VALUE;
    }

    void addCell(Cell c) {
      left = Math.min(left, c.x);
      right = Math.max(right, c.x);
      top = Math.min(top, c.y);
      bottom = Math.max(bottom, c.y);
      c.piece = this;
    }

    boolean isFinite() {
      return left > 0;
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder();
      String lineSep = System.lineSeparator();
      int bWidth = right - left + 2;
      int bHeight = bottom - top + 2;
      char[] borderRow = new char[bWidth];
      for (int yb = 0, y = top - 1; yb < bHeight; yb++, y++) {
        Cell[] upperCellRow = cells[y];
        Cell[] lowerCellRow = cells[y + 1];
        int lastNonSpace = 0;
        for (int xb = 0, x = left - 1; xb < bWidth; xb++, x++) {
          int squareState = 0;
          if (upperCellRow[x].piece == this)
            squareState += 0b1000; // o? ??
          if (upperCellRow[x + 1].piece == this)
            squareState += 0b0100; // ?o ??
          if (lowerCellRow[x].piece == this)
            squareState += 0b0010; // ?? o?
          if (lowerCellRow[x + 1].piece == this)
            squareState += 0b0001; // ?? ?o
          char c = borders[y][x];
          switch (squareState) {
            case 0b0000:
              c = ' ';
              break;
            case 0b0101:
            case 0b1010:
              if (c == '+') {
                c = borders[y][squareState == 0b1010 ? x - 1 : x + 1];
                c = c == '-' || c == '+' ? '+' : '|';
              }
              break;
            case 0b0011:
            case 0b1100:
              if (c == '+') {
                c = borders[squareState == 0b1100 ? y - 1 : y + 1][x];
                c = c == '|' || c == '+' ? '+' : '-';
              }
              break;
            case 0b1111:
              break;
            default:
              c = '+';
          }
          borderRow[xb] = c;
          if (c != ' ')
            lastNonSpace = xb;
        }
        if (yb > 0)
          sb.append(lineSep);
        sb.append(borderRow, 0, lastNonSpace + 1);
      }
      return sb.toString();
    }
  }

  private List<Piece> breakIntoPieces() {
    List<Piece> pieces = new ArrayList<>();
    Set<Cell> queue = new HashSet<>((height + 1) * (width + 1));
    List<Cell> neighbours = new ArrayList<>(4);
    for (Cell[] row : cells)
      for (Cell c : row)
        if (c.piece == null) {
          Piece p = new Piece();
          pieces.add(p);
          while (true) {
            p.addCell(c);
            c.getConnected(neighbours);
            for (Cell n : neighbours)
              if (n.piece == null)
                queue.add(n);
            Iterator<Cell> it = queue.iterator();
            if (!it.hasNext())
              break;
            c = it.next();
            it.remove();
          }
        }
    return pieces;
  }

  public List<String> solve() {
    List<Piece> pieces = breakIntoPieces();
    List<String> strings = new ArrayList<>(pieces.size() - 1);
    for (Piece p : pieces)
      if (p.isFinite())
        strings.add(p.toString());
    return strings;
  }

  public static List<String> solve(String shape) {
    return new BreakEvilPieces(shape).solve();
  }
}
________________________________________
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;

public class BreakEvilPieces
{
  protected static class Pair<T1, T2>
  {
    public T1 v1;
    public T2 v2;

    Pair(T1 v1, T2 v2)
    {
      this.v1 = v1;
      this.v2 = v2;
    }
  }

  protected static class Coordinate
  {
    public final int x, y;

    Coordinate(int x, int y)
    {
      this.x = x;
      this.y = y;
    }

    Coordinate(Coordinate originalCoordinate)
    {
      x = originalCoordinate.x;
      y = originalCoordinate.y;
    }
  }

  protected static class Cell
  {
    public static final int
      QUADRANT_TOP_LEFT = 0,
      QUADRANT_TOP_RIGHT = 1,
      QUADRANT_BOTTOM_LEFT = 2,
      QUADRANT_BOTTOM_RIGHT = 3,
      QUADRANT_COUNT = 4,
      V_BORDER = 1,
      H_BORDER = 2;

    protected Coordinate origin;
    protected int[] quadrants;
    protected int borders;

    Cell(Coordinate c)
    {
      origin = c;
      quadrants = new int[QUADRANT_COUNT];
      borders = 0;
    }

    Cell(Cell originalCell)
    {
      origin = new Coordinate(originalCell.origin);
      quadrants = new int[QUADRANT_COUNT];
      borders = originalCell.borders;

      for(int i=0;i<QUADRANT_COUNT;++i)
      {
        quadrants[i] = originalCell.quadrants[i];
      }
    }

    public Coordinate getOrigin()
    {
      return origin;
    }

    public int getValue(int q)
    {
      if(q >= 0 && q < QUADRANT_COUNT)
      {
        return quadrants[q];
      }

      return 0;
    }

    public void setValue(int q, int v)
    {
      if(q >= 0 && q < QUADRANT_COUNT)
      {
        quadrants[q] = v;
      }
    }

    public void setValue(int v)
    {
      for(int q=0;q<Cell.QUADRANT_COUNT;++q)
      {
        quadrants[q] = v;
      }
    }

    public boolean hasValue()
    {
      for(int quadrant : quadrants)
      {
        if(quadrant > 0)
        {
          return true;
        }
      }

      return false;
    }

    public boolean hasValue(int v)
    {
      for(int quadrant : quadrants)
      {
        if(quadrant == v)
        {
          return true;
        }
      }

      return false;
    }

    public void clearBorders()
    {
      borders = 0;
    }

    public void setBorder(int b)
    {
      borders |= b;
    }

    public boolean hasBorder(int b)
    {
      return (borders & b) == b;
    }

    public int getBorders()
    {
      return borders;
    }
  }

  protected static class Matrix
  {
    protected int width, height;
    protected List<Cell> matrix;

    Matrix(int w, int h)
    {
      width = w;
      height = h;
      matrix = new ArrayList<Cell>(w * h);

      for(int y=0;y<h;++y)
      {
        for(int x=0;x<w;++x)
        {
          matrix.add(new Cell(new Coordinate(x, y)));
        }
      }
    }

    Matrix(Matrix originalMatrix)
    {
      width = originalMatrix.width;
      height = originalMatrix.height;

      matrix = new ArrayList<Cell>(originalMatrix.matrix.size());

      for(Cell cell : originalMatrix.matrix)
      {
        matrix.add(new Cell(cell));
      }
    }

    public int getWidth()
    {
      return width;
    }

    public int getHeight()
    {
      return height;
    }

    public int toOffset(int x, int y)
    {
      return (y * width) + x;
    }

    public Cell getCell(int x, int y)
    {
      if(x >= 0 && y >= 0 && x < width && y < height)
      {
        return matrix.get(toOffset(x, y));
      }

      return null;
    }

    public List<Cell> getCellList()
    {
      return matrix;
    }

    public static Matrix fromString(String shape)
    {
      int i, x, y, lineCount = 1,
        lineLength = 0,
        maxLineLength = 0,
        shapeLength = shape.length();

      for(i=0;i<shapeLength;++i)
      {
        switch(shape.charAt(i))
        {
          case '\n':
            ++lineCount;
            if(lineLength > maxLineLength)
            {
              maxLineLength = lineLength;
            }
            lineLength = 0;
            break;

          default:
            ++lineLength;
            break;
        }
      }

      if(lineLength > maxLineLength)
      {
        maxLineLength = lineLength;
      }

      Matrix matrix = new Matrix(maxLineLength, lineCount);

      loop: for(x=y=i=0;i<shapeLength;++i)
      {
        char c = shape.charAt(i);

        switch(c)
        {
          case '+':
            matrix.getCell(x, y).setBorder(
              Cell.H_BORDER | Cell.V_BORDER
            );
            break;

          case '-':
            matrix.getCell(x, y).setBorder(Cell.H_BORDER);
            break;

          case '|':
            matrix.getCell(x, y).setBorder(Cell.V_BORDER);
            break;

          case '\n':
            x = 0;
            ++y;
            continue loop;
        }

        ++x;
      }

      return matrix;
    }

    public String toString()
    {
      StringBuffer buffer = new StringBuffer();
      int x, y, minSpace = width;

      for(y=0;y<height;++y)
      {
        int start = y * width;
        int end = start + width;

        for(x=start;x<end;++x)
        {
          if(matrix.get(x).hasValue())
          {
            int space = x - (y * width);

            if(space < minSpace)
            {
              minSpace = space;
            }

            break;
          }
        }
      }

      for(y=0;y<height;++y)
      {
        int start = y * width;
        int end = start + width;

        start += minSpace;

        for(x=end-1;x>=start;--x)
        {
          end = x;

          if(matrix.get(x).hasValue())
          {
            end += 1;

            break;
          }
        }

        if(end > start)
        {
          for(x=start;x<end;++x)
          {
            Cell cell = matrix.get(x);

            boolean hasHorizontal = cell.hasBorder(Cell.H_BORDER),
              hasVertical = cell.hasBorder(Cell.V_BORDER);

            if(hasHorizontal && hasVertical)
            {
              char appendChar = '+';
              int tl = cell.getValue(Cell.QUADRANT_TOP_LEFT),
                tr = cell.getValue(Cell.QUADRANT_TOP_RIGHT),
                bl = cell.getValue(Cell.QUADRANT_BOTTOM_LEFT),
                br = cell.getValue(Cell.QUADRANT_BOTTOM_RIGHT);

              if((tl == tr && bl != tl && br != tl) ||
                (bl == br && tl != bl && tr != bl))
              {
                Coordinate origin = cell.getOrigin();
                Cell tc = getCell(origin.x, origin.y - 1),
                  bc = getCell(origin.x, origin.y + 1);

                if((tc == null || !tc.hasBorder(Cell.V_BORDER) ||
                  tc.hasBorder(Cell.V_BORDER | Cell.H_BORDER)) &&
                  (bc == null || !bc.hasBorder(Cell.V_BORDER) ||
                  bc.hasBorder(Cell.V_BORDER | Cell.H_BORDER)))
                {
                  appendChar = '-';
                }
              }
              else if((tl == bl && tr != tl && br != tl) ||
                (tr == br && tl != tr && bl != tr))
              {
                Coordinate origin = cell.getOrigin();
                Cell lc = getCell(origin.x - 1, origin.y),
                  rc = getCell(origin.x + 1, origin.y);

                if((lc == null || !lc.hasBorder(Cell.H_BORDER) ||
                  lc.hasBorder(Cell.V_BORDER | Cell.H_BORDER)) &&
                  (rc == null || !rc.hasBorder(Cell.H_BORDER) ||
                  rc.hasBorder(Cell.V_BORDER | Cell.H_BORDER)))
                {
                  appendChar = '|';
                }
              }

              buffer.append(appendChar);
            }
            else if(hasHorizontal)
            {
              buffer.append('-');
            }
            else if(hasVertical)
            {
              buffer.append('|');
            }
            else
            {
              buffer.append(' ');
            }
          }

          buffer.append('\n');
        }
      }

      if(buffer.length() > 0)
      {
        buffer.setLength(buffer.length() - 1);
      }

      return buffer.toString();
    }
  }

  protected static class Solver
  {
    protected Pair<Cell, Integer> findEmptySpace(Matrix matrix)
    {
      for(Cell cell : matrix.getCellList())
      {
        for(int q=0;q<Cell.QUADRANT_COUNT;++q)
        {
          if(cell.getValue(q) == 0)
          {
            return new Pair<Cell, Integer>(cell, q);
          }
        }
      }

      return null;
    }

    protected int floodFillWithMask(
      Matrix matrix, Cell cell, int mask, int quadrant
    )
    {
      if(cell == null || cell.getValue(quadrant) == mask)
      {
        return 0;
      }

      cell.setValue(quadrant, mask);

      int count = 1;
      Coordinate origin = cell.getOrigin();
      Cell left = matrix.getCell(origin.x - 1, origin.y),
        right = matrix.getCell(origin.x + 1, origin.y),
        top = matrix.getCell(origin.x, origin.y - 1),
        bottom = matrix.getCell(origin.x, origin.y + 1);

      switch(quadrant)
      {
        case Cell.QUADRANT_TOP_LEFT:

          floodFillWithMask(matrix, left, mask, Cell.QUADRANT_TOP_RIGHT);
          floodFillWithMask(matrix, top, mask, Cell.QUADRANT_BOTTOM_LEFT);

          if(!cell.hasBorder(Cell.V_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_TOP_RIGHT
            );
          }

          if(!cell.hasBorder(Cell.H_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_BOTTOM_LEFT
            );
          }

          break;

        case Cell.QUADRANT_TOP_RIGHT:

          floodFillWithMask(matrix, right, mask, Cell.QUADRANT_TOP_LEFT);
          floodFillWithMask(matrix, top, mask, Cell.QUADRANT_BOTTOM_RIGHT);

          if(!cell.hasBorder(Cell.V_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_TOP_LEFT
            );
          }

          if(!cell.hasBorder(Cell.H_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_BOTTOM_RIGHT
            );
          }

          break;

        case Cell.QUADRANT_BOTTOM_LEFT:

          floodFillWithMask(matrix, left, mask, Cell.QUADRANT_BOTTOM_RIGHT);
          floodFillWithMask(matrix, bottom, mask, Cell.QUADRANT_TOP_LEFT);

          if(!cell.hasBorder(Cell.V_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_BOTTOM_RIGHT
            );
          }

          if(!cell.hasBorder(Cell.H_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_TOP_LEFT
            );
          }

          break;

        case Cell.QUADRANT_BOTTOM_RIGHT:

          floodFillWithMask(matrix, right, mask, Cell.QUADRANT_BOTTOM_LEFT);
          floodFillWithMask(matrix, bottom, mask, Cell.QUADRANT_TOP_RIGHT);

          if(!cell.hasBorder(Cell.V_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_BOTTOM_LEFT
            );
          }

          if(!cell.hasBorder(Cell.H_BORDER))
          {
            count += floodFillWithMask(
              matrix, cell, mask, Cell.QUADRANT_TOP_RIGHT
            );
          }

          break;
      }


      return count;
    }

    protected Set<Integer> maskMatrix(Matrix matrix)
    {
      int mask = 1;
      Set<Integer> maskValues = new HashSet<Integer>();

      while(true)
      {
        Pair<Cell, Integer> emptySpace = findEmptySpace(matrix);

        if(emptySpace == null)
        {
          break;
        }

        if(floodFillWithMask(matrix, emptySpace.v1, mask, emptySpace.v2) > 0)
        {
          maskValues.add(mask++);
        }
      }

      return maskValues;
    }

    protected void invalidateMaskValues(
      Matrix matrix, Set<Integer> maskValues
    )
    {
      int x, y, width = matrix.getWidth(), height = matrix.getHeight();

      // top line
      for(x=0,y=0;x<width;++x)
      {
        Cell cell = matrix.getCell(x, y);

        maskValues.remove(cell.getValue(Cell.QUADRANT_TOP_LEFT));
        maskValues.remove(cell.getValue(Cell.QUADRANT_TOP_RIGHT));
      }

      // left column
      for(y=0,x=0;y<height;++y)
      {
        Cell cell = matrix.getCell(x, y);

        maskValues.remove(cell.getValue(Cell.QUADRANT_TOP_LEFT));
        maskValues.remove(cell.getValue(Cell.QUADRANT_BOTTOM_LEFT));
      }

      // bottom line
      for(x=0,y=height-1;x<width;++x)
      {
        Cell cell = matrix.getCell(x, y);

        maskValues.remove(cell.getValue(Cell.QUADRANT_BOTTOM_LEFT));
        maskValues.remove(cell.getValue(Cell.QUADRANT_BOTTOM_RIGHT));
      }

      // right column
      for(y=0,x=width-1;y<height;++y)
      {
        Cell cell = matrix.getCell(x, y);

        maskValues.remove(cell.getValue(Cell.QUADRANT_TOP_RIGHT));
        maskValues.remove(cell.getValue(Cell.QUADRANT_BOTTOM_RIGHT));
      }
    }

    protected String getPiece(Matrix matrix, int maskValue)
    {
      for(Cell cell : matrix.getCellList())
      {
        int removed = 0;

        for(int q=0;q<Cell.QUADRANT_COUNT;++q)
        {
          if(cell.getValue(q) != maskValue)
          {
            ++removed;

            cell.setValue(q, 0);
          }
        }

        if(removed == Cell.QUADRANT_COUNT)
        {
          cell.clearBorders();
        }
      }

      return matrix.toString();
    }

    public List<String> solve(String shape)
    {
      List<String> pieces = new ArrayList<String>();

      if(shape.length() > 0)
      {
        Matrix matrix = Matrix.fromString(shape);
        Set<Integer> maskValues = maskMatrix(matrix);

        invalidateMaskValues(matrix, maskValues);

        for(Integer maskValue : maskValues)
        {
          String piece = getPiece(new Matrix(matrix), maskValue);

          if(piece.length() > 0)
          {
            pieces.add(piece);
          }
        }
      }

      return pieces;
    }
  }

  public static List<String> solve(String shape)
  {
    return new Solver().solve(shape);
  }
}
__________________________________________________________________________________
import java.util.*;
import java.util.stream.*;
import java.awt.Point;

public class BreakEvilPieces {
  
  private static boolean isVertical(char c) {
    return c == '|' || c == '+';
  }
  
  public static List <String> solve(String shape) {
    return new BreakEvilPieces(shape).getPieces();
  }
  
  private Map <Point, Character> nodes = new HashMap <> ();
  private Set <Point>            visit = new HashSet <> ();
  
  private BreakEvilPieces(String shape) {
    shape = shape.replaceAll("(?<=.)(?=.)", "_").replaceAll("(?<![-+])_|_(?![-+])", " ")
                 .replaceAll("\n", "\n\n");
    
    String[] rows = shape.split("\n");
        
    for (int i = 0; i < rows.length; i += 2) for (int j = 0, l = rows[i].length(); j < l; j++) 
      nodes.put(new Point(i, j), rows[i].charAt(j));
      
    for (int i = 1; i < rows.length; i += 2) {
      String u = rows[i - 1], 
             d = rows[i + 1];
      for (int j = 0, l = Math.min(u.length(), d.length()); j < l; j++)
        nodes.put(new Point(i, j), isVertical(u.charAt(j)) && isVertical(d.charAt(j)) ? '_' : ' ');
    }
  }
  
  private Point findNext() {
    return nodes.keySet().stream().filter(p -> nodes.get(p) == ' ' && !visit.contains(p))
                                  .findFirst().orElse(null);
  }
  
  private List <Point> expandPiece(Point curpt) {
    Queue <Point> queue = new LinkedList <> ();
    List <Point>  piece = new ArrayList <> ();
    boolean       close = true;
    Point         nxtpt;
    
    queue.add(curpt);
    visit.add(curpt);
        
    while (!queue.isEmpty()) {
      curpt = queue.poll();
      for (int i = -1; i < 2; i++) for (int j = -1; j < 2; j++) {
        if (visit.contains(nxtpt = new Point(curpt.x + i, curpt.y + j))) continue;
        try {
          if (nodes.get(nxtpt) != ' ') { piece.add(nxtpt); continue; }
          queue.add(nxtpt);
          visit.add(nxtpt);
        }
        catch (Exception e) { close = false; }
      }
    }
    return close ? piece : null;
  }
  
  private List <String> getPieces() {
    List <String> all_pieces = new ArrayList <> ();
    while (true) try {
      List <Point> piece = expandPiece(findNext());
      if (piece != null) all_pieces.add(constructPiece(piece));
    }
    catch (Exception e) { return all_pieces; }
  }
  
  private String constructPiece(List <Point> piece) {
    int min_x = Integer.MAX_VALUE,    max_x = Integer.MIN_VALUE,
        min_y = Integer.MAX_VALUE,    max_y = Integer.MIN_VALUE;
    
    for (Point p : piece) {
      if (p.x < min_x) min_x = p.x;
      if (p.x > max_x) max_x = p.x;
      if (p.y < min_y) min_y = p.y;
      if (p.y > max_y) max_y = p.y;
    }
    
    char[][] answr = new char[(max_x - min_x) / 2 + 1][(max_y - min_y) / 2 + 1];
    for (var r : answr) Arrays.fill(r, ' ');
    for (var p : piece) {
      char c = nodes.get(p);
      if (c == ' ') nodes.remove(p);
      if (c == '_') continue;
      else if (c != '+') answr[(p.x - min_x) / 2][(p.y - min_y) / 2] = c;
      else {
        int hor_adj = 0, ver_adj = 0;
        if (piece.contains(new Point(p.x, p.y - 1))) hor_adj++;
        if (piece.contains(new Point(p.x, p.y + 1))) hor_adj++;
        if (piece.contains(new Point(p.x - 1, p.y))) ver_adj++;
        if (piece.contains(new Point(p.x + 1, p.y))) ver_adj++;
        answr[(p.x - min_x) / 2][(p.y - min_y) / 2] = hor_adj > 0 && ver_adj > 0 ? '+' :
                                                      hor_adj > 1 && ver_adj < 1 ? '-' : '|';
      }
    }
    return Arrays.stream(answr).map(r -> new String(r).replaceAll(" +$", ""))
                               .collect(Collectors.joining("\n"));
  }
}
