solve([X, Y], [X, Y]).

solve([X, Y | T], [A, B]) :-
    solve(T, [U, V]),
    A is X * U + Y * V,
    B is abs(X * V - Y * U).
_____________________________________
solve1([X, Y, Z, T], R) :-
    E is abs(X * T - Y * Z),
    F is abs(X * Z + Y * T),
    G is abs(X * Z - Y * T),
    H is abs(X * T + Y * Z),
    (E =\= 0, F =\= 0 ->
        R = [E, F]
    ;
        R = [G, H]
    ), !.
solve1([X, Y, Z, T| Q], R) :-
    solve([X, Y, Z, T], S),
    append(S, Q, K),
    solve(K, R).

solve(Ls, R) :-
    [X, Y, Z, T| Q] = Ls,
    solve1([X, Y, Z, T| Q], R).
_____________________________________
aux(X, Y, [], R) :- X1 is abs(X), Y1 is abs(Y), R = [X1, Y1], !.
aux(X, Y, [A, B | Xs], R) :-
  X1 is X * A - Y * B,
  Y1 is X * B + Y * A,
  aux(X1, Y1, Xs, R).

solve(Xs, R) :- aux(1, 0, Xs, R).
_____________________________________
solve(Ls, R):- solve(Ls, [], R).
solve([], [A, B], [A1, B1]):- A1 is abs(A), B1 is abs(B), !.
solve([], [A, B, C, D | T], R):- solve([A, B, C, D | T], [], R).
solve([A, B], AR, R):- solve([], [A, B | AR], R).
solve([A, B, C, D | T], AR, R):- solve(T, [A*C + B*D, A*D - B*C | AR], R).
_____________________________________
solve([A,B], [A,B]).
solve([A,B,P,Q|Ls], R) :-
    step(A, B, P, Q, X, Y),
    solve([X,Y|Ls], R).

step(A, B, P, Q, X, Y) :-
    X is A * P + B * Q,
    Y is abs(A * Q - B * P).
