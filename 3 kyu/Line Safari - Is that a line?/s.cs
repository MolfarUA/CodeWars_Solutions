59c5d0b0a25c8c99ca000237


using System;
using System.Collections.Generic;

public class Dinglemouse
{
    public static bool Line(char[][] grid)
    {
      for (int x = 0; x < grid[0].Length; x++) {
        for (int y = 0; y < grid.Length; y++) {
          if (grid[y][x] == 'X') {
            char[][] visited = Array.ConvertAll(grid, x => (char[])x.Clone());
            Queue<int[]> q = new Queue<int[]>();
            
            var p = new int[] {x,y,-1,-1};
            q.Enqueue(p);
            
            while(q.Count > 0) {
              var c = q.Dequeue();
              var dx = c[0];
              var dy = c[1];
              var px = c[2];
              var py = c[3];
              
              var v = visited[dy][dx];
              
              // found the end
              if (v == 'X' && (x != dx || y != dy)) {
                for (int tx = 0; tx < grid[0].Length; tx++) {
                  for (int ty = 0; ty < grid.Length; ty++) {
                    if (visited[ty][tx] != 'V' && visited[ty][tx] != ' ' && visited[ty][tx] != 'X') {
                      return false;
                    }
                  }
                }
                return true;
              }
              
              int qcount = 0;
              
              // enqueue top
              if ((v == 'X' || v == '|' || (v == '+' && dy == py)) && dy > 0 && (visited[dy-1][dx] == '|' || visited[dy-1][dx] == '+' || visited[dy-1][dx] == 'X')) {
                q.Enqueue(new int[] {dx,dy-1,dx,dy});
                qcount++;
              }
              // enqueue bottom
              if ((v == 'X' || v == '|' || (v == '+' && dy == py)) && dy < visited.Length-1 && (visited[dy+1][dx] == '|' || visited[dy+1][dx] == '+' || visited[dy+1][dx] == 'X')) {
                q.Enqueue(new int[] {dx,dy+1,dx,dy});
                qcount++;
              }

              // enqueue left
              if ((v == 'X' || v == '-' || (v == '+' && dx == px)) && dx > 0 && (visited[dy][dx-1] == '-' || visited[dy][dx-1] == '+' || visited[dy][dx-1] == 'X')) {
                q.Enqueue(new int[] {dx-1,dy,dx,dy});
                qcount++;
              }
              // enqueue right
              if ((v == 'X' || v == '-' || (v == '+' && dx == px)) && dx < visited[0].Length-1 && (visited[dy][dx+1] == '-' || visited[dy][dx+1] == '+' || visited[dy][dx+1] == 'X')) {
                q.Enqueue(new int[] {dx+1,dy,dx,dy});
                qcount++;
              }
              
              if (v == 'X' && qcount > 1) {
                return false;
              }
              
              visited[dy][dx] = 'V';
            }
          }
        }
      }
      
      return false;
    }
}
_______________________________________
using System;
using System.Collections.Generic;
using System.Linq;
public class Dinglemouse
{
      public static bool Line(char[][] grid)

