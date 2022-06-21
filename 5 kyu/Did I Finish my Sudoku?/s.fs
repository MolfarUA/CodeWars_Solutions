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
using System;
using System.Collections.Generic;
using System.Linq;

public class Sudoku
{
  public static string DoneOrNot(int[][] board)
        {
            List<int> list = new List<int>();
            int ersteReihe;
            int zweiteReihe;
            int dritteReihe;
            int vierteReihe;
            int fuenfteReihe;
            int sechsteReihe;
            int siebteReihe;
            int achteReihe;
            int neunteReihe;
            int count = 0;
            int proofNumber = 1;
            int proofAll = 1;

            do
            {
                ersteReihe = board[0][count];
                list.Add(ersteReihe);
                zweiteReihe = board[1][count];
                list.Add(zweiteReihe);
                dritteReihe = board[2][count];
                list.Add(dritteReihe);
                vierteReihe = board[3][count];
                list.Add(vierteReihe);
                fuenfteReihe = board[4][count];
                list.Add(fuenfteReihe);
                sechsteReihe = board[5][count];
                list.Add(sechsteReihe);
                siebteReihe = board[6][count];
                list.Add(siebteReihe);
                achteReihe = board[7][count];
                list.Add(achteReihe);
                neunteReihe = board[8][count];
                list.Add(neunteReihe);

                list.Sort();
                foreach (var c in list)
                {
                    if (c == proofNumber)
                    {
                        proofNumber++;
                        proofAll++;
                    }
                }
                proofNumber = 1;
                list.Clear();
                count++;
            } while (count != 9);

            count = 0;
            do
            {
                ersteReihe = board[count][0];
                list.Add(ersteReihe);
                zweiteReihe = board[count][1];
                list.Add(zweiteReihe);
                dritteReihe = board[count][2];
                list.Add(dritteReihe);
                vierteReihe = board[count][3];
                list.Add(vierteReihe);
                fuenfteReihe = board[count][4];
                list.Add(fuenfteReihe);
                sechsteReihe = board[count][5];
                list.Add(sechsteReihe);
                siebteReihe = board[count][6];
                list.Add(siebteReihe);
                achteReihe = board[count][7];
                list.Add(achteReihe);
                neunteReihe = board[count][8];
                list.Add(neunteReihe);

                list.Sort();
                foreach (var c in list)
                {
                    if (c == proofNumber)
                    {
                        proofNumber++;
                        proofAll++;
                    }
                }
                proofNumber = 1;
                list.Clear();
                count++;
            } while (count != 9);

            count = 0;
            int count2 = 0;
            int countEnd = 0;
            do
            {
                ersteReihe = board[count2][count];
                list.Add(ersteReihe);
                zweiteReihe = board[count2][count +1];
                list.Add(zweiteReihe);
                dritteReihe = board[count2][count +2];
                list.Add(dritteReihe);
                vierteReihe = board[count2+1][count];
                list.Add(vierteReihe);
                fuenfteReihe = board[count2+1][count +1];
                list.Add(fuenfteReihe);
                sechsteReihe = board[count2+1][count +2];
                list.Add(sechsteReihe);
                siebteReihe = board[count2+2][count];
                list.Add(siebteReihe);
                achteReihe = board[count2+2][count +1];
                list.Add(achteReihe);
                neunteReihe = board[count2+2][count +2];
                list.Add(neunteReihe);

                list.Sort();
                foreach (var c in list)
                {
                    if (c == proofNumber)
                    {
                        proofNumber++;
                        proofAll++;
                    }
                }
                proofNumber = 1;
                list.Clear();
                count += 3;
                countEnd++;
                if(count > 6)
                {
                    count = 0;
                    count2 += 3;
                }
            } while (countEnd != 9);
            if (proofAll == 244)
            {
                return "Finished!";
            }
            else
                return "Try again!";
        }
}
________________________________
using System.Linq;
using System;
using System.Collections.Generic;
public class Sudoku
{
  public static string DoneOrNot(int[][] board)
  {
List<int> compare = new List<int>() { 1, 2, 3, 4, 5, 6, 7, 8, 9};
int[] row = new int[9];
int[] column = new int[9];
int[] box = new int[9];
//Row, Row Offset, Colomn
int[] boxOffset = new int[3] {0, 0, 0};
for (int i = 0; i < 9; i++)
{
    for (int k = 0; k < 9; k++)
    {
        row[k] = board[i][k];
        column[k] = board[k][i];
        box[k] = board[boxOffset[0] + boxOffset[1]][boxOffset[2]];
        if ((boxOffset[2]+1) % 3 == 0)
        {
            boxOffset[2] -= 2;
            boxOffset[1]++;
        }
        else
            boxOffset[2]++;
    }
    boxOffset[1] = 0;
    if (boxOffset[2] + 3 >= 9)
    {
        boxOffset[2] = 0;
        boxOffset[0] += 3;
    }
    else
        boxOffset[2] += 3;
    if (!row.OrderBy(c => c).SequenceEqual(compare) || !column.OrderBy(c => c).SequenceEqual(compare) || !box.OrderBy(c => c).SequenceEqual(compare))
        return "Try again!";
}
return "Finished!";

  }
}
