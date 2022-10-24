54f8693ea58bce689100065f


using System;
using System.Collections.Generic;
using System.Linq;

public class Decomp
{

    public static string Decompose(string nrStr, string drStr)
    {
        // parse input fraction
        var inputFraction = new Fraction(nrStr, drStr);
        //decompose fraction
        var reducedFractions = inputFraction.Decompose();
        //build result string
        var result = "["; 
        result += reducedFractions.Count > 0 ? reducedFractions.Aggregate("", 
                (current, fractionPart) => current + $"{fractionPart}, ") : "  ";
        result = result.Substring(0, result.Length - 2) + "]";

        return result;
    }

}

/// <summary>
/// Represents a rational number.
/// </summary>
public class Fraction
{
    public long Numerator { get; }
    public long Denominator { get; }

    public Fraction(long numerator, long denominator)
    {
        Numerator = numerator;
        Denominator = denominator;
    }

    public Fraction(string numerator, string denominator)
        : this(long.Parse(numerator), long.Parse(denominator))
    {
    }

    protected bool Equals(Fraction other)
    {
        return Numerator == other.Numerator && Denominator == other.Denominator;
    }

    public override bool Equals(object obj)
    {
        if (ReferenceEquals(null, obj)) return false;
        if (ReferenceEquals(this, obj)) return true;
        if (obj.GetType() != this.GetType()) return false;
        return Equals((Fraction) obj);
    }

    public override int GetHashCode()
    {
        unchecked
        {
            return (Numerator.GetHashCode() * 397) ^ Denominator.GetHashCode();
        }
    }

    public override string ToString()
    {
        return Denominator == 1 ? $"{Numerator}" : $"{Numerator}/{Denominator}";
    }

    /// <summary>
    /// Decomposes this fraction into parts.
    /// </summary>
    /// <returns></returns>
    public List<Fraction> Decompose()
    {
        return Decompose(this);
    }

    public static List<Fraction> Decompose(Fraction fraction)
    {
        var result = new List<Fraction>();
        if (fraction.Numerator == 0 || fraction.Denominator == 0)
            return result;
        //in case of a whole number
        if (fraction.Numerator % fraction.Denominator == 0)
        {
            result.Add(new Fraction(fraction.Numerator/fraction.Denominator, 1));
            return result;
        }
        //calculate all resulting fractions
        do
        {
            var reducedFractions = ReduceStep(fraction);
            if (reducedFractions.Item1.Numerator > 0)
                result.Add(reducedFractions.Item1);
            fraction = reducedFractions.Item2;
        } while (fraction != null);


        return result;
    }

    private static Tuple<Fraction, Fraction> ReduceStep(Fraction fraction)
    {
        if (fraction.Numerator == 0L)
            return new Tuple<Fraction, Fraction>(fraction, null);
        //first fraction
        var resultFraction = new Fraction(1L, DivideWithCeiling(fraction.Denominator, fraction.Numerator));
        if (fraction.Equals(resultFraction))
            return new Tuple<Fraction, Fraction>(resultFraction, null);
        //second fraction
        var numerator = -1L * fraction.Denominator % fraction.Numerator;
        if (numerator < 0)
            numerator += fraction.Numerator;
        var remainderFraction = new Fraction(
            numerator, 
            fraction.Denominator * DivideWithCeiling(fraction.Denominator, fraction.Numerator)
            );
        return new Tuple<Fraction, Fraction>(resultFraction, remainderFraction);
    }

    private static long DivideWithCeiling(long dividend, long divisor)
    {
        var quotient = dividend / divisor;
        var ceiling = dividend % divisor != 0 ? 1 : 0;
        var result = quotient + ceiling;
        return result;
    }
}
_________________________________
using System;
using System.Collections.Generic;

public class Decomp 
{
    public static string Decompose(string nrStr, string drStr) 
    {
        var ans = new List<String>();
        var a = Convert.ToInt64(nrStr);
        var b = Convert.ToInt64(drStr);
        while (a >= b) 
        {
            ans.Add($"{a / b}");
            a %= b;
        }
        while (a > 0) 
        {
            var d = Convert.ToInt64(Math.Ceiling((double)b / a));
            ans.Add($"1/{d}");
            a = a * d - b;
            b *= d;
        }
        return $"[{string.Join(", ", ans)}]";
    }
}
