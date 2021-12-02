from itertools import chain
    
def plants_and_zombies(lawn, zProvider):
    
    DEBUG = False
    X, Y  = len(lawn), len(lawn[0])
    
    class Stuff(object):                                                          # Shooters and Zombies instances
        def __init__(self, x, y, typ, h=0):
            self.x, self.y = x, y
            self.isS  = typ == 'S'
            self.fire = int(typ) if typ not in 'SZ' else 1
            self.h    = h
        
        def __str__(self):       return 'S' if self.isS else str(self.h) if self.h else chr(self.fire+64)
        def __repr__(self):      return "({},{})".format(self.x, self.y)
        def __bool__(self):      return bool(self.h)                              # Behave as "isZomby()"
        def __eq__(self, other): return self.x == other.x and self.y == other.y
        def __hash__(self):      return self.x*X + self.y                         # The hash method reflects only the position in the board, so that a zomby and a shooter at the same position will have the same hash value
        
        def move(self):          self.y -= 1                                      # for zombies
        def damage(self, d):     self.h -= d                                      # for zombies
    
    
    def display():
        if DEBUG:
            print(''.join("{: >2d}".format(y) for y in range(Y)), "\n" + "-"*(2*Y))
            board = [['  ']*Y for _ in range(X)]
            for s in chain(sS, sN, *zombiesRows):
                board[s.x][s.y] = "{: >2}".format(str(s))
            print('\n'.join(map(''.join, board)), "\n" + "-"*(2*Y) + "\n")
    
    
    def makeFire(s, dir=0):                                                       # dir = -1: diag up / 0: straight / 1: diag down
        nFire, z = s.fire, s                                                      # Initiate a fake zombie at the shooter position (allow to continue the exploration of the current direction at the last found zombie)
        while nFire:
            if not dir: z = zombiesRows[z.x] and zombiesRows[z.x][0] or None      # Shoot straight = easy target
            else:
                z, x, y = None, z.x, z.y
                while z is None and 0 <= x+dir < X and y+1 < Y:                   # Shoot diag: seek a matching position in each row...
                    x += dir; y += 1
                    if not zombiesRows[x]: continue
                    z = next((z for z in zombiesRows[x] if z.x == x and z.y == y), None)
            
            if z is None: break                                                   # Not any zomby ahead... So sad...
            d = min(nFire, z.h)
            nFire -= d                                                            # Update the number of shots
            z.damage(d)                                                           # Damage the current zomby...
            if not z.h: zombiesRows[z.x].remove(z)                                # ...and "kill" it if necessary
                
    
    pZ, round = 0, -1                                                             # Initiate the pointer to zProvider index and the round number
    sN, sS = set(), set()                                                         # Sets of numbered and S shooters
    for x,line in enumerate(lawn):
        for y,c in enumerate(line):
            if c != ' ': 
                (sS if c=='S' else sN).add(Stuff(x,y,c))
    sSlst = sorted(sS, key=lambda s: (-s.y,s.x))                                  # List of all the S shooters, in required order
    
    
    zombiesRows = [[] for _ in range(X)]                                          # List of rows of zomby objects (to identify easily thos at the front, facing the shooters)
    while pZ < len(zProvider) or any(map(bool, zombiesRows)):                     # Continue while zombies have to enter the lawn or while some aren't destroyed yet
        round += 1
        
        while pZ < len(zProvider) and zProvider[pZ][0] == round:                  # New zombies (outside of the map, will move into just after)
            row, h = zProvider[pZ][1:]
            zombiesRows[row].append( Stuff(row,Y,'Z',h) )
            pZ += 1
        
        for row in zombiesRows:
            for z in row:
                if not z.y: return round                                          # End of game: crushed defenses...
                else:                                                             # ...or move forward and destroy shooters if needed
                    z.move()
                    if z in sS: sS.remove(z)
                    if z in sN: sN.remove(z)
        
        for s in sN: makeFire(s)                                                  # Numbered shooters firing first
        for s in sSlst:                                                           # S shooters firing in order...
            if s in sS:                                                           #     ...only if the S shooter hasn't been destroyed yet...
                for d in [-1,0,1]: makeFire(s,d)                                  #     Shoot in the 3 directions
        
        if DEBUG:
            print(round, sum(map(len, zombiesRows)) )
            display()
