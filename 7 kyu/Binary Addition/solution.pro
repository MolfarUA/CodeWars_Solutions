binary(0, "0").
binary(1, "1").
binary(N, B) :-
    N > 1,
    L is mod(N, 2), U is div(N, 2),
    binary(L, BL), binary(U, BU),
    string_concat(BU, BL, B).


add_binary(A, B, Binary) :- C is A + B, binary(C, Binary).
__________________________________
convert(0,V,_,V).
convert(N,V,C,Val):-
    Remainder is N mod 2,
    N1 is N//2,
    V1 is V + Remainder*(10^C),
    C1 is C + 1,
    convert(N1,V1,C1,Val).

convert(D,B):-
    D > -1,
    convert(D,0,0,B), !.

add_binary(N,V,B):-
  S is N+V,
  convert(S,BR),
  number_string(BR,B).
 __________________________________
 bin(0, [0]) :- !.
bin(1, [1]) :- !.
bin(N, [X | Xs]) :- divmod(N, 2, N1, X), bin(N1, Xs).

add_binary(A, B, Binary) :-
  S is A + B,
  bin(S, Bin),
  reverse(Bin, Bin2),
  maplist(number_string, Bin2, Bin3),
  atomics_to_string(Bin3, Binary).
__________________________________
add_binary(A, B, Binary) :-
  C is A+B,
  bitify(C, Atoms),
  atomics_to_string(Atoms, Binary).

bitify(N, Out) :-
  Msb is msb(N),
  findall(Bit, (between(0,Msb,I), Bit is getbit(N, I)), Bits),
  reverse(Bits, Out).
__________________________________
add_binary(A, B, Binary) :-
  Sum is A + B,
  format(string(Binary), '~2r', Sum).
__________________________________
dec_bin(0,"0").
dec_bin(1,"1").
dec_bin(N,B):-N>1,X is N mod 2,Y is N//2,dec_bin(Y,B1),atom_concat(B1, X, B).

add_binary(A, B, Binary) :-
  C is A + B,
  dec_bin(C, R),
  atom_string(R, Binary).
