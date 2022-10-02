55c6126177c9441a570000cc


module solution;

import  std.array : split;
import  std.algorithm.sorting : multiSort;
import  std.algorithm.iteration : joiner, map, sum;
import  std.conv : to;

export string orderWeight(string s)
{
    alias digitSum = (x) => x.map!(d => cast(uint)(d - '0')).sum;
    return s.split
            .multiSort!((x, y) => digitSum(x) <  digitSum(y), (x, y) => x < y)
            .joiner(" ")
            .to!string;
}
_____________________________
module solution;

import std.algorithm;
import std.array;

int sumDig(string s) 
{
    int sum = 0;
    for(int i = 0; i < cast(int)s.length; i++) {
        sum += s[i] - '0';
    }
   return sum;
}
bool myComp(string a, string b)
{
    int cp = sumDig(a) - sumDig(b);
    if (cp == 0) 
        return a < b ? true : false;
    return cp < 0 ? true : false;
}
export string orderWeight(string s)
{
    string[] r = s.split(" ");
    return r.sort!((a, b) => myComp(a, b)).join(" ");
}