#####################################
class Lawn:
    """Класс, представляющий поле в игре Plants and Zombies"""

    def __init__(self, lawn_str, zombies):
        self.lawn_size_x = len(lawn_str[0])
        self.lawn_size_y = len(lawn_str)
        self.plants = []
        self.zombies = []
        self.move_number = None
        self.create_lawn(lawn_str, zombies)
        self.plants_sorting()

    class Plant:
        """Класс, представляющий растерие"""
        # Урон (по умолчанию - 1)
        damage = 1

        # Тип
        SUPER = 'S'

        def __init__(self, lawn, x, y, type):
            self.lawn = lawn
            self.x = x
            self.y = y
            if type != self.SUPER:
                type = int(type)
                self.damage = type
            self.type = type
            self.attacked_cells = self.get_attacked_cells()

        class PlantsWin(Exception):
            pass

        def __str__(self):
            return str(self.type).ljust(4, ' ')

        def delete(self):
            """Удаление растения"""
            self.lawn.plants.remove(self)
            self.lawn.put_value(self.x, self.y, None)

        def get_attacked_cells(self):
            """Возвращает ячейки, которые подвергнутся атаке"""
            if self.type == self.SUPER:
                cells = [
                    [],
                    [[x, self.y] for x in range(self.x + 1, self.lawn.lawn_size_x)],
                    []
                ]

                n = 1
                while self.x + n <= self.lawn.lawn_size_x - 1 and self.y - n >= 0:
                    cells[0].append([self.x + n, self.y - n])
                    n += 1

                n = 1
                while self.x + n <= self.lawn.lawn_size_x - 1 and self.y + n <= self.lawn.lawn_size_y - 1:
                    cells[2].append([self.x + n, self.y + n])
                    n += 1

                return cells

            else:
                return [[x, self.y] for x in range(self.x, self.lawn.lawn_size_x)]

        def attack(self):
            """Атака"""
            if self.type == self.SUPER:
                for list_cells in self.attacked_cells:
                    for cell in list_cells:
                        value = self.lawn.get_value(*cell)
                        if isinstance(value, self.lawn.Zombie):
                            value.damage()
                            break
            else:
                for i in range(self.damage):
                    for cell in self.attacked_cells:
                        value = self.lawn.get_value(*cell)
                        if isinstance(value, self.lawn.Zombie):
                            value.damage()
                            break

    class Zombie:
        """Класс, представляющий зомби"""
        # Скорость
        speed = 1

        # Статус
        ALIVE = 1
        DEAD = 0

        def __init__(self, lawn, move_number, row, hp):
            self.lawn = lawn
            self.move_number = int(move_number)
            self.x = None
            self.y = int(row)
            self.hp = int(hp)
            self.stat = self.ALIVE
            self.moving = False
            self.deleted = False

        class ZombieWin(Exception):
            pass

        def __str__(self):
            return str('Z' + str(self.hp)).ljust(4, ' ')

        def change_zombie_location(self):
            """Изменение местоположения зомби (движение на одну клетку)"""
            prev_x = self.x + 1
            if prev_x < self.lawn.lawn_size_x:
                self.lawn.put_value(prev_x, self.y, None)
            self.lawn.put_value(self.x, self.y, self)

        def delete(self):
            """Удаление зомби в случае его смерти"""
            if not self.deleted:
                self.lawn.zombies.remove(self)
                self.lawn.put_value(self.x, self.y, None)
                self.deleted == True

        def can_move(self):
            """Проверка, может ли зомби двигаться"""
            # Если зомби достиг края карты - игра окончена
            if self.x is not None and self.x <= 0:
                raise self.ZombieWin
            # Если жизни зомби закончились - зомби умирает
            if self.stat == self.ALIVE and self.hp <= 0:
                self.stat = self.DEAD
            # Если зомби мертв - он не может двигаться (да ладно?!)
            if self.stat == self.DEAD:
                return False
            else:
                # Если зомби может двигаться - разрещить движение
                if self.moving:
                    return True
                else: # Если не может - проверить, сможет ли сейчас.
                    if self.lawn.move_number >= self.move_number:
                        self.moving = True
                        return True
                    else:
                        return False

        def remove_dead_plant(self):
            """Удаление убитого растения"""
            value = self.lawn.get_value(self.x, self.y)
            if isinstance(value, self.lawn.Plant):
                value.delete()

        def move(self):
            """Движение зомби"""
            if self.can_move():
                if self.x is None:
                    self.x = self.lawn.lawn_size_x
                self.x -= 1
                self.remove_dead_plant()
                self.change_zombie_location()
            elif self.stat == self.DEAD:
                self.delete()

        def damage(self):
            """Получение урона от выстрела. Если жизней не осталось - зомби погибает"""
            self.hp -= 1
            if self.hp <= 0:
                self.delete()

    def get_value(self, x, y):
        """Получение значения из двумерного списка, представляющего поле"""
        return self.lawn[y][x]

    def put_value(self, x, y, value):
        """Поместить значение в поле"""
        self.lawn[y][x] = value

    def create_lawn(self, lawn_str, zombies):
        """Создание поля из входных данных"""
        self.lawn = [[None] * self.lawn_size_x for _ in range(self.lawn_size_y)]
        # Создание и помещение на поле растений
        for y, string in enumerate(lawn_str):
            for x, v in enumerate(string):
                if v != " ":
                    plant = self.Plant(self, x, y, v)
                    self.plants.append(plant)
                    self.lawn[y][x] = plant
        # Создание зомби
        for zombie_info in zombies:
            zombie = self.Zombie(self, *zombie_info)
            self.zombies.append(zombie)

    def plants_sorting(self):
        """Сортировка растений. Нумерованные растения стреляют одновременно,
        а S растения - в порядке справа налево и сверху вниз"""
        numeric = []
        super = []
        for pl in self.plants:
            if pl.type == self.Plant.SUPER:
                super.append(pl)
            else:
                numeric.append(pl)
        super_sorting_y = lambda p: p.y
        super_sorting_x = lambda p: p.x
        super.sort(key=super_sorting_y)
        super.sort(key=super_sorting_x, reverse=True)
        numeric.extend(super)
        self.plants = numeric

    def is_game_over(self):
        """Проверка на конец игры"""
        if len(self.zombies) <= 0:
            return True
        elif not all([z.x > 0 for z in self.zombies if z.x is not None]):
            return True
        else:
            return False

    def zombie_move(self):
        """Движение всех зомби"""
        for zombie in self.zombies:
            zombie.move()

    def plants_attack(self):
        """Атака растений"""
        for plant in self.plants:
            plant.attack()

    def game(self):
        """Основной цикл игры"""
        self.move_number = 0
        while not self.is_game_over():
            try:
                self.zombie_move()
            except self.Zombie.ZombieWin:
                return self.move_number
            try:
                self.plants_attack()
            except self.Plant.PlantsWin:
                return None
            self.move_number += 1
        else:
            if len(self.zombies) <= 0:
                return None
            else:
                return self.move_number

def plants_and_zombies(lawn,zombies):
    pwz = Lawn(lawn, zombies)
    return pwz.game()
########################################
def plants_and_zombies(lawn,zombies):
    PvZ = Game(lawn, zombies)
    end = PvZ.run()
    return end
    
