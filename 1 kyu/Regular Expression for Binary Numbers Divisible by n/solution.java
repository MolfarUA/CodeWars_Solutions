5993c1d917bc97d05d000068



import java.util.*;

class FSM {
  private final int n; // state count
  private final int m; // alphabet size
  private final char[] alphabet;
  private final int[][] transitions;

  public FSM(char[] alphabet, int[][] transitions) {
    n = transitions.length;
    m = alphabet.length;
    this.alphabet = alphabet;
    this.transitions = transitions;
  }

  private enum Embrace { // parentheses condition
    SEQ_OR, OR, NEVER
  };

  private static void addStar(StringBuilder sb) {
    int lastIndex = sb.length() - 1;
    if (sb.charAt(lastIndex) == '+')
      sb.setCharAt(lastIndex, '*');
    else
      sb.append('*');
  }

  private class RegexConverter {
    final int n = FSM.this.n;
    final String[][] ts; // transition strings
    final int[][] cl; // connection levels

    RegexConverter() {
      ts = new String[n][n];
      setPrimitiveTransitions();
      cl = new int[n][n];
      setConnectionLevels();
    }

    void setPrimitiveTransitions() {
      String[] trSymbols = new String[n];
      for (int i = 0; i < n; i++)
        trSymbols[i] = "";
      for (int i = 0; i < n; i++) {
        int[] transitionRow = transitions[i];
        for (int j = 0; j < m; j++)
          trSymbols[transitionRow[j]] += alphabet[j];
        String[] regexRow = ts[i];
        for (int j = 0; j < n; j++) {
          String smb = trSymbols[j];
          switch (smb.length()) {
            case 2:
              smb = '[' + smb + ']';
            case 1:
              regexRow[j] = smb;
              trSymbols[j] = "";
          }
        }
      }
    }

    void setConnectionLevels() {
      List<Integer> left = new ArrayList<>(n - 1);
      List<Integer> right = new ArrayList<>(n - 1);
      for (int src = 0; src < n; src++)
        for (int dest = 0; dest < n; dest++)
          if (ts[src][dest] != null)
            cl[src][dest] = n + 1;
      for (int i = n - 1; i >= 0; i--) {
        int i1 = i + 1;
        for (int src = 0; src < n; src++)
          if (src != i)
            if (ts[src][i] != null)
              left.add(src);
            else
              for (int j = i1; j < n; j++)
                if (cl[src][j] != 0 && ts[j][i] != null) {
                  left.add(src);
                  break;
                }
        for (int dest = 0; dest < n; dest++)
          if (dest != i)
            if (ts[i][dest] != null)
              right.add(dest);
            else
              for (int j = i1; j < n; j++)
                if (ts[i][j] != null && cl[j][dest] != 0) {
                  right.add(dest);
                  break;
                }
        for (int src : left) {
          int[] clRow = cl[src];
          for (int dest : right)
            if (clRow[dest] == 0)
              clRow[dest] = i1;
        }
        left.clear();
        right.clear();
      }
    }

    // Path only through { wb, wb + 1, ... , n - 1 }; wb stands for way bound.
    void addPath(StringBuilder sb, int src, int dest, int wb, Embrace embCond) {
      assert cl[src][dest] > wb;
      if (wb == n) {
        sb.append(ts[src][dest]);
        return;
      }
      int nextWb = wb + 1;
      boolean wbToWb = cl[wb][wb] > nextWb;
      if (wb != src && wb != dest) {
        boolean withoutWb = cl[src][dest] > nextWb;
        boolean srcWbDest = cl[src][wb] > nextWb && cl[wb][dest] > nextWb;
        if (srcWbDest) {
          boolean embrace = (withoutWb ? 2 : 1) > embCond.ordinal();
          if (embrace)
            sb.append('(');
          addPath(sb, src, wb, nextWb, Embrace.OR);
          if (wbToWb) {
            addPath(sb, wb, wb, nextWb, Embrace.SEQ_OR);
            addStar(sb);
          }
          addPath(sb, wb, dest, nextWb, Embrace.OR);
          if (withoutWb) {
            sb.append('|');
            addPath(sb, src, dest, nextWb, Embrace.NEVER);
          }
          if (embrace)
            sb.append(')');
        } else
          addPath(sb, src, dest, nextWb, embCond);
      } else if (src == dest) {
        addPath(sb, src, src, nextWb, Embrace.SEQ_OR);
        sb.append('+');
      } else if (wbToWb) {
        boolean embrace = embCond == Embrace.SEQ_OR;
        if (embrace)
          sb.append('(');
        if (wb == src) {
          addPath(sb, wb, wb, nextWb, Embrace.SEQ_OR);
          addStar(sb);
          addPath(sb, wb, dest, nextWb, Embrace.OR);
        } else {
          addPath(sb, src, wb, nextWb, Embrace.OR);
          addPath(sb, wb, wb, nextWb, Embrace.SEQ_OR);
          addStar(sb);
        }
        if (embrace)
          sb.append(')');
      } else
        addPath(sb, src, dest, nextWb, embCond);
    }

