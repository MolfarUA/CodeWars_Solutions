52f677797c461daaf7000740


module solution;

import std.algorithm : reduce;
import std.bigint : BigInt;
import std.numeric : gcd;

export BigInt solution(ulong[] arr) 
{
    return BigInt(arr.length) * arr.reduce!gcd;
}
_______________________________
module solution;

import std.bigint;
import std.numeric;

export BigInt solution(ulong[] arr) {
    ulong r = 0;
    for (int i=0; i<arr.length; i++) r = r.gcd(arr[i]);
    return BigInt(r) * BigInt(arr.length);
}
_______________________________
module solution;

import std.algorithm.iteration : fold, map;
import std.numeric : gcd;
import std.bigint;

export alias solution = a => BigInt(a.fold!(gcd)) * BigInt(a.length);
