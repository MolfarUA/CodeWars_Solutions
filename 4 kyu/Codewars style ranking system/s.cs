using System;

public class User
{
    private int _rank;
    public int rank
    {
        get { return _rank; }
        set { _rank = value == 0 ? 1 : value; }
    }
    private int _progress;
    public int progress
    {
        get { return rank == 8 ? 0 : _progress; }
        set
        {
            rank += value / 100;
            _progress = value % 100;
        }
    }

    public User()
    {
        rank = -8;
        progress = 0;
    }

    public void incProgress(int level)
    {
        if (level < -8 || level > 8 || level == 0)
            throw new ArgumentException();

        int tempLevel = level > 0 ? level - 1 : level;
        int tempRank = rank > 0 ? rank - 1 : rank;
        int diff = tempLevel - tempRank;
        
        progress += diff < -1 ? 0 : diff == -1 ? 1 : diff == 0 ? 3 : 10 * diff * diff;
    }
}
_____________________________________
using System;
using System.Linq;

public class User
{
    private static readonly int[] Ranks = new int[] { -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8 };
    private int _rankIndex = 0;
    public int progress { get; private set; }
    public int rank => Ranks[_rankIndex];
    public void incProgress(int activityRank)
    {        
        if (!IsValidRank(activityRank)) throw new ArgumentException("Invalid activity rank");
        if (rank == 8) return;
        var activityRankIndex = Array.IndexOf(Ranks, activityRank);
        var rankDifference = activityRankIndex - _rankIndex;
        if (rankDifference < -2) return;
        else if (rankDifference == -1) progress++;
        else if (rankDifference == 0) progress += 3;
        else progress += (10 * rankDifference * rankDifference);
        UpdateRank();
    }
    private void UpdateRank()
    {
        if (progress >= 100)
        {
            var rankIncrease = progress / 100;
            _rankIndex += rankIncrease;
            var maxRankIndex = Ranks.Length - 1;
            if (_rankIndex >= maxRankIndex)  {
              _rankIndex = maxRankIndex;
              progress = 0;
            } else {
              progress %= 100;
            }            
        }
    }
    private static bool IsValidRank(int inputRank) => Ranks.Contains(inputRank);
}
_____________________________________
using System;
using System.Linq;

public class User
{
    private static int[] ranks = new int[] {-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8};
    public int rankPtr;
    public int rank;
    public int progress;
  
    public User()
    {
        rankPtr = 0;
        rank = ranks[0];
        progress = 0;
    }
    
    public void incProgress(int rank)
    {
        if (!ranks.Contains(rank))
          throw new ArgumentException();
        progress += calculateProgress(rank);
        if (progress >= 100)
          rankUp();
    }
  
    private void rankUp()
    {
        rankPtr += (int) progress / 100;
        progress %= 100;
        rank = ranks[rankPtr];
        if (rank == ranks[ranks.Length - 1])
          progress = 0;
    }
  
    private int calculateProgress(int rank)
    {
        int diff = Array.IndexOf(ranks, rank) - rankPtr;
        if (rankPtr >= ranks.Length - 1 || diff < -1) return 0;
        else if (diff  >  0) return 10 * diff * diff;
        else if (diff ==  0) return 3;
        else if (diff == -1) return 1;
        return 0;
    }
}
_____________________________________
using System;

public class User
{
  private int _rank = -8;
  private int _progress = 0;
  
  public int rank => _rank;
  public int progress => _progress;
  
  public void incProgress(int activityRank)
  {
    if (activityRank == 0 || activityRank > 8 || activityRank < -8)
    {
        throw new ArgumentException(null, nameof(activityRank));
    }

    var rankDiff = activityRank - _rank;

    if (_rank < 0 && activityRank > 0)
    {
      rankDiff--;
    } else if (_rank > 0 && activityRank < 0)
    {
      rankDiff++;
    }
    
    _progress += CalculateProgress(rankDiff);

    while (_progress >= 100)
    {
      _progress -= 100;
      _rank += _rank + 1 == 0 ? 2 : 1;
    }
    
    if (_rank == 8) _progress = 0;
  }
  
  private int CalculateProgress(int rankDiff)
  {
    if (rankDiff == 0) return 3;
    if (rankDiff == -1) return 1;
    if (rankDiff <= -2) return 0;   
    
    return 10 * rankDiff * rankDiff;
  }
}

