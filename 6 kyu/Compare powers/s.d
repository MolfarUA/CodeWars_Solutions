55b2549a781b5336c0000103


module solution;
import std.math;

export int comparePowers(const ulong[2] n1, const ulong[2] n2)
{
    alias f = n => n[1] * log(cast(double)n[0]);
    return cmp(f(n2), f(n1));
}
________________________________
module solution;


import std.math;

export int comparePowers(const ulong[2] n1, const ulong[2] n2)
{
    auto d = n1[1] * log(cast(double) n1[0]) - n2[1] * log(cast(double) n2[0]);
    return (d < 0) - (d > 0);
}
