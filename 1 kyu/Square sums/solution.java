import java.util.*;
import java.util.stream.*;

public class SquareSums {
    
    final static private int TOP = 1200;
    final static private Set<Integer> SQ = IntStream.range(1, (int) Math.sqrt(2*TOP) + 1)
                                                    .map( n -> n*n ).boxed()
                                                    .collect(Collectors.toSet());
    
    
    public static List<Integer> buildUpTo(final int top) {
        
        List<Cnd> cnds = IntStream.range(1,top+1).mapToObj(Cnd::new).collect(Collectors.toList());
        for(final Cnd c: cnds) {
            SQ.stream().filter(  sq -> c.n<sq && sq-c.n<=top && 2*c.n!=sq )
                       .forEach( sq -> c.add( cnds.get(sq-c.n-1) ) );
        }
        Collections.sort(cnds);
        if (cnds.get(0).size()==1) cnds.removeIf(c->c.size()!=1);
        
        var out = new Stack<Integer>();
        return dfs(out, top, cnds) ? new ArrayList<>(out) : null;
    }
    
    
    private static boolean dfs(Stack<Integer> out, int top, List<Cnd> cnds) {
        
        if (out.size()==top) return true;
        if (cnds.isEmpty() || cnds.get(0).isEmpty() && out.size()+1!=top) return false;
        
        for (Cnd c: cnds) {
            List<Cnd> cuts = c.unLink();
            out.push(c.n);
            if (dfs(out,top, c.getCnds())) return true;
            out.pop();
            c.link(cuts);
        }
        return false;
    }
    
    
    //------------------------------------------------------------------
    
    private static class Cnd extends HashSet<Cnd> implements Comparable<Cnd> {
        private int n;
        
        private Cnd(int n){ super(); this.n=n; }
        
        private List<Cnd> getCnds(){ return this.stream().sorted().collect(Collectors.toList()); }
        
        private void link(List<Cnd> others) { 
            for(Cnd c: others) c.add(this); 
        }
        private List<Cnd> unLink() {
            List<Cnd> cuts = new ArrayList<>(this);
            for(Cnd c: cuts) c.remove(this);
            return cuts;
        }
        @Override public int compareTo(Cnd o) {
            return this.size()!=o.size() ? this.size()-o.size() : o.n-this.n; 
        }
        @Override public int     hashCode()       { return n; }
        @Override public boolean equals(Object o) { return o!=null && (o instanceof Cnd) && ((Cnd) o).n==this.n; }
        @Override public String  toString()       { 
            return String.format("Cnd(%d, {%s})", n, this.stream().map( c -> c.n+"" ).collect(Collectors.joining(","))); 
        }
    }
}
______________________________________________
import java.util.*;

public class SquareSums {
    
    public static List<Integer> buildUpTo(int n) {
        var graph = buildGraph(n);
        var candidates = new ArrayList<Integer>();
        for(int i=1;i<=n;i++) candidates.add(i);
        return DFS(graph, candidates, new ArrayList<Integer>(), n);
    }
  
    public static List<Set<Integer>> buildGraph(int n){
        var graph = new ArrayList<Set<Integer>>();
        var squares = new ArrayList<Integer>();
    
        for(int i=2;i*i<n*2;i++){
          squares.add(i*i);
        } 
        for(int i=0;i<=n;i++){
            graph.add(new HashSet<Integer>());
            for(int j:squares){
                if(i<j){
                    int diff= j-i;
                    if( diff == i ) continue;
                    if( diff <= n ) graph.get(i).add(diff);
                    else break;
                }
            }
        }   
        return graph;
    }
  
    public static List<Integer> DFS( List<Set<Integer>> graph, List<Integer> candidates, List<Integer> path, int n ){
        if( path.size() == n ) return path;
        candidates.sort((a, b) -> Integer.compare(graph.get(a).size(), graph.get(b).size()));
        for(var candidate: candidates){
            path.add(candidate);
            graph.get(candidate).forEach(e -> graph.get(e).remove(candidate));
            if(DFS(graph, new ArrayList<Integer>(graph.get(candidate)), path, n) != null) return path;
            path.remove(path.size()-1);
            graph.get(candidate).forEach(e -> graph.get(e).add(candidate));
        }
        return null;
    }
}
______________________________________
import java.util.*;
import java.util.function.Consumer;

public class SquareSums {
  public static final int MAX_N = 1600;
  private final int n;
  private final Consumer<List<Integer>> solutionProcessor;
  private final Integer[][] adjacent;
  private final Integer[] chain;
  private final boolean[] remaining;

