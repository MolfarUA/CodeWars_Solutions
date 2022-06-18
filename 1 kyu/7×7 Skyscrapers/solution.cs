5917a2205ffc30ec3a0000a8

using System.Collections.Generic;
using System;
using System.Linq;

public class Skyscrapers
{
        public static int size = 7;
        public static bool isNeedUpdate;

        public class Point
        {
            public int x;
            public int y;
        }

        public static List<int>[][] InitializeSkyscrapersMap(int[][] city, int[] clues)
        {
            var table = new int[7][][];
            table[0] = new int[7][];

            table[0][0] = new int[] { 0, 0, 0, 0, 0, 0, 7 };
            table[0][1] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[0][2] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[0][3] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[0][4] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[0][5] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[0][6] = new int[] { 1, 2, 3, 4, 5, 6, 0 };

            table[1] = new int[7][];
            table[1][0] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[1][1] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[1][2] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[1][3] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[1][4] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[1][5] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[1][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            table[2] = new int[7][];
            table[2][0] = new int[] { 1, 2, 3, 4, 6, 0, 0 };
            table[2][1] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[2][2] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[2][3] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[2][4] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[2][5] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[2][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            table[3] = new int[7][];
            table[3][0] = new int[] { 1, 2, 3, 4, 0, 0, 0 };
            table[3][1] = new int[] { 1, 2, 3, 4, 5, 0, 0 };
            table[3][2] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[3][3] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[3][4] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[3][5] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[3][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            table[4] = new int[7][];
            table[4][0] = new int[] { 1, 2, 3, 0, 0, 0, 0 };
            table[4][1] = new int[] { 1, 2, 3, 4, 0, 0, 0 };
            table[4][2] = new int[] { 1, 2, 3, 4, 5, 0, 0 };
            table[4][3] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[4][4] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[4][5] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[4][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            table[5] = new int[7][];
            table[5][0] = new int[] { 1, 2, 0, 0, 0, 0, 0 };
            table[5][1] = new int[] { 1, 2, 3, 0, 0, 0, 0 };
            table[5][2] = new int[] { 1, 2, 3, 4, 0, 0, 0 };
            table[5][3] = new int[] { 1, 2, 3, 4, 5, 0, 0 };
            table[5][4] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[5][5] = new int[] { 1, 2, 3, 4, 5, 6, 7 };
            table[5][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            table[6] = new int[7][];
            table[6][0] = new int[] { 1, 0, 0, 0, 0, 0, 0 };
            table[6][1] = new int[] { 1, 2, 0, 0, 0, 0, 0 };
            table[6][2] = new int[] { 1, 2, 3, 0, 0, 0, 0 };
            table[6][3] = new int[] { 1, 2, 3, 4, 0, 0, 0 };
            table[6][4] = new int[] { 1, 2, 3, 4, 5, 0, 0 };
            table[6][5] = new int[] { 1, 2, 3, 4, 5, 6, 0 };
            table[6][6] = new int[] { 1, 2, 3, 4, 5, 6, 7 };

            var skyscrapersMap = new List<int>[size][];
            for (int y = 0; y < size; y++)
            {
                skyscrapersMap[y] = new List<int>[size];
                for (int x = 0; x < size; x++)
                {
                    skyscrapersMap[y][x] = new List<int>();
                    for (int h = 1; h <= size; h++)
                        skyscrapersMap[y][x].Add(h);
                }
            }

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    if (city[y][x] != 0)
                    {
                        for (int i = 0; i < size; i++)
                        {
                            skyscrapersMap[i][x].Remove(city[y][x]);
                            skyscrapersMap[y][i].Remove(city[y][x]);
                        }
                        skyscrapersMap[y][x].Add(city[y][x]);
                    }
                }
            }

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    for (int h = 0; h < size; h++)
                    {
                        if (clues[x] > 0 && table[clues[x] - 1][y][h] == 0)
                            skyscrapersMap[y][x].Remove(h + 1);
                        if (clues[y + size] > 0 && table[clues[y + size] - 1][size - x - 1][h] == 0)
                            skyscrapersMap[y][x].Remove(h + 1);
                        if (clues[3 * size - x - 1] > 0 && table[clues[3 * size - x - 1] - 1][size - y - 1][h] == 0)
                            skyscrapersMap[y][x].Remove(h + 1);
                        if (clues[4 * size - y - 1] > 0 && table[clues[4 * size - y - 1] - 1][x][h] == 0)
                            skyscrapersMap[y][x].Remove(h + 1);
                    }
                }
            }
            return skyscrapersMap;
        }

        public static void FillCity(ref int[][] city, int[] clues)
        {
            for (int i = 0; i < 4 * size; i++)
            {
                if (clues[i] == 1)
                {
                    if (i < size)
                        city[0][i] = size;
                    else if (i < 2 * size)
                        city[i - size][6] = size;
                    else if (i < 3 * size)
                        city[size - 1][3 * size - i - 1] = size;
                    else if (i < 4 * size)
                        city[4 * size - i - 1][0] = size;
                }
                else if (clues[i] == size)
                {
                    if (i < size)
                    {
                        for (int j = 0; j < size; j++)
                            city[j][i] = j + 1;
                    }
                    else if (i < 2 * size)
                    {
                        for (int j = 0; j < size; j++)
                            city[i - size][j] = size - j;
                    }
                    else if (i < 3 * size)
                    {
                        for (int j = 0; j < size; j++)
                            city[j][3 * size] = size - j;
                    }
                    else if (i < 4 * size)
                    {
                        for (int j = 0; j < size; j++)
                            city[4 * size - i][j] = j + 1;
                    }
                }
            }
        }

        public static void SetSkyscraper(int x, int y, int height, ref int[][] city, ref List<int>[][] skyscraperMap)
        {
            if (city[y][x] != 0)
                return;

            city[y][x] = height;
            for (int i = 0; i < size; i++)
            {
                skyscraperMap[y][i].Remove(height);
                skyscraperMap[i][x].Remove(height);
            }
            skyscraperMap[y][x].Clear();
            skyscraperMap[y][x].Add(height);
            isNeedUpdate = true;
        }

        public static void FillCityWithSkyscraperMap(ref int[][] city, ref List<int>[][] skyscraperMap)
        {
            for (int y = 0; y < size; y++)
                for (int x = 0; x < size; x++)
                    if (skyscraperMap[y][x].Count == 1)
                        SetSkyscraper(x, y, skyscraperMap[y][x].First(), ref city, ref skyscraperMap);

            int count = 0;
            int index = 0;
            for (int k = 0; k < size; k++)
            {
                for (int height = 1; height <= size; height++)
                {
                    count = 0;
                    index = 0;
                    for (int i = 0; i < size; i++)
                    {
                        if (skyscraperMap[i][k].Contains(height))
                        {
                            count++;
                            index = i;
                        }
                    }
                    if (count == 1)
                        SetSkyscraper(k, index, height, ref city, ref skyscraperMap);

                    count = 0;
                    index = 0;
                    for (int i = 0; i < size; i++)
                    {
                        if (skyscraperMap[k][i].Contains(height))
                        {
                            count++;
                            index = i;
                        }
                    }
                    if (count == 1)
                        SetSkyscraper(index, k, height, ref city, ref skyscraperMap);
                }
            }
        }

        public static bool CityIsValid(int[][] city, List<int>[][] skyscraperMap, int[] clues)
        {
            for (int x = 0; x < size; x++)
                for (int y = 0; y < size; y++)
                    if (skyscraperMap[y][x].Count != 1 || city[y][x] == 0)
                        return false;

            for (int x = 0; x < size; x++)
                for (int y = 0; y < size; y++)
                    if (!(CheckRow(city, y, clues[27 - y], clues[7 + y]) && CheckColumn(city, x, clues[x], clues[20 - x])))
                        return false;
            return true;
        }

        public static int[][] SolvePuzzle(int[] clues)
        {
            var city = new int[size][];
            for (int i = 0; i < size; i++)
                city[i] = new int[size];

            FillCity(ref city, clues);
            var skyscraperMap = InitializeSkyscrapersMap(city, clues);

            Solve(ref city, ref skyscraperMap, clues);
            return city;
        }

        public static bool Solve(ref int[][] city, ref List<int>[][] skyscraperMap, int[] clues)
        {
            for (int x = 0; x < size; x++)
                for (int y = 0; y < size; y++)
                    if (!(CheckRow(city, y, clues[27 - y], clues[7 + y]) && CheckColumn(city, x, clues[x], clues[20 - x])))
                        return false;

            var copyCity = new int[size][];
            for (int i = 0; i < size; i++)
                copyCity[i] = new int[size];

            var copySkyscraper = new List<int>[size][];
            for (int x = 0; x < size; x++)
            {
                copySkyscraper[x] = new List<int>[size];
                for (int y = 0; y < size; y++)
                    copySkyscraper[x][y] = new List<int>();
            }

            CopyMaps(city, skyscraperMap, ref copyCity, ref copySkyscraper);

            isNeedUpdate = true;
            while (isNeedUpdate)
            {
                isNeedUpdate = false;
                FillCityWithSkyscraperMap(ref city, ref skyscraperMap);
                if (CityIsValid(city, skyscraperMap, clues))
                    return true;

                FillForwardHorizontal(ref city, ref skyscraperMap, clues);
                FillForwardVertical(ref city, ref skyscraperMap, clues);
                FillBackwardHorizontal(ref city, ref skyscraperMap, clues);
                FillBackwardVertical(ref city, ref skyscraperMap, clues);
            }

            for (int x = 0; x < size; x++)
                for (int y = 0; y < size; y++)
                    if (!(CheckRow(city, y, clues[27 - y], clues[7 + y]) && CheckColumn(city, x, clues[x], clues[20 - x])))
                        return false;

            var middleCopyCity = new int[size][];
            for (int i = 0; i < size; i++)
                middleCopyCity[i] = new int[size];

            var middleCopySkyscraper = new List<int>[size][];
            for (int x = 0; x < size; x++)
            {
                middleCopySkyscraper[x] = new List<int>[size];
                for (int y = 0; y < size; y++)
                    middleCopySkyscraper[x][y] = new List<int>();
            }

            CopyMaps(city, skyscraperMap, ref middleCopyCity, ref middleCopySkyscraper);

            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    if (skyscraperMap[y][x].Count == 0 && city[y][x] == 0)
                        return false;

                    if (city[y][x] == 0)
                    {
                        foreach (var height in skyscraperMap[y][x].ToList())
                        {
                            SetSkyscraper(x, y, height, ref city, ref skyscraperMap);

                            if ((CheckRow(city, y, clues[27 - y], clues[7 + y]) && CheckColumn(city, x, clues[x], clues[20 - x])))
                                if (Solve(ref city, ref skyscraperMap, clues))
                                    return true;

                            CopyMaps(middleCopyCity, middleCopySkyscraper, ref city, ref skyscraperMap);
                        }
                        return false;
                    }
                }
            }
            CopyMaps(copyCity, copySkyscraper, ref city, ref skyscraperMap);
            return false;
        }

        public static void CopyMaps(int[][] sCity, List<int>[][] sSkyscraperMap, ref int[][] dCity, ref List<int>[][] dSkyscraperMap)
        {
            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                {
                    dCity[y][x] = sCity[y][x];
                    dSkyscraperMap[y][x] = sSkyscraperMap[y][x].ToList();
                }
            }
        }

        public static void FillForwardHorizontal(ref int[][] city, ref List<int>[][] skyscraperMap, int[] clues)
        {
            var cityPoints = new List<Point>();
            for (int y = 0; y < size; y++)
            {
                for (int x = 0; x < size; x++)
                    cityPoints.Add(new Point() { x = x, y = y });

                SolveLine(ref city, ref skyscraperMap, cityPoints.ToArray(), clues[4 * size - y - 1]);
                cityPoints.Clear();
            }
        }

        public static void FillBackwardHorizontal(ref int[][] city, ref List<int>[][] skyscraperMap, int[] clues)
        {
            var cityPoints = new List<Point>();
            for (int y = 0; y < size; y++)
            {
                for (int x = size - 1; x >= 0; x--)
                    cityPoints.Add(new Point() { x = x, y = y });

                SolveLine(ref city, ref skyscraperMap, cityPoints.ToArray(), clues[size + y]);
                cityPoints.Clear();
            }
        }

        public static void FillForwardVertical(ref int[][] city, ref List<int>[][] skyscraperMap, int[] clues)
        {
            var cityPoints = new List<Point>();
            for (int x = 0; x < size; x++)
            {
                for (int y = 0; y < size; y++)
                    cityPoints.Add(new Point() { x = x, y = y });

                SolveLine(ref city, ref skyscraperMap, cityPoints.ToArray(), clues[x]);
                cityPoints.Clear();
            }
        }

        public static void FillBackwardVertical(ref int[][] city, ref List<int>[][] skyscraperMap, int[] clues)
        {
            var cityPoints = new List<Point>();
            for (int x = 0; x < size; x++)
            {
                for (int y = size - 1; y >= 0; y--)
                    cityPoints.Add(new Point() { x = x, y = y });

                SolveLine(ref city, ref skyscraperMap, cityPoints.ToArray(), clues[3 * size - x - 1]);
                cityPoints.Clear();
            }
        }

        public static void SolveLine(ref int[][] city, ref List<int>[][] skyscraperMap, Point[] cityPoints, int clue)
        {
            var possibleSolve = new List<int>[size];
            for (int i = 0; i < 7; i++)
                possibleSolve[i] = new List<int>();

            foreach (var skyscraper1 in skyscraperMap[cityPoints[0].y][cityPoints[0].x])
            {
                foreach (var skyscraper2 in skyscraperMap[cityPoints[1].y][cityPoints[1].x])
                {
                    foreach (var skyscraper3 in skyscraperMap[cityPoints[2].y][cityPoints[2].x])
                    {
                        foreach (var skyscraper4 in skyscraperMap[cityPoints[3].y][cityPoints[3].x])
                        {
                            foreach (var skyscraper5 in skyscraperMap[cityPoints[4].y][cityPoints[4].x])
                            {
                                foreach (var skyscraper6 in skyscraperMap[cityPoints[5].y][cityPoints[5].x])
                                {
                                    foreach (var skyscraper7 in skyscraperMap[cityPoints[6].y][cityPoints[6].x])
                                    {
                                        if (!CheckSckyscrapers(skyscraper1, skyscraper2, skyscraper3, skyscraper4, skyscraper5, skyscraper6, skyscraper7))
                                            continue;

                                        int visibleCount = GetCountVisibility(skyscraper1, skyscraper2, skyscraper3, skyscraper4, skyscraper5, skyscraper6, skyscraper7);
                                        if (visibleCount == clue)
                                        {
                                            possibleSolve[0].Add(skyscraper1);
                                            possibleSolve[1].Add(skyscraper2);
                                            possibleSolve[2].Add(skyscraper3);
                                            possibleSolve[3].Add(skyscraper4);
                                            possibleSolve[4].Add(skyscraper5);
                                            possibleSolve[5].Add(skyscraper6);
                                            possibleSolve[6].Add(skyscraper7);

                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            if (possibleSolve[0].Count == 0)
                return;
                
            for (int i = 0; i < size; i++)
            {
                for (int height = 1; height < size; height++)
                {
                    if (!possibleSolve[i].Contains(height) && skyscraperMap[cityPoints[i].y][cityPoints[i].x].Contains(height))
                    {
                        skyscraperMap[cityPoints[i].y][cityPoints[i].x].Remove(height);
                        if (skyscraperMap[cityPoints[i].y][cityPoints[i].x].Count == 1)
                        {
                            var h = skyscraperMap[cityPoints[i].y][cityPoints[i].x].First();
                            SetSkyscraper(cityPoints[i].x, cityPoints[i].y, h, ref city, ref skyscraperMap);
                        }
                    }
                }
            }
        }

        public static bool CheckRow(int[][] city, int row, int left, int right)
        {
            if (left != 0)
            {
                int visibleCount = 0;
                int max = 0;
                int zerosCount = 0;
                for (int i = 0; i < 7; i++)
                {
                    if (city[row][i] > max)
                    {
                        max = city[row][i];
                        visibleCount += 1;
                    }
                    if (city[row][i] == 0)
                    {
                        zerosCount += 1;
                        break;
                    }
                }
                if ((zerosCount == 0 && left != visibleCount) || left < visibleCount)
                    return false;
            }
            if (right != 0)
            {
                int visibleCount = 0;
                int max = 0;
                int zerosCount = 0;
                for (int i = 6; i >= 0; i--)
                {
                    if (city[row][i] > max)
                    {
                        max = city[row][i];
                        visibleCount += 1;
                    }
                    if (city[row][i] == 0)
                    {
                        zerosCount += 1;
                        break;
                    }
                }
                if ((zerosCount == 0 && right != visibleCount) || right < visibleCount)
                    return false;
            }
            return true;
        }

        public static bool CheckColumn(int[][] city, int column, int up, int down)
        {
            if (up != 0)
            {
                int visibleCount = 0;
                int max = 0;
                int zerosCount = 0;
                for (int i = 0; i < 7; i++)
                {
                    if (city[i][column] > max)
                    {
                        max = city[i][column];
                        visibleCount += 1;
                    }
                    if (city[i][column] == 0)
                    {
                        zerosCount += 1;
                        break;
                    }

                }
                if ((zerosCount == 0 && up != visibleCount) || up < visibleCount)
                    return false;
            }
            if (down != 0)
            {
                int visibleCount = 0;
                int max = 0;
                int zerosCount = 0;
                for (int i = 6; i >= 0; i--)
                {
                    if (city[i][column] > max)
                    {
                        max = city[i][column];
                        visibleCount += 1;
                    }
                    if (city[i][column] == 0)
                    {
                        zerosCount += 1;
                        break;
                    }
                }
                if ((zerosCount == 0 && down != visibleCount) || down < visibleCount)
                    return false;
            }
            return true;
        }

        public static int GetCountVisibility(int a, int b, int c, int d, int e, int f, int g)
        {
            int count = 1;
            count += b > a ? 1 : 0;
            count += c > b && c > a ? 1 : 0;
            count += d > c && d > b && d > a ? 1 : 0;
            count += e > d && e > c && e > b && e > a ? 1 : 0;
            count += f > e && f > d && f > c && f > b && f > a ? 1 : 0;
            count += g > f && g > e && g > d && g > c && g > b && g > a ? 1 : 0;
            return count;
        }

        public static bool CheckSckyscrapers(int a, int b, int c, int d, int e, int f, int g)
        {
            return !(a == b || a == c || a == d || a == e || a == f || a == g ||
                      b == c || b == d || b == e || b == f || b == g ||
                      c == d || c == e || c == f || c == g ||
                      d == e || d == f || d == g ||
                      e == f || e == g ||
                      f == g);
        }
}

___________________________________________________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Skyscrapers
{
    public static int[][] SolvePuzzle(int[] c)
    {
        int len = c.Length / 4;
        Dictionary<int, List<int>> puzzle = new Dictionary<int, List<int>>();
        int[][] rit = new int[len][];

        // Set the default rit
        for (int i = 0; i < len; i++)
            rit[i] = new int[len];

        // Init the puzzle
        for (int i = 0; i < len*len; i++)
        {
            // Add all possible numbers as available choices
            puzzle.Add(i, new List<int>()); 
            for (int j = 1; j <= len; j++)
                puzzle[i].Add(j);
        }

        // Solve puzzle
        bool error = false;
        RemovedFixedMoves(puzzle, c);
        while (!error && !CheckSingleItems(puzzle, c))
            error = CleanMoves(puzzle, c);

        if (!error) { 
            // Reverse puzzle for rit
            for (int i = 0; i < len*len; i++)
                 rit[i / len][i % len] = puzzle[i].ElementAt(0);
        }

        return rit;
    }

    public static void RemovedFixedMoves(Dictionary<int, List<int>> puzzle, int[] clues)
    {
        int i = 0;
        int opposite_i = 0;
        int j = 0;
        int step = 1;
        int len = clues.Length / 4;

        // Parse all clues removing moves not allowed
        foreach (int c in clues)
        {
            // Set direction of row / col scan
            GetDirection(i, len, ref j, ref step, ref opposite_i);

            // Clean fixed moves
            switch (c)
            {
                case 1:
                    SetCellNum(puzzle, clues, j, len);
                    break;

                case 2:
                    puzzle[j].Remove(len);
                    puzzle[j+step].Remove(len -1);
                    break;

                case 3:
                    puzzle[j].Remove(len);
                    puzzle[j].Remove(len-1);
                    puzzle[j + step].Remove(len);
                    break;

                case 4:
                    puzzle[j].Remove(len);
                    puzzle[j].Remove(len-1);
                    puzzle[j].Remove(len-2);
                    puzzle[j + step].Remove(len);
                    puzzle[j + step].Remove(len-1);
                    puzzle[j + step*2].Remove(len);
                    break;

                case 5:
                    for (int z=0; z<len-3; z++)
                        puzzle[j+z*step].Remove(len);
                    break;

                default:
                    if (c == len) {
                        // Set fixed numbers
                        for (int z = 0; z < len; z++)
                            SetCellNum(puzzle, clues, j + z * step, z + 1);
                    }
                    break;
            }

            ++i;
        }
    }

    public static void SetCellNum(Dictionary<int, List<int>> puzzle, int[] clues, int pos, int num)
    {
        int len = clues.Length / 4;
        int row = pos / len;
        int col = pos % len;

        // Clear number from row and col cross
        for (int i = 0; i < len; i++)
        {
            int posRow = row * len + i;
            int posCol = (i * len) + col;

            puzzle[posRow].Remove(num);
            puzzle[posCol].Remove(num);
        }

        // Set at specific cell the number required
        puzzle[pos].Clear();
        puzzle[pos].Add(num);
    }

    public static void RemoveCellNum(Dictionary<int, List<int>> puzzle, int[] clues, int pos, int num)
    {
        int len = clues.Length / 4;
        int row = pos / len;
        int col = pos % len;

        // Clear number from row and col cross
        for (int i = 0; i < len; i++)
        {
            int posRow = row * len + i;
            int posCol = (i * len) + col;

            puzzle[posRow].Remove(num);
            puzzle[posCol].Remove(num);
        }

        // Set at specific cell the number required
        puzzle[pos].Clear();
        puzzle[pos].Add(num);
    }


    public static bool CleanMoves(Dictionary<int, List<int>> puzzle, int[] clues)
    {
        int i = 0;
        int opposite_i = 0;
        int j = 0;
        int step = 1;
        int len = clues.Length / 4;
        bool wrongTable = false;

        // Parse all clues removing moves not allowed
        foreach (int c in clues)
        {
            if (c != 0) { 

                // Set direction of row / col scan
                GetDirection(i, len, ref j, ref step, ref opposite_i);

                // Create a copy of the array list to check
                Dictionary<int, List<int>> puzzleTmp = new Dictionary<int, List<int>>();
                int[] tmpCount = new int[len];
                for (int z = 0; z < len; z++) {

                    puzzleTmp[z] = new List<int>();

                    for (int w = 0; w < puzzle[j + z * step].Count; w++)
                    {
                        int elem = puzzle[j + z * step].ElementAt(w);
                        puzzleTmp[z].Add(elem);
                    }

                    tmpCount[z] = puzzleTmp[z].Count;
                    puzzle[j + z * step].Clear();
                }

                // Get number of object to test
                int[] tmpCheck = new int[len];
                int[] tmpPos = new int[len];
                int[] tmpRim = new int[len];
                bool found = false;
                int scanLine = 0;
                
                for (int erase = 0; erase < len; erase++) { 
                    tmpPos[erase] = tmpCheck[erase] = 0;
                    tmpRim[erase] = tmpCount[erase] - 1;
                }

                // Generate all possible scan considering no duplicates
                while (scanLine < len && tmpRim[scanLine] >= 0)
                { 
                    bool error = false;
                    int x = scanLine;
                    while (x < len && !error)
                    {
                        found = false;
                        while (tmpRim[x] >= 0 && !found)
                        {
                            tmpCheck[x] = puzzleTmp[x].ElementAt(tmpPos[x]);

                            found = true;
                            for (int check = 0; check < x; check++)
                                if (tmpCheck[check] == tmpCheck[x])
                                    found = false;

                            if (!found) { 
                                ++tmpPos[x];
                                --tmpRim[x];
                            }
                        }

                        if (!found)
                            error = true;
                        else
                            ++x;
                    }

                    if (!error) { 
                        // Check if ok as clue
                        found = CheckClue(tmpCheck, c);
                        if (found)
                        {
                            Array.Reverse(tmpCheck);
                            found = CheckClue(tmpCheck, clues[opposite_i]);
                            Array.Reverse(tmpCheck);

                            if (found) 
                                AddSequenceToBoard(puzzle, tmpCheck, j, step);
                        }
                    }

                    // Next if over the limit, go to next line
                    int seek = x - 1;
                    while (seek > 0 && tmpRim[seek] == 0) { --seek; }
                    scanLine = seek;

                    // Check next
                    ++tmpPos[scanLine];
                    --tmpRim[scanLine];

                    // Reste and restart the scan
                    for (int e = scanLine + 1; e<len; e++) { 
                        tmpPos[e] = 0;
                        tmpRim[e] = tmpCount[e]-1;
                    }
                }

            // Check if we added single numbers to avoid duplication in cross the cell
            for (int z = 0; z < len; z++) {
                int pos = j + z * step;

                if (puzzle[pos].Count == 1)
                    SetCellNum(puzzle,clues,pos,puzzle[pos].ElementAt(0));

                if (puzzle[pos].Count == 0)
                    wrongTable = true;
                }
            }

            ++i;
        }

        return wrongTable;
    }

    public static void AddSequenceToBoard(Dictionary<int, List<int>> puzzle, int[] tmpCheck, int j, int step)
    {
        // Add the sequence as possible option for the line
        for (int z = 0; z < tmpCheck.Length; z++)
        {
            if (puzzle[j + z * step].Count > 0 && puzzle[j + z * step].Contains(tmpCheck[z]))
                continue;
            puzzle[j + z * step].Add(tmpCheck[z]);
        }
    }

    public static bool CheckSingleItems(Dictionary<int, List<int>> puzzle, int[] clues)
    {
        bool notChanged = false;
        int len = clues.Length / 4;
        bool completed = true; 

        while (!notChanged)
        {
            int i = 0;
            int opposite_i = 0;
            int j = 0;
            int step = 1;

            notChanged = true;
            completed = true;

            // Parse all clues removing moves not allowed
            foreach (int c in clues)
            {
                // Set direction of row / col scan
                GetDirection(i, len, ref j, ref step, ref opposite_i);

                // Check single presence in the array
                for (int num = 1; num <= len; num++)
                {
                    // Verify presence >1
                    int found = 0;
                    int posFound = -1;
                    for (int z = 0; z < len; z++)
                    {
                        if (puzzle[j + z * step].Contains(num))
                        {
                            ++found;
                            posFound = j + z * step;
                        }
                    }

                    // If found == 1 clear all options and set the unique num found
                    if (found == 1 && puzzle[posFound].Count > 1)
                    {
                        SetCellNum(puzzle, clues, posFound, num);
                        notChanged = false;
                    }

                    if (found != 1)
                        completed = false;
                }

                ++i;
            }
        }

        return completed;
    }

    public static void GetDirection(int i, int len, ref int j, ref int step, ref int oppi)
    {
        // Set direction of row / col scan
        int selDiv = i / len;
        int selMod = i % len;
        switch (selDiv)
        {
            case 0:
                j = selMod;
                step = len;

                oppi = (len*3) - i - 1;
                break;
            case 1:
                j = len * (selMod + 1) - 1;
                step = -1;

                oppi = (len*4-1) - i + len;
                break;
            case 2:
                j = len * len - selMod - 1;
                step = -len;

                oppi = len*3 - i - 1;
                break;
            case 3:
                j = len * (len - selMod - 1);
                step = +1;

                oppi = (len*4-1) - i + len;
                break;
        }
    }

    public static bool CheckClue(int[] array, int clue)
    {
        int deltaClue = clue;

        // If clue > 0 check it
        if (deltaClue > 0) { 
            int max = 0;
            int i = 0;

            // Check if clue is correct for the array
            while (i < array.Length && deltaClue >= 0)
            {
                if (array[i] > max) { 
                   --deltaClue;
                    max = array[i];
                }

                ++i;
            }
        }

        return deltaClue == 0;
    }
}
________________________________________________________________________-
using System;
using System.Collections.Generic;

public static class Skyscrapers
{
  private const int N = 7;
  private const int Sides = 4;
  private const int Mask = (1 << N) - 1;



  private static readonly int[] StartValues;
  private static readonly int[] StepValues;



  static Skyscrapers()
  {
    StartValues = new[]
    {
      0, 1, 2, 3, 4, 5, 6,
      6, 13, 20, 27, 34, 41, 48,
      48, 47, 46, 45, 44, 43, 42,
      42, 35, 28, 21, 14, 7, 0
    };
    StepValues = new[]
    {
      7, 7, 7, 7, 7, 7, 7,
      -1, -1, -1, -1, -1, -1, -1,
      -7, -7, -7, -7, -7, -7, -7,
      1, 1, 1, 1, 1, 1, 1
    };
  }



  private static void SetValue(
    ref int[] possible, int value, int offset)
  {
    var mask = Mask ^ (1 << offset);
    var row = value - value % N;
    var column = value % N;

    for (var i = 0; i < N; ++i)
    {
      possible[row + i] &= mask;
      possible[column + i * N] &= mask;
    }

    possible[value] = 1 << offset;
  }

  private static int GetPossibleCount(
    int value)
  {
    var n = 0;

    while (value > 0)
    {
      n += value & 1;

      value >>= 1;
    }

    return n;
  }

  private static bool IsValid(
    ref int[] clues, ref int[] possible)
  {
    for (var i = 0; i < Sides * N; ++i)
    {
      if (clues[i] == 0)
        continue;

      var isDecided = true;

      for (int j = StartValues[i], k = 0; k < N; j += StepValues[i], ++k)
      {
        if (GetPossibleCount(possible[j]) == 1)
          continue;

        isDecided = false;

        break;
      }

      if (!isDecided)
        continue;

      var max = 0;
      var clue = 0;

      for (int j = StartValues[i], k = 0; k < N; j += StepValues[i], ++k)
      {
        if (max >= possible[j])
          continue;

        max = possible[j];

        ++clue;
      }

      if (clue != clues[i])
        return false;
    }

    return true;
  }

  private static void Filter(
    ref int[] clues, ref int[] possible)
  {
    for (var i = 0; i < Sides * N; ++i)
    {
      if (clues[i] != 2)
        continue;

      var mask = Mask;

      for (var j = N - 1; j >= 0; --j)
      {
        mask ^= 1 << j;

        if (((1 << j) & possible[StartValues[i]]) > 0)
          break;
      }

      for (int j = StartValues[i] + StepValues[i], k = 1; k < N; j += StepValues[i], ++k)
      {
        if (((1 << (N - 1)) & possible[j]) > 0)
          break;

        if ((possible[j] | mask) != mask)
          possible[j] &= mask;
      }
    }
  }

  private static void MakeUnique(ref int[] possible)
  {
    while (true)
    {
      var decidesCount = 0;

      for (var i = 0; i < Sides / 2 * N; ++i)
      {
        var possibleIndexes =
          new Dictionary<int, List<int>>();

        for (int j = StartValues[i], k = 0; k < N; j += StepValues[i], ++k)
        {
          for (var m = 0; m < N; ++m)
          {
            if (((1 << m) & possible[j]) <= 0)
              continue;

            if (!possibleIndexes.ContainsKey(m))
              possibleIndexes[m] = new List<int>();

            possibleIndexes[m].Add(j);
          }
        }

        foreach (var (key, value) in possibleIndexes)
        {
          if (value.Count != 1)
            continue;

          if (possible[value[0]] == (1 << key))
            continue;

          ++decidesCount;

          SetValue(ref possible,
            value[0], key);
        }
      }

      if (decidesCount > 0)
        continue;

      break;
    }
  }

  private static void Prepare(
    ref int[] clues, ref int[] possible)
  {
    for (var i = 0; i < Sides * N; ++i)
    {
      if (clues[i] == 0)
        continue;

      for (int j = StartValues[i], k = 0; k < N; j += StepValues[i], ++k)
      {
        var mask = Mask;

        for (var m = N + k - clues[i] + 1; m < N; ++m)
        {
          mask ^= 1 << m;
        }

        possible[j] &= mask;
      }
    }

    MakeUnique(
      ref possible);
    Filter(ref clues,
      ref possible);
  }

  private static bool Process(
    ref int[][] result, ref int[] clues,
    ref int[] possible, ref bool[] visited)
  {
    var index = -1;
    var minCount = 10000;

    for (var i = 0; i < N * N; ++i)
    {
      var count = GetPossibleCount(
        possible[i]);

      if (minCount <= count
        || visited[i])
      {
        continue;
      }

      index = i;
      minCount = count;
    }

    if (index == -1)
    {
      if (!IsValid(ref clues, ref possible))
        return false;

      for (var i = 0; i < N * N; ++i)
      {
        var quotient = i / N;
        var remainder = i % N;

        for (var j = 0; j < N; ++j)
        {
          if ((1 << j) != possible[i])
            continue;

          result[quotient][remainder] = j + 1;

          break;
        }
      }

      return true;
    }

    var possibleCopy = new int[N * N];

    Array.Copy(possible,
      possibleCopy, N * N);

    for (var j = N - 1; j >= 0; --j)
    {
      var mask = (1 << j) & possible[index];

      if (mask <= 0)
        continue;

      visited[index] = true;

      SetValue(ref possible,
        index, j);

      var isFound = false;

      if (IsValid(ref clues,
        ref possible))
      {
        isFound = Process(ref result,
          ref clues, ref possible,
          ref visited);
      }

      visited[index] = false;

      Array.Copy(possibleCopy,
        possible, N * N);

      if (isFound)
        return true;
    }

    return false;
  }



  public static int[][] SolvePuzzle(
    int[] clues)
  {
    var possible = new int[N * N];
    var visited = new bool[N * N];

    for (var i = 0; i < N * N; ++i)
    {
      possible[i] = Mask;
      visited[i] = true;
    }

    var result = new int[N][];

    for (var i = 0; i < N; ++i)
    {
      result[i] = new int[N];
    }

    Prepare(ref clues,
      ref possible);

    for (var i = 0; i < N * N; ++i)
    {
      var count = GetPossibleCount(
        possible[i]);

      if (count > 1)
        visited[i] = false;
    }

    Process(ref result, ref clues,
      ref possible, ref visited);

    return result;
  }
}