class Game:
    
    def __init__(self, lawn, zombies):
        self.lawn = [list(e) for e in lawn]
        self.end_f = len(lawn[0])
        self.l = len(lawn)
        self.zombies = { (y,t+(self.end_f-1)):h for t,y,h in zombies }
        self.gameOver = 0
        
    def _action(self):
        for func, shoot in zip((lambda x:x not in ' S', lambda x:x == 'S'), ( ((0,1),), ((-1,1),(0,1),(1,1)) ) ):
            for y in range(self.end_f-1,-1,-1):
                for x in range(self.l):
                    if func(self.lawn[x][y]):
                        st = self.lawn[x][y]
                        self._make_shooting(x,y, shoot, (1 if st == 'S' else int(st)) )
        self._moveZone()
            
    def _make_shooting(self, X_,Y_, typeS, damage ):
        for x,y in typeS:
            for _ in range(damage):
                X, Y = X_, Y_
                while Y<self.end_f-1 and -1<X<self.l:
                    X, Y = X+x, Y+y
                    if self.zombies.get((X,Y)):
                        self.zombies[(X,Y)] -= 1
                        break
        
    def _moveZone(self):
        tz = {}
        for (x,y),h in self.zombies.items():
            if h:
                tz[(x, y-1)] = h
                self._terminated(x, y-1)
                if not y: self.gameOver = 1
        self.zombies = tz
    
    def _terminated(self, x, y):
        if y<self.end_f and  self.lawn[x][y] != ' ': self.lawn[x][y] = ' '
                
    def run(self, timer = 0):
        while not self.gameOver:
            self._action()
            timer += 1
            if not self.zombies: return
        return timer
############################################
class Lawn:
    def __init__(self):
        self.shooters = []
        self.zombies = []
        self.idx = None

    def init(self, lawn, zombies):
        self.idx = len(lawn), len(lawn[0])
        for i, row in enumerate(lawn):
            for j, x in enumerate(row):
                if x != ' ':
                    shooter = Shooter(x, i, j)
                    shooter.init(self.idx)
                    self.shooters.append(shooter)

        self.shooters.sort(key=lambda shooter: shooter.idx[1], reverse=True)

        for zombie in zombies:
            x = Zombie(zombie[0], zombie[1], zombie[2])
            x.init(self.idx)
            self.zombies.append(x)

    def get_zombies(self, i):
        return [zombie for zombie in self.zombies if zombie.app <= i and zombie.hp > 0]


class Shooter:
    def __init__(self, x, i, j):
        self.type = x
        self.idx = i, j
        self.range = None

    def init(self, idx):
        if self.type == 'S':
            range_0 = set(zip([i for i in range(self.idx[0] - 1, -1, -1)],
                              [j for j in range(self.idx[1] + 1, idx[1])]))

            range_1 = set([(self.idx[0], j) for j in range(self.idx[1] + 1, idx[1])])

            range_2 = set(zip([i for i in range(self.idx[0] + 1, idx[0])],
                              [j for j in range(self.idx[1] + 1, idx[1])]))

            self.range = range_0, range_1, range_2
        else:
            self.range = set([(self.idx[0], j) for j in range(self.idx[1] + 1, idx[1])])

    def shoot(self, zombies, targets):
        if self.type == 'S':
            count = 1
        else:
            count = int(self.type)

        for _ in range(0, count):
            try:
                targets[0].hp -= 1
                if targets[0].hp == 0:
                    dead_zombie = targets.pop(0)
                    zombies.remove(dead_zombie)
            except IndexError:
                break


class Zombie:
    def __init__(self, i, j, k):
        self.app = i
        self.row = j
        self.hp = k
        self.range = None

    def init(self, idx):
        self.range = sorted([(self.row, j) for j in range(0, idx[1])], key=lambda idx: idx[1], reverse=True)


def get_targets(shooter, zombies, type):
    if type == 'S':
        targets = []
        for i in range(0, 3):
            targets.append([zombie for zombie in zombies if {zombie.range[0]} & shooter.range[i]])
            targets[i].sort(key=lambda zombie: zombie.range[0][1])
        return targets
    else:
        targets = [zombie for zombie in zombies if {zombie.range[0]} & shooter.range]
        targets.sort(key=lambda zombie: zombie.range[0][1])
        return targets


# solution


def plants_and_zombies(lawn, zombies):
    turf = Lawn()
    turf.init(lawn, zombies)

    dict_shooters = {}
    for shooter in turf.shooters:
        dict_shooters[shooter.idx] = shooter

    min_moves_for_shooters_to_win = max([zombie.app for zombie in turf.zombies])

    i = 0
    while True:
        zombies = turf.get_zombies(i)
        if not zombies and i >= min_moves_for_shooters_to_win:
            print('shooters win at move {}'.format(i - 1))
            return None

        zombies_move = [zombie for zombie in zombies if zombie.app < i]
        for zombie in zombies_move:
            zombie.range.pop(0)
            if not zombie.range:
                print('zombies win at move {}'.format(i))
                return i
            zombie_idx = zombie.range[0]
            if zombie_idx in dict_shooters:
                turf.shooters.remove(dict_shooters[zombie_idx])
                del dict_shooters[zombie_idx]

        # output before shooting
        # arr = get_arr(turf.idx, i)
        # shooters_to_arr(arr, turf.shooters)
        # zombies_to_arr(arr, zombies)
        # write_from_arr(arr)

        num_shooters = [shooter for shooter in turf.shooters if shooter.type.isdigit()]
        s_shooters = [shooter for shooter in turf.shooters if shooter.type == 'S']

        for shooter in num_shooters:
            targets = get_targets(shooter, zombies, shooter.type)
            shooter.shoot(zombies, targets)

        for shooter in s_shooters:
            targets = get_targets(shooter, zombies, shooter.type)
            for j in range(0, 3):
                shooter.shoot(zombies, targets[j])

        # output after shooting
        # arr = get_arr(turf.idx, i)
        # shooters_to_arr(arr, turf.shooters)
        # zombies_to_arr(arr, zombies)
        # write_from_arr(arr)

        i += 1
#####################################################
def countZombies(bakuran):
    count = 0
    for line in bakuran:
        for cell in line:
            if type(cell) == list:
                count += 1
    return count

