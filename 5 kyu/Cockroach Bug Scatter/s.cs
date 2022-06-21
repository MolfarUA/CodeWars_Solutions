59aac7a9485a4dd82e00003e


using System.Linq;
public class Dinglemouse
{
  public static int[] Cockroaches(char[][] room)
  {   
    var flatWalls = room[0].Reverse()                            // U
        .Concat(room.Select(r => r[0]))                          // L
        .Concat(room.Last())                                     // D
        .Concat(room.Select(r => r.Last()).Reverse()).ToList();  // R
    flatWalls.Add(flatWalls.First(char.IsDigit));      // repeat the first hole at end to complete room.
    int rL = room.Length, rW = room[0].Length;
    var wallHits = room.SelectMany((row,r) => row.Select((l,c) => 
        (l == 'U') ? rW -c -1 :
        (l == 'L') ? rW + r :
        (l == 'D') ? rL + rW + c : 
        (l == 'R') ? rW*2 + rL*2 -r -1 : -1));  // if not a cockroach, assign wall index -1
    return new int[10].Select((_,h) => wallHits.Count(x => x > 0 && h == flatWalls.Skip(x).First(char.IsDigit)-'0')).ToArray();
  }
}
________________________________
using System;
public class Dinglemouse
{
    public static int[] Cockroaches(char[][] room)
{  
    int[] res = new int[10] {0,0,0,0,0,0,0,0,0,0};
    for (int i = 0; i < room.Length; i++)
        for(int j = 0; j < room[i].Length; j++)
        {
            switch(room[i][j])
            {
                case 'U':                    
                    Top(ref room,ref res, 0, j);
                    room[i][j] = ' ';
                        break;
                case 'L':
                    Left(ref room, ref res, i, 0);
                    room[i][j] = ' ';
                    break;
                case 'D':
                    Bot(ref room, ref res, room.Length-1, j);
                    room[i][j] = ' ';
                    break;
                case 'R':
                    Right(ref room, ref res, i, room[room.Length-1].Length - 1);
                    room[i][j] = ' ';
                    break;
            }
        }
    return res;
}
public static void Top(ref char[][] room,ref int[] r,int f,int s)
{
    
    for (; s > 0; s--)
    { 
        
        if (room[f][s] >= '0' && room[f][s] <= '9')
        {
            r[Convert.ToInt32(room[f][s ]) - 48] += 1;
            return;
        }        
    }
    Left(ref room, ref r, f, s);
}
public static void Left(ref char[][] room, ref int[] r, int f, int s)
{
    for (; f <room.Length-1; f++)
    {
        if (room[f][s] >= '0' && room[f][s] <= '9')
        {
            r[Convert.ToInt32(room[f][s]) - 48] += 1;
            return;
        }
    }
    Bot(ref room, ref r, f, s);
}

public static void Bot(ref char[][] room, ref int[] r, int f, int s)
{
    for (; s < room[room.Length - 1].Length-1; s++)
    {
        if (room[f][s] >= '0' && room[f][s] <= '9')
        {
            r[Convert.ToInt32(room[f][s]) - 48] += 1;
            return;
        }
    }
    Right(ref room, ref r, f, s); 
}
public static void Right(ref char[][] room, ref int[] r, int f, int s)
{
    for (; f >= 0; f--)
    {
        
        if (room[f][s] >= '0' && room[f][s] <= '9')
        {
            r[Convert.ToInt32(room[f][s]) - 48] += 1;
            return;
        }
    }
    Top(ref room, ref r, f+1, s);
}
}
________________________________
using System;
using System.Collections.Generic;
using System.Linq;

