55df87b23ed27f40b90001e5


module solution;

export string calculateSpecial(ubyte p, ubyte b) {
    auto alpha = "0123456789abcdef";
    auto res = "";
    uint m = p, n = cast(uint)(p * b - 1), d = 0;
    while (m != p || d != p) {
        m *= b;
        d = m / n;
        m %= n;
        res = res ~ alpha[d];
    }
    return res;
}
____________________________
module solution;

export string calculateSpecial(ubyte lastDigit, ubyte base) 
{
    string alpha = "0123456789abcdef", result;
    int dividend = cast(int)lastDigit, divisor = cast(int)lastDigit * cast(int)base - 1, digit = 0;
    while (digit != lastDigit || dividend != lastDigit) {
        dividend *= cast(int)base;
        digit = dividend / divisor;
        dividend %= divisor;
        result ~= alpha[digit];
    }
    return result;
}
