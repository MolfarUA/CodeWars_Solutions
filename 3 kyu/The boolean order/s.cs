59eb1e4a0863c7ff7e000008


using System;
using System.Numerics;
    public class BooleanOrder
    {
        int length; readonly bool[] values; readonly char[] op;
        public BooleanOrder(string operands, string operators)
        {
            (length, values, op) = (operands.Length, new bool[operands.Length], new char[operands.Length - 1]);
            for (int a = 0; a < length; a++)
                values[a] = operands[a] == 't';
            for (int a = 0; a + 1 < length; a++)
                op[a] = operators[a];
        }
        public BigInteger Solve()
        {
            BigInteger[,] F = new BigInteger[length, length], T = new BigInteger[length, length];
            for (int i = 0; i < length; i++)
                (T[i, i], F[i, i]) = values[i] ? (1, 0) : (0, 1);
            for (int a = 1; a < length; ++a)
                for (int b = 0, c = a; c < length; ++b, ++c)
                    for (int d = b; d < a + b; ++d)
                        switch (op[d])
                        {
                            case '&':
                                T[b, c] += T[b, d] * T[d + 1, c];
                                F[b, c] += (T[b, d] + F[b, d]) * (T[d + 1, c] + F[d + 1, c]) - T[b, d] * T[d + 1, c];
                                break;
                            case '|':
                                F[b, c] += F[b, d] * F[d + 1, c];
                                T[b, c] += (T[b, d] + F[b, d]) * (T[d + 1, c] + F[d + 1, c]) - F[b, d] * F[d + 1, c];
                                break;
                            default:
                                T[b, c] += F[b, d] * T[d + 1, c] + T[b, d] * F[d + 1, c];
                                F[b, c] += T[b, d] * T[d + 1, c] + F[b, d] * F[d + 1, c];
                                break;
                        }
            return T[0, --length];
        }
    }
