55f9b48403f6b87a7c0000bd


paperwork(N, M, NM) :- N > 0, M > 0, NM is N * M, !.
paperwork(_, _, 0).
__________________________
paperwork(N, M, Result) :-
  N >= 0,
  M >= 0,
  Result is N*M;
  Result is 0.
__________________________
paperwork(N, M, 0):-
  N<0, !.
  
paperwork(N, M, 0):-
  M<0, !.
  
paperwork(N, M, Result):-
  Result is N*M.
__________________________
paperwork(N, M, 0) :- (N<0 ; M<0), !.
paperwork(N, M, Result) :- Result is N*M.
__________________________
paperwork(N, M, Result) :-
  (N<0;M<0),
  Result = 0.
paperwork(N, M, Result) :-
  Result is N*M.
__________________________
paperwork(N, M, Result) :- N < 0, Result is 0, !.
paperwork(N, M, Result) :- M < 0, Result is 0, !.
paperwork(N, M, Result) :- Result is N*M.
