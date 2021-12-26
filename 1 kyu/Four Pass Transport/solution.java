import codewars_test as test
from solution import four_pass


#verify user solution
def verify_(stations,user,ref):
    def fail(s):
        test.expect(False,s)
        return False
    fgrid = lambda r: print(print_grid(r)) if show_graph_debug else None
    if not stations or type(stations) != list or len(stations) != 4 or not all([type(x) == int and x >= 0 and x < 100 for x in stations]):
        raise Exception('Invalid input')
    ref_error = False
    if ref == None:
        if user != None: fgrid(stations)
        test.assert_equals(user,ref,'This test has no solution.')
        return user == None
    if not user or type(user) != list or len(user) > 99 or not all([type(v) == int and v >= 0 and v < 100 for v in user]):
        return fail('Invalid solution: Your solution must be an array of integers between 0 and 99.')
    ul = len(user)
    rl = len(ref)
    if ul != len(set(user)):
        fgrid(stations)
        return fail('You have duplicate values in your output:\n{}'.format(user))
    elif ul != rl:
        if ul < rl: ref_error = True
        else:
            fgrid(stations)
            return fail('The minimum necessary length is {}. Your output length is {}.\nHere is a valid output for reference:\n{}\nHere is your output:\n{}'.format(rl,ul,ref,user))
    prv = stations[0]
    q = 1
    if user[0] != prv:
        fgrid(stations)
        return fail('The first value must be the position of the first station.\nYour output:\n{}'.format(user))
    for i in range(1,ul):
        vn = user[i]
        if vn not in [v + prv for v in [10,-10,1,-1]]:
            fgrid(stations)
            return fail('Values ${} and ${} are not adjacent cells.\nYour output:\n{}'.format(prv,vn,user))
        if vn == stations[q]: q += 1
        prv = vn
    if q != 4:
        fgrid(stations)
        return fail('The candy must be processed at each station in ascending order\nYour output:\n{}'.format(user))
    test.assert_equals(user,user)
    if ref_error:
        fgrid(stations)
        print('An error has been found with this kata. Please post a comment in the Discourse section of this kata with the following:\nStations: {}\nSolution: {}'.format(stations,user))
    return True


#ensure no duplicate tests
completed_tests = {}
#too many initial failed tests result in early termination of tests
fail_count = 0