def computeDamageShooter(bakuran):
    res = []
    for line in bakuran:
        damage = 0
        for cell in line:
            if type(cell) != list and cell != "S" and cell != " ":
                damage += int(cell)
        res.append(damage)
    return res

def sShooters(bakuran):
    s_indices = []
    max_col = len(bakuran[0]) - 1
    max_row = len(bakuran) - 1
    for row, line in enumerate(bakuran):
        for col, cell in enumerate(line):
            if type(cell) != list and cell == "S":
                s_indices.append((row, col))
    s_indices.sort(key=lambda x: (x[1], -x[0]), reverse=True)

    for s in s_indices:
        row, col = s
        #straight
        for c in range(col, max_col+1):
            if type(bakuran[row][c]) == list:
                cell = bakuran[row][c]
                health = cell[0]
                new_health = health - 1
                if new_health < 1: bakuran[row][c] = " "
                else: bakuran[row][c] = [new_health]
                break

        row, col = s
        #diagonal up
        while True:
            row -= 1
            col += 1
            
            if row < 0 or col > max_col:
                break
        
            # damage-an
            if type(bakuran[row][col]) == list:
                cell = bakuran[row][col]
                health = cell[0]
                new_health = health - 1
                if new_health < 1: bakuran[row][col] = " "
                else: bakuran[row][col] = [new_health]
                break
        row, col = s
        #diagonal down
        while True:
            row += 1
            col += 1
            
            if row > max_row or col > max_col:
                break
        
            # damage-an
            if type(bakuran[row][col]) == list:
                cell = bakuran[row][col]
                health = cell[0]
                new_health = health - 1
                if new_health < 1: bakuran[row][col] = " "
                else: bakuran[row][col] = [new_health]
                break

            


def shoot(bakuran, damages):
    for r, (damage, line) in enumerate(zip(damages, bakuran)):
        for i, cell in enumerate(line):
            if type(cell) == list:
                d = damage
                col = i
                while d > 0 and col < len(bakuran[0]):
                    frieza = bakuran[r][col]
                    if type(frieza) == list:
                        h = frieza[0]
                        new_health = h - d
                        if new_health < 1:
                            bakuran[r][col] = " "
                            d -= h
                        else:
                            bakuran[r][col] = [new_health]
                            break
                    col += 1
                break


# true if lose
def galaw(bakuran):
    zombies = []
    for row, line in enumerate(bakuran):
        for col, cell, in enumerate(line):
            if type(cell) == list:
                zombies.append((row, col))

    zombies.sort(key= lambda x: x[1])

    for zombie in zombies:
        row, col = zombie
        health = bakuran[row][col]
        bakuran[row][col] = " "
        col -= 1
        if col < 0:
            return True
        bakuran[row][col] = health
    
    return False


        

def plants_and_zombies(lawn, zombies):
    bakuran = []
    for line in lawn:
        x = []
        for c in line:
            x.append(c)
        bakuran.append(x)
    max_col = len(bakuran[0])-1
    turn = 0
    while True:
        pop_list = []
        for i, zombie in enumerate(zombies):
            t, r, h = zombie
            if t == turn:
                bakuran[r][max_col] = [h]
                pop_list.append(zombie)
        for x in pop_list:
            zombies.remove(x)
        c = countZombies(bakuran)
        if c == 0:
            if len(zombies) < 1:
                return None
            turn += 1
        else:
            damages = computeDamageShooter(bakuran)
            shoot(bakuran, damages)
            sShooters(bakuran)
            turn += 1
            if galaw(bakuran):
                return turn
#########################################
def plants_and_zombies(lawn,zombies):
    lawn = [[i for i in j] for j in lawn]
    row_l, col_l, m = len(lawn), len(lawn[0]), max(zombies,key=lambda x:x[0])[0]
    
    for move in range(999):
        for i, j in enumerate(lawn):                                         # move existing zombie to the left one step ahead
            for k, l in enumerate(j):
                if l[0] == 'z' : lawn[i][k - 1], lawn[i][k] = lawn[i][k], ' '
    
        new_zombie = [i for i in zombies if i[0] == move]                    # enter new zombie
        for i in new_zombie:
            lawn[i[1]][col_l - 1] = 'z' + str(i[2])
                                                                             # shooting starts    
        total_raw_d = {i: 0 for i in range(row_l)}                          
        total_s_d = []                                                       # store the damage of shooters
        for i, j in enumerate(lawn):
            for k, l in enumerate(j):
                if l.isdigit() : total_raw_d[i] += int(l)
                elif l == 'S' : total_s_d.append([i, k])
    
        for i, j in enumerate(lawn):                                         # numbered shooter shoots
            for k, l in enumerate(j):
                if l[0] == 'z':
                    r_d, z_score = total_raw_d[i], int(l[1:])
                    if r_d >= z_score :  total_raw_d[i] -= z_score ; lawn[i][k] = ' '
                    elif r_d < z_score : total_raw_d[i] = 0 ; lawn[i][k] = 'z' + str(z_score - r_d) ; break
                    if total_raw_d[i] == 0 : break
    
        total_s_d = sorted(total_s_d, key=lambda x: (-x[1], x[0]))           # s shooter shoots  # priority
        A = lambda s, se, see, e, ee, eee: list(zip(list(range(s, se, see)), list(range(e, ee, eee)))) # diagonal generator
        def do(t):
            for k, l in t:
                if lawn[k][l][0] == 'z':
                    if lawn[k][l][1:] == '1' : lawn[k][l] = ' '
                    else : lawn[k][l] = 'z' + str(int(lawn[k][l][1:]) - 1)
                    return 
        for i, j in total_s_d:
            do([[i, k] for k in range(j + 1, col_l)])                         # straight
            do(A(i - 1, -1, -1, j + 1, col_l, 1))                             # top diag
            do(A(i + 1, row_l, 1, j + 1, col_l, 1))                           # down diag
        if any(lawn[k][0][0] == 'z' for k in range(row_l)) : return move+1
        if move > m and all(lawn[k][j][0] != 'z' for k in range(row_l) for j in range(col_l)) : return
