58738d518ec3b4bf95000192


using System;
using System.Collections.Generic;
using System.Text;

public class RoboScript
{
  enum Direction { Right, Up, Left, Down }
  public static string Execute(string code)
  {
    code = Expand(code);
    var commands = new List<(int dX, int dY)>();
    int startX = 0, startY = 0, x = 0, y = 0, width = 1, height = 1; // 1 X 1

    foreach(var (dX, dY) in Interpret(code))
    {
      commands.Add((dX, dY));
      if(dY == 0) // Move horizontally.
      {
        if(dX > 0) // Right.
        {
          var repeat = x + dX + 1 - width;
          if(repeat > 0) // Add columns to the right.
          {
            width += repeat;
          }
        }
        else // Left.
        {
          var repeat = -dX - x;
          if(repeat > 0) // Add columns to the left.
          {
            width += repeat;
            x += repeat;
            startX += repeat;
          }
        }
        x += dX;
      }
      else if(dY > 0) // Down.
      {
        var repeat = y + dY + 1 - height;
        if(repeat > 0) // Add rows after current row.
        {
          height += repeat;
        }
        y += dY;
      }
      else // Up.
      {
        var repeat = -dY - y;
        if(repeat > 0) // Add rows before current row.
        {
          height += repeat;
          y += repeat;
          startY += repeat;
        }
        y += dY;
      }
    }
    // 2nd Pass.
    return String.Create((width * height) + (2 * (height - 1)), // 2X for '\n\r'.
      (commands, startX, startY, width), (builder, state) =>
    {
      var width = state.width;
      for(var index = 0; index < builder.Length;)
      {
        for(var column = 0; column < width; column++, index++)
        {
          builder[index] = ' ';
        }
        if(index < builder.Length)
        {
          builder[index++] = '\r';
          builder[index++] = '\n';
        }
      }
      width += 2;
      var x = state.startX;
      var y = state.startY;
      builder[(y * width) + x] = '*';

      for(var index = 0; index < state.commands.Count; index++)
      {
        var (dX, dY) = commands[index];
        if(dY == 0) // Move horizontally.
        {
          if(dX > 0) // Right.
          {
            for(var i = 0; i < dX; i++) { x++; builder[(y * width) + x] = '*'; }
          }
          else // Left.
          {
            for(var i = 0; i < -dX; i++) { x--; builder[(y * width) + x] = '*'; }
          }
        }
        else if(dY > 0) // Down.
        {
          for(var i = 0; i < dY; i++) { y++; builder[(y * width) + x] = '*'; }
        }
        else // Up.
        {
          for(var i = 0; i < -dY; i++) { y--; builder[(y * width) + x] = '*'; }
        }
      }
    });

    static IEnumerable<(int dX, int dY)> Interpret(string code)
    {
      var direction = Direction.Right;
      for(var index = 0; index < code.Length;)
      {
        if(TryReadCount(code, 'F', ref index, out var count))
        {
          switch(direction)
          {
            case Direction.Right: yield return (count, 0); break;
            case Direction.Left: yield return (-count, 0); break;
            case Direction.Up: yield return (0, -count); break;
            case Direction.Down: yield return (0, count); break;
          }
        }
        if(TryReadCount(code, 'L', ref index, out count))
        {
          direction = (Direction)(((int)direction + count) % 4);
        }
        if(TryReadCount(code, 'R', ref index, out count))
        {
          var dir = ((int)direction - count) % 4;
          if(dir < 0) { dir += 4; }
          direction = (Direction)dir;
        }
      }
    }
    static bool TryReadCount(string input, char command, ref int index, out int count)
    {
      count = 0;
      var start = index;
      while(index < input.Length && command == input[index]) { index++; }
      if(start != index)
      {
        count = index - start; // Caters for FFFF, now for F5.
        start = index;
        while(index < input.Length && Char.IsNumber(input[index])) { index++; }
        if(Int32.TryParse(input.AsSpan()[start..index], out var @int)) { count += @int - 1; }
        return count > 0; // Ignore 0 counts!
      }
      return false;
    }

    static string Expand(string code)
    {
      var builder = new StringBuilder();
      do
      {
        var end = -1;
        while(++end < code.Length) { if(code[end] == ')') { break; } }
        if(end == code.Length) { return code; }
        var start = end;
        while(--start >= 0) { if(code[start] == '(') { break; } }
        var index = -1;
        while(++index < start) { builder.Append(code[index]); }
        index = end + 1;
        while(index < code.Length && Char.IsNumber(code[index])) { index++; }
        var count = 1;
        if(index != end + 1 && !Int32.TryParse(code.AsSpan()[(end + 1)..index], out count)) { count = 1; }
        builder.Append(new StringBuilder().Insert(0, code.AsSpan()[(start + 1)..end].ToString(), count));
        while(index < code.Length) { builder.Append(code[index++]); }
        code = builder.ToString();
        builder.Clear();
      }
      while(true);
    }
  }  
}
__________________________
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

