576986639772456f6f00030c


using System.Collections.Generic;
using System.Linq;
using System;

public class Finder
{
       public static int PathFinder(string maze)
        {
            var m = maze.Split('\n').Select(s=>s.Select(c => int.Parse(""+c)).ToArray()).ToArray();
            var n = m.Length;
            var points = new Point[n, n];
            int i, j;
            var neighbors = new List<Point>();

            for (i = 0; i < n; ++i)
                for (j = 0; j < n; ++j)
                    points[i, j] = new Point { I = i, J = j, Heuristic = (n - i) + (n - j) };
            var heap = new BinaryHeap<Point>();
            points[0,0].Moves = 0;
            heap.Add(points[0,0]);
            while (heap.Count != 0)
            {
                var here = heap.Remove();
                i = here.I;
                j = here.J;
                if (i == n - 1 && j == n - 1)
                    return here.Moves;
                neighbors.Clear();
                if (i + 1 < n) neighbors.Add(points[i + 1, j]);
                if (j + 1 < n) neighbors.Add(points[i, j + 1]);
                if (i - 1 >= 0) neighbors.Add(points[i - 1, j]);
                if (j - 1 >= 0) neighbors.Add(points[i, j - 1]);
                foreach (var neighbor in neighbors)
                {
                    var moves = here.Moves + Math.Abs(m[i][j] - m[neighbor.I][neighbor.J]);
                    if (moves < neighbor.Moves)
                    {
                        neighbor.Moves = moves;
                        neighbor.Score = moves + neighbor.Heuristic;
                        heap.AddOrUpdate(neighbor);
                    }
                }
            }
            return -1;
        }

        public class Point : IComparable<Point>
        {
            public int I { get; set; }
            public int J { get; set; }
            public int Score { get; set; } = int.MaxValue;
            public int Moves { get; set; } = int.MaxValue;
            public int Heuristic { get; set; }

            public int CompareTo(Point other)
            {
                return Score.CompareTo(other.Score);
            }
        }
    
       public class BinaryHeap<T> where T : IComparable<T>
    {
        private List<T> _heap = new List<T>();
        private Dictionary<T, int> _items = new Dictionary<T, int>();

        public int Count => _heap.Count;


        public bool Contains(T item) => _items.ContainsKey(item);

        public void Add(T item)
        {
            if (Contains(item)) throw new Exception("Item already added.");
            _heap.Add(item);
            UpdateIndices(Count-1);
            BubbleUp(_heap.Count - 1);
        }

        public T Peek() => _heap.FirstOrDefault();
        public T Remove()
        {
            if (_heap.Count == 0) return default(T);
            var top = _heap.First();
            var last = _heap.Last();
            _heap.RemoveAt(_heap.Count - 1);
            _items.Remove(top);
            if (_heap.Count == 0)
                return top;
            _heap[0] = last;
            BubbleDown(0);
            return top;
        }

        public void AddOrUpdate(T item) {
            if (_items.ContainsKey(item)) {
                BubbleUp(_items[item]);
                BubbleDown(_items[item]);
            }
            else Add(item);
        }

        private void BubbleUp(int index)
        {
            var i = index;
            var p = (i - 1) / 2;
            while (i > 0 && i < _heap.Count && _heap[i].CompareTo(_heap[p]) < 0)
            {
                Swap(i, p);
                i = p;
                p = (i - 1) / 2;
            }
        }

        private void BubbleDown(int index)
        {
            int i = index;
            int c = i * 2 + 1;
            bool swapped = true;
            while (c < _heap.Count && swapped)
            {
                if (c+1 < _heap.Count && _heap[c+1].CompareTo(_heap[c]) < 0)
                    ++c;
                if (_heap[i].CompareTo(_heap[c]) > 0)
                {
                    Swap(i, c);
                    i = c;
                    c = i * 2 + 1;
                }
                else swapped = false;
            }
        }

        private void Swap(int i, int j)
        {
            var t = _heap[i];
            _heap[i] = _heap[j];
            _heap[j] = t;
            UpdateIndices(i, j);
        }

        private void UpdateIndices(params int[] indices)
        {
            foreach (var i in indices)
            {
                _items[_heap[i]] = i;
            }
        }
    }
}
_____________________________
using System;
using System.Collections.Generic;
    
