59eb1e4a0863c7ff7e000008


import java.util.*;
import java.math.BigInteger;

public class BooleanOrder {
    
    private Map<String,BigInteger[]> memo = new HashMap<>();
    private String s, ops;
        
    protected BooleanOrder(final String operands, final String operators) {
        s   = operands;
        ops = operators;
    }
    
    public BigInteger solve() { return evaluate(s, ops)[1]; }
    
    
    private BigInteger[] evaluate(String s, String ops) {
        
        String keyMemo = s+ops;
        if (memo.containsKey(keyMemo)) return memo.get(keyMemo);
            
        BigInteger[] c = {BigInteger.ZERO, BigInteger.ZERO};
        if (ops.isEmpty()) {
            int idx = s.equals("t") ? 1 : 0;
            c[idx]  = c[idx].add(BigInteger.ONE);
            
        } else {
            int n = 0, m = 0;
            for (int i = 0 ; i < ops.length() ; i++) { n = -1;
                for (BigInteger v:     evaluate(s.substring(0,i+1), ops.substring(0,i)) ) { n++; m = -1;
                    for (BigInteger w: evaluate(s.substring(i+1),   ops.substring(i+1)) ) { m++;
                        int idx = apply(ops.charAt(i), n, m);
                        c[idx]  = c[idx].add( v.multiply(w) );
                    }
                }
            }
        }
        memo.put(keyMemo, c);
        return c;
    }
    
    private int apply(char op, int n, int m) {
        boolean a = n==1, b = m==1;
        return (  op == '|' ? a || b
                : op == '&' ? a && b
                :             a ^  b ) ? 1 : 0;
    }
}
_________________________________________
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;

public class BooleanOrder {
  private static final List<BigInteger> catalans = new ArrayList<>();
  static {
    catalans.add(BigInteger.ONE);
  }

  private static BigInteger catalan(int n) {
    int s = catalans.size();
    while (s <= n) {
      BigInteger sum = BigInteger.ZERO;
      for (int i = 0; i < s; i++)
        sum = sum.add(catalans.get(i).multiply(catalans.get(s - 1 - i)));
      catalans.add(sum);
      s++;
    }
    return catalans.get(n);
  }

  private static boolean[] parseOperands(String operands) {
    boolean[] result = new boolean[operands.length()];
    int i = 0;
    for (char c : operands.toCharArray())
      switch (c) {
        case 't':
          result[i] = true;
        case 'f':
          i++;
          break;
        default:
          throw new IllegalArgumentException("Wrong operand: " + c);
      }
    return result;
  }

  public enum Operator {
    AND, OR, XOR
  };

  private static Operator[] parseOperators(String operators) {
    Operator[] result = new Operator[operators.length()];
    int i = 0;
    for (char c : operators.toCharArray())
      switch (c) {
        case '&':
          result[i++] = Operator.AND;
          break;
        case '|':
          result[i++] = Operator.OR;
          break;
        case '^':
          result[i++] = Operator.XOR;
          break;
        default:
          throw new IllegalArgumentException("Wrong operator: " + c);
      }
    return result;
  }

  private final boolean[] operands;
  private final Operator[] operators;
  private final int n; // total number of operands
  /* count[b][s] counts arrangements of s operators on substring 
   * from index b (inclusive) to index e (exclusive) that evaluate to true.
   * Here s = e - b - 1, 0 <= b < e <= n,  0 <= s + b <= n - 1 */
  private final BigInteger[][] count;

  public BooleanOrder(final String operands, final String operators) {
    n = operands.length();
    if (operators.length() + 1 != n)
      throw new IllegalArgumentException("Too many operands");
    this.operands = parseOperands(operands);
    this.operators = parseOperators(operators);
    count = new BigInteger[n][];
    for (int b = 0; b < n; b++)
      count[b] = new BigInteger[n - b]; // 0 <= s < n - b
  }

  private static BigInteger totalCount(int b, int e) {
    return catalan(e - b - 1);
  }

  private BigInteger trueCount(int b, int e) {
    return count[b][e - b - 1];
  }

  private BigInteger falseCount(int b, int e) {
    return totalCount(b, e).subtract(trueCount(b, e));
  }

  public BigInteger solve() {
    for (int b = 0; b < n; b++)
      count[b][0] = operands[b] ? BigInteger.ONE : BigInteger.ZERO;
    for (int s = 1; s < n; s++)
      for (int b = 0; b < n - s; b++) {
        int e = b + s + 1;
        BigInteger sum = BigInteger.ZERO;
        for (int m = b + 1; m < e; m++) // beginning of second substring
          switch (operators[m - 1]) {
            case AND:
              sum = sum.add(trueCount(b, m).multiply(trueCount(m, e)));
              break;
            case OR:
              sum = sum.add(falseCount(b, m).multiply(trueCount(m, e)));
              sum = sum.add(trueCount(b, m).multiply(totalCount(m, e)));
              break;
            case XOR:
              sum = sum.add(falseCount(b, m).multiply(trueCount(m, e)));
              sum = sum.add(trueCount(b, m).multiply(falseCount(m, e)));
              break;
          }
        count[b][s] = sum;
      }
    return trueCount(0, n);
  }
}
_________________________________________
import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

/*
  dmtdlm - 08.08.2020
*/
public class BooleanOrder
{
    BigInteger result;

