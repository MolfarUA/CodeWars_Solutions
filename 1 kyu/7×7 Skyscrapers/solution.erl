-module(skyscrapers).
-export([solvePuzzle/1]).

-record(perm, { idx, values, packed }).


factorial(Number) ->
    Fac = fun
        Fac(N, Acc) when N =< 1 -> Acc;
        Fac(N, Acc) -> Fac(N - 1, Acc * N)
    end,
    Fac(Number, 1).

allPermutations(PUZZLESIZE) ->
    Permute = fun
        Permute([]) -> [[]];
        Permute(L) -> [[H|T] || H <- L, T <- Permute(L--[H])]
    end,

    PackValues = fun(P) -> lists:map(fun(V) -> 1 bsl V end, P) end,

    array:fix(
        array:map(
            fun(Idx, P) ->
                #perm { idx = Idx, values = array:fix(array:from_list(P)), packed = array:fix(array:from_list(PackValues(P))) }
            end,
            array:from_list(Permute(lists:seq(1, PUZZLESIZE)))
        )
    ).

solvePuzzle(Clues) ->
    PUZZLESIZE = 7,
    ROWINDEXES = lists:seq(0, PUZZLESIZE - 1),
    ALLPERMUTATIONS = allPermutations(PUZZLESIZE),
    NUMROWPERMUTATIONS = factorial(PUZZLESIZE),
    ALLPERMUTATIONINDEXES = lists:seq(0, NUMROWPERMUTATIONS-1),

    RowFromClues = fun
        (0, 0) -> ALLPERMUTATIONINDEXES;
        (L, R) ->
            Visible = fun
                (_, 0, 0) -> true;
                (Row, ClueLeft, ClueRight) ->
                   V = fun
                        V(Idx, _, _, CountLeft, CountRight) when Idx < 0 -> { CountLeft, CountRight };
                        V(Idx, MaxLeft, MaxRight, CountLeft, CountRight) ->
                            ValueLeft = array:get(PUZZLESIZE - Idx - 1, Row),
                            ValueRight = array:get(Idx, Row),
                            V(
                                Idx-1,
                                max(MaxLeft, ValueLeft),
                                max(MaxRight, ValueRight),
                                if ValueLeft > MaxLeft -> CountLeft + 1; true -> CountLeft end,
                                if ValueRight > MaxRight -> CountRight + 1; true -> CountRight end
                            )
                    end,

                    { ResultL, ResultR } = V(PUZZLESIZE - 1, 0, 0, 0, 0),
                    ((ClueLeft == 0) or (ClueLeft == ResultL)) and ((ClueRight == 0) or (ClueRight == ResultR))
            end,

            lists:filter(
                fun(Idx) -> Visible((array:get(Idx, ALLPERMUTATIONS))#perm.values, L, R) end,
                ALLPERMUTATIONINDEXES
            )
    end,

    IntersectAllRows = fun
        (PossibleSolution) ->
            IntersectRows = fun
                ({X, Y}, Sol) ->
                    RY = maps:get(Y, Sol),
                    RX = maps:get(PUZZLESIZE + X, Sol),
                    VMASK = lists:foldl(
                        fun(Idx, Acc) -> Acc bor (array:get(X, (array:get(Idx, ALLPERMUTATIONS))#perm.packed)) end,
                        0,
                        RY
                    ) band lists:foldl(
                        fun(Idx, Acc) -> Acc bor (array:get(Y, (array:get(Idx, ALLPERMUTATIONS))#perm.packed)) end,
                        0,
                        RX
                    ),
                    S1 = maps:update(
                        Y,
                        lists:filter(
                            fun(Idx) -> (array:get(X, (array:get(Idx, ALLPERMUTATIONS))#perm.packed) band VMASK) /= 0 end,
                            RY
                        ),
                        Sol
                    ),
                    maps:update(
                        PUZZLESIZE + X,
                        lists:filter(
                            fun(Idx) -> (array:get(Y, (array:get(Idx, ALLPERMUTATIONS))#perm.packed) band VMASK) /= 0 end,
                            RX
                        ),
                        S1
                    )
            end,

            lists:foldl(
                IntersectRows,
                PossibleSolution,
                lists:flatten(
                    lists:map(
                        fun(X) ->
                            lists:map(
                                fun(Y) -> { X, Y } end,
                                ROWINDEXES
                            )
                        end,
                        ROWINDEXES
                    )
                )
            )
    end,

    FindSolution = fun
        FindSolution(Sol) ->
            NewSol = IntersectAllRows(Sol),
            AnyUnsolvableRows = maps:fold(
                fun(_, V, Acc) -> Acc or (length(V) == 0) end,
                false,
                NewSol
            ),
            if
                AnyUnsolvableRows -> undefined;
                true ->
                    UndeterminedRowIndexes = lists:filter(
                        fun(K) ->
                            V = maps:get(K, NewSol),
                            case V of
                                [_] -> false;
                                _ -> true
                            end
                        end,
                        maps:keys(NewSol)
                    ),
                    case UndeterminedRowIndexes of
                        [] -> NewSol;
                        [FirstUndeterminedRowIdx|_] ->
                            Row = maps:get(FirstUndeterminedRowIdx, NewSol),
                            TryEachPossibility = fun
                                TryEachPossibility([]) -> undefined;
                                TryEachPossibility([Ridx|T]) ->
                                    TryThisSolution = maps:update(
                                        FirstUndeterminedRowIdx,
                                        [Ridx],
                                        NewSol
                                    ),
                                    DidItWork = FindSolution(TryThisSolution),
                                    case DidItWork of
                                        undefined -> TryEachPossibility(T);
                                        _ -> DidItWork
                                    end
                            end,
                            TryEachPossibility(Row)
                    end
            end
    end,

    CluesArr = array:from_list(Clues),
    InitialState =
        maps:from_list(
            lists:append(
                lists:map(
                    fun(Idx) -> { Idx, RowFromClues(array:get(PUZZLESIZE * 4 - Idx - 1, CluesArr), array:get(Idx + PUZZLESIZE, CluesArr)) } end,
                    ROWINDEXES
                ),
                lists:map(
                    fun(Idx) -> { Idx + PUZZLESIZE, RowFromClues(array:get(Idx, CluesArr), array:get(PUZZLESIZE * 3 - Idx - 1, CluesArr)) } end,
                    ROWINDEXES
                )
            )
        ),

    case FindSolution(InitialState) of
        undefined -> undefined;
        Solved ->
            lists:map(
                fun(RIdx) ->
                    [PIdx|_] = maps:get(RIdx, Solved),
                    array:to_list((array:get(PIdx, ALLPERMUTATIONS))#perm.values)
                end,
                ROWINDEXES
            )
    end.