############################################
def plants_and_zombies(l,z):
    sums = 0
    lawn = [list(x) for x in l]
    zombies = z
    active,move = [],0
    row,col = len(lawn),len(lawn[0])
    while True:
        
        for i,j,k in zombies:
            if i == move:
                active.append({"addr":(j,col-1),"hp":k,"stat":"n"})
        zombies = [x for x in zombies if x[0] != move]        

        for x in active:
            if x["stat"] == "o":
                a,b=x["addr"]
                x["addr"]=(a,b-1)
            elif x["stat"] == "n":
                x["stat"] = "o"
               
        for i in range(0,row):
            pellet = 0
            for j in range(0,col):
                if lawn[i][j].isnumeric():
                    pellet+=int(lawn[i][j])
            for _j in range(0,col):
                if pellet == 0:break
                for x in active:
                    if x["addr"]==(i,_j) and x["hp"]>0:
                        if x["hp"]>= pellet:
                            x["hp"]-=pellet
                            pellet = 0
                        else:
                            pellet -= x["hp"]
                            x["hp"] = 0
                        break        

        S = []
        for i in range(col-1,-1,-1):
            for j in range(0,row):
                if lawn[j][i] == "S" and (j,i) not in S:
                    S.append((j,i))
        
        active = [x for x in active if x["hp"] != 0]

        record= [x.get("addr") for x in active]
        
        for i,j in S:
            b1,b2,b3 = False,False,False
            for straight in range(j+1,col):
                if b1 == True:break
                if (i,straight) in record:
                    for x in active:
                        if x["addr"]==(i,straight) and x["hp"]>0:
                            x["hp"]-=1
                            b1 = True
                            break
            for r,c in zip(range(i,-1,-1),range(j,40)):
                if b2 == True:break
                if (r,c) in record:
                    for x in active:                    
                        if x["addr"]==(r,c) and x["hp"]>0:
                            x["hp"]-=1
                            b2 = True
                            break
            for x,y in zip(range(i,row),range(j,col)):
                if b3 == True:break
                if (x,y) in record:
                    for i in active:
                        if i["addr"] == (x,y) and i["hp"]>0:
                            i["hp"]-=1
                            b3 = True
                            break              
         
        active = [x for x in active if x["hp"] != 0]        

        for i in range(0,row):
            for j in range(0,col):
                if lawn[i][j].isnumeric() or lawn[i][j] == "S":
                    for x in active:
                        if x["addr"] == (i,j+1):
                            lawn[i][j]=" "
                            break
        move += 1
        if zombies == [] and active == []:return None
        for x in active:
            if x["addr"][1] == 0:
                return move
#########################################
def plants_and_zombies(lawn, zombie_q):
    p_shooter = {(r, c):int(v) for r, row in enumerate(lawn) for c, v in enumerate(row) if v.isdigit()}
    s_shooter = {(r, c) for r, row in enumerate(lawn) for c, v in enumerate(row) if v == 'S'}
    zombies, zombie_q, rowmax, colmax, move = {}, zombie_q[::-1], len(lawn), len(lawn[0])  , 0
    
    while zombie_q or zombies:
        # Move existing zombies forward one 
        zombies = {(r, c-1):zombies[(r, c)] for r, c in zombies}
        
        while zombie_q and zombie_q[-1][0] == move:
            _, r, health = zombie_q.pop()
            zombies[(r, colmax-1)] = health

        p_shooter, s_shooter = {p:p_shooter[p] for p in p_shooter if p not in zombies}, {s for s in s_shooter if s not in zombies}

        # P shooters Fire!
        for r, c in p_shooter:
            f = p_shooter[(r,c)]
            for zc in sorted(c for zr, c in zombies if zr == r):
                if zombies[(r, zc)] > f:
                    zombies[(r, zc)] -= f
                    break
                    
                f -= zombies[(r, zc)]
                del zombies[(r, zc)]
        
        # S shooters Fire!
        for r, c in sorted(s_shooter, key=lambda k: (-k[1], k[0])):
            for dr, dc in [(-1, 1), (0, 1), (1, 1)]:
                rr, cc = r, c
                while True:
                    rr, cc  = rr + dr, cc + dc
                    if (rr, cc) in zombies:
                        zombies[(rr, cc)] -= 1
                        if zombies[(rr, cc)] < 1:
                            del zombies[(rr, cc)]
                        break
                    if cc >= colmax or rr < 0 or rr >= rowmax: break
                              
        if any(c < 0 for _, c in zombies): return move
                
        move += 1
######################################
class Lawn:
    def __init__(self, lawn_map, zombies):
        self.length = len(lawn_map[0])
        result = []
        for row in range(len(lawn_map)):
            row_map = []
            for col in range(self.length):
                if lawn_map[row][col] == ' ':
                    row_map.append(' ')
                else:
                    row_map.append(Plant(lawn_map[row][col], row, col))
            result.append(row_map)
        self.map = result
        self.zombies = [Zombie(*items) for items in zombies]

    def move_zombies(self, turn):
        if not self.zombies:
            return 0
        for zombie in self.zombies:
            if zombie.i <= turn:
                col = zombie.i - turn - 1
                try:
                    self.map[zombie.row][col] = zombie
                    if zombie.i < turn:
                        self.map[zombie.row][col + 1] = ' '
                except IndexError:
                    return turn
    
    def shoot_plants(self):
        num_shooters = []
        s_shooters = []
        for col in reversed(range(self.length)):
            for row in range(len(self.map)):
                item = self.map[row][col]
                if isinstance(item, Plant):
                    (num_shooters, s_shooters)[item.is_s].append(item)
        for shooter in num_shooters + s_shooters:
            shooter.shoot(self)


class Zombie:
    def __init__(self, i, row, hp):
        self.i = i
        self.row = row
        self.hp = hp
    
    def get_shot(self, lawn, col):
        self.hp -= 1
        if self.hp <= 0:
            lawn.map[self.row][col] = ' '
            lawn.zombies.remove(self)
        
        
