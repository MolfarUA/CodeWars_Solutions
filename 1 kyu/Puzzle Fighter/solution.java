class Piece {
  constructor(color) {
    this.color = color;
    this.powerGem = false;
  }
}

class RegularPiece extends Piece {
  constructor(color) {
    super(color);
  }
}

class EmptyPiece extends Piece {
  constructor() {
    super(' ');
  }
}

class Gem {
  constructor(sx, sy, ex, ey, color) {
    this.startX = sx;
    this.startY = sy;
    this.endX = ex;
    this.endY = ey;
    this.color = color;
  }
}

class Spot {
  constructor(x, y, color = ' ') {
    this.x = x;
    this.y = y;
    this.piece = new Piece(color);
  }
  
  get occupied() {
    return this.piece.color !== ' ';
  }
  
  clear() {
    this.piece = new EmptyPiece();
  }
}

class Game {
  constructor(instructions) {
    this.instructions = instructions;
    this.board = [...Array(12)].map((_, i) => [...Array(6)].map(($, j) => new Spot(i, j)));
    this.gems = [];
    this.move = 0;
    this.continueEffects = true;
  }
  
  execute() {
    for (const [pair, instructions] of this.instructions) {
      this.move++;
      let ax = 0, ay = 3, bx = 1, by = 3;
      let pos = 0;
      for (let c of instructions) {
        switch(c) {
            case 'L': {
              if (ay && by) ay--, by--;
              break;
            }
            case 'R': {
              if (ay < 5 && by < 5) ay++, by++;
              break;
            }
            case 'A': {
              if (pos === 0) by++, bx--;
              if (pos === 1) bx++, by++;
              if (pos === 2) ax--, by--;
              if (pos === 3) ax++, by--;
              pos += 3;
              break;
            }
            case 'B': {
              if (pos === 0) bx--, by--;
              if (pos === 1) ax++, by++;
              if (pos === 2) ax--, by++;
              if (pos === 3) bx++, by--;
              pos++;
              break;
            }
        }
        pos %= 4;
        if (ay < 0 || by < 0) ay++, by++;
        if (ay > 5 || by > 5) ay--, by--;
      }
      
      if (this.board[ax][ay].occupied || this.board[bx][by].occupied) {
        // Top reached
        return;
      }
      this.board[ax][ay].piece = new Piece(pair[0]);
      this.board[bx][by].piece = new Piece(pair[1]);
      this.continueEffects = true;
      
      while (this.continueEffects) {
        this.continueEffects = false;
        this.dropPieces();
        this.performEffects();
        this.dropPieces();
      }
      //this.displayBoard();
    }
  }
  
  performEffects() {
    this.destroyGems();
    this.removeBrokenGems();
    this.mergeSingles();
    this.mergeSinglesWithGems();
    this.mergeGemsWithGems();
  }
  
  removeBrokenGems() {
    for (let i = this.gems.length - 1; i >= 0; i--) {
      let gem = this.gems[i];
      if (!this.board[gem.startX][gem.startY].occupied) {
        this.gems.splice(i, 1);
      }
    }
  }
  
  mergeSingles() {
    for (let x = 0; x < 11; x++) {
      for (let y = 0; y < 5; y++) {
        let piece = this.board[x][y].piece;
        let color = piece.color;
        if (piece.powerGem || color === ' ') continue;
        let h = 0, w = 0;
        while (y + w < 5 
               && this.board[x][y + w + 1].piece.color === color
               && !this.board[x][y + w + 1].piece.powerGem
               && this.board[x + 1][y + w + 1].piece.color === color
               && !this.board[x + 1][y + w + 1].piece.powerGem) w++;
        if (w < 1) continue;
        for (; x + h < 11; h++) {
          let all = true;
          for (let k = x + h, l = y; l <= y + w; l++) {
            if (this.board[k+1][l].piece.color !== color
               || this.board[k+1][l].piece.powerGem) all = false;
          }
          if (!all) break;
        }
        if (h < 1) continue;
        const newGem = new Gem(x, y, x + h, y + w, color);
        this.gems.push(newGem);
        for (let i = x; i <= x + h; i++) {
          for (let j = y; j <= y + w; j++) {
            this.board[i][j].piece.powerGem = true;
          }
        }
      }
    }
  }
  
