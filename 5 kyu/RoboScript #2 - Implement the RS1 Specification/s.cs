5870fa11aa0428da750000da


using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public class RoboScript
{
  private static readonly IDictionary<char, Action<Robot>> commands = new Dictionary<char, Action<Robot>>
  {
    { 'F', robot => robot.MoveForward() },
    { 'L', robot => robot.TurnLeft() },
    { 'R', robot => robot.TurnRight() }
  };

  public static string Execute(string code)
  {
    // make the shorthands explicit
    foreach (var command in commands.Keys)
    {
      code = Regex.Replace(code, $"{command}(?<repeats>\\d+)", match => new String(command, int.Parse(match.Groups["repeats"].Value)));
    }

    var robot = new Robot();

    foreach (var command in code)
    {
      commands[command](robot);
    }

    return robot.Plot();
  }

  private class Robot
  {
    private static readonly (int X, int Y)[] directions = new (int X, int Y)[]
    {
      (1, 0), (0, -1), (-1, 0), (0, 1) // right, down, left, up
    };

    private readonly ISet<(int X, int Y)> tape = new HashSet<(int X, int Y)>();

    private (int X, int Y) position = (0, 0);
    private int direction = 0;

    public Robot()
    {
      tape.Add(position);
    }

    public void MoveForward()
    {
      position = (position.X + directions[direction].X, position.Y + directions[direction].Y);
      tape.Add(position);
    }

    public void TurnLeft()
    {
      direction = (direction + 3) % 4; // 1 left turn is equivalent to 3 right turns 
    }

    public void TurnRight()
    {
      direction = (direction + 1) % 4;
    }

    public string Plot()
    {
      var xRange = tape.Aggregate((Min: 0, Max: 0), (range, record) => (Math.Min(record.X, range.Min), Math.Max(record.X, range.Max)));
      int lowestX = xRange.Min;
      int lineLength = xRange.Max - lowestX + 1;
      
      var lines = 
        tape
           .GroupBy(record => record.Y)
           .OrderByDescending(row => row.Key)
           .Select(row => row.Select(record => record.X - lowestX))
           .Select(indeces => PlotIndeces(indeces));

      return string.Join("\r\n", lines);
      
      string PlotIndeces(IEnumerable<int> indeces)
      {
        var chars = new char[lineLength];
        foreach (var index in indeces)
        {
          chars[index] = '*';
        }
        return string.Concat(chars.Select(c => c == default(char) ? ' ' : c));
      }
    }
  }
}
__________________________
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

public class RoboScript
{
  private class Point
  {
    public int X {get; private set;}
    public int Y {get; private set;}
    public Point(int x, int y)
    {
      X = x;
      Y = y;
    }
  }
  
  public static string Execute(string code)
  {
    // Implement your RS1 interpreter here
    string cleaned = ConvertString(code);
    List<Point> routes = new List<Point>();
    int maxX = 0, minX = 0, maxY = 0, minY = 0;
    int direction = 0;
    routes.Add(new Point(0,0));
    foreach (char order in cleaned)
    {
      Point pNew = GetNextPoint(routes.Last(), order, ref direction);
      if(pNew!=null)
      {
        routes.Add(pNew);
        maxX = Math.Max(maxX, pNew.X);
        minX = Math.Min(minX, pNew.X);
        maxY = Math.Max(maxY, pNew.Y);
        minY = Math.Min(minY, pNew.Y);
      }
    }
    
    List<StringBuilder> map = GetMap(maxX-minX+1, maxY-minY+1);
    foreach(Point p in routes)
    {
      map[p.X-minX][p.Y-minY] = '*';
    }
      
    return string.Join("\r\n", map);
  }
  
  private static string ConvertString(string input)
  {
      return Regex.Replace(input, @"[FLR]\d+", o=>new string(o.Value[0], int.Parse(o.Value.Substring(1))));
  }
  