    Map<String, SubRes> cache = new HashMap<>();

    public BooleanOrder(String operands, String operators)
    {
        result = solve(operands, operators).t;
    }

    private static class SubRes
    {
        BigInteger t;
        BigInteger f;

        public SubRes(BigInteger t, BigInteger f)
        {
            this.t = t;
            this.f = f;
        }

        void addT(BigInteger v1, BigInteger v2)
        {
            t = t.add(v1.multiply(v2));
        }

        void addF(BigInteger v1, BigInteger v2)
        {
            f = f.add(v1.multiply(v2));
        }
    }

    private SubRes solve(String values, String ops)
    {
        if (values.length() == 1)
        {
            return values.equals("t") ?
                    new SubRes(BigInteger.ONE, BigInteger.ZERO) :
                    new SubRes(BigInteger.ZERO, BigInteger.ONE);
        }

        // optimization
        String key = values + ops;
        SubRes res = cache.get(key);
        if (res != null)
            return res;

        res = new SubRes(BigInteger.ZERO, BigInteger.ZERO);
        for (int i = 0; i < ops.length(); i++)
        {
            char operator = ops.charAt(i);
            String av = values.substring(0, i + 1);
            String bv = values.substring(i + 1);
            String ao = ops.substring(0, i);
            String bo = ops.substring(i + 1);

            SubRes a = solve(av, ao);
            SubRes b = solve(bv, bo);

            if (operator == '&')
            {
                res.addF(a.f, b.f);
                res.addF(a.f, b.t);
                res.addF(a.t, b.f);
                res.addT(a.t, b.t);
            }
            else if (operator == '|')
            {
                res.addF(a.f, b.f);
                res.addT(a.f, b.t);
                res.addT(a.t, b.f);
                res.addT(a.t, b.t);
            }
            else if (operator == '^')
            {
                res.addF(a.f, b.f);
                res.addT(a.f, b.t);
                res.addT(a.t, b.f);
                res.addF(a.t, b.t);
            }
        }

        cache.put(key, res);

        return res;
    }

    public BigInteger solve() {
        // Your code here
        return result;
    }
}
_________________________________________
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class BooleanOrder {
    private final String operands;
    private final String operators;
    private final List<List<BigInteger>> trues;
    private final List<List<BigInteger>> falses;

    public BooleanOrder(final String operands, final String operators) {
        this.operands = operands;
        this.operators = operators;
        trues = IntStream.generate(operands::length)
                .limit(operands.length())
                .mapToObj(i -> new ArrayList<>(Collections.nCopies(i, BigInteger.ZERO)))
                .collect(Collectors.toList());
        falses = IntStream.generate(operands::length)
                .limit(operands.length())
                .mapToObj(i -> new ArrayList<>(Collections.nCopies(i, BigInteger.ZERO)))
                .collect(Collectors.toList());
    }

    public BigInteger solve() {
        IntStream.range(0, operands.length())
                .forEach(i -> {
                    falses.get(i).set(i, operands.charAt(i) == 'f' ? BigInteger.ONE : BigInteger.ZERO);
                    trues.get(i).set(i, operands.charAt(i) == 't' ? BigInteger.ONE : BigInteger.ZERO);
                });

        IntStream.range(1, operands.length())
                .forEach(subsequenceLen -> IntStream.range(0, operands.length() - subsequenceLen)
                        .forEach(i -> {
                            int j = i + subsequenceLen;
                            IntStream.range(i, j)
                                    .forEach(k -> {
                                        solveSubproblem(i, j, k);
                                    });
                        }));
        return trues.get(0).get(operands.length() - 1);
    }

    public void solveSubproblem(int i, int j, int k) {
        BigInteger totalFront = trues.get(i).get(k).add(falses.get(i).get(k));
        BigInteger totalRear = trues.get(k + 1).get(j).add(falses.get(k + 1).get(j));
        switch (operators.charAt(k)) {
            case '&':
                trues.get(i).set(j, trues.get(i).get(j).add(
                        trues.get(i).get(k).multiply(trues.get(k + 1).get(j))
                ));
                falses.get(i).set(j, falses.get(i).get(j).add(
                        totalFront.multiply(totalRear).subtract(
                                trues.get(i).get(k).multiply(trues.get(k + 1).get(j))
                        )
                ));
                break;
            case '|':
                falses.get(i).set(j, falses.get(i).get(j).add(
                        falses.get(i).get(k).multiply(falses.get(k + 1).get(j))
                ));
                trues.get(i).set(j, trues.get(i).get(j).add(
                        totalFront.multiply(totalRear).subtract(
                                falses.get(i).get(k).multiply(falses.get(k + 1).get(j))
                        )
                ));
                break;
            case '^':
                trues.get(i).set(j, trues.get(i).get(j).add(
                        falses.get(i).get(k).multiply(trues.get(k + 1).get(j)).add(
                                trues.get(i).get(k).multiply(falses.get(k + 1).get(j))
                        )
                ));
                falses.get(i).set(j, falses.get(i).get(j).add(
                        trues.get(i).get(k).multiply(trues.get(k + 1).get(j)).add(
                                falses.get(i).get(k).multiply(falses.get(k + 1).get(j))
                        )
                ));
                break;
        }
    }
}