class Plant:
    def __init__(self, char, row, col):
        self.row = row
        self.col = col
        if char.isdigit():
            self.shots = int(char)
            self.is_s = False
        else:
            self.shots = 1
            self.is_s = True
    
    def shoot(self, lawn):
        vert_dirs = ((0,), (-1, 0, 1))[self.is_s]
        for dv in vert_dirs:
            for shot in range(self.shots):
                shot_col = self.col
                shot_row = self.row
                while shot_col < lawn.length and 0 <= shot_row < len(lawn.map):
                    target = lawn.map[shot_row][shot_col]
                    if isinstance(target, Zombie):
                        target.get_shot(lawn, shot_col)
                        break
                    else:
                        shot_col += 1
                        shot_row += dv


def plants_and_zombies(lawn, zombies):
    lawn = Lawn(lawn, zombies)
    turn = 0
    while True:
        result = lawn.move_zombies(turn)
        if isinstance(result, int):
            if result > 0:
                return result
            return None
        lawn.shoot_plants()
        turn += 1
############################################
def plants_and_zombies(lawn,zombies):
    
    # print(lawn, zombies, sep='\n')
    
    import numpy as np
    
    # Build grid representation
    width = len(lawn[0])
    height = len(lawn)
    
    _shooters = [[
        0 if ch == ' ' or ch == 'S'
        else ord(ch) - ord('0')
        for ch in row
    ] for row in lawn]
    
    _supers = [[
        -1 if ch == 'S'
        else 0
        for ch in row
    ] for row in lawn]
    
    shooter_field = np.array(_shooters)
    super_field = np.array(_supers)
    zombie_field = np.zeros((height, width), dtype=int)
    
    # Attack a location on the map
    # Returns leftover damage
    def attack(row, col, damage):
        if row < 0 or row >= len(zombie_field):
            return 0
        elif col < 0 or col >= len(zombie_field[0]):
            return 0
        if zombie_field[row][col] > 0:
            zombie_field[row][col] -= damage
            damage = 0
            if zombie_field[row][col] < 0:
                damage = abs(zombie_field[row][col])
                zombie_field[row][col] = 0
        return damage
    
    # Update zombie_field if a straigh shot is shot
    # Return leftover damage
    def shoot_straight(row, damage):
        for col in range(len(zombie_field[0])):
            damage = attack(row, col, damage)
            if damage == 0:
                break # All damage absorbed
        return damage
    
    # Update zombie_field after a top-diagonal shot
    # Return leftover damage
    def shoot_top(row, col, damage):
        while damage:
            damage = attack(row, col, damage)
            if damage == 0:
                break
            row, col = row-1, col+1
        return damage
    
    # Update zombie_field after a bottom-diagonal shot
    # Return leftover damage
    def shoot_down(row, col, damage):
        while damage:
            damage = attack(row, col, damage)
            if damage == 0:
                break
            row, col = row+1, col+1
        return damage
    
    
    # ######### #
    # Game loop #
    # ######### #
    zombie_ground_zero = False
    move_num = 0
    while not zombie_ground_zero:
        # Move zombies
        zombie_field = np.roll(zombie_field, -1)
        # Generate zombies
        while len(zombies) and zombies[0][0] == move_num:
            _, row, health = zombies.pop(0)
            zombie_field[row][-1] = health
        
        # Destroy turrets
        shooter_field = np.where(
            (shooter_field > 0) & (zombie_field > 0)
            , 0, shooter_field
        ).astype(int)
        
        super_field = np.where(
            (super_field == -1) & (zombie_field > 0)
            , 0, super_field
        ).astype(int)
        
        # input()
        # print(move_num, super_field + shooter_field + zombie_field, ' ', sep='\n')
        
        # Cluster Shoot
        row_damage = np.array([np.sum(row) for row in shooter_field])
        for i in range(len(zombie_field)):
            shoot_straight(i, row_damage[i]) 
            
        # Super Shoot
        # Right-Left, then top-bottom
        for x in range(len(zombie_field[0])-1, -1, -1):
            for i in range(len(zombie_field)):
                if super_field[i][x] == -1:
                    # Shoot straight
                    shoot_straight(i, 1)
                    # Shoot top-diagonal
                    shoot_top(i, x, 1)
                    # Shoot bottom-diagonal
                    shoot_down(i, x, 1)
        
        # Update game status
        # input()
        # print(super_field + shooter_field + zombie_field, '\n')
        zombie_ground_zero = (zombie_field.T[0] > 0).any()
        move_num += 1
        
        if not len(zombies) and not np.sum(zombie_field): # No more zombies left
            return None
    
    # print(zombie_field.T[0])
    return move_num
####################################################
def plants_and_zombies(lawn, zombies):
    b_l, b_z = lawn, zombies
    try:
        los = {s : {} for s in [(i, j) for i in range(len(lawn)) for j in range(len(lawn[i])) if lawn[i][j] == 'S']}
        lawn = [[int(sym) for sym in line.replace(' ', '0').replace('S', '0')] for line in lawn]
        for s in los:
            top = [[s[0] - i, s[1] + i] for i in range(1, min(s[0], len(lawn[0]) - s[1] - 1) + 1)]
            mid = [[s[0], s[1] + i] for i in range(1, len(lawn[0]) - s[1])]
            low = [[s[0] + i, s[1] + i] for i in range(1, min(len(lawn) - s[0] - 1, len(lawn[0]) - s[1] - 1) + 1)]
            los[s] = {'top': top, 'mid': mid, 'low': low}
        
        moves = 0
        while zombies or any(s < 0 for sub in lawn for s in sub):
            # move all existing zombie
            zombie_pos = [(i, j) for i in range(len(lawn)) for j in range(len(lawn[i])) if lawn[i][j] != 'S' and lawn[i][j] < 0]
            if any(z[1] == 0 for z in zombie_pos):
                break
            for z in zombie_pos:
                lawn[z[0]][z[1]-1], lawn[z[0]][z[1]] = lawn[z[0]][z[1]], 0
                if (z[0], z[1]-1) in los:
                    del los[(z[0], z[1]-1)]
    
            # adding all new zombie
            for z in (z for z in zombies if z[0] == moves):
                lawn[z[1]][-1] = -z[2]
    
            zombies = [z for z in zombies if z[0] > moves]
                
            # shoting with all normal plants
            for line in lawn:
                total_shots = sum(x for x in line if x > 0)
                for j, z in enumerate(line):
                    if z != 'S' and z < 0:
                        if total_shots > abs(z):
                            line[j] = 0
                            total_shots -= abs(z)
                        else:
                            line[j] += total_shots
                            total_shots = 0
                            break
            # shoting with all special plants:
            for s in sorted(los, key=lambda x:(-x[1], x[0])):
                for direct in ['top', 'mid', 'low']:
                    line = los[s][direct]
                    for cell in line:
                        if lawn[cell[0]][cell[1]] != 'S' and lawn[cell[0]][cell[1]] < 0:
                            lawn[cell[0]][cell[1]] += 1
                            break
            moves += 1
            
        if not (zombies or any(s < 0 for sub in lawn for s in sub)):
            return None
    except:
          print(b_l, b_z)
    return moves