  private static Point GetNextPoint(Point last, char order, ref int direciton)
  {
    if(last == null)
    {
      return new Point(0,0);
    }
    
    if (order=='F')
    {
      if (direciton==0)
      {
        return new Point(last.X, last.Y+1);
      }
      else if (direciton==1)
      {
        return new Point(last.X-1, last.Y);
      }
      else if (direciton==2)
      {
        return new Point(last.X, last.Y-1);
      }
      else if (direciton==3)
      {
        return new Point(last.X+1, last.Y);
      }
    }
    else if (order=='L')
    {
      direciton = ((direciton+1)%4+4)%4;
    }
    else if (order=='R')
    {
      direciton = ((direciton-1)%4+4)%4;
    }
    return null;
  }
  
  private static List<StringBuilder> GetMap(int x, int y)
  {
    return Enumerable.Range(0,x).Select(i=>new StringBuilder(new String(' ', y))).ToList();
  }
}
__________________________
using System;
using System.Text;
using System.Numerics;
using System.Collections.Generic;

public class RoboScript {
    public static string validCmds = "LRF";
    public static int dim = 2000, offset = dim / 2;
    
    public static int xPos = 0, yPos = 0, dir = 0;
    public static int xMin = 0, yMin = 0, xMax = 0, yMax = 0; 
    public static bool [,] floor = new bool[1,1];

    public static string Execute(string code) {
        xPos = 0; yPos = 0; dir = 0;
        xMin = 0; yMin = 0; xMax = 0; yMax = 0; 
        floor = new bool[dim, dim]; floor[offset, offset] = true;

        Navigator(code);
        return FloorToString();
    }

    public static string FloorToString() {
        StringBuilder res = new StringBuilder();

        for (int y = yMax; y >= yMin; y--) {
            for (int x = xMin; x <= xMax; x++) 
                res.Append(floor[x + offset, y + offset] ? '*' : ' ');
            res.Append("\r\n");
        }
        return res.Remove(res.Length - 2, 2).ToString();
    }

    public static void Navigator(string path) {
        var steps = Parse(path);

        for (int i = 0; i < steps.Count; i++) {
            string cmd = steps[i];

            if (validCmds.Contains(cmd)) {
                int itr = 1;

                if (i + 1 < steps.Count && !validCmds.Contains(steps[i + 1]))
                    itr = Convert.ToInt32(steps[++i]);

                Action(cmd, itr);
            }
        }
    }

    public static void Action(string cmd, int itr) {
        switch (cmd) {
            case "R":
                dir += (4 - itr); dir %= 4;
                break;

            case "L":
                dir += itr; dir %= 4;
                break;
                
            case "F":
                switch (dir) {
                    case 0:
                        for (int x = xPos + 1; x <= xPos + itr; x++)
                            floor[x + offset, yPos + offset] = true;
                        xPos += itr;
                        break;

                    case 1:
                        for (int y = yPos + 1; y <= yPos + itr; y++)
                            floor[xPos + offset, y + offset] = true;
                        yPos += itr;
                        break;

                    case 2:
                        for (int x = xPos - 1; x >= xPos - itr; x--)
                            floor[x + offset, yPos + offset] = true;
                        xPos -= itr;
                        break;

                    case 3:
                        for (int y = yPos - 1; y >= yPos - itr; y--)
                            floor[xPos + offset, y + offset] = true;
                        yPos -= itr;
                        break;
                }
                xMin = Math.Min(xMin, xPos); xMax = Math.Max(xMax, xPos);
                yMin = Math.Min(yMin, yPos); yMax = Math.Max(yMax, yPos);
                break;
        }
    }

    public static List<string> Parse(string path) {
        var steps = new List<string>();

        for (int ix = 0; ix < path.Length; ix++) {
            if (validCmds.Contains(path[ix])) {
                steps.Add(path[ix].ToString());
            } else if (Char.IsDigit(path[ix])) {
                string num = "" + path[ix];

                while (ix + 1 < path.Length && Char.IsDigit(path[ix + 1])) {
                    num += path[++ix];
                }
                steps.Add(num);
            }
        }
        return steps;
    }
}