    String toRegex(int initialState, int finalState) {
      if (cl[initialState][finalState] == 0)
        return "a\bc";
      StringBuilder sb = new StringBuilder();
      addPath(sb, initialState, finalState, 0, Embrace.NEVER);
      return sb.toString();
    }
  }

  public String toRegex(int initialState, int finalState) {
    return new RegexConverter().toRegex(initialState, finalState);
  }
}

public class Solution {
  public static FSM remainder(int mod) {
    char[] alphabet = { '0', '1' };
    int[][] transitions = new int[mod][2];
    for (int m = 0; m < mod; m++)
      for (int d = 0; d < 2; d++)
        transitions[m][d] = (2 * m + d) % mod;
    return new FSM(alphabet, transitions);
  }

  public String regexDivisibleBy(int n) {
    return "0|1" + (n > 1 ? remainder(n).toRegex(1, 0) : "[01]*");
  }
}
___________________________________________________________
public class Solution {
    public String regexDivisibleBy(int n) {
        if (n==1)
            return "^[01]*$";
        String[][] graph = new String[n][n];
        for (int i = 0; i < n; i++) {
            graph[i][(2*i)%n] = "0";
            graph[i][(2*i+1)%n] = "1";
        }
        for (int k = n-1; k >= 0; k--) {
            String loop = graph[k][k]==null ? "" : graph[k][k]+"*";
            for (int i = 0; i < k; i++) {
                if (graph[i][k] != null) {
                    for (int j = 0; j < k; j++) {
                        if (graph[k][j] != null) {
                            String s = graph[i][j]==null ? "" : graph[i][j]+"|";
                            graph[i][j] = "(?:" + s + graph[i][k] + loop + graph[k][j] + ")";
                        }
                    }
                }
            }
        }
        return "^" + graph[0][0] + "*$";
    }
}
___________________________________________________________
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Map;
import java.util.HashMap;
import java.util.stream.IntStream;

public class Solution {
    
    public String regexDivisibleBy(int n) {
        
        Node[] nodArr = IntStream.range(0,n).mapToObj( i -> new Node(i) ).toArray(Node[]::new);
        for (int j = 0 ; j < n ; j++)
            nodArr[j].link(nodArr[(j*2)%n], nodArr[(j*2+1)%n]);
        
        return String.format("^%s$", getRegexFromGrahp(nodArr[0], "", new HashSet<Node>()).get(nodArr[0]).get(0));
    }
    
    private Map<Node,List<String>> getRegexFromGrahp(Node nod, String bit, Set<Node> seensInBranch) {
        
        Map<Node,List<String>> treeReg = new HashMap<Node,List<String>>();
        String reduced = "";
        
        if (!seensInBranch.contains(nod)) {
        
            for (int i = 0 ; i < 2 ; i++) {
                Set<Node> nextSeens = new HashSet<Node>(seensInBranch);
                nextSeens.add(nod);
                Map<Node,List<String>> dct = getRegexFromGrahp(nod.get(i), ""+i, nextSeens);
                for (Node child: dct.keySet()) {
                    treeReg.computeIfAbsent( child, v -> new ArrayList<String>() ).addAll(dct.get(child));
                }
            }
            
            if (treeReg.containsKey(nod)) {
                List<String> lstReg = treeReg.remove(nod);
                String sBit = String.join("|", lstReg);
                reduced = String.format(sBit.length() == 1 ? "%s*" : "(%s)*", sBit);
            }
            
            for (Node ext: treeReg.keySet()) {
                treeReg.put(ext, new ArrayList<String>(Arrays.asList( 
                                 bit + reduced + 
                                 String.format(treeReg.get(ext).size() == 1 ? "%s" : "(%s)",
                                               String.join("|", treeReg.get(ext)) ))));
            }
        }
        if (treeReg.isEmpty()) treeReg.put(nod, new ArrayList<String>(Arrays.asList(bit + reduced)));
        
        return treeReg;
    }
    
    
    static class Node {
        
        private int val;
        private Node[] next = new Node[2];
    
        Node(int val)                         { this.val = val; }
        protected void link(Node n0, Node n1) { next[0] = n0; next[1] = n1; }
        protected int val()                   { return val; }
        protected Node get(int i)             { return next[i]; }
        
        @Override public int hashCode()       { return val; }
        @Override public String toString()    { return "Node("+val+")"; }
        @Override public boolean equals(Object other) {
            if (other == null || !(other instanceof Node)) return false;
            return val == ((Node) other).val();
        }
    }
}
___________________________________________________________
import java.util.HashMap;
import java.util.ArrayList;