#####################################
def plants_and_zombies(lawn,zombies):
    zombies_hp= sum([zombies[i][2] for i in range(len(zombies))])   
    zombies_marchant=[[]for i in range(len(lawn))]                      #ligne[colonne,hp]
    tourelles_point_liste=[[]for i in range(len(lawn))]                 #ligne[colonne,force]
    tourelles_s_liste=[]                                                #[colonne,ligne]
    index=0
                                                              
    for i in range(len(lawn)):                                          #tourelles_point_liste + tourelles_s_liste création
        for j in range(len(lawn[i])):
            if lawn[i][j]=='S':
                tourelles_s_liste.append([j,i])
            elif lawn[i][j]!=' ':
                tourelles_point_liste[i].append([j,int(lawn[i][j])])

    while zombies_hp!=0:
        for i in range(len(zombies)):                                   #départ des bons zombies
            if zombies[i][0]==index:
                ajout=[len(lawn[1]),zombies[i][2]]
                zombies_marchant[zombies[i][1]].append(ajout)
        for i in range(len(zombies_marchant)):                          #déplacement des zombies et destruction des tourelles
            for j in range(len(zombies_marchant[i])): 
                z=0              
                zombies_marchant[i][j][0]-=1
                if zombies_marchant[i][j][0]<0:
                    return index
                if len(tourelles_point_liste[i])!=0 and zombies_marchant[i][j][0]==tourelles_point_liste[i][len(tourelles_point_liste[i])-1][0]:
                    tourelles_point_liste[i].pop()
                for x in range(len(tourelles_s_liste)):
                    if tourelles_s_liste[x-z][1]==i and tourelles_s_liste[x-z][0]==zombies_marchant[i][j][0]:
                        tourelles_s_liste.pop(x)
                        z+=1
        for i in range(len(tourelles_point_liste)):                     #tire des tourelles points
            if len(zombies_marchant[i])!=0 and len(tourelles_point_liste[i])!=0:
                for j in range(len(tourelles_point_liste[i])):
                    nombre_tires=tourelles_point_liste[i][j][1]
                    for t in range(nombre_tires):
                        if len(zombies_marchant[i])!=0:
                            zombies_hp-=1
                            zombies_marchant[i][0][1]-=1
                            if zombies_marchant[i][0][1]<=0:
                                zombies_marchant[i].pop(0)
        tourelles_s_liste.sort(reverse = True, key=lambda x: x[0])      #trie des tourelles S
        for i in range(len(tourelles_s_liste)):                         #tire des tourelles S
            if len(zombies_marchant[tourelles_s_liste[i][1]])!=0:       #tire tous droit
                zombies_hp-=1
                zombies_marchant[tourelles_s_liste[i][1]][0][1]-=1
                if zombies_marchant[tourelles_s_liste[i][1]][0][1]<=0:
                    zombies_marchant[tourelles_s_liste[i][1]].pop(0)
            securite=True
            id=1 
            for j in range(tourelles_s_liste[i][1]+1,len(lawn)):         #tire diagonale bas
                if securite==True:
                    case=tourelles_s_liste[i][0]+id
                    id+=1
                    z=0
                    for x in range(len(zombies_marchant[j])):
                        if zombies_marchant[j][x-z][0]==case:
                            securite=False
                            zombies_marchant[j][x-z][1]-=1
                            zombies_hp-=1
                            if zombies_marchant[j][x-z][1]==0:
                                zombies_marchant[j].pop(x-z)
                                z+=1
            securite=True
            id=1
            for j in range(tourelles_s_liste[i][1]-1,-1,-1):             #tire diagonale haut
                if securite==True:
                    case=tourelles_s_liste[i][0]+id
                    id+=1
                    z=0
                    for x in range(len(zombies_marchant[j])):
                        if zombies_marchant[j][x-z][0]==case:
                            securite=False
                            zombies_marchant[j][x-z][1]-=1
                            zombies_hp-=1
                            if zombies_marchant[j][x-z][1]==0:
                                zombies_marchant[j].pop(x-z)
                                z+=1
        index+=1
    return None 
