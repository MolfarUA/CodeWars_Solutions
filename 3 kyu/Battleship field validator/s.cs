52bb6539a4cf1b12d90005b7


namespace Solution {
  using System;
    using System.Collections.Generic;
    using System.Linq;
    
    public class BattleShip
    {
        public string Type { get; set; }
        public int Length { get; set; }
        public int Count { get; set; }
    }
    
    public static class BattleshipField
    {
        private static readonly List<BattleShip> Ships = new List<BattleShip>
        {
            new BattleShip { Type = "Battleship", Length = 4, Count = 1 },
            new BattleShip { Type = "Cruiser", Length = 3, Count = 2 },
            new BattleShip { Type = "Torpedo boat", Length = 2, Count = 3 },
            new BattleShip { Type = "Submarine", Length = 1, Count = 4 }
        };

        public static bool ValidateBattlefield(int[,] battlefield)
        {
            // Test number of cells.
            if (battlefield.Cast<int>().Sum() != Ships.Sum(s => s.Count * s.Length))
            {
                return Fail("Wrong number of cells!");
            }

            var height = battlefield.GetLength(0);
            var width = battlefield.GetLength(1);
            var lengths = new List<int> { 0, 0, 0, 0 };

            for (var i = 0; i < battlefield.Length; i++)
            {
                var y = i % width;
                var x = (int)Math.Floor((double)i / width);

                var cell = battlefield[x, y];

                if (cell == 0)
                {
                    // The current cell is 0. Continue with the next cell.
                    continue;
                }

                // The current cell is 1. Validation, go!

                // Test diagonals
                if (y < height - 1)
                {
                    if (x < width - 1 && battlefield[x + 1, y + 1] == 1)
                    {
                        return Fail("Can't have a neighbour to the bottom right");
                    }

                    if (x > 0 && battlefield[x - 1, y + 1] == 1)
                    {
                        return Fail("Can't have a neighbour to the bottom left!");
                    }
                }

                // Count the ship's length.
                var hasLeft = x > 0 && battlefield[x - 1, y] == 1;
                var hasRight = x < width - 1 && battlefield[x + 1, y] == 1;
                var hasTop = y > 0 && battlefield[x, y - 1] == 1;
                var hasBottom = y < height - 1 && battlefield[x, y + 1] == 1;

                if (!new[] { hasLeft, hasRight, hasTop, hasBottom }.Any(b => b))
                {
                    lengths[0]++;
                }
                else if (!hasLeft && hasRight)
                {
                    var length = battlefield.CountShipLength(x, y, true);
                    lengths[length - 1]++;
                }
                else if (!hasTop && hasBottom)
                {
                    var length = battlefield.CountShipLength(x, y, false);
                    lengths[length - 1]++;
                }
            }

            // Validate found ships
            Console.WriteLine("  Validation succesfull. Counting ships...\n" +
                              $"  Battleships:   {lengths[3]}\n" +
                              $"  Cruisers:      {lengths[2]}\n" +
                              $"  Torpedo boats: {lengths[1]}\n" +
                              $"  Submarines:    {lengths[0]}");

            for(var i = 0; i < Ships.Count; i++)
            {
                if (lengths[i] != 4 - i)
                {
                    return Fail($"Incorrect number of {Ships[i].Type.ToLowerInvariant()}s: {lengths[0]}");
                }
            }

            // All validation passed
            Console.WriteLine("  Success! This barttlefield is valid!");

            return true;
        }

        /// <summary>
        /// Fails the test and log a error message.
        /// </summary>
        /// <param name="message">The error message.</param>
        /// <returns></returns>
        private static bool Fail(string message)
        {
            Console.WriteLine($"  Error: {message}");
            return false;
        }