public class Solution {
    public String regexDivisibleBy(int n) {

        // Construct Equations representing the DFA
        HashMap<Integer, ArrayList<Equation>> eqs = new HashMap<>();
        for (int i = 0; i < n; i++)
            eqs.put(i, new ArrayList<>());
        for (int i = 0; i < n; i++) {
            eqs.get((i*2) % n).add(new Equation(i, "0"));
            eqs.get((i*2 + 1) % n).add(new Equation(i, "1"));
        }

        for (int toElim = n-1; toElim > 0; toElim--) {
            
            // Remove self references
            ArrayList<Equation> allSelf = new ArrayList<>();
            for (Equation t : eqs.get(toElim))
                if (t.pre == toElim) allSelf.add(t);
            if (allSelf.size() > 0) {
                HashMap<Integer, ArrayList<Equation>> allOther = Equation.groupedByPre(eqs.get(toElim));
                String star = "";
                if (allSelf.size() == 1 && allSelf.get(0).re.length() == 1) {
                    star = allSelf.get(0).re + "*";
                } else {
                    star = "(?:" + String.join("|", Equation.getAllRe(allSelf)) + ")*";
                }
                for (int k : allOther.keySet()) {
                    ArrayList<Equation> nodes = allOther.get(k);
                    String pre = "";
                    if (nodes.size() <= 1) {
                        pre = nodes.get(0).re;
                    } else {
                        pre = "(?:" + String.join("|", Equation.getAllRe(nodes)) + ")";
                    }
                    eqs.get(toElim).add(new Equation(k, pre + star));
                    for (Equation node : nodes)
                        eqs.get(toElim).remove(node);
                }
                final int toElimFinal = toElim;
                eqs.get(toElim).removeIf(t -> t.pre == toElimFinal);   
            }

            // Substitute into other equations
            for (int toSub = 0; toSub < toElim; toSub++) {
                for (Equation nOld : (ArrayList<Equation>) eqs.get(toSub).clone()) {
                    if (nOld.pre != toElim) continue;
                    for (Equation nSub : eqs.get(toElim))
                        eqs.get(toSub).add(new Equation(nSub.pre, nSub.re + nOld.re));
                    eqs.get(toSub).remove(nOld);
                }
                HashMap<Integer, ArrayList<Equation>> allNodes = Equation.groupedByPre(eqs.get(toSub));
                for (int k : allNodes.keySet()) {
                    ArrayList<Equation> nodes = allNodes.get(k);
                    if (allNodes.size() <= 1) continue;
                    String newRe = "(?:" + String.join("|", Equation.getAllRe(nodes)) + ")";
                    eqs.get(toSub).add(new Equation(k, newRe));
                    for (Equation node : nodes)
                        eqs.get(toSub).remove(node);
                }
            }

            eqs.remove(toElim);
        }

        return "^" + "(?:" + String.join("|", Equation.getAllRe(eqs.get(0))) + ")+$";

    }
}



class Equation {
    public int pre;
    public String re;

    public Equation(int p, String r) {
        pre = p;
        re = r;
    }

    public static ArrayList<String> getAllRe(ArrayList<Equation> equations) {
        ArrayList<String> allRe = new ArrayList<>();
        for (Equation t : equations)
            allRe.add(t.re);
        return allRe;
    }

    public static HashMap<Integer, ArrayList<Equation>> groupedByPre(ArrayList<Equation> equations) {
        HashMap<Integer, ArrayList<Equation>> grouped = new HashMap<>();
        for (Equation t : equations) {
            if (!grouped.containsKey(t.pre)) {
                grouped.put(t.pre, new ArrayList<>());
            }
            grouped.get(t.pre).add(t);
        }
        return grouped;
    }
}
___________________________________________________________
import java.util.*;
import java.util.function.Consumer;

public class Solution {
  public String regexDivisibleBy(int n) {
    return new DFA(n).toReg();
  }
}

class DFA {
  public final static String                  CHARS     = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
  public final static Map<Character, Integer> VALUE_MAP = new HashMap<>();
  private final       Node[]                  nodes;
  
  public DFA(int n) {
    this(2, n);
  }
  
  public DFA(int radix, int n) {
    if (radix > CHARS.length()) throw new RuntimeException(
        String.format("Radix should enough condition: 1 < radix < %s", CHARS.length() + 1));
    nodes = new Node[n];
    for (int i = 0; i < CHARS.length(); i++) VALUE_MAP.put(CHARS.charAt(i), i);
    for (int i = 0; i < n; i++) nodes[i] = new Node(Math.max(n, radix), i);
    for (int i = 0; i < n; i++)
      for (int j = 0; j < radix; j++) {
        int to = (i * radix + j) % n;
        StringBuilder stringBuilder = nodes[i].to[to] != null ?
                                      nodes[i].to[to].reg.append('|') :
                                      new StringBuilder();
        nodes[i].link(nodes[to], stringBuilder.append(CHARS.charAt(j)));
      }
  }
  