        {
            int[] pos = new int[] {0,0};
            char[] dir = new char[] {' '};

            var fullline = FullLine(grid);

            List<string> history = new List<string>();

            Start(grid,pos);
            history.Add($"{pos[0]}{pos[1]}");
            InitialMove(grid,pos,dir);
            history.Add($"{pos[0]}{pos[1]}");


            if(dir[0] == 'L') return false;        
            if(grid[pos[0]][pos[1]] == ' ') return false;
            if(grid[pos[0]][pos[1]] == 'X' && (Enumerable.SequenceEqual(history.OrderBy(x => x), fullline.OrderBy(x => x)))) return true;   

                       
            while(true)

            {     

                     
                
                try
                {
                     Move(grid,pos,dir,history);

                     grid[pos[0]][pos[1]] = grid[pos[0]][pos[1]];
                     
                     if(!history.Contains($"{pos[0]}{pos[1]}"))

                     {
                        history.Add($"{pos[0]}{pos[1]}");
                     }

                     else
                     {
                         Console.WriteLine($"I already was at position {pos[0]}:{pos[1]}");
                         return false;
                     }
                     
                }   

                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                    return false;   
                } 

               if(dir[0] == 'L') return false;        
               if(grid[pos[0]][pos[1]] == ' ') return false;
               if(grid[pos[0]][pos[1]] == 'X' && (Enumerable.SequenceEqual(history.OrderBy(x => x), fullline.OrderBy(x => x)))) return true;   

                
               
            }
                       
        }

        public static void Move(char[][] grid, int[] pos, char[] dir, List<string> history)

        {       

            if(grid[pos[0]][pos[1]] == '-')

            {
                if(!history.Contains($"{pos[0]}{pos[1] + 1}"))

                {                    
                    pos[1]++;
                    dir[0] = 'E';
                    Console.WriteLine($"going east to position {pos[0]}:{pos[1]}");               
                                           
                }

                else if(!history.Contains($"{pos[0]}{pos[1] - 1}"))

                {
                    pos[1]--;
                    dir[0] = 'W';
                    Console.WriteLine($"going west to position {pos[0]}:{pos[1]}");
                }

                else

                {
                    dir[0] = 'L';
                }

            }

           else if(grid[pos[0]][pos[1]] == '|')

            {
                if(!history.Contains($"{pos[0] + 1}{pos[1]}"))

                {
                    pos[0]++;
                    dir[0] = 'S';
                    Console.WriteLine($"going south to position {pos[0]}:{pos[1]}");
                }

                else if(!history.Contains($"{pos[0] - 1}{pos[1]}"))

                {
                    pos[0]--;
                    dir[0] = 'N';
                    Console.WriteLine($"going north to position {pos[0]}:{pos[1]}");
                }

                else

                {
                    dir[0] = 'L';
                }
            }

           else if(grid[pos[0]][pos[1]] == '+')

            {
                if(dir[0] == 'E' || dir[0] == 'W')

                {
                    if((pos[0] < grid.Length - 1 && !history.Contains($"{pos[0] + 1}{pos[1]}"))
                     &&  (grid[pos[0] + 1][pos[1]] == '|' || grid[pos[0] + 1][pos[1]] == '+' || grid[pos[0] + 1][pos[1]] == 'X' )) 

                    {
                        pos[0]++;
                        dir[0] = 'S';
                        Console.WriteLine($"at cross going south to position {pos[0]}:{pos[1]}");
                    }  

                   else if((pos[0] > 0 && !history.Contains($"{pos[0] - 1}{pos[1]}")) 
                   && (grid[pos[0] - 1][pos[1]] == '|' || grid[pos[0] - 1][pos[1]] == '+' || grid[pos[0] - 1][pos[1]] == 'X'))  

                   {
                        pos[0]--;
                        dir[0] = 'N';
                        Console.WriteLine($"at cross going north to position {pos[0]}:{pos[1]}");
                   }                
                    
                }

                else if(dir[0] == 'N' || dir[0] == 'S')

                {
                  if((pos[1] > 0 && !history.Contains($"{pos[0]}{pos[1] - 1}"))
                    && (grid[pos[0]][pos[1] - 1] == '-' || grid[pos[0]][pos[1] - 1] == '+' || grid[pos[0]][pos[1] - 1] == 'X'))  

                   {
                        pos[1]--;
                        dir[0] = 'W';
                        Console.WriteLine($"at cross going west to position {pos[0]}:{pos[1]}");                      
                   }             
                                                           
                    else if((pos[1] < grid[0].Length - 1 && !history.Contains($"{pos[0]}{pos[1] + 1}"))
                     && (grid[pos[0]][pos[1] + 1] == '-' || grid[pos[0]][pos[1] + 1] == '+' || grid[pos[0]][pos[1] + 1] == 'X')) 

                    {
                        pos[1]++;
                        dir[0] = 'E';
                        Console.WriteLine($"at cross going east to position {pos[0]}:{pos[1]}");
                    }  

                      
                    
                }

                else

                {
                    dir[0] = 'L';
                }

            }                  
        }

        
        public static void Start(char[][] grid, int[] pos)

        {
            for(int i = 0; i < grid.Length; i++)

            {
                for(int j = 0; j < grid[0].Length; j++)

                {
                    if(grid[i][j] == 'X')

                    {
                        pos[0] = i;
                        pos[1] = j;
                    }                   

                }
            }        

            Console.WriteLine($"Set starting position as {pos[0]}:{pos[1]}");
        }

        public static void InitialMove(char[][] grid, int[] pos, char[] dir)
        {

            

            if (pos[0] - 1 >= 0 &&
             (grid[pos[0] - 1][pos[1]] == '|' || grid[pos[0] - 1][pos[1]] == '+' || grid[pos[0] - 1][pos[1]] == 'X'))
            {
                pos[0]--;
                Console.WriteLine("Going north");
                dir[0] = 'N';
            } 

            else if (pos[0] + 1 < grid.Length 
            && (grid[pos[0] + 1][pos[1]] == '|' || grid[pos[0] + 1][pos[1]] == '+' || grid[pos[0] + 1][pos[1]] == 'X'))
            {
                pos[0]++;
                Console.WriteLine("Going south");
                dir[0] = 'S';
            }          

            else if (pos[1] - 1 >= 0
             && (grid[pos[0]][pos[1] - 1] == '-' || grid[pos[0]][pos[1] - 1] == '+' || grid[pos[0]][pos[1] - 1] == 'X'))
            {
                pos[1]--;
                Console.WriteLine("Going west");
                dir[0] = 'W';
            } 

            else  if (pos[1] + 1 < grid[0].Length 
            && (grid[pos[0]][pos[1] + 1] == '-' || grid[pos[0]][pos[1] + 1] == '+' || grid[pos[0]][pos[1] + 1] == 'X'))
            
            {
                pos[1]++;
                Console.WriteLine("Going East");
                dir[0] = 'E';
            }    

            else
            {
                dir[0] = 'L';
            }                            
                            
        }

        
        public static List<string> FullLine(char[][] grid)

        {

            var list = new List<string>();


            for (int i = 0; i < grid.Length; i++)

            {
                for (int j = 0; j < grid[0].Length; j++)

                {

                    if (grid[i][j] == 'X' || grid[i][j] == '-' || grid[i][j] == '|' || grid[i][j] == '+')
                    {
                        list.Add($"{i}{j}");
                    }

                }
            }

            return list;


        }
}
_______________________________________
using System;
using System.Collections.Generic;
using System.Linq;

  public static class Dinglemouse
  {
      public static bool Line(char[][] grid)
      {
          PathWalker walker = new PathWalker();
          var result = walker.WalkTheLine(grid);
          return result;
      }
  }
  
  /// <summary>
  /// Represents a utility that will walk a valid line based on rules described in this kata:
  /// https://www.codewars.com/kata/59c5d0b0a25c8c99ca000237/train/csharp
  /// </summary>
  public class PathWalker
  {
      private const char LineTerminator = 'X';
      private const char Horizontal = '-';
      private const char Vertical = '|';
      private const char Corner = '+';
  
      private readonly IGridUtility<char> _gridUtility;
  
      /// <summary>
      /// Initializes a new instance of the <see cref="PathWalker"/> class.
      /// </summary>
      public PathWalker() : this(new GridUtility<char>())
      {
      }
  
      /// <summary>
      /// Initialized a new instance of the <see cref="PathWalker"/> class with injected dependency.
      /// </summary>
      /// <param name="gridUtility">An implementation of <see cref="IGridUtility{char}"/> used for common grid operations.</param>
      public PathWalker(IGridUtility<char> gridUtility)
      {
          this._gridUtility = gridUtility;
      }
  
      /// <summary>
      /// Walk a valid line in the grid.
      /// </summary>
      /// <param name="grid">The grid.</param>
      /// <returns></returns>
      public bool WalkTheLine(char[][] grid)
      {
          // Validate input
          if (grid is null)
          {
              throw new ArgumentNullException(nameof(grid));
          }
  
          // Extract rows containing the X terminator
          var pointRows = grid.Where(n => n.Contains(LineTerminator));
  
          // Try walking from pointA
          var pointa = (y: Array.IndexOf(grid, pointRows.First()), x: Array.IndexOf(pointRows.First(), LineTerminator));
          HashSet<(int, int)> loga = new HashSet<(int, int)>();
          var result = Walk(grid, pointa, loga);
          if (result)
          {
              if (CheckForExtra(grid, loga)) return false;
              return result;
          }
  
          // Try walking from pointB
          var pointb = (y: Array.IndexOf(grid, pointRows.Last()), x: Array.FindLastIndex(pointRows.Last(), c => c == LineTerminator));
          HashSet<(int, int)> logb = new HashSet<(int, int)>();
          result = Walk(grid, pointb, logb);
          if (result) result ^= CheckForExtra(grid, logb);
          return result;
      }
  
      /// <summary>
      /// Walk the line from a starting coordinate.
      /// </summary>
      /// <param name="grid">The grid.</param>
      /// <param name="coord">The starting coordinate.</param>
      /// <param name="log">The log of walk moves from the starting point.</param>
      /// <returns>True if the path is valid; otherwise false</returns>
      private bool Walk(char[][] grid, (int y, int x) coord, HashSet<(int, int)> log)
      {
          // Log starting point
          log.Add(coord);
  
          // Get the next move
          var move = GetNextMove(
              grid,
              coord,
              log,
              (coord.y + -1, coord.x + 0),
              (coord.y + 0, coord.x + 1),
              (coord.y + 1, coord.x + 0),
              (coord.y + 0, coord.x + -1));
  
          return move();
      }
  
      /// <summary>
      /// Get the next viable move. If we can move more than one direction then the path is invalid.
      /// </summary>
      /// <param name="grid">The grid.</param>
      /// <param name="coord">The starting coordinate.</param>
      /// <param name="log">The log of walk moves from the starting point.</param>
      /// <param name="coords">The collection of coordinates to check.</param>
      /// <returns>A delegate function that will return true or false if there is a valid step along the path.</returns>
      private Func<bool> GetNextMove(char[][] grid, (int y, int x) coord, HashSet<(int, int)> log, params (int y, int x)[] coords)
      {
          if (coords.Length == 0) return () => false;
          List<Func<bool>> moves = new List<Func<bool>>();
          foreach (var dest in coords)
          {
              // Check to see if we have been there
              if (log.Contains(dest)) continue;
  
              // Vertical
              if (dest.y != coord.y
                  && _gridUtility.SafeCheck(grid, dest, LineTerminator, Vertical, Corner))
              {
                  moves.Add(() => WalkY(grid, coord, dest.y - coord.y, log));
              }
  
              // Horizontal
              if (dest.x != coord.x
                  && _gridUtility.SafeCheck(grid, dest, LineTerminator, Horizontal, Corner))
              {
                  moves.Add(() => WalkX(grid, coord, dest.x - coord.x, log));
              }
          }
  
          // If there is more than one valid move, then the path is ambiguous
          // If there are no moves, then there is not a valid path
          if (moves.Count == 1) return moves.First();
  
          return () => false;
      }
  
      /// <summary>
      /// Walk along the x-axis.
      /// </summary>
      /// <param name="grid">The grid.</param>
      /// <param name="coord">The starting coordinate.</param>
      /// <param name="direction">The direction to walk. 1 for right, -1 for left.</param>
      /// <param name="log">The log of walk moves from the starting point.</param>
      /// <returns>True if the line is valid; otherwise false.</returns>
      private bool WalkX(char[][] grid, (int y, int x) coord, int direction, HashSet<(int, int)> log)
      {
          var dest = (y: coord.y + 0, x: coord.x + direction);
          if (!log.Add(dest)) return false;
          char c = grid[dest.y][dest.x];
  
          // Make decisions about this step
          switch (c)
          {
              case Horizontal:
                  return GetNextMove(grid, dest, log, (dest.y + 0, dest.x + direction))();
  
              case Corner:
                  return GetNextMove(grid, dest, log,
                      (dest.y + 1, dest.x),
                      (dest.y - 1, dest.x))();
  
              case LineTerminator:
  
                  return true;
  
              default:
                  return false;
          }
      }
  
      /// <summary>
      /// Walk along the y-axis.
      /// </summary>
      /// <param name="grid">The grid.</param>
      /// <param name="coord">The starting coordinate.</param>
      /// <param name="direction">The direction to walk. 1 for left, -1 for right.</param>
      /// <param name="log">The log of walk moves from the starting point.</param>
      /// <returns>True if the line is valid; otherwise false.</returns>
      private bool WalkY(char[][] grid, (int y, int x) coord, int direction, HashSet<(int, int)> log)
      {
          var dest = (y: coord.y + direction, x: coord.x);
          if (!log.Add(dest)) return false;
          char c = grid[dest.y][dest.x];
  
          // Make decisions about this step
          switch (c)
          {
              case Vertical:
                  return GetNextMove(grid, dest, log, (dest.y + direction, dest.x + 0))();
  
              case Corner:
                  return GetNextMove(grid, dest, log,
                      (dest.y + 0, dest.x + 1),
                      (dest.y + 0, dest.x + -1))();
  
              case LineTerminator:
  
                  return true;
  
              default:
                  return false;
          }
      }
  
      /// <summary>
      /// Check the grid for extra line characters that are not part of a path.
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="log">The log of walk moves from the starting point.</param>
      /// <returns>True if the extra chars are found; otherwise false</returns>
      private static bool CheckForExtra(char[][] grid, HashSet<(int, int)> log)
      {
          char[] chars = new char[] { Horizontal, Vertical, Corner };
          for (int y = 0; y < grid.Length; y++)
          {
              for (int x = 0; x < grid[y].Length; x++)
              {
                  if (log.Contains((y, x))) continue;
                  char c = grid[y][x];
                  if (chars.Any(n => n == c))
                  {
                      return true;
                  }
              }
          }
          return false;
      }
  }
  
  /// <summary>
  /// Represents a utility for common operations on a 2 dimensional grid.
  /// </summary>
  /// <typeparam name="T">The type contained in each cell of the grid.</typeparam>
  public class GridUtility<T> : IGridUtility<T>
  {
      /// <inheritdoc/>
      public bool IsOutOfBounds(T[][] grid, (int y, int x) coord)
      {
          if (coord.y < 0 || coord.y >= grid.Length) return true;
          if (coord.x < 0 || coord.x >= grid[coord.y].Length) return true;
          return false;
      }
  
      /// <inheritdoc/>
      public bool SafeCheck(T[][] grid, (int y, int x) coord, params T[] items)
      {
          if (IsOutOfBounds(grid, coord)) return false;
          return (items.Contains(grid[coord.y][coord.x]));
      }
  
      /// <inheritdoc/>
      public IEnumerable<T[]> GetRowsWithItem(T[][] grid, T item)
      {
          return grid.Where(n => n.Contains(item));
      }
  
      /// <inheritdoc/>
      public T GetItem(T[][] grid, (int y, int x) coord)
      {
          return grid[coord.y][coord.x];
      }
  
      /// <inheritdoc/>
      public bool TryGetItem(T[][] grid, (int y, int x) coord, out T item)
      {
          item = default(T);
          if (IsOutOfBounds(grid, coord)) return false;
          item = GetItem(grid, coord);
          return true;
      }
  }
  
  /// <summary>
  /// Defines a utility for common operations on a 2 dimensional grid.
  /// </summary>
  /// <typeparam name="T">The type contained in each cell of the grid.</typeparam>
  public interface IGridUtility<T>
  {
      /// <summary>
      /// Get an item from the grid at the specified coordinate.
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="coord">The coordinat.</param>
      /// <returns>The item.</returns>
      T GetItem(T[][] grid, (int y, int x) coord);
  
      /// <summary>
      /// Retrieves rows from the grid that contain a specified item.
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="item">The item to look for.</param>
      /// <returns>A collection of grid rows.</returns>
      IEnumerable<T[]> GetRowsWithItem(T[][] grid, T item);
  
      /// <summary>
      /// Test to see if the specified coordinates are outside the bounds of the grid
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="coord">The coordinate to check.</param>
      /// <returns>True if the coordinates are outside the bounds of the grid; otherwise false.</returns>
      bool IsOutOfBounds(T[][] grid, (int y, int x) coord);
  
      /// <summary>
      /// Check to see if the item at the specified coordinates matches any items in the params collection.
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="coord">The coordinate to check.</param>
      /// <param name="items">The items to look for.</param>
      /// <returns>True is if one of the items is found; otherwise false.</returns>
      bool SafeCheck(T[][] grid, (int y, int x) coord, params T[] items);
  
      /// <summary>
      /// Try get an item from the grid at the specified coordinate.
      /// </summary>
      /// <param name="grid">The grid</param>
      /// <param name="coord">The coordinat.</param>
      /// <param name="item">The found item or null.</param>
      /// <returns>True if the item found; otherwise false.</returns>
      bool TryGetItem(T[][] grid, (int y, int x) coord, out T item);
  }