public class RoboScript
{
  private static readonly IDictionary<char, Action<Robot>> commands = new Dictionary<char, Action<Robot>>
  {
    ['F'] = robot => robot.MoveForward(),
    ['L'] = robot => robot.TurnLeft(),
    ['R'] = robot => robot.TurnRight()
  };
  
  public static string Execute(string code)
  {
    // make the groupings explicit
    while (groupings.IsMatch(code)) code = groupings.Replace(code, expander);
  
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
  
  private static readonly Regex  groupings = new Regex(@"\((?<commands>[^()]+)\)(?<repeats>\d*)"); // matches the innermost groups only
  
  private static readonly MatchEvaluator expander = match => String.Concat(Enumerable.Repeat(match.Groups["commands"].Value, int.TryParse(match.Groups["repeats"].Value, out int repeats) ? repeats : 1));

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
using System.Text.RegularExpressions;
public class RoboScript
{
    public static string Execute(string code)
    {
        Console.WriteLine(code);
        char direction = 'R';
        var position = (0, 0);
        var trace =
            Regex.Replace
            (
                new List<string>() { 'S' + code }
                .Select(z =>
                {
                    Regex regex = new Regex(@"(\(\w+\)|[A-Z])(\d+)");
                    while (regex.IsMatch(z))
                    {
                        z = regex.Replace
                        (
                            z,
                            x =>
                            {
                                string trimmed = Regex.Replace(x.Groups[1].Value, @"[\(\)]", "");
                                return string.Concat(Enumerable.Range(0, int.Parse(x.Groups[2].Value)).Select(_ => trimmed));
                            }
                        );
                    };
                    return z;
                })
                .First(),
                @"[\(\)]",
                ""
            )
            .Select(x =>
            {
                switch (x)
                {
                    case 'F': return direction;
                    case 'S': return x;
                    default:
                        direction =
                            new Dictionary<(char, char), char>
                            {
                                [('R', 'L')] = 'U',
                                [('R', 'R')] = 'D',
                                [('L', 'L')] = 'D',
                                [('L', 'R')] = 'U',
                                [('U', 'L')] = 'L',
                                [('U', 'R')] = 'R',
                                [('D', 'L')] = 'R',
                                [('D', 'R')] = 'L',

                            }
                            [(direction, x)];
                    return 'Z';
                }
            })
            .Where(x => x != 'Z')
            .Select(x =>
            {
                (int dx, int dy) =
                    new Dictionary<char, (int, int)>
                    {
                        ['S'] = (0, 0),
                        ['U'] = (0, 1),
                        ['D'] = (0, -1),
                        ['L'] = (-1, 0),
                        ['R'] = (1, 0),
                    }
                    [x];
                position = (position.Item1 + dx, position.Item2 + dy);
                return position;
            })
            .ToList();
        (int xmin, int xmax, int ymin, int ymax) =
            trace.Aggregate
            (
                (0, 0, 0, 0),
                ((int xmin, int xmax, int ymin, int ymax) edge, (int x, int y) u) =>
                    (
                        Math.Min(edge.xmin, u.x),
                        Math.Max(edge.xmax, u.x),
                        Math.Min(edge.ymin, u.y),
                        Math.Max(edge.ymax, u.y)
                    )
            );
        return
            string.Join
            (
                "\r\n",
                trace
                .GroupBy(u => u.Item2)
                .OrderByDescending(u => u.Key)
                .Select(u => string.Concat(Enumerable.Range(0, xmax - xmin + 1).Select(i => u.Contains((i + xmin, u.Key)) ? "*" : " ")))
            );
    }
}