  public String toReg() {
    for (int i = nodes.length - 1; i > 0; i--) remove(i);
    return nodes[0].to[0].reg.insert(0, '(').append(")*").toString();
  }
  
  private void remove(int i) {
    Node node = nodes[i];
    for (Relation from : node.from)
      if (from != null && from.one != from.two)
        for (Relation to : node.to)
          if (to != null && to.one != to.two) relink(from, to, node);
  }
  
  private void relink(Relation from, Relation to, Node current) {
    Node          last     = from.one == current ? from.two : from.one;
    Node          next     = to.one == current ? to.two : to.one;
    Relation      relation = last.to[next.value];
    StringBuilder origin   = relation == null ? new StringBuilder() : new StringBuilder(relation.reg);
    StringBuilder self     = current.self == null ? new StringBuilder() : new StringBuilder(current.self);
    StringBuilder come     = new StringBuilder(from.reg), go = new StringBuilder(to.reg);
    if (isOr(come.toString())) come.insert(0, '(').append(')');
    if (isOr(go.toString())) go.insert(0, '(').append(')');
    if (self.length() > 1) self.insert(0, '(').append(')');
    if (self.length() > 0) self.append('*');
    come.append(self).append(go);
    if (origin.length() > 0) come.insert(0, '|').insert(0, origin);
    last.link(next, come);
    last.to[current.value]   = null;
    next.from[current.value] = null;
  }
  
  private static boolean isOr(String s) {
    String not = "[^(|)]", del = "\\(\\|\\)";
    return s.replaceAll(not, "").replaceAll(del, "").indexOf('|') != -1;
  }
  
  public static class Relation {
    private final StringBuilder reg;
    private final Node          one, two;
    
    public Relation(Node one, Node two, StringBuilder reg) {
      this.one = one;
      this.two = two;
      this.reg = reg;
    }
  }
  
  private static class Node {
    private final Relation[] to, from;
    private final int           value;
    private       StringBuilder self;
    
    private Node(int n, int val) {
      value = val;
      to    = new Relation[n];
      from  = new Relation[n];
    }
    
    private void link(Node next, StringBuilder reg) {
      Relation relation = new Relation(this, next, reg);
      to[next.value]   = relation;
      next.from[value] = relation;
      if (this == next) self = reg;
    }
  }
}
___________________________________________________________
ublic class Solution {
        private static String Plus(String s) {
          return !s.isEmpty() ? "(" + s + ")+" : s;
          }

        private static String Brackets(String s) {return !s.isEmpty() ? "(" + s + ")" : s;}

        private static String Asterisk(String s) {return !s.isEmpty() ? "(" + s + ")*" : s;}

        private static String Or(String s, String s1) {return !s.isEmpty() ? "(" + s + ")|(" + s1 + ")" : s1;}

        private static void SimplifyDfa(int n, String[][] dfa, int start, int finish)
        {
            for (int i = 0; i < n; ++i)
            {
                if (i == start || i == finish) continue;

                for (int j = 0; j < n; ++j)
                {
                    if (j == i || dfa[j][i] == "") continue;

                    for (int q = 0; q < n; ++q)
                    {
                        if (q == i || dfa[i][q] == "") continue;

                        dfa[j][q] = Or(dfa[j][q], Brackets(dfa[j][i]) + Asterisk(dfa[i][i]) + Brackets(dfa[i][q]));
                    }
                }

                for (int j = 0; j < n; ++j)
                {
                    dfa[i][j] = "";
                }
            }
        }

        private static String DfaToRegularExpression(int n, String[][] dfa, int start, int finish)
        {
            SimplifyDfa(n, dfa, start, finish);
            return start == finish ?
                    "^"+Plus(dfa[start][start])+"$" :
                    "not implemented";
        }

    public String regexDivisibleBy(int n) {
        int start = 0, finish = 0;
            String[][] dfa = new String[n][];
            for (int i = 0; i < n; ++i)
            {
              dfa[i] = new String[n];
                for (int j = 0; j < n; ++j)
                {
                    dfa[i][j] = "";
                }
                dfa[i][(i * 2) % n] = Or(dfa[i][(i * 2) % n], "0");
                dfa[i][(i * 2 + 1) % n] = Or(dfa[i][(i * 2 + 1) % n], "1");
            }

            return DfaToRegularExpression(n, dfa, start, finish);
    }
}