        /// <summary>
        /// Counts the ship's length for a x / y position on the current battlefield.
        /// </summary>
        /// <param name="x">The current x coordinate.</param>
        /// <param name="y">The current y coordinate.</param>
        /// <param name="battlefield">The battlefield.</param>
        /// <param name="isHorizontal">if set to <c>true</c> count the ship in horizontal orientation. Otherwise, count the vertical orientation.</param>
        /// <returns></returns>
        private static int CountShipLength(this int[,] battlefield, int x, int y, bool isHorizontal)
        {
            var height = battlefield.GetLength(0);
            var width = battlefield.GetLength(1);
            var cell = battlefield[x, y];

            if (cell == 0 || // cell isn't 1, so return 0.
                isHorizontal && x == width - 1 || // We're at the right edge of the field, don't count further.
                !isHorizontal && y == height - 1) // We're at the bottom edge of the field, don't count further.
            {
                return cell;
            }

            // Count the current cell plus a possible neighbour, recursively.
            return cell +
                   battlefield.CountShipLength(
                       isHorizontal ? x + 1 : x,
                       !isHorizontal ? y + 1 : y,
                       isHorizontal);
        }
    }
  }
____________________________________________________________
using System.Collections.Generic;
public class BattleshipField
{
  public static bool ValidateBattlefield(int[,] field)
  {
    var ships = new List<int>();    
    for (var x = 0; x < 10; x++)
      for (var y = 0; y < 10; y++)
        if (field[x, y] == 1)
        {
          var length = 1;
          while (x + length < 10 && field[x + length, y] == 1)
            field[x + length++, y] = 0;
          while (y + length < 10 && field[x, y + length] == 1)
            field[x, y + length++] = 0;          
          ships.Add(length);          
        }    
    ships.Sort();
    return string.Join("", ships) == "1111222334";
  }
}
____________________________________________________________
namespace Solution {
  using System;
  using System.Linq;
  public class BattleshipField {
    public static int[,] data;
    public static bool L(int a, int b) { return ( a<0 || b<0 || a>10 || b>10 || (data[a,b] == 0) ); }
    
    public static bool ValidateBattlefield(int[,] field) {
      data = field;
      var flot = new int[5];
      
      for(var a = 0; a<10; a++)
      {
        int v = 0;
        int z = 0;
        
        for(var b = 0; b<10; b++)
        {
          
          if (field[a,b] == 1 && 
            L(a-1, b) &&
            L(a-1, b+1) &&
            L(a-1, b-1) &&
            L(a+1, b) &&
            L(a+1, b+1) &&
            L(a+1, b-1) 
          )
            v++;
          else
          {
            if (v>4) return false;
            if (v!=0) flot[v]++;
            v = 0;
          }
          
          if (field[b,a] == 1 &&
            L(b, a-1) &&
            L(b+1,a-1) &&
            L(b-1,a-1) &&
            L(b, a+1) &&
            L(b+1, a+1) &&
            L(b-1, a+1) 
          )
            z++;
          else
          {
            if (z>4) return false;
            if (z!=0) flot[z]++;
            z = 0;
          }
        }
      }
    return flot[4]==1 && flot[3]==2 && flot[2]==3 && flot[1]==4*2;
    }
  }
}
____________________________________________________________
using System;
using System.Collections.Generic;

namespace Solution
{
  public class BattleshipField
  {
    private static Dictionary<int, int> _sizes = new Dictionary<int, int>
    {
        {1, 4},
        {2, 3},
        {3, 2},
        {4, 1}
    };
    
    public static bool ValidateBattlefield(int[,] field)
    {
      bool Check(int i, int j)
      {
          if (j < 0 || field[i, j] == 0) return true;
    
          var nextRow = i + 1;
          return Check(nextRow, j + 1) && Check(nextRow, j - 1);
      }
    
      int CheckByRow(int i, int j)
      {
          if (field[i, j] != 1 || j > 9) return 0;
    
          field[i, j] = -1;
          return 1 + CheckByRow(i, ++j);
      }
    
      int CheckByColumn(int i, int j)
      {
          if (field[i, j] != 1 || i > 9) return 0;
    
          field[i, j] = -1;
          return 1 + CheckByColumn(++i, j);
      }
    
      for (var i = 0; i < 9; i++)
      {
          for (var j = 0; j < 9; j++)
          {
              if (field[i, j] != 1) continue;
              if (!Check(i, j)) return false;
    
              var nextRow = i + 1;
              var nextColumn = j + 1;
              var length = 1;
    
              if (field[i, nextColumn] == 1)
              {
                  length += CheckByRow(i, nextColumn);
              }
              else if (field[nextRow, j] == 1)
              {
                  length += CheckByColumn(nextRow, j);
              }
    
              _sizes[length]--;
              if (_sizes[length] < 0) return false;
          }
      }
    
      return true;
    }
  }
}
