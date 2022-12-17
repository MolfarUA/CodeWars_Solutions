564e1d90c41a8423230000bc

using System;
using System.Linq;

public class KnightKing
{
  public static string KnightVsKing(object[] np, object[] kp)
  {
    int ny = (int)np[0], ky = (int)kp[0];
    int nx = (int) ((string)np[1])[0], kx = (int) ((string)kp[1])[0];
    
    if (Math.Abs(nx - kx) <= 1 && Math.Abs(ny - ky) <= 1) {
      return "King";
    }
    
    if (Math.Abs(nx - kx) == 2 && Math.Abs(ny - ky) == 1 ||
        Math.Abs(nx - kx) == 1 && Math.Abs(ny - ky) == 2) {
      return "Knight";
    }
    
    return "None";
  }
}
_______________________________________
public class KnightKing
{
  public static string KnightVsKing(object[] knightPosition, object[] kingPosition)
  {
    var x = (int) knightPosition[0] - (int) kingPosition[0];
    var y = ((string) knightPosition[1])[0] - ((string) kingPosition[1])[0];
    var d = x * x + y * y;
    return d < 3 ? "King" : d == 5 ? "Knight" : "None";
  }
}
_______________________________________
using System;
using System.Linq;

public class KnightKing
{
  public static string KnightVsKing(object[] knightPosition, object[] kingPosition)
  {
    var distance = new Position(knightPosition) - new Position(kingPosition);
    var knightMoves = new Position[8]{new Position(2,-1), new Position(2, 1), new Position(1, -2), new Position(1, 2), new Position(-2, -1), new Position(-2, 1), new Position(-1, -2), new Position(-1, 2) };
    var kingMoves = new Position[8]{new Position(1,-1), new Position(1, 0), new Position(1, 1), new Position(0, -1), new Position(0, 1), new Position(-1, -1), new Position(-1, 0), new Position(-1, 1) };
    if (knightMoves.Any(move => move.Equals(distance))) return "Knight";
    else if (kingMoves.Any(move => move.Equals(distance))) return "King";
    else return "None";
  }
}

public class Position : IEquatable<Position>
{
  public int Y { get; private set; }
  public int X { get; private set; }
  public static Position operator - (Position a, Position b)
  {
    return new Position(a.Y - b.Y, a.X - b.X);
  }
  public bool Equals(Position other) => (Y == other.Y && X == other.X);
  public Position(int y, int x) { X = x; Y = y; }
  public Position(object[] position)
  {
    Y = (int)position[0];
    X = (((string)position[1])[0] - 64);
  }
}