  public SquareSums(int n, Consumer<List<Integer>> solutionProcessor) {
    if (n < 3)
      throw new IllegalArgumentException("n is too small");
    this.n = n;
    this.solutionProcessor = solutionProcessor;
    adjacent = new Integer[n + 1][];
    chain = new Integer[n];
    remaining = new boolean[n + 1];
    for (int i = 1; i <= n; i++) {
      adjacent[i] = connArray(i, n);
      chain[i - 1] = integerCache[i];
      remaining[i] = true;
    }
  }

  private static final Integer[] integerCache = new Integer[MAX_N + 1];
  static {
    for (int i = 0; i <= MAX_N; i++)
      integerCache[i] = i;
  }
  
  private static final boolean[][] connected = new boolean[MAX_N + 1][MAX_N + 1];
  static {
    int a = 1;
    while (true) {
      a++;
      int s = a * a;
      if (s > 2 * MAX_N - 1)
        break;
      for (int i = 1; i <= MAX_N; i++) {
        int j = s - i;
        if (j > 0 && j <= MAX_N && j != i)
          connected[i][j] = true;
      }
    }
  }

  private static Integer[] connArray(int i, int n) {
    List<Integer> connList = new ArrayList<>();
    boolean[] connRow = connected[i];
    for (int j = 1; j <= n; j++)
      if (connRow[j])
        connList.add(integerCache[j]);
    return connList.toArray(new Integer[connList.size()]);
  }

  private void swapChain(int i, int j) {
    if (i == j)
      return;
    Integer t = chain[i];
    chain[i] = chain[j];
    chain[j] = t;
  }

  private void solveNarrowed(int leftIndex, int rightIndex) {
    Integer left = integerCache[chain[leftIndex]];
    Integer right = integerCache[chain[rightIndex]];
    if (rightIndex == leftIndex + 2) {
      boolean[] lastConn = connected[chain[leftIndex + 1]];
      if (lastConn[left] && lastConn[right])
        solutionProcessor.accept(Arrays.asList(chain.clone()));
      return;
    }
    List<Integer> leftAdj = new ArrayList<>();
    List<Integer> rightAdj = new ArrayList<>();
    Integer needsLeft = null;
    Integer needsRight = null;
    for (int i = leftIndex + 1; i < rightIndex; i++) {
      int adjCount = 0;
      boolean aLeft = false;
      boolean aRight = false;
      Integer ii = integerCache[i];
      for (Integer j : adjacent[chain[i]])
        if (remaining[j]) {
          adjCount++;
          if (j == left) {
            aLeft = true;
            leftAdj.add(ii);
          } else if (j == right) {
            aRight = true;
            rightAdj.add(ii);
          }
        }
      if (adjCount < 2)
        return;
      if (adjCount == 2)
        if (aLeft)
          if (aRight || needsLeft != null)
            return;
          else
            needsLeft = ii;
        else if (aRight)
          if (needsRight != null)
            return;
          else
            needsRight = ii;
    }
    if (needsLeft != null)
      leftAdj = Collections.singletonList(needsLeft);
    int laCount = leftAdj.size();
    if (needsRight != null)
      rightAdj = Collections.singletonList(needsRight);
    int raCount = rightAdj.size();
    if (laCount == 0 || raCount == 0)
      return;
    if (laCount <= raCount) {
      remaining[left] = false;
      int nextLeftIndex = leftIndex + 1;
      for (int nextLeft : leftAdj) {
        swapChain(nextLeftIndex, nextLeft);
        solveNarrowed(nextLeftIndex, rightIndex);
        swapChain(nextLeftIndex, nextLeft);
      }
      remaining[left] = true;
    } else {
      remaining[right] = false;
      int prevRightIndex = rightIndex - 1;
      for (int prevRight : rightAdj) {
        swapChain(prevRight, prevRightIndex);
        solveNarrowed(leftIndex, prevRightIndex);
        swapChain(prevRight, prevRightIndex);
      }
      remaining[right] = true;
    }
  }

  // Solutions that are mirrors of each other are considered equal.
  // This also applies to solutionCount() and printAllSolutions().
  public void solveComplete() {
    int n1 = n - 1;
    for (int i = 0; i < n1; i++) {
      swapChain(0, i);
      for (int j = i + 1; j < n; j++) {
        swapChain(j, n1);
        solveNarrowed(0, n1);
        swapChain(j, n1);
      }
      swapChain(0, i);
    }
  }