public static class Finder
{
    public static int PathFinder(string mazeString)
    {
        // Initialize maze
        string[] mazeRows = mazeString.Split(new[] {"\n"}, StringSplitOptions.None);

        int mazeSize = mazeRows.Length, mazeEdge = mazeSize - 1;
        int[][] mazeMap = new int[mazeSize][], climbRoundsMap = new int[mazeSize][];

        for (var mazeRow = 0; mazeRow < mazeSize; mazeRow++)
        {
            mazeMap[mazeRow] = new int[mazeSize];
            climbRoundsMap[mazeRow] = new int[mazeSize];
            for (var mazeColumn = 0; mazeColumn < mazeSize; mazeColumn++)
            {
                mazeMap[mazeRow][mazeColumn] = mazeRows[mazeRow][mazeColumn] - '0';
                climbRoundsMap[mazeRow][mazeColumn] = -1;
            }
        }

        climbRoundsMap[0][0] = 0;

        // Get the result
        // right -> down -> left -> up
        int[] xDirections = {1, 0, -1, 0}, yDirections = {0, 1, 0, -1};

        // [ 0: <x>, 1: <y>, 2: <climbRounds>, 3: <previousX>, 4: <previousY> ]
        var queue = new Queue<int[]>();
        queue.Enqueue(new[] {0, 0, 0, -1, -1});

        while (queue.Count > 0)
        {
            var path = queue.Dequeue();
            int x = path[0], y = path[1], climbRounds = path[2], altitude = mazeMap[y][x], prevX = path[3], prevY = path[4];
            
            // Do not continue this path if other paths reached current tile with less amount of climb rounds
            if (climbRoundsMap[y][x] < climbRounds) continue;

            for (int direction = 0; direction < 4; direction++)
            {
                int nextX = x + xDirections[direction], nextY = y + yDirections[direction];

                // Previous step and out of bounds check
                if (nextX == prevX && nextY == prevY || nextX < 0 || nextY < 0 || nextX > mazeEdge || nextY > mazeEdge) continue;

                int altitudeDifference = altitude - mazeMap[nextY][nextX],
                    nextClimbRounds = climbRounds + (altitudeDifference < 0 ? -altitudeDifference : altitudeDifference);
                
                // Skip tile if previous iterations reached tile with less amount of climb rounds
                int prevClimbRounds = climbRoundsMap[nextY][nextX];
                if (prevClimbRounds != -1 && prevClimbRounds <= nextClimbRounds) continue;

                climbRoundsMap[nextY][nextX] = nextClimbRounds;

                queue.Enqueue(new[] {nextX, nextY, nextClimbRounds, x, y});
            }
        }
        
        return climbRoundsMap[mazeEdge][mazeEdge];
    }
}
_____________________________
using System;
using System.Linq;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;

public class Finder
{
    static int bestValue = 0;
    static Node[][] nodes;
    static VisitedNode[][] visited;

    public static int PathFinder(string maze)
    {
        string[] stringGrid = maze.Split('\n');
      
        int lastIndexY = stringGrid.Length - 1;
        int lastIndexX = stringGrid[0].Length - 1;
        int len = stringGrid.Length;

        int[][] grid = new int[len][];
        for (int y = 0; y < len; y++)
        {
            grid[y] = new int[len];
            for (int x = 0; x < stringGrid[0].Length; x++)
            {
                grid[y][x] = stringGrid[y][x] - '0';
            }
        }

        if (nodes == null)
            nodes = CreateNodes(100);
        SetAdjacentNodes(grid, nodes);         


        visited = CreateVisited(len);
        bestValue = Math.Min(DumbSolution(grid, nodes, 0, 0, lastIndexX, lastIndexY, false),
            DumbSolution(grid, nodes, 0, 0, lastIndexX, lastIndexY, true));

        for (int y = len - 1; y >= 0; y--)
        {
            for (int x = len - 1; x >= 0; x--)
            {
                if (visited[y][x] == null)
                    visited[y][x] = new VisitedNode(Math.Min(
                            DumbSolution(grid, nodes, 0, 0, x, y, false),
                            DumbSolution(grid, nodes, 0, 0, x, y, true))
                        , false);
            }
        }

        Connection connection;
        QueueElement queueElement = new QueueElement();
        queueElement.node = nodes[0][0];

        Queue<QueueElement> queue = new Queue<QueueElement>();
        queue.Enqueue(queueElement);

        QueueElement subQueueElement = new QueueElement();
        VisitedNode visitedNodeInfo;
        Node node;
        int i = 0;
        int sum = 0;
        int op = 0;
        while (queue.Count > 0)
        {
            queueElement = queue.Dequeue();
            node = queueElement.node;
            if (node.y == lastIndexY && node.x == lastIndexX)
            {
                bestValue = queueElement.steps;
            }
            else
            {
                for (i = 3; i >= 0; i--)
                {
                    if(node.AdjacentNodes[i].node != null)
                    {
                        connection = node.AdjacentNodes[i];
                        visitedNodeInfo = visited[connection.node.y][connection.node.x];
                        op = grid[connection.node.y][connection.node.x] - grid[lastIndexY][lastIndexX];
                        sum = queueElement.steps + connection.traverseCost;

                        if (connection.node != node
                            && ((visitedNodeInfo.visited && sum < visitedNodeInfo.steps) || (!visitedNodeInfo.visited && sum <= visitedNodeInfo.steps))
                            && (queueElement.steps + (connection.node.x == lastIndexX && connection.node.y == lastIndexY ? 0 : connection.traverseCost) + ((op + (op >> 31)) ^ (op >> 31))) < bestValue
                        )
                        {
                            visitedNodeInfo.steps = sum;
                            subQueueElement.steps = sum;

                            visitedNodeInfo.visited = true;
                            subQueueElement.node = connection.node;
                            subQueueElement.lastNode = node;

                            queue.Enqueue(subQueueElement);
                        }
                    }
                }
            }
        }
        return bestValue;
    }