public class Dinglemouse
{
    public static int[] Cockroaches(char[][] room)
    {
        int[] cockRoachesInHoles = new int[10] {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        char[] holes = new char[10] {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
        char[] directs = new char[4] {'U', 'D', 'L', 'R'};

        List<Cockroache> cockRoaches = new List<Cockroache>(); 
        List<Vector2> upHoles = new List<Vector2>();
        List<Vector2> downHoles = new List<Vector2>();
        List<Vector2> rightHoles = new List<Vector2>();
        List<Vector2> leftHoles = new List<Vector2>();

        Vector2 upleftHole = new Vector2(-1, -1);
        Vector2 uprightHole = new Vector2(-1, -1);
        Vector2 downleftHole = new Vector2(-1, -1);
        Vector2 downrightHole = new Vector2(-1, -1);


        int height = room.Length;
        int width = room[0].Length;
        int h, w;
        
            //Count all CockRoaches
        for(h = 1; h < height - 1; h++)
        {
            for(w = 1; w < width - 1; w++)
            {
                if(directs.Contains(room[h][w]))
                {
                    cockRoaches.Add(new Cockroache(new Vector2(w, h), room[h][w]));
                }
            }
        }
        
            //Count all upHoles
        h = 0;
        for(w = 1; w < width - 1; w++)
        {
            if(holes.Contains(room[h][w]))
            {
                upHoles.Add(new Vector2(w, h));
            }
        }
            //Count all downHoles
        h = height - 1;
        for(w = 1; w < width - 1; w++)
        {
            if(holes.Contains(room[h][w]))
            {
                downHoles.Add(new Vector2(w, h));
            }
        }
            //Count all rightHoles
        w = width - 1;
        for(h = 1; h < height - 1; h++)
        {
            if(holes.Contains(room[h][w]))
            {
                rightHoles.Add(new Vector2(w, h));
            }
        }
            //Count all leftHoles
        w = 0;
        for(h = 1; h < height -1; h++)
        {
            if(holes.Contains(room[h][w]))
            {
                leftHoles.Add(new Vector2(w, h));
            }
        }

            //Check Corners
        if(holes.Contains(room[0][0]))
        {
            upleftHole.X = 0;
            upleftHole.Y = 0;
        }
        if(holes.Contains(room[height - 1][0]))
        {
            downleftHole.Y = 0;
            downleftHole.X = width - 1;
        }
        if(holes.Contains(room[0][width - 1]))
        {
            uprightHole.Y = height - 1;
            uprightHole.X = 0;
        }
        if(holes.Contains(room[height - 1][width - 1]))
        {
            downrightHole.Y = height - 1;
            downrightHole.X = width - 1;
        }

        foreach(Cockroache cockroache in cockRoaches)
        {
            Vector2 hole = new Vector2(-1, -1);
            switch(cockroache.Direct)
            {
                case 'U':
                cockroache.Position.Y = 0;
                break;
                case 'D':
                cockroache.Position.Y = height - 1;
                break;
                case 'R':
                cockroache.Position.X = width - 1;
                break;
                case 'L':
                cockroache.Position.X = 0;
                break;
            }
            
            while(hole.Y == -1 && hole.X == -1)
            {
                if(cockroache.Position.X == 0 && cockroache.Position.Y == 0)
                {
                    if(upleftHole.X != -1 && upleftHole.Y != -1)
                    {
                        hole = cockroache.Position;
                        break;
                    } 
                    cockroache.Position.Y = 1;
                }
                else if(cockroache.Position.X == 0 && cockroache.Position.Y == height - 1)
                {
                    if(downleftHole.X != -1 && downleftHole.Y != -1)
                    {
                        hole = cockroache.Position;
                        break;
                    } 
                    cockroache.Position.X = 1;
                }
                else if(cockroache.Position.X == width - 1 && cockroache.Position.Y == 0)
                {
                    if(uprightHole.X != -1 && uprightHole.Y != -1)
                    {
                        hole = cockroache.Position;
                        break;
                    }
                    cockroache.Position.X = width - 2;
                }
                else if(cockroache.Position.X == width - 1 && cockroache.Position.Y == height - 1)
                {
                    if(downrightHole.X != -1 && downrightHole.Y != -1)
                    {
                        hole = cockroache.Position;
                        break;
                    }
                    cockroache.Position.Y = height - 2;
                }
                else if(cockroache.Position.Y == 0)
                {
                    Vector2 min = new Vector2(-1, -1);
                    foreach(Vector2 fHole in upHoles)
                    {
                        if(cockroache.Position.X - fHole.X >= 0)
                        {
                            if(min.X == -1 && min.Y == -1)
                            {
                                min = fHole;
                            }
                            else if(cockroache.Position.X - fHole.X < cockroache.Position.X - min.X)
                            {
                                min = fHole;
                            }
                        }
                    }

                    if(min.X != -1 && min.Y != -1)
                    {
                        hole = min;
                    }
                    else
                    {
                        cockroache.Position.X = 0;
                    } 
                    
                }
                else if(cockroache.Position.Y == height - 1)
                {
                    Vector2 min = new Vector2(-1, -1);

                    foreach(Vector2 fHole in downHoles)
                    {
                       if(fHole.X - cockroache.Position.X >= 0)
                       {
                            if(min.X == -1 && min.Y == -1)
                            {
                                    min = fHole;
                            }
                            else if(fHole.X - cockroache.Position.X < min.X - cockroache.Position.X)
                            {
                                    min = fHole;
                            }
                       } 
                    }

                    if(min.X != -1 && min.Y != -1)
                    {
                        hole = min;
                    }
                    else
                    {
                        cockroache.Position.X = width - 1;
                    } 
                }
                else if(cockroache.Position.X == 0)
                {
                    Vector2 min = new Vector2(-1, -1);

                    foreach(Vector2 fHole in leftHoles)
                    {
                        if(fHole.Y - cockroache.Position.Y >= 0)
                        {
                            if(min.X == -1 && min.Y == -1)
                            {
                                min = fHole;
                            }
                            else if(fHole.Y - cockroache.Position.Y < min.Y - cockroache.Position.Y)
                            {
                                min = fHole;
                            }   
                        }               
                    }

                    if(min.X != -1 && min.Y != -1)
                    {
                        hole = min;
                    }
                    else
                    {
                        cockroache.Position.Y = height - 1;
                    } 
                }
                else if(cockroache.Position.X == width - 1)
                {
                    Vector2 min = new Vector2(-1, -1);
                    
                     foreach(Vector2 fHole in rightHoles)
                    {
                        if(cockroache.Position.Y - fHole.Y >= 0)
                        {
                            if(min.X == -1 && min.Y == -1)
                            {
                                    min = fHole;
                            }
                            else if(cockroache.Position.Y - fHole.Y < cockroache.Position.Y - min.Y)
                            {
                                    min = fHole;
                            }
                        }
                    }


                    if(min.X != -1 && min.Y != -1)
                    {
                        hole = min;
                    }
                    else
                    {
                        cockroache.Position.Y = 0;
                    } 
                }    
            }
            cockRoachesInHoles[Convert.ToInt32(room[hole.Y][hole.X].ToString())] += 1;
        }

    
        return cockRoachesInHoles;
    }
}

class Cockroache
{
    public Vector2 Position;
    public char Direct;

    private Cockroache() {}

    public Cockroache(Vector2 position, char direct)
    {
        Position = position;
        Direct = direct;
    } 
}

struct Vector2
{
    public int X;
    public int Y;

    public Vector2(int x, int y)
    {
        X = x;
        Y = y;
    }
}