  @SuppressWarnings("serial")
  private static class BreakSearchException extends RuntimeException {
  }

  public static List<Integer> firstSolution(int n) {
    @SuppressWarnings("unchecked")
    List<Integer>[] solutions = new List[1];
    try {
      new SquareSums(n, solution -> {
        solutions[0] = solution;
        throw new BreakSearchException();
      }).solveComplete();
    } catch (BreakSearchException e) {
    }
    return solutions[0];
  }

  public static int solutionCount(int n) {
    int[] counter = new int[1];
    new SquareSums(n, solution -> {
      counter[0]++;
    }).solveComplete();
    return counter[0];
  }

  public static void printAllSolutions(int n) {
    System.out.println("All solutions for n = " + n + ":");
    new SquareSums(n, solution -> {
      System.out.println(solution);
    }).solveComplete();
  }

  public static boolean isCircle(List<Integer> solution) {
    return connected[solution.get(0)][solution.get(solution.size() - 1)];
  }

  public static List<Integer> expandCircle(List<Integer> solution) {
    int n = solution.size() + 1;
    boolean[] nConn = connected[n];
    int i = 0;
    while (!nConn[solution.get(i)])
      i++;
    i++;
    List<Integer> result = new ArrayList<>(n);
    result.addAll(solution.subList(i, n - 1));
    result.addAll(solution.subList(0, i));
    result.add(integerCache[n]);
    return result;
  }

  public static List<Integer> close(List<Integer> solution) {
    if (isCircle(solution))
      return solution;
    int n = solution.size();
    int n1 = n - 1;
    int last = solution.get(n1);
    int[] links = new int[n];
    links[1] = 1;
    int i;
    for (i = 1; i < n1; i++) {
      if (links[i] == 0)
        continue;
      boolean[] prevConn = connected[solution.get(i - 1)];
      if (prevConn[last]) {
        links[n1] = i;
        break;
      }
      for (int j = i + 1; j < n1; j++)
        if (links[j] == 0 && prevConn[solution.get(j)])
          links[j] = i;
    }
    if (i == n1)
      return null;
    int k = 0;
    i = n1;
    do {
      k++;
      i = links[i];
    } while (i != 1);
    int[] parts = new int[k + 1];
    i = n1;
    for (int j = k; j >= 0; j--) {
      parts[j] = i;
      i = links[i];
    }
    List<Integer> result = new ArrayList<>(n);
    result.add(solution.get(0));
    for (i = 1; i <= k; i += 2)
      for (int j = parts[i - 1]; j < parts[i]; j++)
        result.add(solution.get(j));
    result.add(last);
    i -= 2;
    if (i == k)
      i -= 2;
    for (; i > 0; i -= 2)
      for (int j = parts[i + 1] - 1; j >= parts[i]; j--)
        result.add(solution.get(j));
    return result;
  }

  private static final Random rand = java.util.concurrent.ThreadLocalRandom.current();

  public static boolean flipTail(List<Integer> solution) {
    int n = solution.size();
    boolean[] lastConn = connected[solution.get(n - 1)];
    List<Integer> connInd = new ArrayList<>();
    for (int i = 0, end = n - 3; i <= end; i++)
      if (lastConn[solution.get(i)])
        connInd.add(integerCache[i]);
    if (connInd.isEmpty()) // Cannot cut, last number has only one neighbour
      return false;
    Collections.reverse(solution.subList(connInd.get(rand.nextInt(connInd.size())) + 1, n));
    return true;
  }

  private static final List<List<Integer>> solutionCache = new ArrayList<>(MAX_N + 1);
  static {
    Collections.addAll(solutionCache, null, Collections.singletonList(1), null);
  }

  private static final int MAX_ATTEMPTS = 1000;

  public static List<Integer> buildUpTo(int n) {
    if (n > MAX_N)
      throw new IllegalArgumentException("n is too large");
    int m = solutionCache.size() - 1; // last n in cache
    if (m >= n)
      return solutionCache.get(n);
    List<Integer> solution = solutionCache.get(m);
    do {
      m++;
      if (solution != null && isCircle(solution))
        solution = expandCircle(solution);
      else
        solution = firstSolution(m);
      if (solution != null)
        for (int i = 1; i <= MAX_ATTEMPTS; i++) {
          List<Integer> circle = close(solution);
          if (circle != null) {
            solution = circle;
            break;
          }
          Collections.reverse(solution);
          flipTail(solution);
        }
      solutionCache.add(solution);
    } while (m < n);
    return solution;
  }
}
