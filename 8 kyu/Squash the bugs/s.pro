56f173a35b91399a05000cb7


find_longest(String, Result) :-
  split_string(String, " ", "", Words),
  maplist(string_length, Words, Lengths),
  max_list(Lengths, Result).
__________________________
find_longest(S, R) :-
  split_string(S, " ", "", W),
  maplist(string_length, W, LS),
  max_list(LS, R).
__________________________
find_longest(S, R) :-
  split_string(S, " ", "", W),
  maplist(string_length, W, L),
  max_list(L, R).
