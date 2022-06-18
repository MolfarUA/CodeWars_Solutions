56d0a591c6c8b466ca00118b


is_triangular(T, 1) :- ceiling(sqrt(8*T+1)) =:= sqrt(8*T+1).
is_triangular(_, 0).
__________________________
is_triangular(T, 1) :- float_fractional_part(sqrt(8 * T + 1)) =:= 0, !.
is_triangular(_, 0).
__________________________
% Return 1 if triangular, else 0
is_triangular(T, Result) :-
  is_it_triangular(T,Result,0).

is_it_triangular(N,R,C):-
  Temp is (C*(C+1)/2),
  (Temp>N)->
  Temp is C*(C+1)/2,
  R is 0;
  Temp is (C*(C+1)/2),
  (Temp=N)->
  R is 1;
  NextIndex is C+1,
  is_it_triangular(N,R,NextIndex).
__________________________
triangle(_, S, S).
triangle(X, S, F) :- 
  S < F, 
  X1 is X + 1, 
  S1 is S + X, 
  triangle(X1, S1, F).
is_triangular(T, R) :- 
  (triangle(1, 0, T) -> R is 1; R is 0).
__________________________
is_triangular(T, R) :- N is 8*T+1, nth_integer_root_and_remainder(2, N, _, 0), R=1 ; R=0.
__________________________
is_triangular(T, R) :- is_triangular_(T), !, R = 1.
is_triangular(_, 0).

is_triangular_(X) :-
  M is 8 * X + 1,
  nth_integer_root_and_remainder(2, M, _, Rem),
  Rem = 0.
__________________________
is_triangular(T, Result) :- 
  M is sqrt(8 * T + 1),
  N is truncate(M),
  ( M =:= N 
    -> Result is 1
     ; Result is 0 ).