  mergeSinglesWithGems() {
    for (const gem of this.gems) {
      const color = gem.color;
      
      if (gem.startY > 0) {
        let all = true;
        for (let x = gem.startX, y = gem.startY - 1; x <= gem.endX; x++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.startY--;
          for (let x = gem.startX, y = gem.startY; x <= gem.endX; x++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles on LEFT
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.endY < 5) {
        let all = true;
        for (let x = gem.startX, y = gem.endY + 1; x <= gem.endX; x++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.endY++;
          for (let x = gem.startX, y = gem.endY; x <= gem.endX; x++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles on RIGHT
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.startX > 0) {
        let all = true;
        for (let x = gem.startX - 1, y = gem.startY; y <= gem.endY; y++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.startX--;
          for (let x = gem.startX, y = gem.startY; y <= gem.endY; y++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles ABOVE
          this.mergeSinglesWithGems();
        }
      }
      
      if (gem.endX < 11) {
        let all = true;
        for (let x = gem.endX + 1, y = gem.startY; y <= gem.endY; y++) {
          if (this.board[x][y].piece.color !== color || this.board[x][y].piece.powerGem) {
            all = false;
          }
        }
        if (all) {
          gem.endX++;
          for (let x = gem.endX, y = gem.startY; y <= gem.endY; y++) {
            this.board[x][y].piece.powerGem = true;
          }
          // Merging gem with singles BELOW
          this.mergeSinglesWithGems();
        }
      }
      
    }
  }
  
  mergeGemsWithGems() {
    for (const gem of this.gems) {
      let right = this.gems.findIndex(other => other.color === gem.color && other.startX === gem.startX && other.endX === gem.endX && other.startY === gem.endY + 1);
      if (right !== -1) {
        // Merging 2 gems horizontally
        gem.endY = this.gems[right].endY;
        this.gems.splice(right, 1);
        this.mergeGemsWithGems();
      }
    }
    for (const gem of this.gems) {
      let below = this.gems.findIndex(other => other.color === gem.color && other.startY === gem.startY && other.endY === gem.endY && other.startX === gem.endX + 1);
      if (below !== -1) {
        // Merging 2 gems vertically
        gem.endX = this.gems[below].endX;
        this.gems.splice(below, 1);
        this.mergeGemsWithGems();
      }
    }
  }
  
  displayBoard() {
    console.log(`Board at move ${this.move}:`);
    console.log('-'.repeat(8));
    [...Array(12)].forEach((_, i) => console.log(`|${this.board[i].map(s => s.piece.color).join('')}|`));
    console.log('-'.repeat(8));
  }
  
  destroy(x, y, color) {
    if (x < 0 || y < 0 || x >= 12 || y >= 6) return;
    if (this.board[x][y].piece.color.toUpperCase() !== color.toUpperCase()) return;
    this.board[x][y].clear();
    for (const [dx, dy] of [ [0, -1], [-1, 0], [0, 1], [1, 0] ]) {
      this.destroy(x + dx, y + dy, color);
    }
  }
  
  destroyGems() {
    for (let x = 0; x < 12; x++) {
      for (let y = 0; y < 6; y++) {
        let color = this.board[x][y].piece.color;
        if (color === '0') {
          if (x !== 11 && this.board[x+1][y].occupied && this.board[x+1][y].piece.color !== '0') {
            let color = this.board[x+1][y].piece.color.toUpperCase();
            for (let i = 0; i < 12; i++) {
              for (let j = 0; j < 6; j++) {
                if (this.board[i][j].piece.color.toUpperCase() === color) {
                  this.board[i][j].clear();
                }
              }
            }
          }
          this.board[x][y].clear();
        } else if (/[rgby]/.test(color)) {
          for (const [dx, dy] of [ [0, -1], [-1, 0], [0, 1], [1, 0] ]) {
            let nx = x + dx, ny = y + dy;
            if (nx < 0 || ny < 0 || nx >= 12 || ny >= 6) continue;
            let col = this.board[nx][ny].piece.color;
            if (col.toUpperCase() === color.toUpperCase()) {
              this.destroy(nx, ny, col);
              this.board[x][y].clear();
            }
          }
        }
      }
    }
  }
  
  dropPieces() {
    let modified = false;
    for (let i = 11; i >= 0; i--) {
      for (let j = 0; j < 6; j++) {
        if (this.board[i][j].piece.color !== ' ') {
          if (this.board[i][j].piece.powerGem) {
            const gem = this.gems.find(gem => i === gem.endX && j === gem.endY);
            if (!gem) continue;
            // move all powergem's pieces down
            for (let k = i + 1; k < 12; k++) {
              let isClearBelow = true;
              for (let l = gem.startY; l <= gem.endY; l++) {
                if (this.board[k][l].occupied) isClearBelow = false;
              }
              if (!isClearBelow) break;
              for (let l = k; l > gem.startX; l--) {
                for (let m = j; m >= gem.startY; m--) {
                  this.board[l][m].piece = this.board[l - 1][m].piece;
                  this.board[l - 1][m].piece = new EmptyPiece();
                }
              }
              gem.startX++;
              gem.endX++;
              modified = true;
            }
          } else {
            // non-powergem pieces
            for (let k = i + 1; k < 12; k++) {
              if (this.board[k][j].occupied) break;
              this.board[k][j].piece = this.board[k - 1][j].piece;
              this.board[k - 1][j].piece = new EmptyPiece();
              modified = true;
            }
          }
        }
      }
    }
    if (modified) {
      this.continueEffects = true;
      this.dropPieces();
    }
  }
  
  
  
  toString() {
    return this.board.map(row => row.map(spot => spot.piece.color).join('')).join('\n');
  }
}

function puzzleFighter(arr) {
  const board = [...Array(12)].map(_ => ' '.repeat(6));
  const game = new Game(arr);
  game.execute();
  return game.toString();
}

###############################
import java.util.*;

public class PuzzleFighter {
    private static final int WIDTH = 6;
    private static final int HEIGHT = 12;
    private static final int MAX_X = WIDTH - 1;
    private static final int MAX_Y = HEIGHT - 1;
    private static final int DROP_ALLEY = 3;
    private static final int[][][][] NEIGHBOURS = new int[HEIGHT][WIDTH][][];
    static {
        List<int[]> nList = new ArrayList<>(4);
        for (int y = 0; y <= MAX_Y; y++) {
            int[][][] nRow = NEIGHBOURS[y];
            for (int x = 0; x <= MAX_X; x++) {
                if (x > 0)
                    nList.add(new int[] { y, x - 1 });
                if (x < MAX_X)
                    nList.add(new int[] { y, x + 1 });
                if (y > 0)
                    nList.add(new int[] { y - 1, x });
                if (y < MAX_Y)
                    nList.add(new int[] { y + 1, x });
                nRow[x] = nList.toArray(new int[nList.size()][]);
                nList.clear();
            }
        }
    }

    private enum Color {
        RED('R'), BLUE('B'), GREEN('G'), YELLOW('Y'), RAINBOW('0');

        char letter;

        Color(char letter) {
            this.letter = letter;
        }
    }

    private final Gem[][] field = new Gem[HEIGHT][WIDTH];
    private final GemExpander expander = new GemExpander(field);

    private static class Gem {
        final Color color;
        final boolean special;
        int x0; // left column of the gem
        int y0; // bottom row of the gem
        int x1; // right column of the gem, 0 <= x0 <= x1 <= MAX_X
        int y1; // top row of the gem, 0 <= y0 <= y1 <= MAX_Y

        Gem(int x, int y, char c) {
            special = Character.isLowerCase(c) || c == '0';
            if (special)
                c = Character.toUpperCase(c);
            Color clr = null;
            for (Color cv : Color.values())
                if (c == cv.letter) {
                    clr = cv;
                    break;
                }
            if (clr == null)
                throw new IllegalArgumentException("Inadmissible color letter: " + c);
            color = clr;
            x0 = x1 = x;
            y0 = y1 = y;
        }

        Gem(int x0, int y0, int x1, int y1, Color c) {
            color = c;
            special = false;
            this.x0 = x0;
            this.y0 = y0;
            this.x1 = x1;
            this.y1 = y1;
        }

        Gem putOnField(Gem[][] field) {
            for (int y = y0; y <= y1; y++) {
                Gem[] row = field[y];
                for (int x = x0; x <= x1; x++)
                    row[x] = this;
            }
            return this;
        }

        boolean drop(Gem[][] field) {
            int y0n;
            outer:
            for (y0n = y0 - 1; y0n >= 0; y0n--) {
                Gem[] row = field[y0n];
                for (int x = x0; x <= x1; x++)
                    if (row[x] != null)
                        break outer;
            }
            y0n++;
            if (y0n == y0)
                return false;
            int y1n = y0n + (y1 - y0);
            for (int y = Math.max(y0, y1n + 1); y <= y1; y++)
                Arrays.fill(field[y], x0, x1 + 1, null);
            for (int y = Math.min(y0 - 1, y1n); y >= y0n; y--)
                Arrays.fill(field[y], x0, x1 + 1, this);
            y0 = y0n;
            y1 = y1n;
            return true;
        }
    }

    private Gem[] droppedPair(String gemsStr, String instructons) {
        int x1 = DROP_ALLEY;
        int r = 0; // rotation: 0 - second gem is below first, 1 - to left, 2 - above, 3 - to right
        for (int i = 0, len = instructons.length(); i < len; i++) {
            switch (instructons.charAt(i)) {
                case 'L':
                    x1--;
                    break;
                case 'R':
                    x1++;
                    break;
                case 'A':
                    r--;
                    break;
                case 'B':
                    r++;
                    break;
            }
            r = (r + 4) % 4;
            if (x1 < 0 || x1 == 0 && r == 1)
                x1++;
            else if (x1 > MAX_X || x1 == MAX_X && r == 3)
                x1--;
        }
        int y1 = MAX_Y;
        int x2 = x1;
        int y2 = y1;
        switch (r) {
            case 0:
                y2--;
                break;
            case 1:
                x2--;
                break;
            case 2:
                y1--;
                break;
            case 3:
                x2++;
                break;
        }
        return field[y1][x1] == null && field[y2][x2] == null
                ? new Gem[] { new Gem(x1, y1, gemsStr.charAt(0)).putOnField(field),
                        new Gem(x2, y2, gemsStr.charAt(1)).putOnField(field) }
                : null;
    }

    private boolean drop() {
        boolean dropped = false;
        Gem[] row = field[0];
        for (int y = 1; y <= MAX_Y; y++) {
            Gem[] lowerRow = row;
            row = field[y];
            for (int x = 0; x <= MAX_X; x++) {
                Gem g = row[x];
                if (g != null) {
                    if (lowerRow[x] == null)
                        dropped |= g.drop(field);
                    x = g.x1;
                }
            }
        }
        return dropped;
    }

    private boolean shatter() { // apply Crash and Rainbow Gems' effects
        List<Gem> rainbowGems = new ArrayList<>();
        List<Gem> crashGems = new ArrayList<>();
        for (Gem[] row : field)
            for (Gem g : row)
                if (g != null && g.special)
                    if (g.color == Color.RAINBOW)
                        rainbowGems.add(g);
                    else
                        crashGems.add(g);
        boolean shattered = false;
        if (!rainbowGems.isEmpty()) {
            Set<Color> removedColors = EnumSet.noneOf(Color.class);
            for (Gem g : rainbowGems)
                if (g.y0 > 0) {
                    Gem lower = field[g.y0 - 1][g.x0];
                    if (lower != null)
                        removedColors.add(lower.color);
                }
            for (Gem g : rainbowGems)
                field[g.y0][g.x0] = null;
            if (!removedColors.isEmpty()) {
                shattered = true;
                crashGems.clear();
                for (int y = 0; y < HEIGHT; y++) {
                    Gem[] row = field[y];
                    for (int x = 0; x < WIDTH; x++) {
                        Gem g = row[x];
                        if (g != null) {
                            Color c = g.color;
                            if (removedColors.contains(c))
                                row[x] = null;
                            else if (g.special && c != Color.RAINBOW)
                                crashGems.add(g);
                        }
                    }
                }
            }
        }
        if (!crashGems.isEmpty()) {
            Queue<int[]> queue = new ArrayDeque<>();
            for (Gem crGem : crashGems) {
                if (field[crGem.y0][crGem.x0] == null) // already crashed
                    continue;
                field[crGem.y0][crGem.x0] = null;
                Color crashColor = crGem.color;
                boolean crashed = false;
                for (int[] cell = new int[] { crGem.y0, crGem.x0 }; cell != null; cell = queue.poll())
                    for (int[] nCell : NEIGHBOURS[cell[0]][cell[1]]) {
                        Gem g = field[nCell[0]][nCell[1]];
                        if (g != null && g.color == crashColor) {
                            field[nCell[0]][nCell[1]] = null;
                            crashed = true;
                            queue.add(nCell);
                        }
                    }
                if (crashed)
                    shattered = true;
                else
                    field[crGem.y0][crGem.x0] = crGem;
            }
        }
        return shattered;
    }

    private static boolean individualOfColor(Gem g, Color c) {
        return g != null && g.color == c && g.x0 == g.x1;
    }

    private void combineIndividuals(int yStart, int xStart) {
        Gem[] currentRow = field[yStart];
        Gem[] belowRow = field[yStart - 1];
        xStart--;
        while (true) {
            xStart++;
            if (xStart >= MAX_X) {
                yStart--;
                if (yStart == 0)
                    return;
                currentRow = belowRow;
                belowRow = field[yStart - 1];
                xStart = 0;
            }
            Gem g = currentRow[xStart];
            if (g == null || g.special)
                continue;
            Color c = g.color;
            int xEnd;
            for (xEnd = xStart; xEnd <= MAX_X; xEnd++) {
                if (!individualOfColor(currentRow[xEnd], c))
                    break;
                if (!individualOfColor(belowRow[xEnd], c))
                    break;
            }
            if (xEnd < xStart + 2)
                continue;
            int yEnd;
            outer:
            for (yEnd = yStart - 2; yEnd >= 0; yEnd--) {
                Gem[] row = field[yEnd];
                for (int x = xStart; x < xEnd; x++)
                    if (!individualOfColor(row[x], c))
                        break outer;
            }
            new Gem(xStart, yEnd + 1, --xEnd, yStart, c).putOnField(field);
            xStart = xEnd;
        }
    }

    private static class GemExpander {
        Gem[][] field;
        Queue<int[]> queue = new ArrayDeque<>();
        int x0;
        int y0;
        int x1;
        int y1;

        GemExpander(Gem[][] field) {
            this.field = field;
        }

        void expandLeftwards() {
            x0--;
            for (int y = y0; y <= y1; y++)
                queue.add(new int[] { y, x0 });
        }

        void expandRightwards() {
            x1++;
            for (int y = y0; y <= y1; y++)
                queue.add(new int[] { y, x1 });
        }

        void expandDownwards() {
            y0--;
            for (int x = x0; x <= x1; x++)
                queue.add(new int[] { y0, x });
        }

        void expandUpwards() {
            y1++;
            for (int x = x0; x <= x1; x++)
                queue.add(new int[] { y1, x });
        }

        void addGem(Gem g) {
            while (g.x0 < x0)
                expandLeftwards();
            while (x1 < g.x1)
                expandRightwards();
            while (g.y0 < y0)
                expandDownwards();
            while (y1 < g.y1)
                expandUpwards();
        }

        Gem expand(Gem powerGem, char initialDirection) {
            x0 = powerGem.x0;
            y0 = powerGem.y0;
            x1 = powerGem.x1;
            y1 = powerGem.y1;
            switch (initialDirection) {
                case 'L':
                    if (x0 > 0)
                        expandLeftwards();
                    else
                        return null;
                    break;
                case 'R':
                    if (x1 < MAX_X)
                        expandRightwards();
                    else
                        return null;
                    break;
                case 'D':
                    if (y0 > 0)
                        expandDownwards();
                    else
                        return null;
                    break;
                case 'U':
                    if (y1 < MAX_Y)
                        expandUpwards();
                    else
                        return null;
                    break;
            }
            Color c = powerGem.color;
            while (true) {
                int[] cell = queue.poll();
                if (cell == null)
                    break;
                Gem g = field[cell[0]][cell[1]];
                if (g == null || g.color != c) {
                    queue.clear();
                    return null;
                }
                if (g.x0 != g.x1) // Power Gem
                    addGem(g);
            }
            return new Gem(x0, y0, x1, y1, c);
        }
    }

    private static Gem bestOf(Gem previousBest, Gem newExpand) {
        if (previousBest == null)
            return newExpand;
        if (newExpand == null)
            return previousBest;
        int d = previousBest.y1 - newExpand.y1;
        if (d == 0)
            d = (previousBest.x1 - previousBest.x0) - (newExpand.x1 - newExpand.x0);
        if (d == 0)
            d = newExpand.x0 - previousBest.x0;
        return d >= 0 ? previousBest : newExpand;
    }

    private boolean expandPowers(int yStart, int xStart, char... directions) {
        Gem bestExpand = null;
        Gem[] row = field[yStart];
        xStart--;
        while (true) {
            xStart++;
            if (xStart >= MAX_X) {
                yStart--;
                if (yStart == 0)
                    break;
                row = field[yStart];
                xStart = 0;
            }
            Gem g = row[xStart];
            if (g == null || g.special || g.x0 == g.x1)
                continue;
            boolean topLeft = g.y1 == yStart && g.x0 == xStart;
            xStart = g.x1;
            if (topLeft)
                for (char dir : directions)
                    bestExpand = bestOf(bestExpand, expander.expand(g, dir));
        }
        if (bestExpand == null)
            return false;
        bestExpand.putOnField(field);
        return true;
    }

    private void combine() { // make Power Gems
        int yStart = MAX_Y;
        int xStart = 0;
        outer:
        for (yStart = MAX_Y; yStart > 0; yStart--) { // we skip the bottommost row
            Gem[] row = field[yStart];
            for (xStart = 0; xStart < MAX_X; xStart++) // we skip the rightmost column
                if (row[xStart] != null)
                    break outer;
        }
        if (yStart == 0)
            return;
        combineIndividuals(yStart, xStart);
        boolean expanded = true;
        do {
            while (expandPowers(yStart, xStart, 'L', 'R'))
                expanded = true;
            if (!expanded)
                break;
            expanded = false;
        } while (expandPowers(yStart, xStart, 'U', 'D'));
    }

    private void move(Gem[] pair) {
        drop();
        boolean shattered;
        do {
            shattered = shatter();
            combine();
        } while (shattered && drop());
    }

    private String gameState() {
        char[] chars = new char[HEIGHT * (WIDTH + 1) - 1];
        int i = 0;
        for (int y = MAX_Y; y >= 0; y--) {
            for (Gem g : field[y]) {
                char c;
                if (g != null) {
                    c = g.color.letter;
                    if (g.special)
                        c = Character.toLowerCase(c);
                } else
                    c = ' ';
                chars[i++] = c;
            }
            if (y > 0)
                chars[i++] = '\n';
        }
        return new String(chars);
    }

    public static String play(String[][] arrMoves) {
        PuzzleFighter pf = new PuzzleFighter();
        for (String[] s : arrMoves) {
            Gem[] pair = pf.droppedPair(s[0], s[1]);
            if (pair == null) // gem stack overflow
                break;
            pf.move(pair);
        }
        return pf.gameState();
    }
}

#######################################
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

public class PuzzleFighter {
    
    public static String play(String[][] arrMoves) { 
        // Need help with debugging?
        // Uncomment the line below to see the game state for each Gem pair:
        // Preloaded.SEE_STATES = true;
    
        PlayingField playingField = new PlayingField();
        for (String[] instruction : arrMoves) {
            if (!playingField.startMoves(instruction[0], instruction[1])) break;
            playingField.runMove();
            do {
                playingField.combineGems(true);
                playingField.combineGems(false);
                playingField.crashRainbowGems();
                playingField.crashGems();
            } while (playingField.runMove());
        }
        return playingField.getState();
    }
}

class PlayingField {
    private static final int FIELD_WIDTH = 6;
    private static final int FIELD_HEIGHT = 12;
    private static final int EXT_FIELD_HEIGHT = FIELD_HEIGHT + 3;
    private static final int INPUT_COLUMN = 3;
    private final Gem[][] cells = new Gem[EXT_FIELD_HEIGHT][FIELD_WIDTH];
    private final List<Gem> crashGems = new ArrayList<>();
    private final List<Gem> rainbowGems = new ArrayList<>();

    public boolean startMoves(String pairGems, String displacement) {
        Gem gem1 = new Gem(pairGems.charAt(0), INPUT_COLUMN, FIELD_HEIGHT + 1);
        Gem gem2 = new Gem(pairGems.charAt(1), INPUT_COLUMN, FIELD_HEIGHT);

        displacement.chars().forEach(move -> movePair(gem1, gem2, move));

        if (gem1.bottom == gem2.bottom) {
            if (cells[FIELD_HEIGHT - 1][gem1.left] != null || cells[FIELD_HEIGHT - 1][gem2.left] != null) return false;
        } else {
            if (cells[FIELD_HEIGHT - 2][gem1.left] != null) return false;
        }

        Stream.of(gem1, gem2).forEach(gem -> {
            cells[gem.bottom][gem.left] = gem;
            if (gem.type == GemType.CRASH) crashGems.add(gem);
            else if (gem.type == GemType.RAINBOW) rainbowGems.add(gem);
        });

        return true;
    }

    public String getState() {
        StringBuilder builder = new StringBuilder();
        for (int i = FIELD_HEIGHT - 1; i >= 0; i--) {
            for (int j = 0; j < FIELD_WIDTH; j++) {
                builder.append(gemChar(cells[i][j]));
            }
            if (i != 0) builder.append('\n');
        }
        return builder.toString();
    }

    public boolean runMove() {
        boolean wasMoves = false;
        boolean wasMovesInCurrentIteration;
        do {
            wasMovesInCurrentIteration = false;
            for (int i = 0; i < EXT_FIELD_HEIGHT - 1; i++) {
                for (int j = 0; j < FIELD_WIDTH; j++) {
                    if (cells[i][j] != null) continue;
                    Gem gem = cells[i + 1][j];
                    if (gem == null || gem.bottom != i + 1 || gem.left != j) continue;
                    if (!gem.lowerClean()) continue;
                    if (!wasMovesInCurrentIteration) {
                        wasMovesInCurrentIteration = true;
                        if (!wasMoves) wasMoves = true;
                    }
                    gem.moveDown();
                }
            }
        } while (wasMovesInCurrentIteration);
        return wasMoves;
    }

    public void crashRainbowGems() {
        if (rainbowGems.isEmpty()) return;
        Gem rainbowOne = rainbowGems.get(0);
        GemColor color1 = rainbowOne.lowerColor();

        if (rainbowGems.size() > 1) {
            Gem rainbowTwo = rainbowGems.get(1);
            GemColor color2 = rainbowTwo.lowerColor();
            deleteColor(color2);
            rainbowTwo.removeFromField();
        }

        deleteColor(color1);
        rainbowOne.removeFromField();
        rainbowGems.clear();
    }

    private void deleteColor(GemColor extractingColor) {
        for (int i = 0; i < FIELD_HEIGHT; i++) {
            for (int j = 0; j < FIELD_WIDTH; j++) {
                Gem gem = cells[i][j];
                if (gem != null && gem.color == extractingColor) {
                    gem.removeFromField();
                }
            }
        }
    }

    public void crashGems() {
        if (crashGems.isEmpty()) return;
        int i = 0;
        while (i < crashGems.size()) {
            Gem crashGem = crashGems.get(i++);
            List<Gem> sameAround = crashGem.gemsSameAround();
            if (sameAround.size() == 0) continue;
            i--;
            sameAround.add(0, crashGem);
            for (int j = 0; j < sameAround.size(); j++) {
                for (Gem gem : sameAround.get(j).gemsSameAround()) {
                    if (!sameAround.contains(gem)) sameAround.add(gem);
                }
            }
            sameAround.forEach(Gem::removeFromField);
        }
    }

    public void combineGems(boolean onlyOrdinal) {
        for (int i = FIELD_HEIGHT - 1; i > 0; i--) {
            for (int j = 0; j < FIELD_WIDTH - 1; j++) {
                Gem gem = cells[i][j];
                if (gem == null) continue;

                if (onlyOrdinal) {
                    if (gem.type != GemType.ORDINAL) continue;
                } else {
                    if (gem.type != GemType.ORDINAL && gem.type != GemType.POWER) continue;
                }

                int gemTop = gem.bottom + gem.gemHeight - 1;

                if (i != gemTop || j != gem.left) continue;

                int rightRect = gem.left + Math.max(gem.gemWidth - 1, 1);
                int bottomRect = Math.min(gem.bottom, gemTop - 1);

                ResultOfTest resultOfTest = testRect(i, j, bottomRect, rightRect, onlyOrdinal);
                if (resultOfTest == ResultOfTest.BAD) continue;
                boolean minimalSizeTook = resultOfTest == ResultOfTest.GOOD;

                for (int probeRight = rightRect + 1; probeRight < FIELD_WIDTH; probeRight++) {
                    resultOfTest = testRect(i, j, bottomRect, probeRight, onlyOrdinal);
                    if (resultOfTest == ResultOfTest.GOOD) rightRect = probeRight;
                    else if (resultOfTest == ResultOfTest.BAD) break;
                }

                for (int probeBottom = bottomRect - 1; probeBottom >= 0; probeBottom--) {
                    resultOfTest = testRect(i, j, probeBottom, rightRect, onlyOrdinal);
                    if (resultOfTest == ResultOfTest.GOOD) bottomRect = probeBottom;
                    else if (resultOfTest == ResultOfTest.BAD) break;
                }

                combineRect(gemTop, gem.left, bottomRect, rightRect, minimalSizeTook);
            }
        }
    }

    private void combineRect(int topRect, int leftRect, int bottomRect, int rightRect, boolean minimalSizeTook) {
        Gem gem = cells[topRect][leftRect];

        int gemWidth = rightRect - leftRect + 1;
        int gemHeight = topRect - bottomRect + 1;

        if (!minimalSizeTook && gemWidth == 2 && gemHeight == 2) return;
        if (gem.bottom <= bottomRect && gem.left + gem.gemWidth - 1 >= rightRect) return;

        gem.type = GemType.POWER;
        gem.gemWidth = gemWidth;
        gem.bottom = bottomRect;
        gem.gemHeight = gemHeight;

        for (int i = bottomRect; i <= topRect; i++) {
            for (int j = leftRect; j <= rightRect; j++) {
                cells[i][j] = gem;
            }
        }
    }

    private ResultOfTest testRect(int topRect, int leftRect, int bottomRect, int rightRect, boolean onlyOrdinal) {
        ResultOfTest resultOfTest = ResultOfTest.GOOD;
        GemColor color = cells[topRect][leftRect].color;
        for (int i = bottomRect; i <= topRect; i++) {
            Gem testGem = cells[i][rightRect];
            if (testGem == null || testGem.color != color) return ResultOfTest.BAD;
            if (onlyOrdinal) {
                if (testGem.type != GemType.ORDINAL) return ResultOfTest.BAD;
            } else {
                if (testGem.type != GemType.ORDINAL && testGem.type != GemType.POWER) return ResultOfTest.BAD;
            }
            if (testGem.left < leftRect || testGem.bottom + testGem.gemHeight - 1 > topRect) return ResultOfTest.BAD;
            if (testGem.bottom < bottomRect || testGem.left + testGem.gemWidth - 1 > rightRect) {
                resultOfTest = ResultOfTest.MAYBE;
            }
        }
        for (int j = leftRect; j <= rightRect; j++) {
            Gem testGem = cells[bottomRect][j];
            if (testGem == null || testGem.color != color) return ResultOfTest.BAD;
            if (onlyOrdinal) {
                if (testGem.type != GemType.ORDINAL) return ResultOfTest.BAD;
            } else {
                if (testGem.type != GemType.ORDINAL && testGem.type != GemType.POWER) return ResultOfTest.BAD;
            }
            if (testGem.left < leftRect || testGem.bottom + testGem.gemHeight - 1 > topRect) return ResultOfTest.BAD;
            if (testGem.bottom < bottomRect || testGem.left + testGem.gemWidth - 1 > rightRect) {
                resultOfTest = ResultOfTest.MAYBE;
            }
        }
        return resultOfTest;
    }

    private void movePair(Gem gem1, Gem gem2, int move) {
        switch (move) {
            case 'L':
                gem1.left--;
                gem2.left--;
                break;
            case 'R':
                gem1.left++;
                gem2.left++;
                break;
            case 'A':
                if (gem2.left < gem1.left) {
                    gem2.left++;
                    gem2.bottom--;
                } else if (gem2.left > gem1.left) {
                    gem2.left--;
                    gem2.bottom++;
                } else if (gem2.bottom < gem1.bottom) {
                    gem2.left++;
                    gem2.bottom++;
                } else if (gem2.bottom > gem1.bottom) {
                    gem2.left--;
                    gem2.bottom--;
                }
                break;
            case 'B':
                if (gem2.left < gem1.left) {
                    gem2.left++;
                    gem2.bottom++;
                } else if (gem2.left > gem1.left) {
                    gem2.left--;
                    gem2.bottom--;
                } else if (gem2.bottom < gem1.bottom) {
                    gem2.left--;
                    gem2.bottom++;
                } else if (gem2.bottom > gem1.bottom) {
                    gem2.left++;
                    gem2.bottom--;
                }
                break;
        }

        int offset;

        if (0 > (offset = Math.min(gem1.left, gem2.left))) {
            gem1.left -= offset;
            gem2.left -= offset;
        }

        if (0 > (offset = FIELD_WIDTH - 1 - Math.max(gem1.left, gem2.left))) {
            gem1.left += offset;
            gem2.left += offset;
        }
    }

    private char gemChar(Gem gem) {
        if (gem == null) return ' ';
        if (gem.type == GemType.RAINBOW) return '0';
        if (gem.type == GemType.CRASH) return gem.color.toLoChar();
        return gem.color.toUpChar();
    }

    enum GemType {
        ORDINAL,
        POWER,
        CRASH,
        RAINBOW;

        public static GemType ofChar(char letter) {
            switch (letter) {
                case 'r':
                case 'b':
                case 'g':
                case 'y':
                    return CRASH;
                case '0':
                    return RAINBOW;
            }
            return ORDINAL;
        }
    }

    enum GemColor {
        RED,
        BLUE,
        GREEN,
        YELLOW;

        public static GemColor ofChar(char letter) {
            switch (letter) {
                case 'R':
                case 'r':
                    return RED;
                case 'B':
                case 'b':
                    return BLUE;
                case 'G':
                case 'g':
                    return GREEN;
                case 'Y':
                case 'y':
                    return YELLOW;
            }
            return null;
        }

        public char toUpChar() {
            switch (this) {
                case RED:
                    return 'R';
                case BLUE:
                    return 'B';
                case GREEN:
                    return 'G';
                case YELLOW:
                    return 'Y';
            }
            return ' ';
        }

        public char toLoChar() {
            switch (this) {
                case RED:
                    return 'r';
                case BLUE:
                    return 'b';
                case GREEN:
                    return 'g';
                case YELLOW:
                    return 'y';
            }
            return ' ';
        }

    }

    enum ResultOfTest {
        GOOD,
        BAD,
        MAYBE
    }

    class Gem {
        int left;
        int bottom;
        GemColor color;
        GemType type;
        int gemWidth = 1;
        int gemHeight = 1;

        public Gem(char letter, int left, int bottom) {
            this.left = left;
            this.bottom = bottom;
            this.color = GemColor.ofChar(letter);
            this.type = GemType.ofChar(letter);
        }

        public boolean lowerClean() {
            if (bottom == 0) return false;
            for (int i = 0; i < gemWidth; i++) {
                if (cells[bottom - 1][left + i] != null) return false;
            }
            return true;
        }

        public GemColor lowerColor() {
            if (bottom == 0) return null;
            for (int i = 0; i < gemWidth; i++) {
                Gem lowerGem = cells[bottom - 1][left + i];
                if (lowerGem != null) return lowerGem.color;
            }
            return null;
        }

        public void moveDown() {
            for (int i = 0; i < gemWidth; i++) {
                cells[bottom + gemHeight - 1][left + i] = null;
                cells[bottom - 1][left + i] = this;
            }
            this.bottom--;
        }

        public void removeFromField() {
            for (int i = bottom; i < bottom + gemHeight; i++) {
                for (int j = left; j < left + gemWidth; j++) {
                    cells[i][j] = null;
                }
            }
            if (type == GemType.CRASH) crashGems.remove(this);
            if (type == GemType.RAINBOW) rainbowGems.remove(this);
        }

        public List<Gem> gemsSameAround() {
            List<Gem> around = new ArrayList<>();
            if (bottom > 0) {
                for (int i = left; i < left + gemWidth; i++) {
                    Gem gem = cells[bottom - 1][i];
                    if (gem != null && gem.color == color) around.add(gem);
                }
            }
            if (left > 0) {
                for (int i = bottom; i < bottom + gemHeight; i++) {
                    Gem gem = cells[i][left - 1];
                    if (gem != null && gem.color == color) around.add(gem);
                }
            }
            if (bottom + gemHeight < FIELD_HEIGHT) {
                for (int i = left; i < left + gemWidth; i++) {
                    Gem gem = cells[bottom + gemHeight][i];
                    if (gem != null && gem.color == color) around.add(gem);
                }
            }
            if (left + gemWidth < FIELD_WIDTH) {
                for (int i = bottom; i < bottom + gemHeight; i++) {
                    Gem gem = cells[i][left + gemWidth];
                    if (gem != null && gem.color == color) around.add(gem);
                }
            }
            return around;
        }//gnomed
        @Override
        public String toString() {
            return String.valueOf(gemChar(this));
        }
    }
}
