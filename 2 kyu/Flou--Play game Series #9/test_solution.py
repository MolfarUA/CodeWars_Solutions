test.describe('Basic Tests')

i = 0

game_map = '''+----+
|B...|
|....|
|....|
|....|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|B...|
|....|
|....|
|...B|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|.B..|
|....|
|....|
|..B.|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|.BB.|
|....|
|....|
|....|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|B...|
|B...|
|....|
|....|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|B..B|
|....|
|....|
|.B..|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|....|
|B...|
|B...|
|...B|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|...B|
|B...|
|....|
|..B.|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|B..B|
|....|
|....|
|...B|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+----+
|....|
|...B|
|.B..|
|B...|
+----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|.....|
|....B|
|...B.|
|.....|
|....B|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|B....|
|.B...|
|.B...|
|.....|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|BB.BB|
|.....|
|.....|
|.....|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|..B..|
|.....|
|.....|
|..B..|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|...BB|
|.....|
|.....|
|B....|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|.....|
|.B.B.|
|.B...|
|.....|
|...B.|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|.....|
|B....|
|.B...|
|.B..B|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|.BB..|
|.....|
|.....|
|..BB.|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|.....|
|BB...|
|..B..|
|..B..|
|..B..|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+-----+
|...B.|
|.....|
|...B.|
|.BB..|
|.....|
+-----+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|B.....|
|......|
|.....B|
|..B...|
|......|
|.....B|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|..BB..|
|......|
|......|
|..BB..|
|......|
|......|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|......|
|......|
|....B.|
|.B....|
|......|
|B...B.|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|B.....|
|..B...|
|...B..|
|..B...|
|......|
|......|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|B.....|
|......|
|...B..|
|...B..|
|...B..|
|...B..|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|......|
|BB....|
|......|
|...B..|
|......|
|....BB|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|......|
|.B..B.|
|......|
|......|
|......|
|B.B..B|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|B.....|
|B.....|
|......|
|....B.|
|....B.|
|....B.|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|......|
|BBB...|
|......|
|......|
|..BB..|
|......|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|......|
|......|
|......|
|..B...|
|......|
|......|
+------+'''

check_solution(game_map, play_flou(game_map), i)
i += 1

game_map = '''+------+
|BB....|
|B.....|
|......|
|......|
|......|
|......|
+------+'''

check_solution(game_map, play_flou(game_map), i)

from random import randint

def rndtest(big):
    if big:
        h = randint(6,12)
        w = randint(6,12)
        n = randint(3,6)
    else:
        h = randint(4,7)
        w = randint(4,7)
        n = randint(1,3)
    map = [list('|'+w*'.'+'|') for _ in range(h)]
    for _ in range(n):
        map[randint(0,h-1)][randint(1,w-2)] = 'B'
    r = '+'+w*'-'+'+'
    return r+'\n'+'\n'.join([''.join(r) for r in map])+'\n'+r

print("<COMPLETEDIN::>")
print("<COMPLETEDIN::>")
test.describe('100 Random Tests')

for i in range(100):
    game_map = rndtest(50<i)
    check_solution(game_map, play_flou(game_map), i)
