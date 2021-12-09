def gerrymander(s):
    supporterMap = [[0 if c != 'O' else 1 for c in row] for row in s.split()]
    regionIDMap = [[0 for c in row] for row in s.split()]
    regionIDMap[0][0] = 1
    def next_move(x,y):
        if (y > 0): yield [x,y-1]  # go left
        if (x > 0): yield [x-1,y]  # go up
        if (y < 4): yield [x,y+1]  # go right
        if (x < 4): yield [x+1,y]  # go down
    def electoral_college_win_feasible(regionID, electoral_votes):
        return regionID - electoral_votes <= 3
    def DFS_with_backtracking(zzz, zz, region_size, popular_vote_in_region, regionID, electoral_votes):
        def zero_index(regionIDMap):
            for i in range(len(regionIDMap)):
                for j in range(len(regionIDMap[0])):
                    if regionIDMap[i][j] == 0: return [i, j]
            return -1
        if region_size == 5:             # capacity reached
            regionID += 1
            if popular_vote_in_region >= 3: electoral_votes += 1  # region has popular-vote majority
            if regionID > 5: return electoral_votes >= 3  # win if electoral-college majority reached
            elif electoral_college_win_feasible(regionID, electoral_votes):
                [x,y] = zero_index(regionIDMap)
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(None, x*5 + y, 1, supporterMap[x][y], regionID, electoral_votes): 
                    return True
                regionIDMap[x][y] = 0          # backtrack
            return False
        for [x,y] in next_move(int((zz-zz%5)/5),zz%5):
            if regionIDMap[x][y] == 0:         # if unexplored field
                regionIDMap[x][y] = regionID
                if DFS_with_backtracking(zz, x*5 + y, region_size + 1, 
                                         popular_vote_in_region + supporterMap[x][y], regionID, electoral_votes):
                    return True
                regionIDMap[x][y] = 0          # backtrack
        return zzz is not None and DFS_with_backtracking(None, zzz, region_size, popular_vote_in_region,
                                                       regionID, electoral_votes)
    feasible = DFS_with_backtracking(None, 0, 1, supporterMap[0][0], 1, 0)
    region_map = [''.join(map(str, regionIDMap[i])) for i in [0,1,2,3,4]]
    return '\n'.join(region_map) if feasible else None
