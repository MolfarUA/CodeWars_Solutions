import java.util.Arrays;
public class User {
  private int[] ranks = {-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8};
  private int curRank = 0;
  public int progress = 0;
  public int rank = -8;
  public void incProgress(int kRank) {
    kRank = Arrays.binarySearch(ranks, kRank);
    if(kRank < 0) throw new RuntimeException("Invalid rank");
    if(ranks[curRank] == 8) return;
    if(kRank == curRank) progress += 3;
    else if(kRank == curRank - 1) progress++;
    else if(kRank > curRank) {
      int diff = kRank - curRank;
      progress += 10 * diff * diff;
    }
    while(progress >= 100) {
      curRank++;
      updateRank();
      progress -= 100;
      if(ranks[curRank] == 8) {
        progress = 0;
        return;
      }
    }
  }
  private void updateRank() {
    rank = ranks[curRank];
  }
}
_____________________________________
public class User {
    public int rank = -8;
    public int progress = 0;
    
    // rank getter
    public int getRank() {
        return this.rank;
    }
    
    // rank setter
    public void setRank(int rank) {
         this.rank = rank;
    }
    
    // progress getter
    public int getProgress() {
        return this.progress;
    }
    
    // progress setter
    public void setProgress(int progress) {
         this.progress = progress;
    }
    
    public void incProgress(int rank) { 
        int tempProgress = this.getProgress() + calcProgressToAdd(rank);
        int newRank = this.getRank();
        int newProgress = tempProgress;
        
        if (tempProgress >= 100) {
            newRank = newRank + (tempProgress / 100);
             // ignore zero in range
            if (this.getRank() < 0 && newRank >= 0)
                newRank++;
            newProgress = tempProgress - ((tempProgress / 100) * 100);
        }
        // no more progression if rank is 8;
        if (newRank >= 8)
            newProgress = 0;
        
        this.setRank(newRank);
        this.setProgress(newProgress);
    }
    
    // calculate progress to be add
    public int calcProgressToAdd(int kataRank) {
        if (kataRank == 0 || kataRank > 8 || kataRank < -8) 
            throw new IllegalArgumentException("Invalid Range!!!");
            
        // if statement to ignore zero for getting range    
        if (this.getRank() < 0 && kataRank > 0) {
            kataRank--;
        } else if (this.getRank() > 0 && kataRank < 0) {
            kataRank++;
        }
        
        int diff = kataRank - this.getRank();
        int progressToAdd;
        if (diff == 0)
            progressToAdd = 3;
        else if (diff == -1) 
            progressToAdd = 1;
        else if (diff < -1)
            progressToAdd = 0;
        else 
            progressToAdd = 10 * diff * diff;
        return progressToAdd;
    }
}
_____________________________________
import java.util.*;

public class User {

    private static int MAX_RANK = 8, MAX_PROGRESS = 100;
    private static Set<Integer> RANKS = new HashSet<Integer>( Arrays.asList(-8,-7,-6,-5,-4,-3,-2,-1, 1, 2, 3, 4, 5, 6, 7, 8) );
    
    int rank, progress;
    
    public User() {
        rank = -8;
        progress = 0;
    }
    
    public void incProgress(int kataRank) {
        if (!RANKS.contains(kataRank)) throw new RuntimeException("Invalid rank");
        int dRank = kataRank - rank + (rank > 0 ? 1:-1) * (kataRank*rank < 0 ? 1:0);
        updateProgress(dRank > 0  ? 10 * dRank * dRank:
                       dRank == 0 ? 3:
                       dRank > -2 ? 1:0);
    }
    
    private void updateProgress(int p) {
        int nLevel = (progress+p) / MAX_PROGRESS;
        rank += nLevel + (RANKS.contains(rank+nLevel) ? 0:1);
        progress = rank >= MAX_RANK ? 0 : (progress+p) % MAX_PROGRESS;
    }
}
_____________________________________
class User {
  public int rank = -8;
  public int progress = 0;

  public void incProgress(int rank) {
    if (rank == -9 || rank == 0 || rank == 9) throw new IllegalArgumentException();
    progress += calcucateProgress(rank);
    while(progress >= 100){
      if (this.rank + 1 == 0) this.rank = 0;
      this.rank += 1;
      progress -= 100;
    }
    if (this.rank == 8) progress = 0;
  }

  private int calcucateProgress(int rank){
    int val = 0;
    int inc = Math.abs(this.rank - rank);
    if ((this.rank < 0 && rank > 0) || (this.rank > 0 && rank < 0)) inc -= 1;
    if (this.rank < rank) val = 10 * inc * inc;
    else if (this.rank > rank && inc == 1) val = 1;
    else if (this.rank == rank) val = 3;
    return val;
  }
}
_____________________________________
class User {
    int rank;
    int progress;

    User() {
        this.rank = -8;
        this.progress = 0;
    }

    public void incProgress(int kataRank) {
        if (kataRank < -8 || kataRank > 8 || kataRank == 0) {
            throw new IllegalArgumentException();
        }
        int delta = kataRank - rank;
        delta = (kataRank > 0 && rank < 0) ? delta - 1 : (kataRank < 0 && rank > 0) ? delta + 1 : delta;
        progress += delta < - 1 ? 0 : delta == -1 ? 1 : delta == 0 ? 3 : 10 * delta * delta;
        while (progress >= 100) {
            rank = (rank == 8) ? rank : (rank != -1) ? rank + 1 : rank + 2;
            progress -= 100;
        }
        progress = rank == 8 ? 0 : progress;
    }
}