    public static Node[][] CreateNodes(int size)
    {
        Node[][] nodes = new Node[size][];
        for (int y = 0; y < size; y++)
        {
            nodes[y] = new Node[size];
            for (int x = 0; x < size; x++)
                nodes[y][x] = new Node(x, y);
        }

        return nodes;
    }

    public static void SetAdjacentNodes(int[][] grid, Node[][] nodes)
    {
        Node node;
        for (int y = 0; y < grid.Length; y++)
        {
            for (int x = 0; x < grid.Length; x++)
            {
                node = nodes[y][x];
                if (x > 0)
                {
                    node.AdjacentNodes[0].node = nodes[y][x - 1];
                    node.AdjacentNodes[0].traverseCost = Math.Abs(grid[y][x] - grid[y][x - 1]);
                }
                else
                    node.AdjacentNodes[0].node = null;

                if (y > 0)
                {
                    node.AdjacentNodes[1].node = nodes[y - 1][x];
                    node.AdjacentNodes[1].traverseCost = Math.Abs(grid[y][x] - grid[y - 1][x]);
                }
                else
                    node.AdjacentNodes[1].node = null;

                if (x + 1 < grid.Length)
                {
                    node.AdjacentNodes[2].node = nodes[y][x + 1];
                    node.AdjacentNodes[2].traverseCost = Math.Abs(grid[y][x] - grid[y][x + 1]);
                }
                else
                    node.AdjacentNodes[2].node = null;

                if (y + 1 < grid.Length)
                {
                    node.AdjacentNodes[3].node = nodes[y + 1][x];
                    node.AdjacentNodes[3].traverseCost = Math.Abs(grid[y][x] - grid[y + 1][x]);
                }
                else
                    node.AdjacentNodes[3].node = null;
            }
        }
    }

    public static VisitedNode[][] CreateVisited(int size)
    {
        VisitedNode[][] visited = new VisitedNode[size][];
        for (int y = 0; y < size; y++)
        {
            visited[y] = new VisitedNode[size];
        }

        return visited;
    }

    public static int DumbSolution(int[][] grid, Node[][] nodes, int sourceX, int sourceY, int endX, int endY, bool lessOrEquals)
    {
        int steps = 0;
        Node bestNode = nodes[sourceY][sourceX];
        int bestTraverseCost = int.MaxValue;
        Connection connection;
        Connection bestConnection = null;
        int i = 0;
        while ( (bestNode.x < endX || bestNode.y < endY))
        {
            if (visited[bestNode.y][bestNode.x] == null)
                visited[bestNode.y][bestNode.x] = new VisitedNode(steps, false);
            else
                visited[bestNode.y][bestNode.x].steps = Math.Min(visited[bestNode.y][bestNode.x].steps, steps);

            for (i = 2; i < 4; i++)
            {
                connection = bestNode.AdjacentNodes[i];
                if (connection.node != null && ((!lessOrEquals && connection.traverseCost < bestTraverseCost) || (lessOrEquals && connection.traverseCost <= bestTraverseCost))
                    && connection.node.x <= endX && connection.node.y <= endY)
                {
                    bestConnection = connection;
                    bestTraverseCost = bestConnection.traverseCost;
                }
            }
            bestTraverseCost = int.MaxValue;
            steps += bestConnection.traverseCost;
            bestNode = bestConnection.node;
        }
        return steps;
    }

    public class Node
    {
        public readonly int x;
        public readonly int y;
        public Connection[] AdjacentNodes = new Connection[4];

        public Node(int x, int y)
        {
            this.x = x;
            this.y = y;
            for (int i = 0; i < AdjacentNodes.Length; i++)
                AdjacentNodes[i] = new Connection();
        }
    }

    public class VisitedNode
    {
        public int steps;
        public bool visited;

        public VisitedNode(int s, bool i)
        {
            steps = s;
            visited = i;
        }
    }

    public struct QueueElement
    {
        public Node node;
        public Node lastNode;
        public int steps;
    }

    public class Connection
    {
        public Node node;
        public int traverseCost;
    }
}
