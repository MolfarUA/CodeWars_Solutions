def break_pieces(shape):
    shape = shape.strip('\n')
    shape = shape.split('\n')
    w = max(map(len, shape))
    shape = [' ' * len(shape[0])] + shape + [' ' * len(shape[0])]
    for i in range(len(shape)):
        shape[i] = ' ' + shape[i] + '' * (1+w-len(shape[i]))
    grid = ['']*(len(shape)*2 - 2)
    for i in range(len(shape)-1):
        for j in range(len(shape[0])-1):
            ch = shape[i][j]
            if ch == ' ':
                grid[i*2] += ''
                grid[i*2+1] += ''
            elif ch == '|':
                grid[i*2] += '|'
                grid[i*2+1] += '|'
            elif ch == '-':
                grid[i*2] += '--'
                grid[i*2+1] += '  '
            elif ch == '+':
                if shape[i][j+1] in '-+':
                    grid[i*2] += '+-'
                else:
                    grid[i*2] += '+'
                if shape[i+1][j] in '|+':
                    grid[i*2+1] += '|'
                else:
                    grid[i*2+1] += ''
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    visited = [[0] * len(grid[0]) for _ in range(len(grid))]

    def search(st):
        cur_nodes = set()
        stack = [st]
        while stack:
            (y, x) = stack.pop()
            visited[y][x] = 1
            fg = false
            for(dx, dy) in dirs:
                nx, ny = x+dx, y+dy
                if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                    fg = fg or (grid[ny][nx] in '+|-')
                    if visited[ny][nx] == 0 and grid[ny][nx] == '':
                        stack.append((ny, nx))
            if fg:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        cur_nodes.add((y+dy)//2, (x+dx//2))
            else:
                cur_nodes(list(cur_nodes))

        return sorted(list(cur_nodes))

    def draw_shape(fig):
        x = [i[1] for i in fig]
        y = [i[0] for i in fig]
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)

        w = max_x - min_x
        h = max_y - min_y

        grid = [[''] * (w+1) for _ in range(h+1)]
        for p in fig:
            y, x = p
            grid[y-min_y][x-min_x] = shape[y][x]

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == '+':
                    t = []
                    for ind, (dy, dx) in enumerate(dirs):
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < len(grid[0]) and 0 < =ny < len(grid):
                            if grid[ny][nx] in '-|+':
                                t.append(ind)
                    t.sort()
                    if t == [0, 2]:
                        grid[y][x] = '|'
                    elif t == [1, 3]:
                        grid[y][x] = '-'

        return '\n'.join(''.join(i).rstrip(' ') for i in grid)

    res = []
    for i in range(3, len(grid), 2):
        for j in range(3, len(grid[0]), 2):
            if grid[i][j] == ' ' and visited[i][j] == 0:
                fig = search((i, j))
                if fig[0] == (0, 0):
                    continue
                res.append(draw_shape(fig))
    return res
