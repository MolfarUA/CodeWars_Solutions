586beb5ba44cfc44ed0006c3


sum_even_numbers(Sequence, EvenSum) :-
  include([X] >> (float_fractional_part(X / 2) =:= 0), Sequence, Es),
  sum_list(Es, EvenSum).
_______________________________________
even(X) :- floor(X) =:= X, floor(X) mod 2 =:= 0.

sum_even_numbers(Sequence, EvenSum) :-
  aggregate_all(sum(X), (member(X, Sequence), even(X)), EvenSum).
_______________________________________
sum_even_numbers([X],X).
sum_even_numbers(Xs, R) :-
  aggregate_all(sum(X), (member(X,Xs), X=:=integer(X), 0 is integer(X)/\1), R).
_______________________________________
sum_even_numbers(L, Sum) :- 
  include(even, L, L1),
  sum_list(L1, Sum).
even(X) :-
  0 =:= float_fractional_part(X / 2).