#############################################
def plants_and_zombies(lawn,zombies):
    zombies_hp= sum([zombies[i][2] for i in range(len(zombies))])
    zombies_marchant=[[]for i in range(len(lawn))]  #[colonne,hp]
    tourelles_point_liste=[[]for i in range(len(lawn))]  #ligne[colonne,force]
    tourelles_s_liste=[]  #[colonne]
    index=0
                                                              
    for i in range(len(lawn)):                                      #tourelles_point_liste + tourelles_s_liste création
        for j in range(len(lawn[i])):
            if lawn[i][j]=='S':
                tourelles_s_liste.append([j,i])
            elif lawn[i][j]!=' ':
                tourelles_point_liste[i].append([j,int(lawn[i][j])])

    while zombies_hp!=0 and index<50:
        for i in range(len(zombies)):                               #départ des bons zombies
            if zombies[i][0]==index:
                ajout=[len(lawn[1]),zombies[i][2]]
                zombies_marchant[zombies[i][1]].append(ajout)

        for i in range(len(zombies_marchant)):                      #déplacement des zombies et destruction des tourelles
            for j in range(len(zombies_marchant[i])): 
                z=0              
                zombies_marchant[i][j][0]-=1
                if zombies_marchant[i][j][0]<0:
                    return index
                if len(tourelles_point_liste[i])!=0 and zombies_marchant[i][j][0]==tourelles_point_liste[i][len(tourelles_point_liste[i])-1][0]:
                    tourelles_point_liste[i].pop()
                for x in range(len(tourelles_s_liste)):
                    if tourelles_s_liste[x-z][1]==i and tourelles_s_liste[x-z][0]==zombies_marchant[i][j][0]:
                        tourelles_s_liste.pop(x)
                        z+=1
                
        for i in range(len(tourelles_point_liste)):     #tire des tourelles points
            if len(zombies_marchant[i])!=0 and len(tourelles_point_liste[i])!=0:
                for j in range(len(tourelles_point_liste[i])):
                    nombre_tires=tourelles_point_liste[i][j][1]
                    for t in range(nombre_tires):
                        if len(zombies_marchant[i])!=0:
                            zombies_hp-=1
                            zombies_marchant[i][0][1]-=1
                            if zombies_marchant[i][0][1]<=0:
                                zombies_marchant[i].pop(0)

        tourelles_s_liste.sort(reverse = True, key=lambda x: x[0])

        for i in range(len(tourelles_s_liste)): #[colonne,ligne]        #ligne[colonne,hp]   
            if len(zombies_marchant[tourelles_s_liste[i][1]])!=0:
                zombies_hp-=1
                zombies_marchant[tourelles_s_liste[i][1]][0][1]-=1
                if zombies_marchant[tourelles_s_liste[i][1]][0][1]<=0:
                    zombies_marchant[tourelles_s_liste[i][1]].pop(0)
            securite=True
            id=1 
            for j in range(tourelles_s_liste[i][1]+1,len(lawn)):
                if securite==True:
                    case=tourelles_s_liste[i][0]+id
                    id+=1
                    z=0
                    for x in range(len(zombies_marchant[j])):
                        if zombies_marchant[j][x-z][0]==case:
                            securite=False
                            zombies_marchant[j][x-z][1]-=1
                            zombies_hp-=1
                            if zombies_marchant[j][x-z][1]==0:
                                zombies_marchant[j].pop(x-z)
                                z+=1
            securite=True
            id=1
            for j in range(tourelles_s_liste[i][1]-1,-1,-1):
                if securite==True:
                    case=tourelles_s_liste[i][0]+id
                    id+=1
                    z=0
                    for x in range(len(zombies_marchant[j])):
                        if zombies_marchant[j][x-z][0]==case:
                            securite=False
                            zombies_marchant[j][x-z][1]-=1
                            zombies_hp-=1
                            if zombies_marchant[j][x-z][1]==0:
                                zombies_marchant[j].pop(x-z)
                                z+=1
        index+=1
    return None
#################################
import string


def plants_and_zombies(lawn, zombies):
    diagon = [[-1, 1], [1, 1]]
    m, n = len(lawn), len(lawn[0])
    blues = [[] for i in range(m)]
    s_shoot = [[] for i in range(m)]
    s_shoot_shot = []
    zom_num = len(zombies)
    for i in range(m):
        for j in range(n):
            if lawn[i][j] == 'S':
                s_shoot[i].append(j)
                s_shoot_shot.append((i, j))
            elif lawn[i][j] in string.digits:
                blues[i].append([j, int(lawn[i][j])])
    zombies.sort(key=lambda x: -x[0])
    s_shoot_shot.sort(key=lambda x: (-x[1], x[0]))
    zom_state = [[] for i in range(m)]
    move = 0
    while any(len(r) > 0 for r in zom_state) or len(zombies) > 0:
        while zombies and zombies[-1][0] == move:
            z = zombies.pop()
            zom_state[z[1]].append([n - 1, z[2]])
        for i in range(m):
            if not zom_state[i]:
                continue
            if zom_state[i][0][0] == -1:
                return move
            if blues[i] and blues[i][-1][0] == zom_state[i][0][0]:
                blues[i].pop()
            if s_shoot[i] and s_shoot[i][-1] == zom_state[i][0][0]:
                j = s_shoot[i].pop()
                for idx, s in enumerate(s_shoot_shot):
                    if s == (i, j):
                        s_shoot_shot.pop(idx)
                        break
            shoots = sum([b[1] for b in blues[i]])
            while len(zom_state[i]) > 0 and shoots > 0:
                if zom_state[i][0][1] <= shoots:
                    z = zom_state[i].pop(0)
                    zom_num -= 1
                    shoots -= z[1]
                else:
                    zom_state[i][0][1] -= shoots
                    shoots = 0
        for x, y in s_shoot_shot:
            if zom_state[x]:
                if zom_state[x][0][1] == 1:
                    zom_state[x].pop(0)
                else:
                    zom_state[x][0][1] -= 1
            for dx, dy in diagon:
                k = 1
                stop = False
                while 0 <= x + k * dx < m and 0 <= y + k * dy < n and not stop:
                    i, j = x + k * dx, y + k * dy
                    if zom_state[i]:
                        for idx, z in enumerate(zom_state[i]):
                            if z[0] == j:
                                stop = True
                                if z[1] > 1:
                                    z[1] -= 1
                                else:
                                    zom_state[i].pop(idx)
                                    zom_num -= 1
                                break
                    k += 1
        for i in range(m):
            for z in zom_state[i]:
                z[0] -= 1
        move += 1
    return None
