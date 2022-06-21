53db96041f1a7d32dc0004d2


using System.Linq;

public class Sudoku
{
  public static string DoneOrNot(int[][] board) => IsDone(board) ? "Finished!": "Try again!";
       
  private static bool IsDone(int[][] board)
  {
    return Enumerable
      .Range(0, 9)
      .SelectMany(i => new[]
      {
          board[i].Sum(),
          board.Sum(b => b[i]),
          board.Skip(3 * (i / 3)).Take(3).SelectMany(r => r.Skip(3 * (i % 3)).Take(3)).Sum()
      })
      .All(i => i == 45);
  }
}
________________________________
public class Sudoku
{
  public static string DoneOrNot(int[][] board)
  {
    for (int i = 0; i < 9; i++)
    {
      int sum = 0;
      
      for (int j = 0; j < 9; j++)
        sum += board[i][j] + board[j][i] + board[(i%3)*3+(j%3)][(i/3)*3+(j/3)];
      
      if ( sum != 135 ) return "Try again!";
    }
    
    return "Finished!";
  }
}
________________________________
using System.Collections.Generic;
using System.Linq;
public class Sudoku
{
   public static string DoneOrNot(int[][] board)
        {
            HashSet<int[]> columns = new HashSet<int[]>();
            for (int i = 0; i < 9; i++)
            {
                if (i != 0 && i % 3 == 0 && !ValidRegoin(i-3,i,board))
                    return "Try again!";

                if (!ValidRow(9,board[i]) || !ValidColumn(i,board))
                    return "Try again!";
                
            }
            return "Finished!";
        }

        private static bool ValidRegoin(int begin, int end, int[][] board)
        {
            HashSet<int> hash = new HashSet<int>();
            for (int i = begin; i < end; i++)
            {
                for (int j = begin; j < end; j++)
                {
                    if(!hash.Add(board[i][j]))
                        return false;
                }
            }
            return true;
        }

        private static bool ValidColumn(int column, int[][] board)
        {
            HashSet<int> hash = new HashSet<int>();

            return board.All(row => hash.Add(row[column]));
        }

        private static bool ValidRow(int rowCount, int[] section)
        {
            HashSet<int> hash = new HashSet<int>(section); 
            return hash.Count== rowCount;
        }
}
