55f9bca8ecaa9eac7100004a


-module(kata).
-export([past/3]).

past(H, M, S) -> timer:hours(H) + timer:minutes(M) + timer:seconds(S).
__________________________
-module(kata).
-export([past/3]).

to_millis({seconds, Count}) -> 1000 * Count;
to_millis({minutes, Count}) -> to_millis({seconds, Count * 60});
to_millis({hours,   Count}) -> to_millis({minutes, Count * 60}).

past(H, M, S) -> 
  to_millis({hours,   H}) +
  to_millis({minutes, M}) +
  to_millis({seconds, S}).
__________________________
-module(kata).
-export([past/3]).

past(H, M, S) -> S * 1000 + M * 60000 + H * 3600000 .
__________________________
-module(kata).
-export([past/3]).

past(H, M, S) when H >= 0, H =< 23, M >= 0, M =< 59, S >= 0, S =< 59 ->
  ((H * 60 * 60) + (M * 60) + S) * 1000.
__________________________
-module(kata).
-export([past/3]).
-define(MILL_IN_SEC, 1000).
-define(MILL_IN_MIN, 60 * ?MILL_IN_SEC).
-define(MILL_IN_HOUR, 60 * ?MILL_IN_MIN).

past(H, M, S) ->
  H * ?MILL_IN_HOUR
  + M * ?MILL_IN_MIN
  + S * ?MILL_IN_SEC.