_________________________________________
using System;
using System.Numerics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public class BooleanOrder
{
   
   public static BigInteger AllComb(int n)
   {
     BigInteger[] count = new BigInteger[n + 1];
     count[0] = 1;
     count[1] = 1;
     
     for (int i = 2; i <= n - 1; i++)
     {
       for (int j = 0; j < i; j++)
       {
         count[i] += count[j] * count[i - j - 1];
       }
     }
     
     return count[n - 1];
   }
  
   private static BigInteger HowManyTrues(char operation, BigInteger leftTrues, int leftLength, BigInteger rightTrues, int rightLength)
    {
        BigInteger leftAll = AllComb(leftLength);
        BigInteger rightAll = AllComb(rightLength);
        BigInteger count = 0;

        switch (operation)
        {
            case '|':
                count = leftTrues * rightAll + rightTrues * leftAll - leftTrues * rightTrues;
                break;
            case '^':
                count = leftTrues * (rightAll - rightTrues) + rightTrues * (leftAll - leftTrues);
                break;
            case '&':
                count = leftTrues * rightTrues;
                break;
        }
        return count;
    }

    public static BigInteger sumCounts(BigInteger[,] counts, int pos)
    {
        BigInteger count = 0;
        for (int i = (pos - 1) * pos / 2; i < pos * (pos + 1) / 2; i++) count += counts[i, 2];

        return count;
    }

    public static BigInteger BoolOrderSolve(string operands, string operators)
    {

        // Your code here
        BigInteger[,] counts = new BigInteger[operators.Length * (operators.Length + 1) / 2, 3];
        string[] trues = new string[6] { "t|t", "t|f", "f|t", "t&t", "t^f", "f^t" };

        if (operands[0] == 't') counts[0, 0] = 1;
        if (operands[1] == 't') counts[0, 1] = 1;
        string firstCheck = operands[0].ToString() + operators[0].ToString() + operands[1].ToString();
        if (trues.Contains(firstCheck)) counts[0, 2] = 1;

        for (int i = 1; i < operators.Length; i++)
        {
            counts[(i + 1) * (i + 2) / 2 - 1, 0] = sumCounts(counts, i);
            counts[(i + 1) * (i + 2) / 2 - 1, 1] = operands[i + 1] == 't' ? 1 : 0;
            counts[(i + 1) * (i + 2) / 2 - 1, 2] = HowManyTrues(operators[i], counts[(i + 1) * (i + 2) / 2 - 1, 0], i + 1, counts[(i + 1) * (i + 2) / 2 - 1, 1], 1); 

            for (int j = i - 1; j >= 0; j--)
            {
                counts[i * (i + 1) / 2 + j, 0] = counts[(i - 1) * i / 2 + j, 0];
                counts[i * (i + 1) / 2 + j, 1] += HowManyTrues(operators[i], counts[(i - 1) * i / 2 + j, 1], i - j, counts[(i + 1) * (i + 2) / 2 - 1, 1], 1);
                for (int rightCounter = i - 1; rightCounter >= j + 1; rightCounter--)
                {
                    counts[i * (i + 1) / 2 + j, 1] += HowManyTrues(operators[rightCounter], counts[(rightCounter - 1) * rightCounter / 2 + j, 1], rightCounter - j, counts[i * (i + 1) / 2 + rightCounter, 1], i + 1 - rightCounter);
                }
                counts[i * (i + 1) / 2 + j, 2] = HowManyTrues(operators[j], counts[i * (i + 1) / 2 + j, 0], j + 1, counts[i * (i + 1) / 2 + j, 1], i - j + 1);
            }
        }

        BigInteger final = 0;
        for (int k = operators.Length * (operators.Length + 1) / 2 - 1; k > operators.Length * (operators.Length - 1) / 2 - 1; k--) final += counts[k, 2];

        return final;
    }
   
   string operands;
   string operators;
   
   public BooleanOrder(string operands, string operators)
   {
     this.operands = operands;
     this.operators = operators;
       // Your code here
   }

   public BigInteger Solve()
   {
     
       // Your code here
     
       return BoolOrderSolve(operands, operators);
   }
}
_________________________________________
using System.Collections.Generic;
using bi = System.Numerics.BigInteger;

public class BooleanOrder
{
    static Dictionary<string, bi> TCache = new Dictionary<string, bi>();
    static Dictionary<string, bi> FCache = new Dictionary<string, bi>();
    string input;

    public BooleanOrder(string operands, string operators)
    {
        var e = new char[operands.Length + operators.Length];
        for (int i = 0; i < operands.Length; i++) e[2 * i] = operands[i];
        for (int i = 0; i < operators.Length; i++) e[2 * i + 1] = operators[i];
        input = new string(e);
    }

    public bi Solve() => T(input);

    static bi T(string e)
    {
        if (e.Length == 1) return e[0] == 't' ? 1 : 0;
        if (TCache.TryGetValue(e, out var v)) return v;

        var trues = bi.Zero;
        for (int i = 1; i < e.Length; i += 2)
        {
            string l = e[..i], r = e[(i + 1)..];
            if (e[i] == '|') trues += T(l) * F(r) + F(l) * T(r) + T(l) * T(r);
            if (e[i] == '^') trues += T(l) * F(r) + F(l) * T(r);
            if (e[i] == '&') trues += T(l) * T(r);
        }
        return TCache[e] = trues;
    }

    static bi F(string e)
    {
        if (e.Length == 1) return e[0] == 'f' ? 1 : 0;
        if (FCache.TryGetValue(e, out var v)) return v;

        var falses = bi.Zero;
        for (int i = 1; i < e.Length; i += 2)
        {
            string l = e[..i], r = e[(i + 1)..];
            if (e[i] == '|') falses += F(l) * F(r);
            if (e[i] == '^') falses += T(l) * T(r) + F(l) * F(r);
            if (e[i] == '&') falses += T(l) * F(r) + F(l) * T(r) + F(l) * F(r);
        }
        return FCache[e] = falses;
    }
}