@test.describe('Full Test Suite')
def _():
    @test.it('30 FIXED TESTS')
    def _():
        fixed_tests = [
            [53,38,35,56],# 16
            [51,24,75,57],# 17
            [0,59,50,99],# 37
            [43,55,44,45],# 9
            [43,55,45,44],# 6
            [2,37,92,32],# 26
            [1,69,95,70],# 29
            [24,52,83,28],# 21
            [44,55,43,45],# 12
            [52,58,35,74],# 23
            [62,67,36,86],# 19
            [53,66,22,56],# 22
            [44,72,61,67],# 18
            [24,54,33,46],# 15
            [11,17,14,19],# 19
            [76,67,87,78],# 7
            [42,58,22,56],# 26
            [33,38,31,35],# 25
            [73,78,61,75],# 23
            [37,61,91,36],# 26
            [52,72,61,64],# 12
            [36,96,91,69],# 31
            [83,79,96,7],# 31
            [5,9,0,6],# None
            [92,59,88,11],# 30
            [16,10,18,14],# 27
            [46,28,37,16],# 10
            [3,75,49,2],# 36
            [66,70,69,78],# 20
            [3,7,22,6]# 30
        ]
        fixed_solutions = [
            [53,43,33,23,24,25,26,27,28,38,37,36,35,45,46,56],
            [51,41,42,43,44,34,24,25,35,45,55,65,75,76,77,67,57],
            [0,1,2,3,4,5,6,7,8,9,19,29,39,49,59,58,57,56,55,54,53,52,51,50,60,61,62,63,64,65,66,67,68,69,79,89,99],
            [43,53,63,64,65,55,54,44,45],
            [43,53,54,55,45,44],
            [2,3,4,5,6,7,17,27,37,47,46,45,44,43,53,63,73,83,93,92,82,72,62,52,42,32],
            [1,2,3,4,5,6,7,8,9,19,29,39,49,59,69,79,78,77,76,75,85,95,94,93,92,91,81,71,70],
            [24,34,33,32,42,52,53,63,73,83,84,85,86,87,88,78,68,58,48,38,28],
            [44,54,55,65,64,63,53,43,33,34,35,45],
            [52,53,54,55,56,57,58,48,47,46,36,35,34,33,32,31,41,51,61,71,72,73,74],
            [62,63,64,65,66,67,57,56,46,36,37,38,48,58,68,78,88,87,86],
            [53,54,64,74,75,76,66,65,55,45,35,34,33,32,22,23,24,25,26,36,46,56],
            [44,54,53,63,73,72,62,61,71,81,82,83,84,85,86,87,77,67],
            [24,34,44,54,53,43,33,23,13,14,15,16,26,36,46],
            [11,1,2,3,4,5,6,7,17,16,15,14,24,25,26,27,28,29,19],
            [76,66,67,77,87,88,78],
            [42,43,53,63,64,65,66,67,68,58,48,38,28,27,26,25,24,23,22,32,33,34,35,36,46,56],
            [33,43,44,45,46,47,48,38,28,18,17,16,15,14,13,12,11,21,31,32,22,23,24,25,35],
            [73,74,84,85,86,87,88,78,68,58,57,56,55,54,53,52,51,61,62,63,64,65,75],
            [37,27,26,25,24,23,22,21,31,41,51,61,71,81,91,92,93,94,95,96,86,76,66,56,46,36],
            [52,62,72,71,61,51,41,42,43,44,54,64],
            [36,46,56,66,76,86,96,95,94,93,92,91,81,71,61,51,41,31,21,22,23,24,25,26,27,28,29,39,49,59,69],
            [83,73,74,75,76,77,78,79,89,88,87,86,96,95,94,93,92,82,72,62,52,42,32,22,12,2,3,4,5,6,7],
            None,
            [92,93,94,95,96,97,98,99,89,79,69,59,58,68,78,88,87,86,85,84,83,82,72,62,52,42,32,22,12,11],
            [16,26,25,24,23,22,21,11,10,20,30,31,32,33,34,35,36,37,38,28,18,8,7,6,5,4,14],
            [46,47,48,38,28,27,37,36,26,16],
            [3,4,5,15,25,35,45,55,65,75,76,77,78,68,58,48,49,59,69,79,89,88,87,86,85,84,83,82,72,62,52,42,32,22,12,2],
            [66,65,64,63,62,61,60,70,71,72,73,74,75,76,77,67,68,69,79,78],
            [3,2,1,11,21,31,32,33,34,35,36,37,38,28,18,8,7,17,27,26,25,24,23,22,12,13,14,15,16,6]]

        for r,ref in zip(fixed_tests,fixed_solutions):
            completed_tests[','.join([str(n) for n in r])] = True
            if verify_(r,four_pass(r[:]),ref) == False: fail_count += 1
    

    @test.it('100 RANDOM TESTS')
    def _():
        

        #reference solution
        def ref_fn(ar):
            #verify input
            if not ar or type(ar) != list or len(ar) != 4 or not all([type(v) == int and v >= 0 and v < 100 for v in ar]):
                raise Exception('Invalid input')
            VN = [[-1,0],[0,1],[1,0],[0,-1]]
            link_seq = [[0,1,2],[1,2,0],[0,2,1]]
            ix = [[v//10,v%10] for v in ar]

            def update_dict(r,z={}):
                obj = {}
                for v in r: obj[v] = True
                obj.update(z)
                return obj

            def get_ports(i):
                rz = []
                q1,q2 = ix[i]
                for x,y in VN:
                    z = x+q1 >= 0 and x+q1 < 10 and y+q2 >= 0 and y+q2 < 10 and [q1+x,q2+y]
                    zq = z[0]*10+z[1] if z else None
                    if z:
                        if zq in ar:
                            if i + 1 < 4 and ar[i+1] == zq: rz.append(i+1)
                        else: rz.append(z)
                return rz
                # return list(filter(lambda x:x,rz))

            ecaz = update_dict([str(v).rjust(2,'0') for v in ar])
            ports = [get_ports(i) for i in range(len(ar))]
            codex = list(range(100))
            ngrid = lambda: [[255]*10 for x in range(10)]
            int_r = lambda r: [x*10+y for x,y in r]
            int_sign = lambda r: 1 if r > 0 else -1 if r < 0 else 0

            def mk_grid(r):
                grid = ngrid()
                for v in r: grid[int(v[0])][int(v[1])] = 0
                return grid

            # verify and return path sequence between stations
            def proc(r,obj):
                zr = []
                vx,vy = r[0]
                q = 1
                while q < len(r):
                    if '{}{}'.format(vx,vy) in obj: return False
                    zr.append([vx,vy])
                    wx,wy = r[q]
                    if vx != wx:
                        dx = int_sign(wx-vx)
                        vx += dx
                        while vx != wx:
                            if '{}{}'.format(vx,vy) in obj: return False
                            zr.append([vx,vy])
                            vx += dx
                    else:
                        dy = int_sign(wy-vy)
                        vy += dy
                        while vy != wy:
                            if '{}{}'.format(vx,vy) in obj: return False
                            zr.append([vx,vy])
                            vy += dy
                    vx,vy = wx,wy
                    q += 1
                zr.append([vx,vy])
                return zr

            # unique direct paths between stations
            def construct_tome(i):
                zr = []
                ps1,ps2 = ports[i],ports[i+1]
                if any([v == i+1 for v in ps1]): return [[]]
                tr = False
                for p1 in ps1:
                    if type(p1) == int: return zr
                    p1x,p1y = p1
                    for p2 in ps2:
                        if type(p2) == int: continue
                        p2x,p2y = p2
                        dx = int_sign(p2x-p1x)
                        dy = int_sign(p2y-p1y)
                        if dx == 0 and dy == 0:
                            if '{}{}'.format(p1x,p1y) not in ecaz: zr.append([[p1x,p1y]])
                        elif dx == 0 or dy == 0:
                            tr = proc([p1,p2],ecaz)
                            if tr: zr.append(tr)
                        else:
                            for v in [proc([p1,[p1x,p2y],p2],ecaz),proc([p1,[p2x,p1y],p2],ecaz)]:
                                if v: zr.append(v)
                zrs = [','.join(['{}{}'.format(x,y) for x,y in z]) for z in zr]
                rez = []
                for q,e in enumerate(zr):
                    v = zrs[q]
                    if all([len(v) <= len(g) or g not in v for g in zrs]): rez.append(e)
                return rez

            tome = [construct_tome(n) for n in range(3)]
            tome_hash = [[['{}{}'.format(x,y) for x,y in v] for v in e] for e in tome]

            # find shortest path between final two stations
            def dscan(p1,p2,grid):
                zsets = [{},{}]
                pr1,pr2 = [p1],[p2]
                n = 1
                while len(pr1) and len(pr2):
                    nrs = [[],[]]
                    for q,v in enumerate([pr1,pr2]):
                        for x1,y1 in v:
                            for x2,y2 in [[x1+x,y1+y] for x,y in VN]:
                                if x2 >= 0 and x2 < 10 and y2 >= 0 and y2 < 10 and grid[x2][y2]:
                                    nv = grid[x2][y2]
                                    if '{}{}'.format(x2,y2) in zsets[q^1]:
                                        rrr = [[x1,y1],[x2,y2]]
                                        move_seq = []
                                        if q: rrr.reverse()
                                        for i,vv in enumerate(rrr):
                                            xv,yv = vv
                                            rr = []
                                            while grid[xv][yv] > 1:
                                                rr.append([xv,yv])
                                                xv,yv = list(filter(lambda xy: all([v >= 0 and v < 10 for v in xy]) and grid[xy[0]][xy[1]] < grid[xv][yv] and '{}{}'.format(*xy) in zsets[i],[[xv+x,yv+y] for x,y in VN]))[0]
                                            rr.append([xv,yv])
                                            if i == 0: rr.reverse()
                                            move_seq.extend(rr)
                                        return move_seq
                                    if nv > n:
                                        grid[x2][y2] = n
                                        zsets[q]['{}{}'.format(x2,y2)] = True
                                        nrs[q].append([x2,y2])
                    pr1,pr2 = nrs
                    n += 1
                return False

            # put together stations and inter-station paths
            def audit(qn,sr,cnx3):
                nonlocal codex
                nc = link_seq[qn]
                cnx1,cnx2 = [tome[nc[i]][x] for i,x in enumerate(sr)]
                cnx_seq = [cnx1,cnx2,cnx3]
                nl = sum([len(x) for x in cnx_seq]) + 4
                if nl < len(codex):
                    codex = []
                    for i in range(3):
                        codex.append(ix[i])
                        codex.extend(cnx_seq[nc.index(i)])
                    codex.append(ix[3])

            # find last connection of trio
            def final_cnx(n,obj,qn,sr):
                n1,n2 = n,n+1
                [p1,prt1],[p2,prt2] = [[ix[e],ports[e]] for e in [n1,n2]]
                dx,dy = [int_sign(p2[e]-p1[e]) for e in [0,1]]
                if n2 in prt1: return audit(qn,sr,[])
                for i,x in enumerate([prt1,prt2]):
                    pv = [p1,p2][i]
                    inc = [1,-1][i]
                    cset = list(filter(lambda v: type(v) == list and v[0] in [pv[0],pv[0]+inc*dx] and v[1] in [pv[1],pv[1]+inc*dy] and '{}{}'.format(*v) not in obj, x))
                    if i: setB = cset
                    else: setA = cset
                pathed = False
                for v1 in setA:
                    for v2 in setB:
                        if v1[0] == v2[0] or v1[1] == v2[1]:
                            if v1[0] == v2[0] and v1[1] == v2[1]: tr = [v1]
                            else: tr = proc([v1,v2],obj)
                            if tr: audit(qn,sr,tr)
                        else:
                            for v in [[v1,[v1[0],v2[1]],v2],[v1,[v2[0],v1[1]],v2]]:
                                tr = proc(v,obj)
                                if tr: audit(qn,sr,tr)
                        if tr: pathed = True
                if not pathed:
                    sp = dscan(p1,p2,mk_grid(list(obj.keys())))
                    if sp: return audit(qn,sr,sp)

            # find non-obstructing path pairs
            def forge(r,obj,q):
                [z1,tk1],[z2,tk2] = [[tome[v],tome_hash[v]] for v in r[:2]]
                for i in range(len(z1)):
                    occ = update_dict(tk1[i],obj)
                    for c in range(len(z2)):
                        if all([v not in occ for v in tk2[c]]): final_cnx(r[2],update_dict(tk2[c],occ),q,[i,c])

            [forge(e,ecaz,i) for i,e in enumerate(link_seq)]
            return len(codex) < 100 and int_r(codex) or None
        
        
        #RNG function
        from random import randrange as RR

        #Math.sign
        int_sign = lambda r: 1 if r > 0 else -1 if r < 0 else 0

        #random test generator
        def test_gen():
            grp = set()
            while len(grp) < 4:
                grp.add(RR(100))
            return list(grp)

        #random edge case generator
        def edge_gen(n):
            edge_seq = [3,1,4,2] if RR(2) else [2,4,1,3]
            axis = RR(2)
            inc = 10 if axis else 1
            if n < 2:
                if n == 1: xy1 = [0,9][RR(2)]
                else: xy1 = RR(4)+2
                trz = [2*i*inc+RR(2)*inc+xy1*(1 if axis else 10) for i in range(4)]
                return [trz[edge_seq[q]-1] for q in range(4)]
            else:
                xy1 = RR(6)*10 + RR(6) + 1 if axis else RR(7)*10 + 20 + RR(6)
                trz = [xy1 + inc*i for i in range(4)]
                return [trz[edge_seq[q]-1] for q in range(4)]

        def edge_gen2():
            orientX = [0,90][RR(2)]
            orientY = [0,9][RR(2)]
            ydir = -1 if orientY else 1
            xoff = (RR(4)+2) * 10
            p2 = orientX + orientY + ydir*(RR(3))
            p4 = orientX + p2%10 + ydir*2
            p1 = orientX + p4%10 + ydir*2
            p3 = orientX + [xoff,-xoff][int_sign(orientX)] + p1%10 + ydir
            return [p1,p2,p3,p4]

        #custom random edge cases
        valid_edge_set = [edge_gen(0) for i in range(2)]
        invalid_edge_set = [edge_gen(1) for i in range(2)]
        all_custom_edge = []
        custom_edge_set = valid_edge_set + invalid_edge_set + [edge_gen(2),edge_gen2()]
        for v in custom_edge_set:
            if RR(2): all_custom_edge.append(v)
            else: all_custom_edge.insert(0,v)
        edge_pos = [i*16+RR(16) for i in range(6)]
        edge_c = 0

        for x in all_custom_edge:
            completed_tests[','.join(str(n) for n in x)] = True

        #iterate through random tests
        for i in range(100):
            if edge_c < 6 and edge_pos[edge_c] == i:
                stations = all_custom_edge[edge_c]
                edge_c += 1
            else:
                stations = test_gen()
                while ','.join([str(n) for n in stations]) in completed_tests:
                    stations = test_gen()
                completed_tests[','.join([str(n) for n in stations])] = True
            if verify_(stations,four_pass(stations[:]),ref_fn(stations)) == False:
                fail_count += 1
                if fail_count > 25:
                    print('Early termination due to too many incorrect results. Back to the drawing board...')
                    break
    
                   
##############################
import java.util.*;
import java.util.stream.*;
import java.awt.Point;

  
class FPT {

    final private static int       INF        = 99;
    final private static int[][]   IDX_PERMUT = {{0,1,2}, {0,2,1}, {1,0,2}, {1,2,0}, {2,0,1}, {2,1,0}};
    
    final private static Point[][] MOVES = {{new Point(0,-1), new Point(1,0), new Point(0,1), new Point(-1,0)},
                                            {new Point(-1,0), new Point(0,1), new Point(1,0), new Point(0,-1)}};
    final private Point[] pts;
    final private int[]   stations;
    final private int     MIN;
    
    private List<Integer> shortestPath = null;
    private int           current      = INF;
    
    
    public FPT (int[] stations) {
        pts = Arrays.stream(stations).mapToObj( n -> new Point(n/10, n%10) ).toArray(Point[]::new);
        MIN = 1 + (int) IntStream.range(0,3).map( i -> manhattan(pts[i], pts[i+1])).sum();
        this.stations = stations;
    }
    
    
    public List<Integer> solve() {
        
        for (int[] iP: IDX_PERMUT) {
            int[][] board = new int[10][10];
            for (Point p: pts) board[p.x][p.y] = 1;
            
            dfs(iP, 0, board, new Stack<List<Point>>());
            if (current == MIN) break;
        }
        return shortestPath;
    }
    
    
    private void dfs(int[] iP, int n, int[][] board, Stack<List<Point>> paths) {
        
        if (n==3) {
            int length = 4 + (int) paths.stream().mapToInt(List::size).sum();
            if (length < current) {
                current = length;
                buildPathFrom(iP, paths);
            }
            return;
        }
        
        Point p1 = pts[iP[n]], p2 = pts[iP[n]+1];
        for (Point[] moves: MOVES) {

            List<Point> path = BFS(p1,p2,board,moves);
            if (path == null) continue;
            
            paths.add(path);
            path.forEach( p -> board[p.x][p.y] = 1 );
            
            dfs(iP, n+1, board, paths);
            if (current == MIN) return;
            
            path.forEach( p -> board[p.x][p.y] = 0 );
            paths.pop();
        }
    }


    private void buildPathFrom(int[] iP, List<List<Point>> paths) {

        Map<Integer,List<Integer>> pathMap = new HashMap<>();
        for (int i=0 ; i<3 ; i++) {
            pathMap.put(iP[i], paths.get(i).stream().map(FPT ::linearize).collect(Collectors.toList()) );
        }
        
        shortestPath = new ArrayList<Integer>();
        for (int i=0 ; i<3 ; i++) {
            shortestPath.add(stations[i]);
            shortestPath.addAll(pathMap.get(i));
        }
        shortestPath.add(stations[3]);
    }


    private static int     manhattan(Point p1, Point p2) { return Math.abs(p1.x-p2.x) + Math.abs(p1.y-p2.y); }
    private static Integer linearize(Point p)            { return new Integer(p.x*10 + p.y); }
    

    
    private List<Point> BFS(Point p1, Point p2, int[][] board, Point[] moves) {
        
        Point[][] prev  = new Point[10][10];
        
        int[][] local = new int[10][10];
        for (int x=0 ; x<10 ; x++) for (int y=0 ; y<10 ; y++) {
            local[x][y] = board[x][y]==0 ? INF:0;
        }
        local[p2.x][p2.y] = INF;
        
        Deque<Point> q = new ArrayDeque<>();
        q.add(p1);
        
        while (!q.isEmpty() && !p2.equals( q.peek() )) {
            Point src = q.poll();
            int cost = local[src.x][src.y]+1;
            
            for (Point m: moves) {
                int a = src.x+m.x, b = src.y+m.y;
                if (0<=a && a<10 && 0<=b && b<10) {
                    Point next = new Point(a,b);
                    if (local[a][b] > cost) {
                        prev[a][b]  = src;
                        local[a][b] = cost;
                        q.add(next);
                    }
                }
            }
        }
        
        if (q.isEmpty()) return null;
        
        List<Point> path = new ArrayList<>();
        Point pos = p2;
        while (true) {
            pos = prev[pos.x][pos.y];
            if (p1.equals(pos)) break;
            path.add(pos);
        }
        Collections.reverse(path);
        return path;
    }
}
                   
####################################
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class FPT {

    public static final int W = 10;
    public static final int H = 10;
    private static int trace = 0;

    static int gridDistance(int a, int b) {
        int dr = Math.abs(a / W - b / W);
        int dc = Math.abs(a % W - b % W);
        return dr + dc + 1;
    }

    static int gridDistance(int... locs) {
        int d = 1;
        for (int i = 1; i < locs.length; ++i) {
            d += gridDistance(locs[i - 1], locs[i]) - 1;
        }
        return d;
    }

    static boolean isOccupied(int loc, int[] occupied) {
        int lr = loc / W;
        int rc = loc % W;
        return ((occupied[lr] & (1 << rc)) != 0);
    }

    static void occupy(int loc, int[] occupied) {
        int lr = loc / W;
        int rc = loc % W;
        occupied[lr] |= (1 << rc);
    }

    static class DistanceTable {
        int[] distances;

        public DistanceTable(int[] occupied) {
            distances = new int[W * H];
            for (int r = 0; r < H; ++r) {
                for (int c = 0; c < W; ++c) {
                    int loc = r * W + c;
                    if (isOccupied(loc, occupied)) {
                        distances[loc] = Integer.MAX_VALUE;
                    }
                }
            }
        }

        public DistanceTable findDistances(int loc) {
            distances[loc] = 1;
            boolean gotUpdate;
            do {
                gotUpdate = false;
                for (int p = 0; p < distances.length; ++p) {
                    int n;
                    if (distances[p] == 0 && (n = minNeighbour(p, true)) >= 0) {
                        distances[p] = distances[n] + 1;
                        gotUpdate = true;
                    }
                }
            } while (gotUpdate);
            return this;
        }

        public int minNeighbour(int loc, boolean colsFirst) {
            int r1 = loc / W > 0 && distances[loc - W] > 0 ? distances[loc - W] : Integer.MAX_VALUE;
            int r2 = loc / W + 1 < H && distances[loc + W] > 0 ? distances[loc + W] : Integer.MAX_VALUE;
            int bestr = Math.min(r1, r2);
            int c1 = loc % W > 0 && distances[loc - 1] > 0 ? distances[loc - 1] : Integer.MAX_VALUE;
            int c2 = loc % W + 1 < W && distances[loc + 1] > 0 ? distances[loc + 1] : Integer.MAX_VALUE;
            int bestc = Math.min(c1, c2);
            if (bestc < bestr || bestc == bestr && colsFirst) {
                if (c1 <= c2 && c1 < Integer.MAX_VALUE) {
                    return loc - 1;
                } else if (c2 < c1) {
                    return loc + 1;
                }
            } else {
                if (r1 <= r2 && r1 < Integer.MAX_VALUE) {
                    return loc - W;
                } else if (r2 < r1) {
                    return loc + W;
                }
            }
            return -1;
        }
    }

    static class Path {
        int[] steps;

        public Path(int[] steps) {
            this.steps = steps;
        }

        static Path makeDefaultPath(int a, int b, boolean byColumnFirst, int[] occupied) {
            DistanceTable distanceTable = new DistanceTable(occupied).findDistances(b);
            int n1 = distanceTable.minNeighbour(a, byColumnFirst);
            if (n1 < 0) {
                return null;
            }
            int[] steps = new int[distanceTable.distances[n1] + 1];
            int s = 0;
            steps[s++] = a;
            while (s < steps.length && a != b) {
                if ((a = distanceTable.minNeighbour(a, byColumnFirst)) < 0) {
                    return null;
                }
                steps[s++] = a;
            }
            if (a != b) {
                throw new IllegalStateException("Path did not end where expected! a=" + a + ", b=" + b);
            }
            return new Path(steps);
        }
    }

    static class Grid {

        final int[] stations;
        final Path[] paths;
        final int[] occupied;

        public Grid(int[] stations) {
            this(stations, new Path[stations.length - 1], new int[H]);
        }

        private Grid(int[] stations, Path[] paths, int[] occupied) {
            this.stations = stations;
            this.paths = paths;
            this.occupied = occupied;
            for (int s : stations) {
                occupy(s, occupied);
            }
        }

        public Grid copy() {
            return new Grid(stations, paths.clone(), occupied.clone());
        }

        private boolean findDistance(int[][] table, int r, int c) {
            int mind = Integer.MAX_VALUE;
            for (int dr = -1; dr < 2; ++dr) {
                for (int dc = -1; dc < 2; ++dc) {
                    if ((dr != 0 || dc != 0)
                            && 0 <= r + dr && r + dr < H
                            && 0 <= c + dc && c + dc < W) {
                        int d = table[r + dr][c + dc];
                        if (d > 0 && d < mind) {
                            mind = d + 1;
                        }
                    }
                }
            }
            if (mind < Integer.MAX_VALUE && table[r][c] != mind) {
                table[r][c] = mind;
                return true;
            }
            return false;
        }

        public boolean canAddPath(int sidx, Path p) {
            if (p != null && p.steps[0] == stations[sidx] && p.steps[p.steps.length - 1] == stations[sidx + 1]) {
                for (int s = 1; s + 1 < p.steps.length; ++s) {
                    if (isOccupied(p.steps[s], occupied)) {
                        return false;
                    }
                }
                return true;
            }
            return false;
        }

        public void addPath(int sidx, Path p) {
            for (int s = 1; s + 1 < p.steps.length; ++s) {
                occupy(p.steps[s], occupied);
            }
            paths[sidx] = p;
        }

        public boolean findAndAddPath(int segOpt) {
            boolean byColFirst = (segOpt & 1) != 0;
            boolean reverse = (segOpt & 2) != 0;
            int seg = segOpt >> 2;
            Path p1;
            if (reverse) {
                p1 = Path.makeDefaultPath(stations[seg + 1], stations[seg], byColFirst, occupied);
                if (p1 != null) {
                    int n = p1.steps.length;
                    for (int i = 0; i < n / 2; ++i) {
                        int t = p1.steps[i];
                        p1.steps[i] = p1.steps[n - 1 - i];
                        p1.steps[n - 1 - i] = t;
                    }
                }
            } else {
                p1 = Path.makeDefaultPath(stations[seg], stations[seg + 1], byColFirst, occupied);
            }
            if (canAddPath(seg, p1)) {
                addPath(seg, p1);
                return true;
            }
            return false;
        }

        public int findPaths(int[] order) {
            if (trace > 1) {
                System.out.println("Looking for paths in order " + Arrays.toString(order));
            }
            for (int i = 0; i < order.length; ++i) {
                if (!findAndAddPath(order[i])) {
                    if (trace > 1) {
                        System.out.println("Failed to find segment " + segOptTxt(order[i])
                                + " at step " + i + " in " + Arrays.toString(order));
                        drawPath(this);
                    }
                    return i;
                }
            }
            return order.length;
        }

        public static Grid forStations(int... stations) {
            return new Grid(stations);
        }

        public int getPathLength() {
            int c = 1;
            for (Path path : paths) {
                if (path != null) {
                    c += path.steps.length - 1;
                }
            }
            return c;
        }

        public List<Integer> getPathSteps() {
            List<Integer> steps = new ArrayList<>(getPathLength());
            steps.add(stations[0]);
            for (Path path : paths) {
                if (path != null) {
                    for (int i = 1; i < path.steps.length; ++i) {
                        steps.add(path.steps[i]);
                    }
                }
            }
            return steps;
        }
    }

    Grid grid;

    public FPT(int... stations) {
        grid = new Grid(stations);
    }

    private static boolean contains(int[] a, int value, int lim) {
        for (int i = 0; i < lim; ++i) {
            if (a[i] == value) {
                return true;
            }
        }
        return false;
    }

    private static boolean containsGroup(int[] a, int value, int groupMask, int lim) {
        for (int i = 0; i < lim; ++i) {
            if ((a[i] & ~groupMask) == (value & ~groupMask)) {
                return true;
            }
        }
        return false;
    }

    private static void fillRemaining(int[] a, int at) {
        while (at < a.length) {
            for (int d = 0; d < a.length * 4; ++d) {
                if (!containsGroup(a, d, 3, at)) {
                    a[at] = d;
                    if (++at == a.length) {
                        return;
                    }
                    break;
                }
            }
        }
    }

    private static boolean nextOrder(int[] order, int from) {
        for (int i = from; i >= 0; --i) {
            int d = order[i] + 1;
            while (d < order.length * 4 && containsGroup(order, d, 3, i)) {
                ++d;
            }
            if (d < order.length * 4) {
                order[i] = d;
                fillRemaining(order, i + 1);
                return true;
            }
        }
        return false;
    }

    public List<Integer> solve() {
        int[] order = new int[grid.paths.length];
        fillRemaining(order, 0);
        Grid bestgrid = null;
        int bestlen = 0;
        int score;
        int optimalScore = gridDistance(grid.stations);
        do {
            Grid g = grid.copy();
            if ((score = g.findPaths(order)) == order.length) {
                int len = g.getPathLength();
                if (bestgrid == null || len < bestlen) {
                    if (trace > 0) {
                        System.out.println("Found path for " + Arrays.toString(grid.stations) + " using order "
                                + Arrays.toString(order) + ", length " + len + ", optimal " + optimalScore);
                    }
                    bestgrid = g;
                    bestlen = len;
                    if (len <= optimalScore) {
                        break;
                    }
                }
                --score;
            }
        } while (nextOrder(order, score));
        if (bestgrid != null) {
            grid = bestgrid;
            return bestgrid.getPathSteps();
        }
        return null;
    }

    public static String segOptTxt(int segOpt) {
        boolean byColFirst = (segOpt & 1) != 0;
        boolean reverse = (segOpt & 2) != 0;
        int seg = segOpt >> 2;
        return (reverse ? (seg + 1) + "-" + seg : seg + "-" + (seg + 1)) + (byColFirst ? ",colsFirst" : ",rowsFirst");
    }

    public static char pathChar(int a, int b) {
        int br = b / W;
        int bc = b % W;
        int ar = a / W;
        int ac = a % W;
        if (bc > ac) {
            return '>';
        } else if (bc < ac) {
            return '<';
        } else if (br > ar) {
            return 'v';
        } else if (br < ar) {
            return '^';
        }
        return '*';
    }

    public static void drawPath(Grid grid) {
        char[][] board = new char[H][W];
        for (char[] row : board) {
            Arrays.fill(row, '.');
        }
        List<Integer> steps = grid.getPathSteps();
        for (int i = 1; i + 1 < steps.size(); ++i) {
            int s = steps.get(i);
            board[s / W][s % W] = pathChar(s, steps.get(i + 1));
        }
        for (int i = 0; i < grid.stations.length; ++i) {
            int s = grid.stations[i];
            board[s / W][s % W] = (char) ('0' + i);
        }
        System.out.println(Arrays.stream(board).map(String::valueOf).collect(Collectors.joining("\n")));
    }
}
                   
#################################
import java.util.*;
import java.util.function.*;
import java.awt.Point;

public class FPT {
    
  private static final int[][] DIR = {{0, 1}, {-1, 0}, {0, -1}, {1, 0}};
  
  private class Node extends Point implements Comparable <Node> {
    private int    cost;
    private double estimate;
    private Node   previous;
    
    private Node(double estimate, int cost, Point p, Node previous) { 
      super(p); 
      this.cost     = cost;
      this.estimate = estimate;
      this.previous = previous; 
    }
    
    private List <Node> constructPath() {
      LinkedList <Node> path = new LinkedList <> ();
      for (var n = previous; n.previous != null; n = n.previous) path.addFirst(n);
      return path;
    }
        
    @Override public int compareTo(Node n) { 
      double diff = estimate - n.estimate;
      return diff == 0 ? 0 : diff < 0 ? -1 : 1;
    }
  }
  
  private List <BiFunction <Point, Point, Integer>> calcDistance_funcs = List.of(
    this::xDistance,
    this::yDistance
  );
    
  private int xDistance(Point p1, Point p2) { return Math.abs(p1.y - p2.y); }
  private int yDistance(Point p1, Point p2) { return Math.abs(p1.x - p2.x); }
  private int manhattan(Point p1, Point p2) { return xDistance(p1, p2) + 
                                                     yDistance(p1, p2); }
  
  private char[][]    board = new char[10][10]; 
  private Point[]  stations = new Point[4];                             
  private int      shortest = -3;
  
  public FPT(int[] station_positions) {
    for (int i = 0; i < 4; i++) {
      int x = station_positions[i] / 10, y = station_positions[i] % 10;
      stations[i] = new Point(x, y);
      board[x][y] = 's';
    }  
    for (int i = 0; i < 3; i++) shortest += manhattan(stations[i], stations[i + 1]);
  }
  
  private List <Node> AStar(Point p1, Point p2, 
                            BiFunction <Point, Point, Integer> prioritize_func) {
    
    BiFunction <Point, Point, Double> heuristic = (s, e) -> {
      double epsilon = 0.01;
      return manhattan(s, e) + prioritize_func.apply(s, e) * epsilon;
    };
    
    Queue <Node>      queue = new PriorityQueue <> ();
    Map <Point, Node> nodes = new HashMap <> ();
    Node              begin = new Node(heuristic.apply(p1, p2), 0, p1, null);
    
    queue.offer(begin);
    nodes.put(p1, begin);
    
    while (!queue.isEmpty()) {
      var cur_node = queue.poll();
      if (cur_node.equals(p2)) return cur_node.constructPath();
      
      int new_cost = cur_node.cost + 1;
      for (int[] dir : DIR) {
        int u = cur_node.x + dir[0], v = cur_node.y + dir[1];
        var p = new Point(u, v);
        
        if (u < 0 || v < 0 || u > 9 || v > 9 ||
            board[u][v] == 's' && !p.equals(p2) || board[u][v] == 'x') continue;        
        
        if (!nodes.containsKey(p) || new_cost < nodes.get(p).cost) {
          Node n = new Node(new_cost + heuristic.apply(p, p2), new_cost, p, cur_node);
          nodes.put(p, n);
          queue.offer(n);
        }
      }
    }
    return null;
  }
  
  private Map <Integer, List <Node>> DFS(Set <Integer> visited) {
    if (visited.size() == 3) return Collections.emptyMap();
    
    Map <Integer, List <Node>> paths = null;
    int                        costs = Integer.MAX_VALUE;
    
    outer: for (int i = 0; i < 3; i++) {
      if (visited.contains(i)) continue;
      
      for (BiFunction <Point, Point, Integer> prioritize_func : calcDistance_funcs) {
        List <Node> path = AStar(stations[i], stations[i + 1], prioritize_func);
        if (path == null) continue;
        
        visited.add(i);
        for (Node n : path) board[n.x][n.y] = 'x';
        Map <Integer, List <Node>> new_paths = new TreeMap <> (), next = DFS(visited);
        
        if (next != null) {
          new_paths.put(i, path);
          new_paths.putAll(next);
          int new_costs = new_paths.values().stream().mapToInt(l -> l.size()).sum();
          if (new_costs < costs || paths == null) {
            paths = new_paths;
            costs = new_costs;
          }
        }
        
        visited.remove(i);
        for (Node n : path) board[n.x][n.y] = ' ';
        if (visited.isEmpty() && costs == shortest) break outer;
      }
    }
    return paths;
  }
    
  public List <Integer> solve() {
    Map <Integer, List <Node>> paths = DFS(new HashSet <Integer> ());
    if (paths == null) return null;
    
    List <Integer> answer = new ArrayList <> ();
    for (int i = 0; i < 3; i++) {
      answer.add(stations[i].x * 10 + stations[i].y);
      for (Node n : paths.get(i)) answer.add(n.x * 10 + n.y);
    }
    answer.add(stations[3].x * 10 + stations[3].y);
    return answer;  
  }
}
                   
##################################
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.IntStream;

import static java.util.Arrays.stream;

public class FPT {

    public enum Dir {
        UP(0, -1), DOWN(0, 1), LEFT(-1, 0), RIGHT(1, 0);
        int dx;
        int dy;

        Dir(int dx, int dy) {
            this.dx = dx;
            this.dy = dy;
        }

        static boolean offBounds(int x, int y) {
            return x < 0 || x >= 10 || y < 0 || y >= 10;
        }
    }

    static class Connector {
        int p;
        int x, y;
        Dir dir;

        Connector(int p, Dir dir) {
            this.p = p;
            y = p / 10;
            x = p - y * 10;
            this.dir = dir;
        }

        Connector(int p, Dir dir, int x, int y) {
            this.p = p;
            this.x = x;
            this.y = y;
            this.dir = dir;
        }

        Connector copy() {
            return new Connector(p, dir, x, y);
        }
    }

    static class Segment {
        Connector c1, c2;
        List<Integer> path = new ArrayList<>();

        Segment(Connector c1, Connector c2) {
            this.c1 = c1.copy();
            this.c2 = c2.copy();
        }

        Segment copyDirected(Dir dir) {
            Segment copy = new Segment(c1, c2);
            copy.c1.dir = dir;
            copy.c2.dir = dir;
            return copy;
        }
    }

    static class Grid {
        static final byte STATION = -6;
        static final byte WALL = -5;
        static final byte EMPTY = -1;
        byte[] grid;

        Grid(byte[] grid) {
            this.grid = grid;
        }

        Grid setAll(int setValue, int... walls) {
            for (int w : walls) grid[w] = (byte) setValue;
            return this;
        }

        static Grid empty() {
            byte[] gird = new byte[100];
            Arrays.fill(gird, EMPTY);
            return new Grid(gird);
        }

        Grid copy() {
            return new Grid(grid.clone());
        }

        private void setStep(int p, List<Integer> path) {
            path.add(p);
            grid[p] = WALL;
        }

        int setRoute(Segment s) {
            Grid distMap = this.copy();
            if (s.c1.p == s.c2.p) {
                setStep(s.c1.p, s.path);
                return 1;
            }
            return distMap.search(s.c1, s.c2.p) ? backTrace(s.c2, s.c1.p, distMap, s.path) : -1;
        }

        private Connector nextStep(Connector c) {
            Connector nc = null;
            int mv = 0;
            for (Dir dir : Dir.values()) {
                int x = c.x + dir.dx, y = c.y + dir.dy;
                if (Dir.offBounds(x, y)) continue;
                int pd = x + y * 10, v = grid[pd];
                if (v < 0) continue;
                if (nc == null || v < mv || (v == mv && dir == c.dir)) {
                    mv = v;
                    nc = new Connector(pd, c.dir, x, y);
                }
            }
            return nc;
        }

        private int backTrace(Connector c0, int p2, Grid distMap, List<Integer> path) {
            List<Integer> acc = new ArrayList<>();
            Connector c = c0.copy();
            setStep(c.p, acc);
            int dist = 1;
            for (; c.p != p2; dist++) setStep((c = distMap.nextStep(c)).p, acc);
            Collections.reverse(acc);
            path.addAll(acc);
            return dist;
        }

        private boolean search(Connector c1, int p2) {
            if (grid[c1.p] != EMPTY) return false;
            int[][] frontier = new int[100][];
            int rp = 0, wp = 0;
            frontier[wp++] = new int[]{c1.p, c1.x, c1.y};
            grid[c1.p] = (byte) 0;
            while (wp != rp) {
                int[] p = frontier[rp++];
                byte d = grid[p[0]];
                int x0 = p[1], y0 = p[2];
                for (Dir dir : Dir.values()) {
                    int x = x0 + dir.dx;
                    int y = y0 + dir.dy;
                    if (Dir.offBounds(x, y)) continue;
                    int pd = x + y * 10;
                    if (grid[pd] != EMPTY) continue;
                    if (pd == p2) return true;
                    frontier[wp++] = new int[]{pd, x, y};
                    grid[pd] = (byte) (d + 1);
                }
            }
            return false;
        }
    }

    static class TransportGrid extends Grid {
        Segment[] segments;
        int dist;

        TransportGrid(Grid grid, Dir dir, Segment... segments) {
            super(grid.grid);
            this.segments = stream(segments).map(s -> s.copyDirected(dir)).toArray(Segment[]::new);
            dist = stream(segments).mapToInt(s -> s.path.size()).sum();
        }
    }

    private int[] sta;

    private static int getStIdxByPerm(int perm, int i) {
        return "012021102120201210".charAt(perm * 3 + i) - '0';
    }

    public FPT(int[] st) {
        this.sta = st;
    }

    public List<Integer> solve() {
        Connector[] con = stream(sta).mapToObj(s -> new Connector(s, null)).toArray(Connector[]::new);
        Segment[] seg = IntStream.range(0, 3).mapToObj(i -> new Segment(con[i], con[i + 1])).toArray(Segment[]::new);
        Grid initGrid = Grid.empty().setAll(Grid.STATION, sta);
        int minDist = 0;
        List<Integer> res = null;
        for (int perm = 0; perm < 6; perm++)
            nextPerm:for (Dir dir : Dir.values()) {
                TransportGrid grid = new TransportGrid(initGrid.copy(), dir, seg);
                for (int i = 0; i < 3; i++) {
                    Segment s = grid.segments[getStIdxByPerm(perm, i)];
                    grid.setAll(Grid.EMPTY, s.c1.p, s.c2.p);
                    int d = grid.setRoute(s);
                    if (d == -1) continue nextPerm;
                    else grid.dist += d;
                }
                if (res == null || grid.dist < minDist) {
                    minDist = grid.dist;
                    res = new ArrayList<>();
                    for (int i = 0; i < 3; i++) {
                        Segment s = grid.segments[i];
                        res.addAll(s.path);
                        if (i < 2) res.remove(res.size() - 1);
                    }
                }
            }
        return res;
    }

}
                   
####################################
import java.awt.*;
import java.util.*;
import java.util.List;

public class FPT {

    public class DjikstraPathFinding {

        public class Node {
            public Point pos;
            public Point parent;

            public Node(Point pos, Point parent) {
                this.pos = pos;
                this.parent = parent;
            }
        }

        private boolean[][] closedNodes;
        private Deque<Node> openList;
        private int dimension;
        private Point finalPos;
        private Point startPos;

        public DjikstraPathFinding(boolean[][] closedNodes) {
            this.closedNodes = cloneClosedNodes(closedNodes);
            dimension = closedNodes.length;
            openList = new LinkedList<>();
        }

        private boolean[][] cloneClosedNodes(boolean[][] closedNodes) {
            boolean[][] clonedClosedNodes = new boolean[closedNodes.length][];
            for (int i = 0; i < closedNodes.length; i++) {
                clonedClosedNodes[i] = closedNodes[i].clone();
            }
            return clonedClosedNodes;
        }

        public ArrayList<Point> generatePathTo(Point numPos, Point goToPos, int direction) {
            finalPos = goToPos;
            startPos = numPos;
            if (numPos.x == goToPos.x && numPos.y == goToPos.y) {
                return new ArrayList<>();
            } else {
                return djikstrasPathfinding(null, numPos, direction);
            }

        }

        private ArrayList<Point> djikstrasPathfinding(Point parentPos, Point currentPos, int direction) {
            if (currentPos.x == finalPos.x && currentPos.y == finalPos.y) {
                var list = new ArrayList<Point>();
                list.add(currentPos);
                if (parentPos.x != startPos.x || parentPos.y != startPos.y) {
                    list.add(parentPos);
                }
                return list;
            }
            openNodes(currentPos, direction);
            if (!openList.isEmpty()) {
                Node node = openList.remove();
                var list = djikstrasPathfinding(node.parent, node.pos, direction);
                if (list == null) {
                    return null;
                }
                var peekPos = list.get(list.size() - 1);
                if (peekPos.x == currentPos.x && peekPos.y == currentPos.y && !(parentPos.x == startPos.x && parentPos.y == startPos.y)) {
                    list.add(parentPos);
                }
                return list;
            }
            return null;
        }

        private void openNodes(Point currentPos, int direction){
            switch (direction){
                case 1:
                    if (currentPos.x + 1 < dimension) {
                        manageNode(currentPos, currentPos.x + 1, currentPos.y);
                    }
                    if (currentPos.x - 1 >= 0) {
                        manageNode(currentPos, currentPos.x - 1, currentPos.y);
                    }
                    if (currentPos.y + 1 < dimension) {
                        manageNode(currentPos, currentPos.x, currentPos.y + 1);
                    }
                    if (currentPos.y - 1 >= 0) {
                        manageNode(currentPos, currentPos.x, currentPos.y - 1);
                    }
                    break;
                case 2:
                    if (currentPos.x - 1 >= 0) {
                        manageNode(currentPos, currentPos.x - 1, currentPos.y);
                    }
                    if (currentPos.y + 1 < dimension) {
                        manageNode(currentPos, currentPos.x, currentPos.y + 1);
                    }
                    if (currentPos.y - 1 >= 0) {
                        manageNode(currentPos, currentPos.x, currentPos.y - 1);
                    }
                    if (currentPos.x + 1 < dimension) {
                        manageNode(currentPos, currentPos.x + 1, currentPos.y);
                    }
                    break;
                case 3:
                    if (currentPos.y + 1 < dimension) {
                        manageNode(currentPos, currentPos.x, currentPos.y + 1);
                    }
                    if (currentPos.y - 1 >= 0) {
                        manageNode(currentPos, currentPos.x, currentPos.y - 1);
                    }
                    if (currentPos.x + 1 < dimension) {
                        manageNode(currentPos, currentPos.x + 1, currentPos.y);
                    }
                    if (currentPos.x - 1 >= 0) {
                        manageNode(currentPos, currentPos.x - 1, currentPos.y);
                    }
                    break;
                case 4:
                    if (currentPos.y - 1 >= 0) {
                        manageNode(currentPos, currentPos.x, currentPos.y - 1);
                    }
                    if (currentPos.x + 1 < dimension) {
                        manageNode(currentPos, currentPos.x + 1, currentPos.y);
                    }
                    if (currentPos.x - 1 >= 0) {
                        manageNode(currentPos, currentPos.x - 1, currentPos.y);
                    }
                    if (currentPos.y + 1 < dimension) {
                        manageNode(currentPos, currentPos.x, currentPos.y + 1);
                    }
                    break;
            }
        }

        private void manageNode(Point pos, int x, int y) {
            if (!closedNodes[x][y]) {
                openList.add(new Node(new Point(x, y), pos));
                closedNodes[x][y] = true;
            }
        }
    }

    public int[] stationsArray;
    public List<List<Point>> stations;
    public boolean[][] closedNodes;
    public List<Point> onePath=new ArrayList<>();
    public List<Point> secondPath=new ArrayList<>();
    public List<Point> thirdPath=new ArrayList<>();
    public List<Point> fourthPath=new ArrayList<>();

    public FPT(int[] stations) {
        stationsArray=stations;
        this.stations = convertToStations(stations);
        for (var a:stations) {
            System.out.println(a);
        }
        closedNodes = new boolean[10][];
        for (int i = 0; i < 10; i++) {
            closedNodes[i] = new boolean[10];
        }
    }

    private void closeStations(boolean[][] closedNodes, List<List<Point>> list){
        for (var s:list) {
            closedNodes[s.get(0).x][s.get(0).y]=true;
        }
        closedNodes[list.get(2).get(1).x][list.get(2).get(1).y]=true;
    }

    public List<Integer> solve() {
        var finalInstructions = new ArrayList<Integer>();
        closeStations(closedNodes, stations);
        var list = new ArrayList<Point>();
        for(int i=1;i<=4;i++){//firstPath
            list = recursive(new ArrayList<Point>(), 0, i, replicateMatrix(closedNodes), onePath);
        }
        var temp=stations;
        stations=new ArrayList<List<Point>>();
        stations.add(List.of(temp.get(2).get(1), temp.get(2).get(0)));
        stations.add(List.of(temp.get(1).get(1), temp.get(1).get(0)));
        stations.add(List.of(temp.get(0).get(1), temp.get(0).get(0)));
        for(int i=1;i<=4;i++){//secondPath
            list = recursive(new ArrayList<Point>(), 0, i, replicateMatrix(closedNodes), secondPath);
        }
        stations=new ArrayList<List<Point>>();
        stations.add(List.of(temp.get(0).get(0), temp.get(0).get(1)));
        stations.add(List.of(temp.get(2).get(0), temp.get(2).get(1)));
        stations.add(List.of(temp.get(1).get(0), temp.get(1).get(1)));
        for(int i=1;i<=4;i++){//thirdPath
            list = recursive(new ArrayList<Point>(), 0, i, replicateMatrix(closedNodes), thirdPath);
        }
        stations=new ArrayList<List<Point>>();
        stations.add(List.of(temp.get(1).get(0), temp.get(1).get(1)));
        stations.add(List.of(temp.get(0).get(0), temp.get(0).get(1)));
        stations.add(List.of(temp.get(2).get(0), temp.get(2).get(1)));
        for(int i=1;i<=4;i++){//fourthPath
            list = recursive(new ArrayList<Point>(), 0, i, replicateMatrix(closedNodes), fourthPath);
        }
        if(fourthPath.size()!=0 && (onePath.size()==0 || onePath.size()>=fourthPath.size()) && (secondPath.size()==0 || secondPath.size()>=fourthPath.size()) && (thirdPath.size()==0 || thirdPath.size()>=fourthPath.size())){
            finalInstructions.add(stationsArray[0]);
            finalInstructions.addAll(createFourthPath(fourthPath, temp));
            return finalInstructions;
        }
        if(onePath.size()==0 && secondPath.size()==0 && thirdPath.size()==0 && fourthPath.size()==0)return null;
        if(onePath.size()==0 && secondPath.size()==0 && thirdPath.size()!=0){
            finalInstructions.add(stationsArray[0]);
            finalInstructions.addAll(createThirdPath(thirdPath, temp));
            return finalInstructions;
        }else if(thirdPath.size()==0 && secondPath.size()==0 && onePath.size()!=0){
            finalInstructions.add(stationsArray[0]);
            finalInstructions.addAll(convertPointToInts(onePath));
            return finalInstructions;
        }else if(onePath.size()==0 && thirdPath.size()==0 && secondPath.size()!=0){
            Collections.reverse(secondPath);
            finalInstructions.addAll(convertPointToInts(secondPath));
            finalInstructions.add(stationsArray[3]);
            return finalInstructions;
        }
        if(onePath.size()==0){
            if(secondPath.size()<=thirdPath.size()){
                Collections.reverse(secondPath);
                finalInstructions.addAll(convertPointToInts(secondPath));
                finalInstructions.add(stationsArray[3]);
                return finalInstructions;
            }else{
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(createThirdPath(thirdPath, temp));
                return finalInstructions;
            }
        }else if(secondPath.size()==0){
            if(onePath.size()<=thirdPath.size()){
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(convertPointToInts(onePath));
                return finalInstructions;
            }else{
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(createThirdPath(thirdPath, temp));
                return finalInstructions;
            }
        }else if(thirdPath.size()==0){
            if(onePath.size()<=secondPath.size()){
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(convertPointToInts(onePath));
                return finalInstructions;
            }else{
                Collections.reverse(secondPath);
                finalInstructions.addAll(convertPointToInts(secondPath));
                finalInstructions.add(stationsArray[3]);
                return finalInstructions;
            }
        }
        if(onePath.size()!=0 && secondPath.size()!=0 && thirdPath.size()!=0){
            if(onePath.size()<=secondPath.size() && onePath.size()<=thirdPath.size()){
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(convertPointToInts(onePath));
                return finalInstructions;
            }else if(secondPath.size()<=onePath.size() && secondPath.size()<=thirdPath.size()){
                Collections.reverse(secondPath);
                finalInstructions.addAll(convertPointToInts(secondPath));
                finalInstructions.add(stationsArray[3]);
                return finalInstructions;
            }else if(thirdPath.size()<=onePath.size() && thirdPath.size()<=secondPath.size()){
                finalInstructions.add(stationsArray[0]);
                finalInstructions.addAll(createThirdPath(thirdPath, temp));
                return finalInstructions;
            }
        }
        return null;
    }

    private List<Integer> createThirdPath(List<Point> path, List<List<Point>> tempStations){
        var result=new ArrayList<Integer>();
        var i=path.indexOf(tempStations.get(0).get(1));
        result.addAll(convertPointToInts(path.subList(0,i+1)));
        var i2=path.indexOf(tempStations.get(2).get(1));
        var temp=convertPointToInts(path.subList(i+1,i2+1));
        result.addAll(convertPointToInts(path.subList(i2+1,path.size())));
        result.addAll(temp);
        return result;
    }

    private List<Integer> createFourthPath(List<Point> path, List<List<Point>> tempStations){
        var result=new ArrayList<Integer>();
        var i=path.indexOf(tempStations.get(1).get(1));
        var temp=convertPointToInts(path.subList(0,i+1));
        var i2=path.indexOf(tempStations.get(0).get(1));
        result.addAll(convertPointToInts(path.subList(i+1,i2+1)));
        result.addAll(temp);
        result.addAll(convertPointToInts(path.subList(i2+1,path.size())));
        return result;
    }

    private ArrayList<Point> recursive(ArrayList<Point> instructions, int i, int direction, boolean[][] closedNodes, List<Point> bestPath) {
        if (i == 3) {
            if (bestPath.size()==0 || bestPath.size()>instructions.size()){
                bestPath.removeAll(bestPath);
                bestPath.addAll(instructions);
            }
            return instructions;
        }
        closedNodes[stations.get(i).get(1).x][stations.get(i).get(1).y] = false;
        var list = new DjikstraPathFinding(closedNodes).generatePathTo(stations.get(i).get(0), stations.get(i).get(1), direction);
        closedNodes[stations.get(i).get(1).x][stations.get(i).get(1).y] = true;
        if(list==null) {
            return null;
        }
        blockPath(list, closedNodes);
        Collections.reverse(list);
        instructions.addAll(list);
        list = recursive((ArrayList<Point>) instructions.clone(), i+1, 1, replicateMatrix(closedNodes), bestPath);
        list = recursive((ArrayList<Point>) instructions.clone(), i+1, 2, replicateMatrix(closedNodes), bestPath);
        list = recursive((ArrayList<Point>) instructions.clone(), i+1, 3, replicateMatrix(closedNodes), bestPath);
        list = recursive((ArrayList<Point>) instructions.clone(), i+1, 4, replicateMatrix(closedNodes), bestPath);
        return null;
}

    private List<Integer> convertPointToInts(List<Point> list) {
        List<Integer> listOfInts = new ArrayList<>();
        for (var node : list) {
            listOfInts.add(Integer.parseInt(String.valueOf(node.x) + String.valueOf(node.y)));
        }
        return listOfInts;
    }

    private void blockPath(List<Point> path, boolean[][] closedNodes) {
        for (var node : path) {
            closedNodes[node.x][node.y] = true;
        }
    }

    private List<List<Point>> convertToStations(int[] stations) {
        List<List<Point>> result = new ArrayList<List<Point>>();
        for (int i=0;i<3;i++){
            String stringStation = stations[i] + "";
            String stringStation2 = stations[i+1] + "";
            var list=new ArrayList<Point>();
            if (stringStation.length() == 1) {
                list.add(new Point(0, stations[i]));
            } else {
                list.add(new Point(Integer.parseInt(stringStation.charAt(0) + ""), Integer.parseInt(stringStation.charAt(1) + "")));
            }
            if (stringStation2.length() == 1) {
                list.add(new Point(0, stations[i+1]));
            } else {
                list.add(new Point(Integer.parseInt(stringStation2.charAt(0) + ""), Integer.parseInt(stringStation2.charAt(1) + "")));
            }
            result.add(list);
        }
        return result;
    }

    private void display() {
        for (var line : closedNodes) {
            for (var node : line) {
                System.out.print(node ? "# " : "0 ");
            }
            System.out.println();
        }
        System.out.println();
    }

    private boolean[][] replicateMatrix(boolean[][] matrix) {
        boolean[][] clonedMatrix = new boolean[matrix.length][];
        for (int i = 0; i < matrix.length; i++)
            clonedMatrix[i] = matrix[i].clone();
        return clonedMatrix;
    }
}
                   
##################################
import java.util.*;

public class FPT {

    private int[] fab;
    private int lnPath;
    private List<Integer> path;

    public FPT(int[] fab) {
        this.fab = fab;
    }

    public List<Integer> solve() {
        //генерируем в каком порядке будем искать сегменты для формирования пути
        lnPath = 100;
        int[] segment = new int[]{0, 1, 2};
        generateSegment(0, 3, segment);
        return path;
    }

    private void generateSegment(int l, int r, int[] segment) {//генерация порядка сегментов
        if (l + 1 == r) {
            Set<Integer> visited = new HashSet<>();
            List<Integer>[] paths = new List[3];
            for (List<Integer> path0: new Path(segment[0], segment[0] + 1, visited, fab).getPath()) {
                visited.addAll(path0); paths[segment[0]] = path0;
                for (List<Integer> path1 : new Path(segment[1], segment[1] + 1, visited, fab).getPath()) {
                    visited.addAll(path1); paths[segment[1]] = path1;
                    for (List<Integer> path2 : new Path(segment[2], segment[2] + 1, visited, fab).getPath()) {
                        paths[segment[2]] = path2;
                        if (path0.size() + path1.size() + path2.size() - 2 < lnPath) {
                            path = new LinkedList<>();
                            path.addAll(paths[0]);
                            path.addAll(paths[1].subList(1, paths[1].size()));
                            path.addAll(paths[2].subList(1, paths[2].size()));
                            lnPath = path.size();
                        }
                    }
                    visited.removeAll(path1);
                }
                visited = new HashSet<>();
            }
        } else
            for (int i = l; i < r; i++) {
                int v = segment[l];
                segment[l] = segment[i];
                segment[i] = v;
                generateSegment(l + 1, r, segment);

                v = segment[l];
                segment[l] = segment[i];
                segment[i] = v;
            }
    }
}

class Path {
    private int start;
    private int goal;
    private int[] fab;
    Set<Integer> visited;
    List<List<Integer>> path;

    Path(int start, int goal, Set<Integer> visited, int[] fab) {
        this.start = fab[start];
        this.goal = fab[goal];
        this.visited = visited;
        this.fab = fab;
        path = new LinkedList<>();
    }

    public List<List<Integer>> getPath() {
         aStar(); return path;
    }

    private int[] g;//стоимость пройденного пути
    private int[] f;//вероятностный путь
    private boolean[] v;//были ли мы в этой точке

    private boolean aStar() {
        g = new int[100]; Arrays.fill(g, 100);
        f = new int[100];
        v = new boolean[100];
                for (int i = 0; i < 4; i++) if (fab[i] != goal) v[fab[i]] = true; else visited.remove(fab[i]);
        g[start] = 1;
        Queue<Integer> queue = new PriorityQueue<>((i1, i2) -> Integer.compare(f[i1], f[i2]));
        queue.offer(start);
        while (!queue.isEmpty()) {
            int current = queue.poll();
            v[current] = true;
            for (int succ: successors(current)) {
                g[succ] = Math.min(g[current] + 1, g[succ]);
                f[succ] = g[succ] + h(succ);
                if (!queue.contains(succ)) queue.offer(succ);
            }
            if (v[goal]) {
                path.add(pathReconstruction()); path.add(pathReconstruction2());
                return true;}
        }
        return false;
    }

    private int h(int p) {
        return Math.abs(p / 10 - goal / 10) + Math.abs(p % 10 - goal % 10);
    }

    private List<Integer> successors(int p) {
        List<Integer> ans = new LinkedList<>();
        int p2 = p - 10; if (p > 9 && !visited.contains(p2) && !v[p2]) ans.add(p2);
        p2 = p + 10; if (p < 90 && !visited.contains(p2) && !v[p2]) ans.add(p2);
        p2 = p - 1; if (p % 10 > 0 && !visited.contains(p2) && !v[p2]) ans.add(p2);
        p2 = p + 1; if (p % 10 < 9 && !visited.contains(p2) && !v[p2]) ans.add(p2);
        return ans;
    }

    private List<Integer> pathReconstruction(){
        LinkedList<Integer> ans = new LinkedList<>();
        ans.add(goal);
        int find = g[goal] - 1;
        int idx = goal;
        while (find != 0) {
            int idx2 = 0;
            if (idx > 9 && g[idx - 10] == find) idx2 = idx - 10;
            else if (idx < 90 && g[idx + 10] == find) idx2 = idx + 10;
                 else if (idx % 10 > 0 && g[idx - 1] == find) idx2 = idx - 1;
                      else idx2 = idx + 1;
            idx = idx2; find--;
            ans.addFirst(idx);
        }
        return ans;
    }

    private List<Integer> pathReconstruction2() {
        LinkedList<Integer> ans = new LinkedList<>();
        ans.add(goal);
        int find = g[goal] - 1;
        int idx = goal;
        while (find != 0) {
            int idx2 = 0;
            if (idx % 10 > 0 && g[idx - 1] == find) idx2 = idx - 1;
            else if (idx % 10 < 9 && g[idx + 1] == find) idx2 = idx + 1;
            else if (idx > 9 && g[idx - 10] == find) idx2 = idx - 10;
            else idx2 = idx + 10;
            idx = idx2; find--;
            ans.addFirst(idx);
        }
        return ans;
    }
 
}
                   
######################################
import java.util.*;
import java.util.stream.Collectors;

public class FPT {
    int[] stations;

    public FPT(int[] stations) {
        this.stations = stations;
    }

    public List<Integer> solve() {
        System.out.println(String.format("%d, %d ,%d ,%d", stations[0], stations[1], stations[2], stations[3]));

        List<Point> result = null;
        int min = Integer.MAX_VALUE;
        for (Permutation permutation : permutations()) {
            for (int i = 0; i < 3; i++) {
                List<Point> subPath = find(permutation.pahts(), permutation.start(i), permutation.end(i), permutation.types[i]);
                if (subPath != null) {
                    permutation.addPath(subPath);
                } else {
                    break;
                }
//                printTable(permutation.pahts(),null);
            }
            List<Point> res = permutation.joinedPath();
            if (res != null) {
                if (res.size() < min) {
                    result = res;
                    min = res.size();
                }
            }

        }
        if (result != null) {
            List<Integer> r = result.stream().map(p -> p.x * 10 + p.y).collect(Collectors.toList());
            printTable(result, new Point(stations[3] / 10, stations[3] % 10));
            System.out.println(r.size());
            System.out.println(r);
            return r;
        }
        return null;
    }

    static class Permutation {
        int[] permutation;
        int[] types;
        int[] stations;
        List<List<Point>> paths = new ArrayList<>();

        public Permutation(int[] stations, int[] permutation, int[] types) {
            this.stations = stations;
            this.permutation = permutation;
            this.types = types;
        }

        Point start(int n) {
            return new Point(stations[permutation[n]] / 10, stations[permutation[n]] % 10);
        }

        Point end(int n) {
            return new Point(stations[permutation[n]+1] / 10, stations[permutation[n]+1] % 10);
        }

        void addPath(List<Point> path) {
            if (path != null) {
                paths.add(path);
            }
        }

        List<Point> joinedPath() {
            if (paths.size() != 3) {
                return null;
            } else {
                int [] pp = new int [3];
                pp[permutation[0]] = 0;
                pp[permutation[1]] = 1;
                pp[permutation[2]] = 2;
                List<Point> res = new ArrayList<>(paths.get(pp[0]));
                res.addAll(paths.get(pp[1]).subList(1, paths.get(pp[1]).size()));
                res.addAll(paths.get(pp[2]).subList(1, paths.get(pp[2]).size()));
                return res;
            }
        }
        List<Point> pahts() {
            List<Point> res = new ArrayList<>();
            for (List<Point> p : paths){
                res.addAll(p);
            }
            return res;
        }
    }

    private List<Permutation> permutations() {
        List<Permutation> result = new ArrayList<>();
//        result.add(new Permutation(this.stations, new int[]{0, 1, 2}, new int[]{1, 0, 0}));
        for (int i = 0; i < 8; i++) {
            int[] types = new int[]{i & 1, i & 2, i & 4};
            result.add(new Permutation(this.stations, new int[]{0, 1, 2}, types));
            result.add(new Permutation(this.stations, new int[]{0, 2, 1}, types));
            result.add(new Permutation(this.stations, new int[]{1, 0, 2}, types));
            result.add(new Permutation(this.stations, new int[]{1, 2, 0}, types));
            result.add(new Permutation(this.stations, new int[]{2, 0, 1}, types));
            result.add(new Permutation(this.stations, new int[]{2, 1, 0}, types));
        }
        return result;
    }

    private List<Point> find(List<Point> path, Point p1, Point p2, int type) {
        int[][] t = new int[10][10];
        for (Point p : path) {
            if(p2.x != p.x || p2.y !=p.y) {
                t[p.x][p.y] = -1;
            }
        }
        for (int i=0;i<4;i++){
            Point p = new Point(stations[i]/10,stations[i]%10);
            if(p2.x != p.x || p2.y !=p.y) {
                t[p.x][p.y] = -1;
            }
        }
        Queue<Point> open = new PriorityQueue<>(new PointComparator2(p2,type));
        open.add(p1);
        HashMap<Point, Point> cameFrom = new HashMap<>();
        HashMap<Point, Integer> gScore = new HashMap<>();
        HashSet<Point> closedSet = new HashSet<>();
        gScore.put(p1, 0);

        while (!open.isEmpty()) {
            Point current = open.poll();
            if (current.equals(p2)) {
                return reconstruct_path(cameFrom, current);
            }
            open.remove(current);
            closedSet.add(current);
            for (Point neighbor : neighbors(t, current, type)) {
                if (closedSet.contains(neighbor)) {
                    continue;
                }
                Integer tentative_gScore = gScore.get(current) + 1;
                if (tentative_gScore < gScore.getOrDefault(neighbor, Integer.MAX_VALUE)) {
                    cameFrom.put(neighbor, current);
                    gScore.put(neighbor, tentative_gScore);
                    neighbor.f = tentative_gScore + f(neighbor,p2);
                    if (!open.contains(neighbor)) {
                        open.add(neighbor);
                    }
                }
            }
        }
        return null;
    }

    static class Point {
        int x;
        int y;
        int f;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            Point point = (Point) o;
            return x == point.x &&
                    y == point.y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }
    }

    class PointComparator2 implements Comparator<Point> {
        private Point target;
        int type;

        public PointComparator2(Point target, int type) {
            this.target = target;
            this.type = type;
        }

        @Override
        public int compare(Point p1, Point p2) {
            if(p1.f == p2.f) {
                if(type == 0){
                    return Math.abs(p1.x - target.x) - Math.abs(p2.x - target.x);
                }else {
                    return Math.abs(p1.y - target.y) - Math.abs(p2.y - target.y);
                }
            }else {
                return p1.f - p2.f;
            }
        }
    }

    private int f(Point p1, Point p2) {
        return Math.abs(p1.x - p2.x) + Math.abs(p2.y - p1.y);
    }

    private List<Point> reconstruct_path(HashMap<Point, Point> cameFrom, Point p) {
        List<Point> total_path = new ArrayList<>();
        total_path.add(p);
        while ((p = cameFrom.get(p)) != null) {
            total_path.add(p);
        }
        Collections.reverse(total_path);
        return total_path;
    }

    private List<Point> neighbors(int[][] table, Point p) {
        List<Point> list = new ArrayList<>();
        if (isValid2(table, new Point(p.x - 1, p.y))) list.add(new Point(p.x - 1, p.y));
        if (isValid2(table, new Point(p.x + 1, p.y))) list.add(new Point(p.x + 1, p.y));
        if (isValid2(table, new Point(p.x, p.y - 1))) list.add(new Point(p.x, p.y - 1));
        if (isValid2(table, new Point(p.x, p.y + 1))) list.add(new Point(p.x, p.y + 1));
        return list;
    }

    private List<Point> neighbors(int[][] table, Point p, int type) {
        List<Point> list = new ArrayList<>();
        if(type == 0) {
            if (isValid2(table, new Point(p.x - 1, p.y))) list.add(new Point(p.x - 1, p.y));
            if (isValid2(table, new Point(p.x + 1, p.y))) list.add(new Point(p.x + 1, p.y));
            if (isValid2(table, new Point(p.x, p.y - 1))) list.add(new Point(p.x, p.y - 1));
            if (isValid2(table, new Point(p.x, p.y + 1))) list.add(new Point(p.x, p.y + 1));
        }else{
            if (isValid2(table, new Point(p.x, p.y - 1))) list.add(new Point(p.x, p.y - 1));
            if (isValid2(table, new Point(p.x, p.y + 1))) list.add(new Point(p.x, p.y + 1));
            if (isValid2(table, new Point(p.x - 1, p.y))) list.add(new Point(p.x - 1, p.y));
            if (isValid2(table, new Point(p.x + 1, p.y))) list.add(new Point(p.x + 1, p.y));
        }
        return list;
    }

    private boolean isValid2(int[][] table, Point p) {
        if (p.x < 0 || p.x >= 10 || p.y < 0 || p.y >= 10) {
            return false;
        }
        return table[p.x][p.y] == 0;
    }

    private void printTable(List<Point> path, Point current) {
        int[][] t = new int[10][10];
        if (path != null) {
            for (Point p : path) {
                t[p.x][p.y] = -1;
            }
        }
        for (int i = 0; i < stations.length; i++) {
            t[stations[i] / 10][stations[i] % 10] = i + 1;
        }
        System.out.print("  ");
        for (int i = 0; i < 10; i++) {
            System.out.print(String.format("%2d",i));
        }
        System.out.println();
        for (int i = 0; i < 10; i++) {
            System.out.print(String.format("%2d",i));
            for (int j = 0; j < 10; j++) {
                if (current != null && current.x == i && current.y == j) {
                    System.out.print(" $");
                } else if (t[i][j] > 0) {
                    System.out.print(String.format("%2d",t[i][j]));
                } else if (t[i][j] < 0) {
                    System.out.print(" *");
                } else {
                    System.out.print(" .");
                }
            }
            System.out.println();
        }
        System.out.println();
    }
}
                   
#######################################
import java.awt.Point;
import java.util.*;
import java.util.stream.*;



public class FPT {
    
    final private static int     INF        = 99;
    final private static int[][] IDX_PERMUT = {{0,1,2}, {0,2,1}, {1,0,2}, {1,2,0}, {2,0,1}, {2,1,0}};
    
    final private static Map<Integer,Point> MOVES_MAP = new HashMap<Integer,Point>() {{
            put((int) 'N', new Point(-1, 0));
            put((int) 'S', new Point( 1, 0));
            put((int) 'E', new Point( 0, 1));
            put((int) 'W', new Point( 0,-1));
    }};
    final private static Map<Point,String> DIR_CYCLES_PRECEDENCE = new HashMap<Point,String>() {{  
        //  general direction, "clockwise,anti-clockwise" (not really true for verticals and horizontals...)
        put(new Point( 1, 0), "WNES,ENWS");
        put(new Point( 1, 1), "SWNE,ENWS");
        put(new Point( 0, 1), "SWNE,NWSE");
        put(new Point(-1, 1), "ESWN,NWSE");
        put(new Point(-1, 0), "ESWN,WSEN");
        put(new Point(-1,-1), "NESW,WSEN");
        put(new Point( 0,-1), "NESW,SENW");
        put(new Point( 1,-1), "WNES,SENW");
    }};
    
    
    final private Point[][][] segMovesConfig = new Point[3][2][4];
    final private Point[] pts;
    final private int[]   stations;
    final private int     MIN;

    private List<Integer> shortestPath = null;
    private int           current      = INF;
    private boolean       DEBUG        = false;
    
    
    public FPT(int[] stations) {
        
        pts = Arrays.stream(stations).mapToObj( n -> new Point(n/10, n%10) ).toArray(Point[]::new);
        MIN = 1 + (int) IntStream.range(0,3).map( i -> manhattan(pts[i], pts[i+1])).sum();
        this.stations = stations;
        
        for (int iP=0 ; iP<3 ; iP++) {
            Point p1 = pts[iP],   p2 = pts[iP+1];
            int   dx = p2.x-p1.x, dy = p2.y-p1.y;
            
            Point dir = new Point(dx==0 ? 0 : dx / Math.abs(dx), 
                                  dy==0 ? 0 : dy / Math.abs(dy));
            
            segMovesConfig[iP] = Arrays.stream( DIR_CYCLES_PRECEDENCE.get(dir).split(",") )
                                       .map( s -> s.chars().mapToObj( c -> MOVES_MAP.get(c) ).toArray(Point[]::new) )
                                       .toArray(Point[][]::new);
        }
    }
    
    
    public List<Integer> solve() {
        
        for (int[] iP: IDX_PERMUT) {
            int[][] board = new int[10][10];
            for (Point p: pts) board[p.x][p.y] = 1;
            
            dfs(iP, 0, board, new Stack<List<Point>>());
            if (current == MIN) break;
        }
        return shortestPath;
    }
    
    
    private void dfs(int[] iP, int n, int[][] board, Stack<List<Point>> paths) {
        
        if (n==3) {
            int length = 4 + (int) paths.stream().mapToInt(List::size).sum();
            if (length < current) {
                current = length;
                buildPathFrom(iP, paths);
            }
            return;
        }
        
        Point p1 = pts[iP[n]], p2 = pts[iP[n]+1];
        for (Point[] moves: segMovesConfig[iP[n]]) {

            List<Point> path = aStar(p1,p2,board,moves);
            if (path == null) continue;
            
            paths.add(path);
            path.forEach( p -> board[p.x][p.y] = 1 );
            
            dfs(iP, n+1, board, paths);
            if (current == MIN) return;
            
            path.forEach( p -> board[p.x][p.y] = 0 );
            paths.pop();
        }
    }


    private void buildPathFrom(int[] iP, List<List<Point>> paths) {

        Map<Integer,List<Integer>> pathMap = new HashMap<>();
        for (int i=0 ; i<3 ; i++) {
            pathMap.put(iP[i], paths.get(i).stream().map(FPT::linearize).collect(Collectors.toList()) );
        }
        
        shortestPath = new ArrayList<Integer>();
        for (int i=0 ; i<3 ; i++) {
            shortestPath.add(stations[i]);
            shortestPath.addAll(pathMap.get(i));
        }
        shortestPath.add(stations[3]);
    }


    private static int     manhattan(Point p1, Point p2) { return Math.abs(p1.x-p2.x) + Math.abs(p1.y-p2.y); }
    private static Integer linearize(Point p)            { return new Integer(p.x*10 + p.y); }
    

    
    private List<Point> aStar(Point p1, Point p2, int[][] board, Point[] moves) {
        
        Point[][] prev  = new Point[10][10];
        P[][]     local = new P[10][10];
        for (int x=0 ; x<10 ; x++) for (int y=0 ; y<10 ; y++) {
            local[x][y] = new P(board[x][y]==0 ? INF:0, 0);
        }
        local[p2.x][p2.y] = new P(INF,0);
        
        PriorityQueue<P> q = new PriorityQueue<>();
        q.add(new P(manhattan(p1,p2), 0, 0, 0, p1));                   // P( cost+heuristic, rotation index, insertion order, cost, related Point )
        
        int iG = 0;
        while (!q.isEmpty() && !p2.equals( q.peek().pos )) {
            
            P     curr = q.poll();
            Point src  = curr.pos;
            int   cost = curr.cost+1;
            
            int iR = -1; for (Point m: moves) { iR++;
                int a = src.x+m.x, b = src.y+m.y;
                if (0<=a && a<10 && 0<=b && b<10) {
                    Point next   = new Point(a,b);
                    P     nLocal = new P(cost,iR);
                    if (nLocal.compareTo(local[a][b]) < 0) {
                        prev[a][b]  = src;
                        local[a][b] = nLocal;
                        q.add( new P(cost+manhattan(next,p2), iR, iG++, cost, next) );
                    }
                }
            }
        }
        
        if (q.isEmpty()) return null;
        
        List<Point> path = new ArrayList<>();
        Point pos = p2;
        while (true) {
            pos = prev[pos.x][pos.y];
            if (p1.equals(pos)) break;
            path.add(pos);
        }
        Collections.reverse(path);
        return path;
    }
    
    private static void print(int[] stations, Stack<List<Point>> paths) {
        Map<Integer,String> ss = new HashMap<>();
        for(int i=0;i<4;i++) ss.put(stations[i], ""+(char) (i+65));
        for(int i=0;i<paths.size();i++) { final int ii = i+1; paths.get(i).stream().forEach( p -> ss.put(p.x*10+p.y, ""+ii)); }

        System.out.println("0123456789\n----------");
        IntStream.range(0, 10)
                 .mapToObj( x -> IntStream.range(0,10).mapToObj( y -> ss.getOrDefault(x*10+y, " ") ).collect(Collectors.joining()) )
                 .forEachOrdered(System.out::println);
        System.out.println("----------");
    }
    
    
    private static class P extends Point implements Comparable<P> {
        
        private int   cost = 0,
                      iG   = 0;
        private Point pos  = null;
        
        private P(int x, int y) { super(x,y); }
        private P(Point p)      { super(p.x,p.y); }
        private P(int ch, int iR, int ig, int c, Point p) {              // Version used in the priority queue, for the A* implementation 
            super(ch,iR);
            iG   = ig;
            cost = c;
            pos  = p;
        }

        @Override public int    compareTo(P o)  { return x != o.x ? x-o.x           // closest to end first
                                                       : y != o.y ? y-o.y           // rotation precedence
                                                                  : o.iG-iG; }      // last enqueued point first, if ties
        @Override public String toString()      { return x==-1 ? "x"
                                                       : x==INF ? " "
                                                       : y==0 ? ""+(char) (x+65)
                                                              : ""+(char) (x+97); }
    }
}
