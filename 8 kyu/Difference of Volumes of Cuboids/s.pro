58cb43f4256836ed95000f97


mult(X,Y,Z) :- Z is X * Y.

find_difference(A, B, Diff) :- 
  foldl(mult,A,1,R1),
  foldl(mult,B,1,R2),
  Diff is abs(R1-R2).
________________________
product(In1, In2, Out) :- Out is In1 * In2.

find_difference(A, B, Diff) :-
  foldl(product, A, 1, A_out),
  foldl(product, B, 1, B_out),
  Diff is abs(A_out - B_out).
________________________
prod(A, R) :- foldl([X, T, N] >> (N is X * T), A, 1, R).

find_difference(A, B, Diff) :- 
  prod(A, P1), prod(B, P2),
  Diff is abs(P1 - P2).
________________________
multiplyList([],1).
multiplyList([X|Y], S) :- multiplyList(Y,M), S is X * M. 

find_difference(A, B, Diff) :- multiplyList(A,R), multiplyList(B,R2),
  Diff is abs(R - R2).
